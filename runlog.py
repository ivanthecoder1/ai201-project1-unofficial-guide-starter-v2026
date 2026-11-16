"""
Capstone: the structured request log.

One JSON object per line (JSONL), appended to logs/requests.jsonl, one line
per /ask request the server handles, whether it answered, refused, rejected
the input, or crashed. A file you can read back later, not print().

Each record has named fields so it can be filtered and summed after the fact
(`python tools/log_summary.py` does that). The fields are listed in
FIELDS below and in the README under Instrumentation.

Set AI201_LOG_PATH to write somewhere else (handy for keeping a test session
separate from the real one).
"""

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

import config

LOG_PATH = Path(os.getenv("AI201_LOG_PATH", str(config.ROOT / "logs" / "requests.jsonl")))

# Every record has every one of these keys, in this order. Missing values are
# null rather than absent, so "the field wasn't recorded" and "the field was
# empty" never look the same.
FIELDS = [
    "ts",             # ISO-8601 UTC time the request arrived
    "request_id",     # short random id, also returned to the caller
    "route",          # "/ask"
    "status",         # answered | refused | rejected | error
    "http_status",    # what the caller got back
    "question",       # the input (truncated to 500 chars)
    "answer",         # the output (truncated to 1000 chars); null on reject/error
    "sources",        # files cited to the caller (sorted, as the API returns them)
    "retrieved",      # [{label, distance}] nearest-first, top_k of them
    "best_distance",  # what the relevance gate compared
    "threshold",      # the cutoff it compared against
    "latency_ms",     # whole request, end to end inside the server
    "retrieve_ms",    # embed question + vector search
    "generate_ms",    # prompt + Gemini call; null when refused
    "cache_hit",      # answer came from the local cache (cost 0 tokens)
    "model_attempts", # calls actually sent to Gemini (retries included)
    "prompt_tokens",  # read back from the Gemini response, not estimated
    "output_tokens",
    "total_tokens",
    "model",
    "corpus",
    "error_type",     # exception class, or the reason an input was rejected
    "error",          # message (truncated to 500 chars)
]

_lock = threading.Lock()


def _clip(value, limit):
    if isinstance(value, str) and len(value) > limit:
        return value[:limit] + "…"
    return value


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def write(**fields) -> dict:
    """Append one record. Unknown keys are refused so typos don't go unseen."""
    unknown = set(fields) - set(FIELDS)
    if unknown:
        raise KeyError(f"runlog.write got unknown fields: {sorted(unknown)}")

    record = {name: fields.get(name) for name in FIELDS}
    record["question"] = _clip(record["question"], 500)
    record["answer"] = _clip(record["answer"], 1000)
    record["error"] = _clip(record["error"], 500)

    line = json.dumps(record, ensure_ascii=False)
    try:
        with _lock:
            LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with LOG_PATH.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
    except OSError as exc:
        # Logging must never take the request down with it — but it must not
        # fail silently either.
        import sys

        print(f"[runlog] could not write {LOG_PATH}: {exc}", file=sys.stderr)
    return record


def read(path: Path | None = None) -> list[dict]:
    """Every record in the log, oldest first. Skips (and counts) bad lines."""
    path = path or LOG_PATH
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records
