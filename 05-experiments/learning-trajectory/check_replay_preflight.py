#!/usr/bin/env python3
"""Replay preflight for a registered Q2B-LTB run.

This is a mechanical gate. It does not execute the learner benchmark.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_ROOT = {
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

REQUIRED_REF_KEYS = {"protocol", "benchmark", "task", "preregistration", "verifier", "verifier_contract", "analysis", "schema"}
VERIFIER_VERSION_RE = re.compile(r'VERIFIER_VERSION\s*=\s*"([^"]+)"')


def git_show(commit: str, path: str) -> str | None:
    proc = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        check=False,
        capture_output=True,
        text=True,
    )
    return proc.stdout if proc.returncode == 0 else None


def git_exists(commit: str, path: str) -> bool:
    return git_show(commit, path) is not None


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_replay_preflight.py RUN_RECORD.json", file=sys.stderr)
        return 2

    run_path = Path(sys.argv[1])
    run = json.loads(run_path.read_text())
    failures: list[str] = []

    for key in REQUIRED_ROOT:
        if key not in run:
            failures.append(f"missing root field: {key}")

    refs = run.get("artifact_refs", {})
    missing_refs = REQUIRED_REF_KEYS - set(refs)
    for key in sorted(missing_refs):
        failures.append(f"missing artifact ref: {key}")

    commit = run.get("git_commit")
    if not isinstance(commit, str) or not commit:
        failures.append("git_commit must be non-empty")
        commit = ""

    artifact_text: dict[str, str] = {}
    if commit and refs:
        for key in sorted(REQUIRED_REF_KEYS & set(refs)):
            path = refs[key]
            if not isinstance(path, str) or not path:
                failures.append(f"invalid artifact ref: {key}")
                continue
            content = git_show(commit, path)
            if content is None:
                failures.append(f"unresolvable at {commit}: {key} -> {path}")
            else:
                artifact_text[key] = content

    prereg_path = refs.get("preregistration")
    if isinstance(prereg_path, str) and "template" in prereg_path.lower():
        failures.append("preregistration ref resolves to a template, not a concrete registration instance")
    elif "preregistration" in artifact_text:
        try:
            prereg = json.loads(artifact_text["preregistration"])
        except json.JSONDecodeError as exc:
            failures.append(f"preregistration is not valid JSON: {exc}")
        else:
            for field in ("protocol_version", "benchmark_version", "verifier_version", "task_version"):
                if field in run and prereg.get(field) != run[field]:
                    failures.append(f"preregistration mismatch for {field}")
            if prereg.get("study_id") != run.get("preregistration_id"):
                failures.append("preregistration study_id does not match preregistration_id")
            if prereg.get("execution_status") != "NOT_STARTED":
                failures.append("future preregistration must be explicitly marked NOT_STARTED")
            project = prereg.get("project", {})
            verification = prereg.get("verification", {})
            condition = prereg.get("condition", {})
            model = prereg.get("model", {})
            if project.get("task_file") != refs.get("task"):
                failures.append("preregistration task_file does not match task artifact ref")
            if verification.get("verifier_version") != run.get("verifier_version"):
                failures.append("nested preregistration verifier version does not match run")
            if condition.get("condition_id") != run.get("condition_id"):
                failures.append("preregistration condition_id does not match run")
            if model.get("model_id") != run.get("learner", {}).get("model_id"):
                failures.append("preregistration model_id does not match run learner")

    verifier_path = refs.get("verifier")
    if isinstance(verifier_path, str):
        name = Path(verifier_path).name.lower()
        if "hidden-tests" in name or name.endswith(("-record.json", ".md")):
            failures.append("verifier ref appears to be a result/record document, not an executable verifier artifact")
    if "verifier_contract" in artifact_text:
        if "INDEPENDENT_EXECUTION" not in artifact_text["verifier_contract"]:
            failures.append("verifier contract does not define the independent execution basis")

    if "verifier" in artifact_text:
        match = VERIFIER_VERSION_RE.search(artifact_text["verifier"])
        if not match:
            failures.append("verifier artifact does not expose a machine-readable VERIFIER_VERSION")
        elif match.group(1) != run.get("verifier_version"):
            failures.append(
                f"verifier version mismatch: run={run.get('verifier_version')} artifact={match.group(1)}"
            )

    task_path = refs.get("task")
    if isinstance(task_path, str) and "q2b-mbeddr-002" not in task_path.lower():
        failures.append("task artifact is not the registered Q2B-MBEDDR-002 task")

    if "schema" in artifact_text:
        try:
            schema = json.loads(artifact_text["schema"])
            if schema.get("$id") != "q2b-ltb-run-record-conformance-candidate-0.6":
                failures.append("schema artifact is not the registered conformance-candidate-0.5 schema")
        except json.JSONDecodeError:
            failures.append("schema artifact is not valid JSON")

    if failures:
        print("REPLAY_PREFLIGHT=BLOCKED")
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    print("REPLAY_PREFLIGHT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
