#!/usr/bin/env python3
"""D1 — Failure-to-Leverage Harness.

Standard-library-only research harness for turning discovered failures into
higher-leverage reusable controls, tests, and questions.

The harness is deliberately causal and conservative:
- UNKNOWN is not ABSENT.
- agreement is not independence.
- a result is not a causal attribution.
- a detected failure may be a successful research discovery.
"""
from __future__ import annotations

import argparse
import json
import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "d1-1.0"
STATUSES = {"PASS", "FAIL", "BLOCKED", "UNRESOLVED", "TOOL_ERROR"}
VARIABLE_STATUSES = {"KNOWN_PRESENT", "KNOWN_ABSENT", "INTRODUCED", "PRE_EXISTING",
                     "SHARED", "ISOLATED", "UNKNOWN"}
INFLUENCE = {"NONE", "POTENTIAL", "MATERIAL", "UNKNOWN"}


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def load(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: cannot read JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("dossier root must be a JSON object")
    return data


def validate(dossier: dict[str, Any]) -> list[Finding]:
    errors: list[Finding] = []
    if dossier.get("schema_version") != SCHEMA_VERSION:
        errors.append(Finding("D1-SCHEMA", "BLOCK", "schema_version must be d1-1.0"))

    for key in ("research_id", "problem", "observed_event", "assumptions",
                "variables", "failure", "inversion", "leverage", "downstream",
                "tests"):
        if key not in dossier:
            errors.append(Finding("D1-MISSING", "BLOCK", f"missing required section: {key}"))

    for idx, variable in enumerate(_as_list(dossier.get("variables"))):
        if not isinstance(variable, dict):
            errors.append(Finding("D1-VAR", "BLOCK", f"variables[{idx}] must be an object"))
            continue
        status = variable.get("status")
        influence = variable.get("influence")
        if status not in VARIABLE_STATUSES:
            errors.append(Finding("D1-VAR-STATUS", "BLOCK",
                                  f"variables[{idx}] has invalid status {status!r}"))
        if influence not in INFLUENCE:
            errors.append(Finding("D1-VAR-INFLUENCE", "BLOCK",
                                  f"variables[{idx}] has invalid influence {influence!r}"))

    for idx, assumption in enumerate(_as_list(dossier.get("assumptions"))):
        if not isinstance(assumption, dict):
            errors.append(Finding("D1-ASSUMPTION", "BLOCK",
                                  f"assumptions[{idx}] must be an object"))
    for idx, candidate in enumerate(_as_list(dossier.get("leverage", {}).get("candidate_controls"))):
        if not isinstance(candidate, dict):
            errors.append(Finding("D1-LEVERAGE", "BLOCK",
                                  f"candidate_controls[{idx}] must be an object"))
            continue
        for field in ("impact", "recurrence", "generality", "cost"):
            value = candidate.get(field)
            if not isinstance(value, (int, float)) or value < 0:
                errors.append(Finding("D1-LEVERAGE-SCALE", "BLOCK",
                                      f"candidate_controls[{idx}].{field} must be >= 0"))
    return errors


def analyze(dossier: dict[str, Any]) -> dict[str, Any]:
    findings = validate(dossier)

    variables = _as_list(dossier.get("variables"))
    unknown_influential = [
        v for v in variables
        if isinstance(v, dict)
        and v.get("status") == "UNKNOWN"
        and v.get("influence") in {"POTENTIAL", "MATERIAL", "UNKNOWN"}
    ]

    shared_influential = [
        v for v in variables
        if isinstance(v, dict)
        and v.get("status") == "SHARED"
        and v.get("influence") in {"POTENTIAL", "MATERIAL", "UNKNOWN"}
    ]

    unverified_critical = [
        a for a in _as_list(dossier.get("assumptions"))
        if isinstance(a, dict)
        and a.get("critical", False)
        and a.get("verified") is not True
    ]

    tests = _as_list(dossier.get("tests"))
    failed_tests = [t for t in tests if isinstance(t, dict) and t.get("result") == "FAIL"]
    blocked_tests = [t for t in tests if isinstance(t, dict) and t.get("result") == "BLOCKED"]

    # Cascade depth: count downstream artifacts that explicitly depend on an
    # unresolved variable. This is intentionally explicit rather than inferred
    # from prose, so the provenance edge is inspectable.
    unresolved_names = {
        str(v.get("name"))
        for v in unknown_influential + shared_influential
        if v.get("name")
    }
    cascade_edges: list[dict[str, Any]] = []
    for item in _as_list(dossier.get("downstream")):
        if not isinstance(item, dict):
            continue
        deps = {str(x) for x in _as_list(item.get("depends_on"))}
        hit = sorted(deps & unresolved_names)
        if hit:
            cascade_edges.append({
                "artifact": item.get("artifact"),
                "depends_on_unresolved": hit,
                "decision": item.get("decision"),
            })
    cascade_depth = len(cascade_edges)

    controls: list[dict[str, Any]] = []
    for candidate in _as_list(dossier.get("leverage", {}).get("candidate_controls")):
        if not isinstance(candidate, dict):
            continue
        impact = float(candidate.get("impact", 0))
        recurrence = float(candidate.get("recurrence", 0))
        generality = float(candidate.get("generality", 0))
        cost = max(float(candidate.get("cost", 1)), 1.0)
        score = round((impact * recurrence * generality) / cost, 3)
        controls.append({
            "name": candidate.get("name"),
            "score": score,
            "impact": impact,
            "recurrence": recurrence,
            "generality": generality,
            "cost": cost,
            "reusable_test": candidate.get("reusable_test"),
        })
    controls.sort(key=lambda x: (-x["score"], str(x["name"])))

    derived_questions: list[str] = []
    for v in unknown_influential:
        name = v.get("name", "this unknown variable")
        derived_questions.extend([
            f"What is {name}, where does it enter the system, and who controls it?",
            f"Could {name} explain the observed result without the claimed intervention?",
            f"What ablation would isolate {name} from the claimed capability?",
        ])
    if shared_influential:
        derived_questions.append(
            "What evidence establishes that the apparently independent verifiers do not share the same upstream capability?"
        )
    if unverified_critical:
        derived_questions.append(
            "Which critical assumption remains unverified, and what test would convert it from assumed to measured?"
        )
    if cascade_depth:
        derived_questions.append(
            "Which downstream claims or artifacts must be re-evaluated because they depend on the unresolved variable?"
        )
    derived_questions.extend(_as_list(dossier.get("new_questions")))

    # Preserve order while deduplicating.
    deduped_questions = list(dict.fromkeys(str(q) for q in derived_questions if q))

    candidate_discovery = bool(
        dossier.get("failure", {}).get("description")
        or unknown_influential
        or failed_tests
        or blocked_tests
    )
    leverage_captured = bool(controls and deduped_questions)
    attribution_blocked = bool(unknown_influential or unverified_critical or shared_influential)
    cascade_detected = cascade_depth > 0 or bool(shared_influential and len(tests) > 1)

    if findings:
        verdict = "HARNESS_INPUT_INVALID"
    elif cascade_detected:
        verdict = "CASCADE_DETECTED"
    elif attribution_blocked:
        verdict = "ATTRIBUTION_BLOCKED"
    elif leverage_captured:
        verdict = "LEVERAGE_CAPTURED"
    elif candidate_discovery:
        verdict = "DISCOVERY_CAPTURED"
    else:
        verdict = "NO_NEW_DISCOVERY"

    if findings or attribution_blocked:
        publication_state = "BLOCKED"
    elif cascade_detected:
        publication_state = "REASSESS_DOWNSTREAM"
    elif leverage_captured:
        publication_state = "PROVISIONAL_RESEARCH_DISCOVERY"
    else:
        publication_state = "PROVISIONAL"

    return {
        "schema_version": SCHEMA_VERSION,
        "harness": "D1 Failure-to-Leverage Harness",
        "research_id": dossier.get("research_id"),
        "verdict": verdict,
        "publication_state": publication_state,
        "discovery": {
            "failure": dossier.get("failure"),
            "candidate_discovery": candidate_discovery,
            "new_failure_classes": _as_list(dossier.get("failure", {}).get("new_failure_classes")),
        },
        "attribution": {
            "unknown_influential_variables": unknown_influential,
            "shared_influential_variables": shared_influential,
            "unverified_critical_assumptions": unverified_critical,
            "blocked": attribution_blocked,
        },
        "cascade": {
            "detected": cascade_detected,
            "depth": cascade_depth,
            "edges": cascade_edges,
        },
        "leverage": {
            "captured": leverage_captured,
            "ranked_controls": controls,
            "top_control": controls[0] if controls else None,
        },
        "questions": deduped_questions,
        "test_summary": {
            "total": len(tests),
            "failed": len(failed_tests),
            "blocked": len(blocked_tests),
            "results": [t.get("result") for t in tests if isinstance(t, dict)],
        },
        "next_move": (
            "Freeze downstream attribution; isolate unresolved variables; run ablations; "
            "then promote the highest-leverage reusable control into the next experiment."
            if attribution_blocked or cascade_detected
            else "Instantiate the highest-leverage control as a reusable test and feed the generated questions into the next research cycle."
            if leverage_captured
            else "Run the next justified experiment and preserve the failure/evidence path."
        ),
    }


def template() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "research_id": "D1-YYYY-MM-DD-001",
        "problem": {
            "statement": "",
            "domain": "",
            "stakes": "low|medium|high",
        },
        "observed_event": {
            "result": "",
            "status": "PASS|FAIL|BLOCKED|UNRESOLVED",
        },
        "assumptions": [
            {
                "id": "A1",
                "statement": "",
                "verified": False,
                "critical": True,
            }
        ],
        "variables": [
            {
                "name": "example_unknown_variable",
                "status": "UNKNOWN",
                "influence": "POTENTIAL",
                "provenance": "",
                "shared": False,
                "controlled": False,
            }
        ],
        "failure": {
            "description": "",
            "evidence": "",
            "failure_type": "UNKNOWN_VARIABLE|MISATTRIBUTION|SHARED_CAPABILITY|CORRELATED_ERROR|OTHER",
            "new_failure_classes": [],
        },
        "inversion": {
            "apparent_axiom": "",
            "inverted_axiom": "",
            "competing_explanations": [],
        },
        "leverage": {
            "candidate_controls": [
                {
                    "name": "",
                    "impact": 1,
                    "recurrence": 1,
                    "generality": 1,
                    "cost": 1,
                    "reusable_test": "",
                }
            ]
        },
        "downstream": [
            {
                "artifact": "",
                "depends_on": [],
                "decision": "",
            }
        ],
        "tests": [
            {
                "name": "",
                "result": "BLOCKED",
                "evidence": "",
            }
        ],
        "new_questions": [],
    }


