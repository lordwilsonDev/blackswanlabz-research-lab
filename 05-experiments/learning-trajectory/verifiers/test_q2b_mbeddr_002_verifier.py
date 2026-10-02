#!/usr/bin/env python3
"""Tests the task-specific bounded verifier without running a learner benchmark."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "q2b_mbeddr_002_verifier.py"
PASS_ARTIFACT = HERE / "fixtures" / "pass_controller.py"
FAIL_ARTIFACT = HERE / "fixtures" / "fail_controller.py"


def run(artifact: Path) -> tuple[int, dict]:
    proc = subprocess.run(
        [sys.executable, str(VERIFIER), str(artifact)],
        cwd=str(artifact.parent),
        capture_output=True,
        text=True,
    )
    return proc.returncode, json.loads(proc.stdout)


def main() -> int:
    failures = 0

    code, report = run(PASS_ARTIFACT)
    ok = code == 0 and report["overall_verdict"] == "PASS"
    print(f"{'PASS' if ok else 'FAIL'} passing verifier fixture")
    failures += not ok

    code, report = run(FAIL_ARTIFACT)
    ok = code != 0 and report["overall_verdict"] in {"FAIL", "VERIFIER_ERROR"}
    print(f"{'PASS' if ok else 'FAIL'} failing verifier fixture")
    failures += not ok

    malformed = HERE / "fixtures" / "malformed_controller.py"
    code, report = run(malformed)
    ok = code != 0 and report["overall_verdict"] == "VERIFIER_ERROR"
    print(f"{'PASS' if ok else 'FAIL'} malformed-artifact verifier-error classification")
    failures += not ok

    print("VERIFIER_TEST_RESULT=" + ("PASS" if failures == 0 else "FAIL"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
