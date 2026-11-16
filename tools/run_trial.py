#!/usr/bin/env python3
"""
Capstone: run ONE complete trial of the five criteria, start to finish.

    python tools/run_trial.py --label before --trial 1

What one trial is (the same every time, nothing changed in between):

  1. Start a fresh server: `serve.py` with the cache OFF (AI201_CACHE=0) and
     its log going to results/capstone/<label>_trial<N>.jsonl.
  2. Send the 21 standard requests with tools/drive.py:
       5 in-scope questions x2 (10, should be answered)
       5 out-of-scope questions  (should be refused by the gate)
       6 malformed requests      (should be rejected with a 400)
  3. Stop it. Start a second server on the same log, with an INVALID
     GEMINI_API_KEY in the environment (the real environment variable wins
     over .env), and send 1 in-scope question. That is the deliberately
     triggered model failure criterion 5 asks for.
  4. Stop it and score the trial with tools/check_criteria.py.

Everything a trial produces lands in results/capstone/:
  <label>_trial<N>.jsonl            the server's structured log (the evidence)
  <label>_trial<N>.manifest.jsonl   what the client sent and got back
  <label>_trial<N>_client.txt       drive.py's console output
  <label>_trial<N>_check.txt        the criteria scores

Uses its own port (default 5101) so it never collides with a server you
already have running on 5000. Costs 10 Gemini calls per trial (the model-error
request is rejected by Gemini before any tokens are used).
"""

import argparse
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "capstone"
PY = sys.executable


def start_server(port: int, log: Path, extra_env: dict, server_out: Path) -> subprocess.Popen:
    env = dict(os.environ)
    env.update({"PORT": str(port), "AI201_CACHE": "0", "AI201_LOG_PATH": str(log)})
    env.update(extra_env)
    out = server_out.open("a", encoding="utf-8")
    proc = subprocess.Popen([PY, str(ROOT / "serve.py")], cwd=ROOT, env=env, stdout=out, stderr=subprocess.STDOUT)
    for _ in range(60):
        if proc.poll() is not None:
            sys.exit(f"server exited early — see {server_out}")
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as r:
                if r.status == 200:
                    return proc
        except OSError:
            time.sleep(1)
    proc.terminate()
    sys.exit(f"server never answered /health — see {server_out}")


def stop_server(proc: subprocess.Popen) -> None:
    proc.terminate()
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()


def drive(port: int, manifest: Path, client_out: Path, *args: str) -> None:
    cmd = [PY, str(ROOT / "tools" / "drive.py"), "--url", f"http://127.0.0.1:{port}/ask",
           "--manifest", str(manifest), *args]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    with client_out.open("a", encoding="utf-8") as f:
        f.write(f"$ python tools/drive.py {' '.join(args)}\n{result.stdout}{result.stderr}\n")
    print(result.stdout.rstrip().splitlines()[-2] if result.stdout.strip() else result.stderr)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--label", required=True, help="before or after")
    p.add_argument("--trial", type=int, required=True)
    p.add_argument("--port", type=int, default=5101)
    args = p.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"{args.label}_trial{args.trial}"
    log = OUT / f"{stem}.jsonl"
    manifest = OUT / f"{stem}.manifest.jsonl"
    client_out = OUT / f"{stem}_client.txt"
    check_out = OUT / f"{stem}_check.txt"
    server_out = OUT / f"{stem}_server.txt"
    for f in (log, manifest, client_out, check_out, server_out):
        if f.exists():
            sys.exit(f"{f} already exists — a trial is never overwritten. Use a new --trial number.")

    print(f"Trial {stem}: starting server (cache off) on port {args.port}")
    server = start_server(args.port, log, {}, server_out)
    try:
        drive(args.port, manifest, client_out, "--set", "in", "--repeat", "2")
        drive(args.port, manifest, client_out, "--set", "out")
        drive(args.port, manifest, client_out, "--set", "bad")
    finally:
        stop_server(server)

    print("Restarting with an invalid GEMINI_API_KEY for the model-failure request")
    server = start_server(args.port, log, {"GEMINI_API_KEY": "invalid-key-for-capstone-test"}, server_out)
    try:
        drive(args.port, manifest, client_out, "--set", "in", "--limit", "1", "--phase", "model_error")
    finally:
        stop_server(server)

    result = subprocess.run([PY, str(ROOT / "tools" / "check_criteria.py"), str(log)],
                            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    check_out.write_text(result.stdout + result.stderr, encoding="utf-8")
    print("\n" + result.stdout + result.stderr)


if __name__ == "__main__":
    main()
