#!/usr/bin/env python3
"""Independent bounded verifier for Q2B-MBEDDR-002.

The learner artifact is supplied as a Python module path. The verifier invokes
the module only through the registered adapter contract and never imports
learner reasoning/context.

Expected learner adapter:
    module.create_controller()
    controller.add_state(name, initial=False)
    controller.add_transition(source, event, destination, guard=None)
    controller.quantity(value, unit)
    controller.dispatch(event)
    controller.current_state
    controller.verify_reachability()
    controller.verify_guards(probes)

The adapter contract is intentionally narrow so verifier behavior can be
tested independently from the learner implementation.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


VERIFIER_VERSION = "q2b-mbeddr-002-verifier-0.1.2"
TASK_ID = "Q2B-MBEDDR-002"


def make_result(condition: bool, criterion_id: str, evidence: str, notes: str = "") -> dict[str, object]:
    return {
        "criterion_id": criterion_id,
        "verdict": "PASS" if condition else "FAIL",
        "checked_scope": [criterion_id],
        "unchecked_scope": ["formal proof beyond supplied executable probes"],
        "verification_level": "bounded",
        "evidence_reference": evidence,
        "failure_classification": None if condition else "artifact_failure",
        "notes": notes or None,
    }

def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("learner_artifact", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load learner artifact: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(condition: bool, criterion_id: str, evidence: str, notes: str = "") -> Result:
    return Result(
        criterion_id=criterion_id,
        verdict="PASS" if condition else "FAIL",
        checked_scope=[criterion_id],
        unchecked_scope=["formal proof beyond supplied executable probes"],
        verification_level="bounded",
        evidence_reference=evidence,
        failure_classification=None if condition else "artifact_failure",
        notes=notes or None,
    )


def verify(module_path: Path) -> dict[str, Any]:
    module = load_module(module_path)
    controller = module.create_controller()

    # Criterion C1: scaled compatible quantities.
    q36 = controller.quantity(36, "km/h")
    q10 = controller.quantity(10, "m/s")
    c1 = make_result(
        q36.dimension == q10.dimension and q36.to_si() == q10.to_si(),
        "C1-unit-normalization",
        "probe: 36 km/h == 10 m/s",
    )

    # Criterion C2: incompatible dimensions rejected.
    incompatible_rejected = False
    try:
        controller.compare(controller.quantity(1, "m/s"), controller.quantity(1, "m"))
    except Exception:
        incompatible_rejected = True
    c2 = make_result(
        incompatible_rejected,
        "C2-incompatible-units",
        "probe: m/s compared with m raises",
    )

    # Build the registered controller behavior.
    controller.add_state("Idle", initial=True)
    controller.add_state("Moving")
    controller.add_state("Fast")
    controller.add_transition("Idle", "START", "Moving")
    controller.add_transition("Moving", "TICK", "Fast",
                              guard=("speed", ">=", controller.quantity(10, "m/s")))
    controller.add_transition("Moving", "STOP", "Idle")
    controller.add_transition("Fast", "STOP", "Idle")

    controller.dispatch("START")
    start_ok = controller.current_state == "Moving"
    controller.set_environment(speed=controller.quantity(36, "km/h"))
    controller.dispatch("TICK")
    fast_ok = controller.current_state == "Fast"
    controller.dispatch("STOP")
    stop_ok = controller.current_state == "Idle"
    c3 = make_result(start_ok and fast_ok and stop_ok, "C3-controller-semantics",
               "probe: START -> Moving; 36 km/h TICK -> Fast; STOP -> Idle")

    # Criterion C4: bounded static checks expose the registered verifier hooks.
    reachability = controller.verify_reachability()
    guard_report = controller.verify_guards([
        controller.quantity(9, "m/s"),
        controller.quantity(10, "m/s"),
        controller.quantity(35, "km/h"),
        controller.quantity(36, "km/h"),
    ])
    c4 = make_result(
        isinstance(reachability, dict) and isinstance(guard_report, dict),
        "C4-bounded-static-analysis",
        "probe: reachability and guard verification return structured reports",
        "Bounded by the supplied probe domain.",
    )

    results = [c1, c2, c3, c4]
    if any(not isinstance(r, dict) for r in results):
        raise RuntimeError("internal verifier defect: criterion result was not a dictionary")
    return {
        "verifier_version": VERIFIER_VERSION,
        "task_id": TASK_ID,
        "verification_level": "bounded",
        "results": results,
        "overall_verdict": "PASS" if all(r["verdict"] == "PASS" for r in results) else "FAIL",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: q2b_mbeddr_002_verifier.py ARTIFACT.py", file=sys.stderr)
        return 2

    try:
        report = verify(Path(sys.argv[1]).resolve())
    except Exception as exc:
        report = {
            "verifier_version": VERIFIER_VERSION,
            "task_id": TASK_ID,
            "verification_level": "bounded",
            "overall_verdict": "VERIFIER_ERROR",
            "verifier_error": repr(exc),
        }

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["overall_verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
