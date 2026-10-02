#!/usr/bin/env python3
"""Tests the replay preflight with positive and negative registered records."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check_replay_preflight.py"
VALID = HERE / "replay-fixtures" / "replay-valid-run.json"
INVALID = HERE / "replay-fixtures" / "replay-invalid-run.json"


def run(record: Path) -> int:
    proc = subprocess.run(
        [sys.executable, str(CHECKER), str(record)],
        cwd=str(HERE.parents[1]),
        capture_output=True,
        text=True,
    )
    print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, file=sys.stderr, end="")
    return proc.returncode


def main() -> int:
    failures = 0

    code = run(VALID)
    ok = code == 0
    print(f"{'PASS' if ok else 'FAIL'} replay-valid fixture")
    failures += not ok

    code = run(INVALID)
    ok = code != 0
    print(f"{'PASS' if ok else 'FAIL'} replay-negative fixture")
    failures += not ok

    print("REPLAY_PREFLIGHT_TEST_RESULT=" + ("PASS" if failures == 0 else "FAIL"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
