#!/usr/bin/env python3
"""
Capstone: score one trial against the five criteria in criteria.md (## Capstone).

    python tools/check_criteria.py results/capstone/before_trial1.jsonl

Reads the trial's server log (the .jsonl) and the client-side manifest that
tools/drive.py wrote next to it (<same name>.manifest.jsonl). The manifest is
what makes criterion 1 checkable: it is the list of requests that were SENT,
so a request that never reached the log shows up as missing rather than as
silence.

Scoring follows the criteria as written. Where the wording doesn't settle a
case, the checker doesn't decide — it prints a NOTE and leaves it to the
verdict.

The "main" phase is the 21 standard requests (5 in-scope x2, 5 out-of-scope,
6 malformed). The "model_error" phase is the one request sent to a server
started with an invalid API key, used only by criterion 5.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import runlog  # noqa: E402

FIELDS = runlog.FIELDS


def is_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def check(log_path: Path) -> dict:
    manifest_path = log_path.with_suffix(".manifest.jsonl")
    records = load_jsonl(log_path)
    sent = load_jsonl(manifest_path)
    if not sent:
        sys.exit(f"No manifest at {manifest_path} — run the trial with tools/run_trial.py.")

    by_id: dict[str, list[dict]] = {}
    for r in records:
        by_id.setdefault(r.get("request_id"), []).append(r)

    main = [s for s in sent if s["phase"] == "main"]
    err = [s for s in sent if s["phase"] == "model_error"]
    notes: list[str] = []

    def record_for(s):
        hits = by_id.get(s.get("request_id")) if s.get("request_id") else None
        return hits[0] if hits and len(hits) == 1 else None

    main_records = [record_for(s) for s in main]

    # ── 1. exactly one record per request (main phase) ──────────────────────
    c1 = 0
    for s in main:
        rid = s.get("request_id")
        n = len(by_id.get(rid, [])) if rid else 0
        if n == 1:
            c1 += 1
        else:
            notes.append(f"C1: request '{s['label'][:50]}' (http {s['http_status']}) has {n} log records")
    sent_ids = {s.get("request_id") for s in sent}
    extra = [r for r in records if r.get("request_id") not in sent_ids]
    if extra:
        notes.append(f"C1: {len(extra)} log record(s) match no request that was sent")

    # ── 2. all 23 fields present, nothing extra (main phase) ────────────────
    c2 = 0
    for s, r in zip(main, main_records):
        if r is not None and list(r.keys()) == FIELDS:
            c2 += 1
        elif r is not None:
            notes.append(f"C2: record {r.get('request_id')} keys differ: "
                         f"missing {sorted(set(FIELDS) - set(r))}, extra {sorted(set(r) - set(FIELDS))}")

    # ── 3. timings (main phase) ─────────────────────────────────────────────
    c3 = 0
    for r in main_records:
        if r is None:
            continue
        st = r.get("status")
        ok = is_num(r.get("latency_ms")) and r["latency_ms"] >= 0
        if st == "answered":
            ok = ok and is_num(r.get("retrieve_ms")) and is_num(r.get("generate_ms"))
        elif st == "refused":
            ok = ok and is_num(r.get("retrieve_ms")) and r.get("generate_ms") is None
        elif st == "rejected":
            ok = ok and r.get("retrieve_ms") is None and r.get("generate_ms") is None
        else:
            notes.append(f"C3: main-phase record {r.get('request_id')} has status {st!r}; "
                         f"the criterion doesn't say which stages it reached — counted as a fail")
            ok = False
        if ok:
            c3 += 1
        else:
            notes.append(f"C3: record {r.get('request_id')} ({st}) timings: latency {r.get('latency_ms')}, "
                         f"retrieve {r.get('retrieve_ms')}, generate {r.get('generate_ms')}")

    # ── 4. tokens on answered requests; nulls elsewhere (main phase) ────────
    answered = [r for r in main_records if r and r.get("status") == "answered"]
    c4 = 0
    for r in answered:
        p, o, t = r.get("prompt_tokens"), r.get("output_tokens"), r.get("total_tokens")
        if r.get("cache_hit"):
            notes.append(f"C4: answered record {r['request_id']} was a cache hit — cache was not off")
        if is_num(p) and is_num(o) and t == p + o:
            c4 += 1
            if p == 0 or o == 0:
                notes.append(f"C4: record {r['request_id']} passes but has a 0 token count "
                             f"(prompt {p}, output {o}) — 0 is what the code logs when Gemini sends no usage")
        else:
            notes.append(f"C4: record {r['request_id']} tokens prompt {p}, output {o}, total {t}")
    non_model = [r for r in main_records if r and r.get("status") in ("refused", "rejected")]
    null_ok = sum(
        1 for r in non_model
        if r.get("prompt_tokens") is None and r.get("output_tokens") is None and r.get("total_tokens") is None
    )

    # ── 5. failures carry their details ─────────────────────────────────────
    c5 = 0
    bad = [s for s in main if s["set"] == "bad"]
    for s in bad:
        r = record_for(s)
        if (s["http_status"] == 400 and r is not None and r.get("http_status") == 400
                and r.get("status") == "rejected" and r.get("error_type")):
            c5 += 1
        else:
            notes.append(f"C5: malformed '{s['label']}' → client {s['http_status']}, "
                         f"record {None if r is None else (r.get('status'), r.get('error_type'))}")
    err_record = None
    for s in err:
        r = record_for(s)
        err_record = r
        if (s["http_status"] == 500 and r is not None and r.get("http_status") == 500
                and r.get("status") == "error" and r.get("error_type") and r.get("error")):
            c5 += 1
        else:
            notes.append(f"C5: model-error request → client {s['http_status']}, "
                         f"record {None if r is None else (r.get('status'), r.get('error_type'))}")
    if not err:
        notes.append("C5: no model_error request in this trial's manifest")
    if err_record is not None:
        notes.append(
            "Outside C1–C3's 21: the model-error record has "
            f"latency_ms {err_record.get('latency_ms')}, retrieve_ms {err_record.get('retrieve_ms')}, "
            f"generate_ms {err_record.get('generate_ms')}, error_type {err_record.get('error_type')!r}"
        )

    return {
        "log": str(log_path),
        "sent_main": len(main),
        "records": len(records),
        "c1": (c1, len(main)),
        "c2": (c2, len(main)),
        "c3": (c3, len(main)),
        "c4": (c4, len(answered)),
        "c4_nulls": (null_ok, len(non_model)),
        "c5": (c5, len(bad) + len(err)),
        "notes": notes,
    }


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    res = check(Path(sys.argv[1]))
    print(f"Trial log: {res['log']}")
    print(f"Requests sent (main phase): {res['sent_main']}   records in log: {res['records']}\n")
    print(f"C1  exactly one record per request ........ {res['c1'][0]}/{res['c1'][1]}   (target 21 of 21)")
    print(f"C2  all 23 fields in every record .......... {res['c2'][0]}/{res['c2'][1]}   (target 21 of 21)")
    print(f"C3  timings present / null as specified ... {res['c3'][0]}/{res['c3'][1]}   (target 21 of 21)")
    print(f"C4  token counts on answered requests ..... {res['c4'][0]}/{res['c4'][1]}   (target 10 of 10)")
    print(f"      null tokens on refused + rejected ... {res['c4_nulls'][0]}/{res['c4_nulls'][1]}")
    print(f"C5  failures recorded with details ........ {res['c5'][0]}/{res['c5'][1]}   (target 7 of 7)")
    if res["notes"]:
        print("\nNotes:")
        for n in res["notes"]:
            print(f"  - {n}")


if __name__ == "__main__":
    main()