def run_self_test() -> dict[str, Any]:
    class D1Tests(unittest.TestCase):
        def test_hidden_shared_capability_blocks(self) -> None:
            d = template()
            d["research_id"] = "SELF-HIDDEN"
            d["variables"] = [
                {"name": "shared_vision_preprocessor", "status": "UNKNOWN",
                 "influence": "MATERIAL", "provenance": "unverified",
                 "shared": True, "controlled": False},
            ]
            d["assumptions"] = []
            d["failure"]["description"] = "Two verifiers may share one upstream visual capability."
            d["tests"] = [{"name": "model_a", "result": "PASS"},
                          {"name": "model_b", "result": "PASS"}]
            d["downstream"] = [
                {"artifact": "claim-1", "depends_on": ["shared_vision_preprocessor"],
                 "decision": "publish"},
            ]
            d["leverage"]["candidate_controls"] = [
                {"name": "capability census", "impact": 5, "recurrence": 5,
                 "generality": 5, "cost": 1, "reusable_test": "inventory+ablation"},
            ]
            out = analyze(d)
            self.assertEqual(out["verdict"], "CASCADE_DETECTED")
            self.assertTrue(out["attribution"]["blocked"])
            self.assertEqual(out["cascade"]["depth"], 1)
            self.assertEqual(out["leverage"]["top_control"]["name"], "capability census")

        def test_false_failure_is_attribution_problem(self) -> None:
            d = template()
            d["research_id"] = "SELF-FALSE-FAILURE"
            d["variables"] = [
                {"name": "image_resolution", "status": "PRE_EXISTING",
                 "influence": "MATERIAL", "provenance": "known",
                 "shared": False, "controlled": False},
            ]
            d["assumptions"] = []
            d["failure"]["description"] = "Model failed after degraded image transformation."
            d["tests"] = [{"name": "degraded-pipeline", "result": "FAIL"}]
            out = analyze(d)
            self.assertEqual(out["verdict"], "DISCOVERY_CAPTURED")
            self.assertFalse(out["attribution"]["blocked"])

        def test_clean_leverage_capture(self) -> None:
            d = template()
            d["research_id"] = "SELF-CLEAN"
            d["variables"] = [
                {"name": "controlled_input", "status": "ISOLATED",
                 "influence": "NONE", "provenance": "measured",
                 "shared": False, "controlled": True},
            ]
            d["assumptions"] = []
            d["failure"] = {"description": "A routing assumption failed.",
                            "evidence": "replicated trace",
                            "failure_type": "MISATTRIBUTION",
                            "new_failure_classes": ["router-blindness"]}
            d["leverage"]["candidate_controls"] = [
                {"name": "preflight capability inventory", "impact": 5, "recurrence": 5,
                 "generality": 5, "cost": 1, "reusable_test": "run before attribution"},
            ]
            d["new_questions"] = ["What other capability classes are currently unmodeled?"]
            out = analyze(d)
            self.assertEqual(out["verdict"], "LEVERAGE_CAPTURED")
            self.assertEqual(out["leverage"]["top_control"]["score"], 125.0)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(D1Tests)
    result = unittest.TestResult()
    suite.run(result)
    failures = [str(x[1]) for x in result.failures + result.errors]
    return {
        "harness": "D1 Failure-to-Leverage Harness",
        "status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests": result.testsRun,
        "failures": failures,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init", help="write a blank D1 dossier")
    init_cmd.add_argument("output", type=Path)

    analyze_cmd = sub.add_parser("analyze", help="analyze a D1 dossier")
    analyze_cmd.add_argument("dossier", type=Path)
    analyze_cmd.add_argument("-o", "--output", type=Path)

    sub.add_parser("self-test", help="run deterministic harness tests")

    args = parser.parse_args(argv)

    if args.command == "init":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(template(), indent=2) + "\\n")
        print(args.output)
        return 0

    if args.command == "self-test":
        out = run_self_test()
        print(json.dumps(out, indent=2))
        return 0 if out["status"] == "PASS" else 1

    try:
        dossier = load(args.dossier)
        result = analyze(dossier)
    except ValueError as exc:
        print(f"D1 ERROR: {exc}", file=sys.stderr)
        return 2

    encoded = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\\n")
    else:
        print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
