#!/usr/bin/env python3
"""
Capstone: send a fixed set of requests to the running server.

The server (`python serve.py`) must already be running in another terminal.
Every request this sends lands in logs/requests.jsonl through serve.py, so
this script is how a "trial" is produced: run it, then read the log back
with tools/log_summary.py.

    python tools/drive.py                       in-scope + out-of-scope once each
    python tools/drive.py --set in --repeat 2   the 5 in-scope questions, twice
    python tools/drive.py --set bad             malformed requests (expect 400s)
    python tools/drive.py --set all --rpm 60    everything, paced at 60/minute

Standard library only — no new dependencies.
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# Windows consoles default to cp1252; answers contain characters like "é".
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import questions as qs  # noqa: E402

# Raw request bodies that should each be rejected with a 400 (and logged).
BAD_BODIES = [
    ("empty body", b""),
    ("not JSON", b"this is not json"),
    ("JSON list, not object", b'["what about laundry?"]'),
    ("missing question", b'{"q": "laundry?"}'),
    ("question is a number", b'{"question": 42}'),
    ("blank question", b'{"question": "   "}'),
]


def post(url: str, body: bytes, timeout: float) -> tuple[int, dict, float]:
    req = urllib.request.Request(
        url, data=body, method="POST", headers={"Content-Type": "application/json"}
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status, raw = resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        status, raw = exc.code, exc.read()
    elapsed = (time.perf_counter() - t0) * 1000
    try:
        data = json.loads(raw or b"{}")
    except json.JSONDecodeError:
        data = {"raw": raw.decode("utf-8", "replace")[:200]}
    return status, data, elapsed


def build_requests(which: str) -> list[tuple[str, bytes]]:
    items: list[tuple[str, bytes]] = []
    if which in ("in", "all", "good"):
        for q in qs.answered():
            items.append((q["question"], json.dumps({"question": q["question"]}).encode()))
    if which in ("out", "all", "good"):
        for q in qs.OUT_OF_SCOPE:
            items.append((q, json.dumps({"question": q}).encode()))
    if which in ("bad", "all"):
        items.extend(BAD_BODIES)
    return items


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    # 127.0.0.1, not localhost: on Windows "localhost" tries IPv6 ::1 first, the
    # Flask dev server only listens on IPv4, and the fallback adds ~2 s to every
    # request as seen from the client (the server-side latency_ms is unaffected).
    p.add_argument("--url", default="http://127.0.0.1:5000/ask")
    p.add_argument("--set", default="good", choices=["in", "out", "good", "bad", "all"],
                   help="in=5 test questions, out=5 out-of-scope, good=in+out, bad=malformed, all=everything")
    p.add_argument("--repeat", type=int, default=1, help="send the whole set this many times")
    p.add_argument("--rpm", type=float, default=0, help="pace to this many requests/minute (0 = as fast as answered)")
    p.add_argument("--timeout", type=float, default=120, help="client timeout per request, seconds")
    args = p.parse_args()

    items = build_requests(args.set) * args.repeat
    gap = 60.0 / args.rpm if args.rpm > 0 else 0
    print(f"Sending {len(items)} request(s) to {args.url}\n")

    counts: dict[int, int] = {}
    for i, (label, body) in enumerate(items, 1):
        t_start = time.perf_counter()
        try:
            status, data, ms = post(args.url, body, args.timeout)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            print(f"{i:>3}  ---  client error: {exc}   ({label[:60]})")
            counts[-1] = counts.get(-1, 0) + 1
            continue
        counts[status] = counts.get(status, 0) + 1
        kind = "refused" if data.get("refused") else ("answered" if status == 200 else data.get("error", "")[:40])
        print(f"{i:>3}  {status}  {ms:7.0f} ms  {kind:<10}  {data.get('request_id', '-')}  {label[:60]}")
        if gap:
            time.sleep(max(0.0, gap - (time.perf_counter() - t_start)))

    summary = ", ".join(f"{('client error' if k == -1 else k)}: {v}" for k, v in sorted(counts.items()))
    print(f"\nDone. {summary}")
    print("Read it back with:  python tools/log_summary.py")


if __name__ == "__main__":
    main()
