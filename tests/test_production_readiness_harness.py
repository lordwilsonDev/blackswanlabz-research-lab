import hashlib
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "production_readiness_harness.py"
spec = importlib.util.spec_from_file_location("prh", SCRIPT)
prh = importlib.util.module_from_spec(spec)
sys.modules["prh"] = prh
spec.loader.exec_module(prh)


def _write_evidence(base: Path, evidence_id: str, covers: list[str]) -> dict:
    rel = Path("evidence") / f"{evidence_id.lower()}.json"
    target = base / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({
        "fixture_only": True,
        "evidence_id": evidence_id,
        "covers": covers,
        "result": "PASS",
        "note": "Synthetic test receipt; not production evidence."
    }, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    return {
        "id": evidence_id,
        "path": rel.as_posix(),
        "sha256": digest,
        "kind": "synthetic_test_receipt",
        "source": "unit-test-fixture",
        "observed_at": "2026-10-09",
        "expires_at": "2026-12-31",
        "epistemic_status": "VERIFIED",
        "covers": covers,
    }


def make_case(base: Path, profile="internal") -> dict:
    evaluation_checks = list(prh.PROFILE_CHECKS[profile])
    evidence = [
        _write_evidence(base, "EV-MODEL", ["model.qualification", "model.fallback_test"]),
        _write_evidence(base, "EV-AUTH", ["permissions.least_privilege_test"]),
        _write_evidence(base, "EV-EVAL", ["evaluation.independent_verifier"] + [f"evaluation.{x}" for x in evaluation_checks]),
        _write_evidence(base, "EV-OPS", ["operations.monitoring", "operations.redaction", "operations.rollback_test"]),
        _write_evidence(base, "EV-RELEASE", ["release.authorization"]),
    ]
    pass_with = lambda refs: {"status": "PASS", "evidence_refs": refs, "detail": "synthetic fixture"}
    return {
        "schema_version": "1.0",
        "case_id": "PRH-TEST-001",
        "skill": {
            "id": "fixture.skill", "version": "1.2.0", "owner": "test-owner",
            "purpose": "Exercise the readiness auditor in unit tests.",
            "scope": {"allowed_paths": ["sandbox/**"], "forbidden_paths": ["production/**"]},
        },
        "contract": {
            "inputs": ["well-formed fixture case"], "outputs": ["JSON report"],
            "limitations": ["unit test only"], "acceptance_criteria": ["status follows declared gates"],
        },
        "permissions": {
            "allowed_actions": ["read", "write_sandbox"],
            "denied_actions": ["deploy_production", "change_policy"],
            "approval_required_for": ["merge", "deploy", "external_side_effect"],
            "overbroad": False,
            "least_privilege_test": pass_with(["EV-AUTH"]),
        },
        "model": {
            "provider": "fixture-provider", "model_id": "fixture-model@revision-1",
            "task_profile": "structured output and bounded tool use",
            "required_capabilities": ["schema_fidelity", "tool_use", "abstention"],
            "qualification": {
                "status": "PASS", "evaluated_at": "2026-10-09", "expires_at": "2026-12-01",
                "suite_version": "fixture-suite-1", "known_limits": ["synthetic tests only"],
                "capability_results": {"schema_fidelity": "PASS", "tool_use": "PASS", "abstention": "PASS"},
                "evidence_refs": ["EV-MODEL"],
            },
            "fallback_test": pass_with(["EV-MODEL"]), "version_pinned": True,
        },
        "evaluation": {
            "baseline_id": "baseline-fixture-1", "holdout": True,
            "independent_verifier": pass_with(["EV-EVAL"]),
            "checks": {name: pass_with(["EV-EVAL"]) for name in evaluation_checks},
        },
        "operations": {
            "timeout_seconds": 120, "max_retries": 2, "budget_limit": {"tokens": 20000, "usd": 1.0},
            "monitoring": pass_with(["EV-OPS"]), "redaction": pass_with(["EV-OPS"]),
            "rollback_test": pass_with(["EV-OPS"]), "incident_owner": "test-owner",
            "rollback_plan": "restore pre-run snapshot", "maintenance_trigger": "model/dependency change",
            "rate_limit_policy": "bounded backoff then safe stop", "network_egress_policy": "deny by default",
            "secrets_handling": "no secrets in prompts; scoped reference only", "human_escalation": "page test-owner",
            "concurrency_limit": "one run", "input_size_limit": "64 KiB",
            "user_feedback_channel": "internal issue tracker", "dependencies_pinned": True,
            "idempotency_tested": True, "backup_recovery_tested": True,
        },
        "governance": {
            "data_classification": "synthetic only", "retention_policy": "30 days",
            "deletion_policy": "delete by request after audit hold", "incident_playbook": "playbook-fixture-1",
            "intellectual_property_policy": "lab-owned fixture content", "audit_log_retention": "90 days",
            "deployment_region": "not applicable to unit fixture", "support_boundary": "tests only",
            "deprecation_policy": "versioned with migration notes",
        },
        "release": {
            "profile": profile, "approval_status": "APPROVED", "authorized_by": "unit-test-reviewer",
            "evidence_refs": ["EV-RELEASE"],
        },
        "evidence": evidence,
    }


def test_complete_declared_case_reaches_release_eligible_but_disclaims_limits(tmp_path):
    case = make_case(tmp_path)
    result = prh.Auditor(case, tmp_path, date(2026, 10, 9)).run()
    assert result["status"] == "RELEASE_ELIGIBLE"
    assert result["assessment_type"] == "manifest_preflight_not_live_execution"
    assert any("does not execute tests" in text for text in result["interpretation_limits"])


def test_missing_required_check_cannot_pass(tmp_path):
    case = make_case(tmp_path)
    del case["evaluation"]["checks"]["security"]
    result = prh.Auditor(case, tmp_path, date(2026, 10, 9)).run()
    assert result["status"] == "NOT_READY"
    assert any(c["id"] == "evaluation.security" and c["status"] == "NOT_ASSESSED" for c in result["checks"])


def test_failed_security_check_blocks_release(tmp_path):
    case = make_case(tmp_path)
    case["evaluation"]["checks"]["security"]["status"] = "FAIL"
    result = prh.Auditor(case, tmp_path, date(2026, 10, 9)).run()
    assert result["status"] == "BLOCKED"


def test_tampered_evidence_blocks_release(tmp_path):
    case = make_case(tmp_path)
    evidence = tmp_path / case["evidence"][0]["path"]
    evidence.write_text("tampered\n", encoding="utf-8")
    result = prh.Auditor(case, tmp_path, date(2026, 10, 9)).run()
    assert result["status"] == "BLOCKED"
    assert result["evidence_integrity"]["EV-MODEL"]["status"] == "BLOCKED"


def test_path_traversal_is_blocked(tmp_path):
    case = make_case(tmp_path)
    case["evidence"][0]["path"] = "../outside.json"
    result = prh.Auditor(case, tmp_path, date(2026, 10, 9)).run()
    assert result["status"] == "BLOCKED"


def test_expired_model_qualification_is_not_ready(tmp_path):
    case = make_case(tmp_path)
    case["model"]["qualification"]["expires_at"] = "2026-10-08"
    result = prh.Auditor(case, tmp_path, date(2026, 10, 9)).run()
    assert result["status"] == "NOT_READY"


def test_release_approval_is_separate_from_technical_qualification(tmp_path):
    case = make_case(tmp_path)
    case["release"]["approval_status"] = "PENDING"
    result = prh.Auditor(case, tmp_path, date(2026, 10, 9)).run()
    assert result["status"] == "NOT_READY"
    assert any(c["id"] == "release.authorization" and c["status"] == "NOT_ASSESSED" for c in result["checks"])


def test_inferred_evidence_is_not_silently_promoted(tmp_path):
    case = make_case(tmp_path)
    case["evidence"][0]["epistemic_status"] = "INFERRED"
    result = prh.Auditor(case, tmp_path, date(2026, 10, 9)).run()
    assert result["status"] == "NOT_READY"


def test_high_impact_profile_requires_fail_safe_human_governance(tmp_path):
    case = make_case(tmp_path, "high_impact")
    case["governance"].pop("human_decision_owner", None)
    case["governance"].pop("appeal_or_override_path", None)
    case["governance"].pop("domain_policy_reference", None)
    case["permissions"]["approval_required_for"] = ["merge"]
    result = prh.Auditor(case, tmp_path, date(2026, 10, 9)).run()
    assert result["status"] in {"NOT_READY", "BLOCKED"}
    assert any(c["id"] == "permissions.high_impact_human_gate" and c["status"] == "NOT_ASSESSED" for c in result["checks"])


def test_duplicate_evidence_ids_are_tool_error(tmp_path):
    case = make_case(tmp_path)
    case["evidence"].append(dict(case["evidence"][0]))
    result = prh.Auditor(case, tmp_path, date(2026, 10, 9)).run()
    assert result["status"] == "TOOL_ERROR"


def test_tool_error_remains_distinct_from_failure(tmp_path):
    case = make_case(tmp_path)
    case["evaluation"]["checks"]["unit"]["status"] = "TOOL_ERROR"
    result = prh.Auditor(case, tmp_path, date(2026, 10, 9)).run()
    assert result["status"] == "TOOL_ERROR"


def test_unsupported_schema_version_is_a_tool_error(tmp_path):
    case = make_case(tmp_path)
    case["schema_version"] = "99.0"
    result = prh.Auditor(case, tmp_path, date(2026, 10, 9)).run()
    assert result["status"] == "TOOL_ERROR"
