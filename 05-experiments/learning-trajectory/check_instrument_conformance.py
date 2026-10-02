#!/usr/bin/env python3
"""Deterministic conformance checks for the Three-Process Learning Research instrument."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LT = ROOT / "05-experiments" / "learning-trajectory"
SCHEMA_PATH = LT / "run-record.schema.conformance-candidate.json"

EXPECTED_ROOT = {
    "run_id", "run_record_schema_version", "benchmark_version", "protocol_version", "readiness_gate_version",
    "git_commit", "task_version", "preregistration_id", "verifier_version",
    "analysis_version", "learner", "condition", "condition_id", "problem",
    "process", "timing", "verification", "failure_classification", "resources",
    "resource_budget", "stopping_rules", "contamination_controls",
    "role_separation", "evidence_firewall", "epistemic_status", "status",
}

EXPECTED_Q = [f"Q{i}" for i in range(10)]
EXPECTED_T = [f"t{i}" for i in range(1, 6)]


def report(ok: bool, label: str, details: str = "") -> int:
    print(("PASS " if ok else "FAIL ") + label + (f" — {details}" if details else ""))
    return 0 if ok else 1


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text())
    failures = 0
    root_required = set(schema["required"])

    failures += report(
        EXPECTED_ROOT <= root_required and "artifact_refs" in root_required,
        "root record enforces protocol registration and evidence-boundary fields",
        f"missing={sorted(EXPECTED_ROOT - root_required)}",
    )

    verification = schema["properties"]["verification"]
    vreq = set(verification["required"])
    failures += report(
        {"capability_check", "correctness_check", "verifier_validity", "verifier_version",
         "checked_scope", "unchecked_scope", "verification_level", "reconstruction",
         "retention_epochs"} <= vreq,
        "verification block enforces identity, scope, reconstruction, and retention",
        f"missing={sorted({'capability_check','correctness_check','verifier_validity','verifier_version','checked_scope','unchecked_scope','verification_level','reconstruction','retention_epochs'} - vreq)}",
    )

    q = schema["properties"]["q_milestones"]
    failures += report(
        set(EXPECTED_Q) == set(q["properties"]) and
        set(EXPECTED_Q) == set(q["required"]) and
        q["additionalProperties"] is False,
        "Q0-Q9 are closed-world milestone records",
        f"properties={sorted(q['properties'])} required={sorted(q['required'])}",
    )

    terrain = schema["properties"]["terrain"]
    failures += report(
        set(EXPECTED_T) == set(terrain["properties"]) and
        set(EXPECTED_T) == set(terrain["required"]) and
        terrain["additionalProperties"] is False,
        "T1-T5 are explicit closed-world terrain fields",
        f"properties={sorted(terrain['properties'])} required={sorted(terrain['required'])}",
    )

    problem = schema["properties"]["problem"]
    preq = set(problem["required"])
    pprops = set(problem["properties"])
    needed_ref = {
        "reference_effort", "reference_effort_unit",
        "reference_effort_evidence_tier", "reference_effort_source",
        "reference_effort_comparability"
    }
    failures += report(
        needed_ref <= pprops and needed_ref <= preq,
        "reference effort has provenance and comparability fields",
        f"missing_required={sorted(needed_ref - preq)}",
    )

    resources = schema["properties"]["resources"]
    rreq = set(resources["required"])
    failures += report(
        "assistance_log" in resources["properties"] and "assistance_log" in rreq,
        "assistance is traceable rather than count-only",
    )

    reconstruction = verification["properties"]["reconstruction"]
    failures += report(
        {"task_id", "context_bundle_id", "context_removed", "evaluator_id", "result"}
        <= set(reconstruction["required"]),
        "reconstruction has explicit test conditions",
    )

    retention = verification["properties"]["retention_epochs"]
    failures += report(
        retention["type"] == "array" and retention["minItems"] == 3 and retention["maxItems"] == 3,
        "retention is represented as explicit three-epoch results",
    )

    failures += report(
        {"checked_scope", "unchecked_scope", "verification_level"} <= set(verification["properties"]),
        "verification scope and proof strength are machine-readable",
    )

    print()
    print("CONFORMANCE_RESULT=" + ("FAIL" if failures else "PASS"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
