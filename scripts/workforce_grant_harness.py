#!/usr/bin/env python3
"""Deterministic preflight harness for BlackSwanLabz workforce-grant readiness.

Usage:
  python3 scripts/workforce_grant_harness.py path/to/case.json

The harness intentionally separates:
1. mandatory eligibility gates;
2. evidence completeness;
3. rubric scoring.

It never upgrades UNKNOWN evidence into PASS and never treats a low score as
equivalent to a mandatory eligibility failure.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

GATES = [
    "eligible_applicant", "eligible_employer", "documented_employer_need",
    "eligible_trainees", "occupational_mapping", "required_match",
    "customized_occupational_training", "measurable_outcomes",
    "required_employer_commitments",
]

CATEGORIES = {
    "project_need": 10,
    "economic_impact": 10,
    "training_objectives_outcomes": 20,
    "training_design_cost_implementation": 20,
    "capacity_building": 20,
    "equity_economic_opportunity": 20,
}

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: workforce_grant_harness.py CASE.json", file=sys.stderr)
        return 2
    p = Path(sys.argv[1])
    try:
        case = json.loads(p.read_text())
    except Exception as e:
        print(f"BLOCKED: cannot read case: {e}")
        return 2

    missing = [g for g in GATES if case.get("gates", {}).get(g) is not True]
    score = 0
    category_scores = {}
    for name, maximum in CATEGORIES.items():
        raw = case.get("scores", {}).get(name, 0)
        try:
            value = float(raw)
        except (TypeError, ValueError):
            value = 0
        value = max(0, min(maximum, value))
        category_scores[name] = value
        score += value

    unknowns = case.get("unknowns", [])
    contradictions = case.get("contradictions", [])

    if missing:
        status = "BLOCKED"
        reason = "mandatory_gate_failure"
    elif contradictions:
        status = "BLOCKED"
        reason = "contradictory_evidence"
    elif score < 70:
        status = "NOT_READY"
        reason = "insufficient_internal_score"
    elif unknowns:
        status = "GRANT_READY_PARTNER_REQUIRED"
        reason = "unresolved_evidence"
    else:
        status = "GRANT_READY"
        reason = "all_gates_and_internal_threshold_passed"

    result = {
        "status": status,
        "reason": reason,
        "score": score,
        "max_score": 100,
        "category_scores": category_scores,
        "missing_mandatory_gates": missing,
        "unknowns": unknowns,
        "contradictions": contradictions,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if status in {"GRANT_READY", "GRANT_READY_PARTNER_REQUIRED", "NOT_READY"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
