#!/usr/bin/env python3
"""Deterministic conformance checks for the Three-Process Learning Research instrument.

This test checks whether run-record schema constraints mechanically enforce
requirements stated by protocol-0.1.md and supporting benchmark contracts.
It is intentionally static: it does not run a learner experiment.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LT = ROOT / "05-experiments" / "learning-trajectory"
SCHEMA_PATH = LT / "run-record.schema.json"

REQUIRED_ROOT = {
    "run_id",
    "benchmark_version",
    "protocol_version",
    "readiness_gate_version",
    "git_commit",
    "learner",
    "condition",
    "problem",
    "process",
    "timing",
    "verification",
    "failure_classification",
    "resources",
    "epistemic_status",
    "status",
}

EXPECTED_Q = [f"Q{i}" for i in range(10)]
EXPECTED_T = [f"t{i}" for i in range(1, 6)]
FAILURE_CLASSES = {
    "learner_failure",
    "artifact_failure",
    "verifier_failure",
    "protocol_failure",
    "data_resource_failure",
    "unresolved",
    "none",
}


def check(condition: bool, label: str, details: str = "") -> tuple[bool, str]:
    if condition:
        return True, f"PASS  {label}"
    suffix = f" — {details}" if details else ""
    return False, f"FAIL  {label}{suffix}"


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text())
    failures = 0

    required = set(schema.get("required", []))
    ok, msg = check(
        REQUIRED_ROOT <= required,
        "root required fields enforce protocol identity/evidence linkage",
        f"missing={sorted(REQUIRED_ROOT - required)}",
    )
    print(msg)
    failures += not ok

    verification = schema["properties"]["verification"]
    verification_required = set(verification.get("required", []))
    ok, msg = check(
        {"capability_check", "correctness_check", "verifier_validity", "verifier_version"}
        <= verification_required,
        "verification block requires verifier identity",
        f"missing={sorted({'capability_check', 'correctness_check', 'verifier_validity', 'verifier_version'} - verification_required)}",
    )
    print(msg)
    failures += not ok

    q = schema["properties"]["q_milestones"]
    q_props = set(q.get("properties", {}))
    ok, msg = check(
        set(EXPECTED_Q) <= q_props and q.get("additionalProperties") is False,
        "Q0-Q9 are explicit, closed-world milestone fields",
        f"missing={sorted(set(EXPECTED_Q) - q_props)} additionalProperties={q.get('additionalProperties')}",
    )
    print(msg)
    failures += not ok

    terrain = schema["properties"]["terrain"]
    terrain_props = set(terrain.get("properties", {}))
    ok, msg = check(
        set(EXPECTED_T) <= terrain_props and set(EXPECTED_T) <= set(terrain.get("required", [])),
        "T1-T5 are explicit and required when a terrain record exists",
        f"missing_fields={sorted(set(EXPECTED_T) - terrain_props)} missing_required={sorted(set(EXPECTED_T) - set(terrain.get('required', [])))}",
    )
    print(msg)
    failures += not ok

    problem = schema["properties"]["problem"]["properties"]
    ok, msg = check(
        {"reference_effort", "reference_effort_unit", "reference_effort_evidence_tier"}
        <= set(problem)
        and "reference_effort_source" in problem
        and "reference_effort_comparability" in problem,
        "reference-effort provenance/comparability are structured",
        "missing source/comparability fields",
    )
    print(msg)
    failures += not ok

    resources = schema["properties"]["resources"]["properties"]
    ok, msg = check(
        "assistance_log" in resources and "external_references" in resources,
        "resource ledger can preserve intervention detail",
        "assistance_log missing",
    )
    print(msg)
    failures += not ok

    reconstruction = verification.get("properties", {}).get("reconstruction")
    ok, msg = check(
        isinstance(reconstruction, dict)
        and isinstance(reconstruction.get("properties"), dict)
        and {"task_id", "context_bundle_id", "context_removed", "evaluator_id", "result"}
        <= set(reconstruction["properties"]),
        "reconstruction conditions are structured",
        "reconstruction object missing required condition fields",
    )
    print(msg)
    failures += not ok

    retention = verification.get("properties", {}).get("retention_epochs")
    ok, msg = check(
        isinstance(retention, dict)
        and retention.get("type") == "array"
        and isinstance(retention.get("items"), dict),
        "retention is recorded as explicit epoch results",
        "retention_epochs array missing",
    )
    print(msg)
    failures += not ok

    verifier = verification.get("properties", {})
    ok, msg = check(
        {"checked_scope", "unchecked_scope", "verification_level"} <= set(verifier),
        "verifier scope and strength are structured",
        "missing checked_scope/unchecked_scope/verification_level",
    )
    print(msg)
    failures += not ok

    # The protocol's condition/arm logic must be traceable to preregistration.
    ok, msg = check(
        "condition_id" in schema["properties"],
        "run record links condition to a registered arm identifier",
        "condition_id missing",
    )
    print(msg)
    failures += not ok

    print()
    print(f"CONFORMANCE_RESULT={'FAIL' if failures else 'PASS'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
