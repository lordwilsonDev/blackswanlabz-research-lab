#!/usr/bin/env python3
"""Mutation test for the instrument conformance gate.

The goal is to prove the gate is sensitive to deliberate contract regressions.
No learner or benchmark execution occurs.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "05-experiments" / "learning-trajectory" / "run-record.schema.conformance-candidate.json"


def checks(s: dict[str, object]) -> set[str]:
    failures: set[str] = set()
    req = set(s["required"])  # type: ignore[index]

    if "git_commit" not in req:
        failures.add("exact_git_commit")
    if "artifact_refs" not in req:
        failures.add("artifact_refs")
    if "verifier_version" not in req:
        failures.add("root_verifier_version")

    q = s["properties"]["q_milestones"]  # type: ignore[index]
    if set(q["required"]) != {f"Q{i}" for i in range(10)}:  # type: ignore[index]
        failures.add("q_required")
    if set(q["properties"]) != {f"Q{i}" for i in range(10)}:  # type: ignore[index]
        failures.add("q_properties")
    if q["additionalProperties"] is not False:  # type: ignore[index]
        failures.add("q_closed_world")

    v = s["properties"]["verification"]  # type: ignore[index]
    vreq = set(v["required"])  # type: ignore[index]
    for field in {"verifier_version", "checked_scope", "unchecked_scope", "verification_level", "reconstruction", "retention_epochs"}:
        if field not in vreq:
            failures.add(f"verification_{field}")

    r = s["properties"]["resources"]  # type: ignore[index]
    if "assistance_log" not in r["required"]:  # type: ignore[index]
        failures.add("assistance_log")

    return failures


def main() -> int:
    baseline = json.loads(SCHEMA.read_text())
    baseline_failures = checks(baseline)
    if baseline_failures:
        print("MUTATION_BASELINE=FAIL", sorted(baseline_failures))
        return 1

    mutations: dict[str, callable] = {
        "drop_git_commit": lambda x: x["required"].remove("git_commit"),
        "drop_Q9": lambda x: x["properties"]["q_milestones"]["required"].remove("Q9"),
        "open_Q_milestones": lambda x: x["properties"]["q_milestones"].update({"additionalProperties": True}),
        "drop_verifier_version": lambda x: x["properties"]["verification"]["required"].remove("verifier_version"),
        "drop_assistance_log": lambda x: x["properties"]["resources"]["required"].remove("assistance_log"),
        "drop_task_ref": lambda x: x["properties"]["artifact_refs"]["required"].remove("task"),
    }

    failures = 0
    for name, mutate in mutations.items():
        mutant = copy.deepcopy(baseline)
        mutate(mutant)
        detected = bool(checks(mutant))
        print(f"{'PASS' if detected else 'FAIL'} mutation={name}")
        failures += not detected

    print("MUTATION_RESULT=" + ("PASS" if failures == 0 else "FAIL"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
