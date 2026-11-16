#!/usr/bin/env python3
"""
Capstone: read logs/requests.jsonl back into numbers.

Answers questions about the running system from the log alone — no new code
needed per question, which is the point of having a structured log.

    python tools/log_summary.py                      summarise everything
    python tools/log_summary.py --last 15            only the 15 newest records
    python tools/log_summary.py --since 2026-11-13T18:00
    python tools/log_summary.py --paste 12           print 12 records for the README
    python tools/log_summary.py --price-in 0.10 --price-out 0.40
                                                     also convert tokens to dollars,
                                                     at prices (USD per 1M tokens)
                                                     YOU look up for your model

Token counts are what Gemini reported on each response (usage_metadata), not
estimates. Cache hits cost 0 tokens and are shown separately — measure cost
with the cache off (AI201_CACHE=0) or you are measuring the cache.
"""

import argparse
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# Windows consoles default to cp1252; answers contain characters like "é".
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import runlog  # noqa: E402


def pct(values, q):
    if not values:
        return None
    values = sorted(values)
    k = max(0, min(len(values) - 1, round(q / 100 * (len(values) - 1))))
    return values[k]


def fmt(v, unit=""):
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:,.1f}{unit}"
    return f"{v:,}{unit}"


def describe(label, values, unit=" ms"):
    if not values:
        print(f"  {label:<22} no data")
        return
    print(
        f"  {label:<22} n={len(values):<4} mean {fmt(statistics.fmean(values), unit)}  "
        f"p50 {fmt(pct(values, 50), unit)}  p90 {fmt(pct(values, 90), unit)}  "
        f"max {fmt(max(values), unit)}"
    )


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--log", type=Path, default=None, help="log file (default logs/requests.jsonl)")
    p.add_argument("--last", type=int, default=0, help="only the N newest records")
    p.add_argument("--since", default="", help="only records with ts >= this ISO prefix (UTC)")
    p.add_argument("--paste", type=int, default=0, help="print N records as JSON lines and stop")
    p.add_argument("--price-in", type=float, default=None, help="USD per 1M input tokens")
    p.add_argument("--price-out", type=float, default=None, help="USD per 1M output tokens")
    args = p.parse_args()

    records = runlog.read(args.log)
    if args.since:
        records = [r for r in records if (r.get("ts") or "") >= args.since]
    if args.last:
        records = records[-args.last:]

    if args.paste:
        for r in records[-args.paste:]:
            print(json.dumps(r, ensure_ascii=False))
        return

    if not records:
        print("No records. Start `python serve.py` and send it something (tools/drive.py).")
        return

    print(f"{len(records)} records, {records[0]['ts']} → {records[-1]['ts']}\n")

    by_status: dict[str, int] = {}
    for r in records:
        by_status[r.get("status")] = by_status.get(r.get("status"), 0) + 1
    print("Status:  " + ", ".join(f"{k} {v}" for k, v in sorted(by_status.items(), key=lambda kv: str(kv[0]))))

    errors = [r for r in records if r.get("status") == "error"]
    for r in errors[-5:]:
        print(f"  error  {r['ts']}  {r.get('error_type')}: {(r.get('error') or '')[:100]}")

    answered = [r for r in records if r.get("status") == "answered"]
    live = [r for r in answered if not r.get("cache_hit")]
    cached = [r for r in answered if r.get("cache_hit")]

    print("\nLatency (inside the server):")
    describe("all requests", [r["latency_ms"] for r in records if r.get("latency_ms") is not None])
    describe("answered, live model", [r["latency_ms"] for r in live])
    describe("  retrieve stage", [r["retrieve_ms"] for r in live if r.get("retrieve_ms") is not None])
    describe("  generate stage", [r["generate_ms"] for r in live if r.get("generate_ms") is not None])
    describe("refused (no model)", [r["latency_ms"] for r in records if r.get("status") == "refused"])
    if cached:
        describe("answered from cache", [r["latency_ms"] for r in cached])

    print("\nCost per answered request (live model calls only):")
    if not live:
        print("  no live answered requests in this window (all cached or refused)")
        return
    tin = [r.get("prompt_tokens") or 0 for r in live]
    tout = [r.get("output_tokens") or 0 for r in live]
    ttot = [a + b for a, b in zip(tin, tout)]
    attempts = sum(r.get("model_attempts") or 0 for r in live)
    print(f"  requests                {len(live)}  ({attempts} model calls sent, retries included)")
    describe("input tokens", tin, "")
    describe("output tokens", tout, "")
    describe("total tokens", ttot, "")
    mean_s = statistics.fmean(r["latency_ms"] for r in live) / 1000
    print(f"  mean seconds/request    {mean_s:.2f} s")
    if args.price_in is not None and args.price_out is not None:
        per = statistics.fmean(
            a / 1e6 * args.price_in + b / 1e6 * args.price_out for a, b in zip(tin, tout)
        )
        print(f"  mean USD/request        ${per:.6f}  (at ${args.price_in}/M in, ${args.price_out}/M out)")
    print(f"  refused requests cost   0 tokens ({by_status.get('refused', 0)} of them in this window)")


if __name__ == "__main__":
    main()
