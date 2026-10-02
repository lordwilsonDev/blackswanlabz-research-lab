#!/usr/bin/env python3
"""Check that a registered run has concrete, resolvable replay artifacts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REQUIRED_REF_KEYS = {"protocol", "benchmark", "task", "preregistration", "verifier", "analysis"}
ROOT_REQUIRED = {
    "run_record_schema_version",
    "protocol_version",
    "benchmark_version",
    "git_commit",
    "task_version",
    "preregistration_id",
    "verifier_version",
    "analysis_version",
    "artifact_refs",
}


def git_exists(commit: str, path: str) -> bool:
    proc = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}:{path}"],
        check=False,
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_replay_preflight.py RUN_RECORD.json", file=sys.stderr)
        return 2

    run_path = Path(sys.argv[1])
    run = json.loads(run_path.read_text())

    failures = []
    for key in ROOT_REQUIRED:
        if key not in run:
            failures.append(f"missing root field: {key}")

    refs = run.get("artifact_refs", {})
    missing_refs = REQUIRED_REF_KEYS - set(refs)
    for key in sorted(missing_refs):
        failures.append(f"missing artifact ref: {key}")

    commit = run.get("git_commit")
    if commit and refs:
        for key in sorted(REQUIRED_REF_KEYS & set(refs)):
            path = refs[key]
            if not isinstance(path, str) or not path:
                failures.append(f"invalid artifact ref: {key}")
            elif not git_exists(commit, path):
                failures.append(f"unresolvable at {commit}: {key} -> {path}")

    # A template is not a concrete preregistration record.
    prereg = refs.get("preregistration")
    if isinstance(prereg, str) and "template" in prereg.lower():
        failures.append("preregistration ref resolves to a template, not a concrete registration instance")

    # A run-results text file is not sufficient evidence of an independent verifier.
    verifier = refs.get("verifier")
    if isinstance(verifier, str):
        name = Path(verifier).name.lower()
        if "hidden-tests" in name or name.endswith(("-record.json", ".md")):
            failures.append("verifier ref appears to be a result/record document, not an executable verifier artifact")

    if failures:
        print("REPLAY_PREFLIGHT=BLOCKED")
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    print("REPLAY_PREFLIGHT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
