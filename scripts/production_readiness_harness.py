#!/usr/bin/env python3
"""Deterministic, evidence-integrity-aware preflight for skill readiness manifests.

This v1 audits a declared readiness case. It does NOT execute the tests described by
that case, prove that an external evaluator is independent, or establish that a
self-reported result is true. A passing result means the submitted manifest meets
its declared policy gates and referenced artifacts match their declared hashes.
Production adapters must replace self-reported statuses with collected receipts.

Usage:
  python3 scripts/production_readiness_harness.py CASE.json [--as-of YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Tests are chosen by risk profile; these are policy defaults, not universal laws.
PROFILE_CHECKS: dict[str, tuple[str, ...]] = {
    "research": (
        "unit", "contract", "negative", "adversarial", "regression", "security", "reproducibility"
    ),
    "internal": (
        "unit", "contract", "integration", "e2e", "negative", "adversarial",
        "regression", "security", "mutation", "reproducibility"
    ),
    "customer_facing": (
        "unit", "contract", "integration", "e2e", "negative", "adversarial",
        "regression", "security", "privacy", "performance", "accessibility",
        "mutation", "reproducibility"
    ),
    "high_impact": (
        "unit", "contract", "integration", "e2e", "negative", "adversarial",
        "regression", "security", "privacy", "performance", "mutation",
        "reproducibility", "hazard_analysis", "fail_safe", "domain_review",
        "external_review", "human_acceptance"
    ),
}

HARD_BLOCK_CHECKS = {
    "permissions.least_privilege_test",
    "model.qualification",
    "evaluation.independent_verifier",
    "evaluation.security",
    "evaluation.privacy",
    "evaluation.hazard_analysis",
    "evaluation.fail_safe",
    "evaluation.domain_review",
    "evaluation.external_review",
    "operations.rollback_test",
    "release.authorization",
}

STATUS_MAP = {"PASS", "FAIL", "NOT_RUN", "UNKNOWN", "BLOCKED", "TOOL_ERROR"}
EVIDENCE_STATUSES = {"VERIFIED", "SUPPORTED", "PROVISIONAL", "INFERRED", "UNKNOWN", "CONTRADICTED"}


@dataclass
class Check:
    id: str
    area: str
    status: str
    blocking: bool
    detail: str
    evidence_refs: list[str]


def _get(data: Any, dotted: str, default: Any = None) -> Any:
    cur = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def _nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple)):
        return len(value) > 0
    return value is not None


def _parse_date(value: Any) -> date | None:
    if not isinstance(value, str) or not DATE_RE.match(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class Auditor:
    def __init__(self, case: dict[str, Any], base_dir: Path, as_of: date):
        self.case = case
        self.base_dir = base_dir.resolve()
        self.as_of = as_of
        self.checks: list[Check] = []
        self.evidence_by_id: dict[str, dict[str, Any]] = {}
        self.evidence_integrity: dict[str, dict[str, Any]] = {}
        self.fatal_input_errors: list[str] = []
        self.profile = _get(case, "release.profile", "")
        self.required_checks = PROFILE_CHECKS.get(self.profile, ())
        self._index_evidence()

    def add(self, check_id: str, area: str, status: str, detail: str,
            *, blocking: bool | None = None, evidence_refs: list[str] | None = None) -> None:
        if blocking is None:
            blocking = check_id in HARD_BLOCK_CHECKS or status in {"FAIL", "BLOCKED"}
        self.checks.append(Check(check_id, area, status, bool(blocking), detail,
                                 list(evidence_refs or [])))

    def _index_evidence(self) -> None:
        rows = self.case.get("evidence", [])
        if not isinstance(rows, list):
            self.fatal_input_errors.append("evidence must be an array")
            return
        for row in rows:
            if not isinstance(row, dict):
                self.fatal_input_errors.append("each evidence record must be an object")
                continue
            eid = row.get("id")
            if not isinstance(eid, str) or not eid.strip():
                self.fatal_input_errors.append("every evidence record requires a non-empty id")
                continue
            if eid in self.evidence_by_id:
                self.fatal_input_errors.append(f"duplicate evidence id: {eid}")
                continue
            self.evidence_by_id[eid] = row
            self.evidence_integrity[eid] = self._check_evidence_file(row)

    def _check_evidence_file(self, row: dict[str, Any]) -> dict[str, Any]:
        eid = str(row.get("id", "UNKNOWN"))
        rel = row.get("path")
        declared = row.get("sha256")
        if not isinstance(rel, str) or not rel.strip():
            return {"status": "NOT_ASSESSED", "detail": "evidence path is missing"}
        if Path(rel).is_absolute():
            return {"status": "BLOCKED", "detail": "absolute evidence paths are forbidden"}
        if not isinstance(declared, str) or not HEX_SHA256.match(declared):
            return {"status": "NOT_ASSESSED", "detail": "a 64-character lowercase SHA-256 is required"}
        try:
            # Check containment before requiring existence so even a nonexistent ../ path is blocked.
            candidate = (self.base_dir / rel).resolve(strict=False)
            candidate.relative_to(self.base_dir)
        except ValueError:
            return {"status": "BLOCKED", "detail": "evidence path escapes the case directory"}
        except OSError as exc:
            return {"status": "TOOL_ERROR", "detail": f"cannot resolve evidence artifact: {exc}"}
        try:
            candidate = candidate.resolve(strict=True)
        except FileNotFoundError:
            return {"status": "NOT_ASSESSED", "detail": f"evidence artifact not found: {rel}"}
        except OSError as exc:
            return {"status": "TOOL_ERROR", "detail": f"cannot resolve evidence artifact: {exc}"}
        try:
            candidate.relative_to(self.base_dir)
        except ValueError:
            return {"status": "BLOCKED", "detail": "evidence path escapes the case directory"}
        if not candidate.is_file():
            return {"status": "NOT_ASSESSED", "detail": "evidence path does not resolve to a regular file"}
        try:
            actual = _sha256(candidate)
        except OSError as exc:
            return {"status": "TOOL_ERROR", "detail": f"cannot hash evidence artifact: {exc}"}
        if actual != declared:
            return {"status": "BLOCKED", "detail": "evidence hash mismatch", "declared_sha256": declared,
                    "actual_sha256": actual}
        observed = _parse_date(row.get("observed_at"))
        if observed is None:
            return {"status": "NOT_ASSESSED", "detail": "observed_at must be a real YYYY-MM-DD date"}
        if observed > self.as_of:
            return {"status": "NOT_ASSESSED", "detail": "evidence observation date is in the future"}
        expires = row.get("expires_at")
        if expires is not None:
            expiry = _parse_date(expires)
            if expiry is None:
                return {"status": "NOT_ASSESSED", "detail": "expires_at must be null or YYYY-MM-DD"}
            if expiry < self.as_of:
                return {"status": "STALE", "detail": f"evidence expired on {expiry.isoformat()}"}
        if not _nonempty(row.get("kind")) or not _nonempty(row.get("source")):
            return {"status": "NOT_ASSESSED", "detail": "evidence kind and source are required"}
        if not isinstance(row.get("covers"), list) or not row["covers"]:
            return {"status": "NOT_ASSESSED", "detail": "evidence must declare the checks it covers"}
        # Integrity is intentionally not equivalent to truth or independence.
        return {"status": "PASS", "detail": "artifact exists and its bytes match the declared SHA-256",
                "path": rel, "sha256": actual}

    def evidence_refs_status(self, refs: Any, check_id: str) -> tuple[str, str, list[str]]:
        if not isinstance(refs, list) or not refs:
            return "NOT_ASSESSED", "no evidence references supplied", []
        seen: list[str] = []
        for ref in refs:
            if not isinstance(ref, str) or ref not in self.evidence_by_id:
                return "NOT_ASSESSED", f"unknown evidence reference: {ref}", [str(x) for x in refs]
            row = self.evidence_by_id[ref]
            integrity = self.evidence_integrity.get(ref, {"status": "NOT_ASSESSED", "detail": "not indexed"})
            if integrity["status"] != "PASS":
                return integrity["status"], f"{ref}: {integrity['detail']}", [str(x) for x in refs]
            covers = row.get("covers", [])
            if check_id not in covers and "*" not in covers:
                return "NOT_ASSESSED", f"{ref} does not declare coverage for {check_id}", [str(x) for x in refs]
            state = row.get("epistemic_status", "UNKNOWN")
            if state not in EVIDENCE_STATUSES:
                return "NOT_ASSESSED", f"{ref} has invalid epistemic_status", [str(x) for x in refs]
            if state == "CONTRADICTED":
                return "FAIL", f"{ref} is marked CONTRADICTED", [str(x) for x in refs]
            # The checker does not silently promote provisional/inferred/supported items.
            if state != "VERIFIED":
                return "NOT_ASSESSED", f"{ref} is {state}, not VERIFIED", [str(x) for x in refs]
            seen.append(ref)
        return "PASS", "referenced artifacts exist, hash-match, are current, and declare coverage", seen

    def evaluate_declared_status(self, check_id: str, area: str, obj: Any,
                                 *, blocking: bool | None = None) -> None:
        if not isinstance(obj, dict):
            self.add(check_id, area, "NOT_ASSESSED", "check record is missing or is not an object",
                     blocking=blocking)
            return
        status = obj.get("status")
        if status not in STATUS_MAP:
            self.add(check_id, area, "NOT_ASSESSED", "status must be PASS/FAIL/NOT_RUN/UNKNOWN/BLOCKED/TOOL_ERROR",
                     blocking=blocking)
            return
        if status in {"FAIL", "BLOCKED", "TOOL_ERROR"}:
            self.add(check_id, area, status,
                     f"declared check result is {status}: {obj.get('detail', 'no detail supplied')}",
                     blocking=blocking, evidence_refs=obj.get("evidence_refs", []))
            return
        if status != "PASS":
            self.add(check_id, area, "NOT_ASSESSED", f"declared check result is {status}",
                     blocking=blocking, evidence_refs=obj.get("evidence_refs", []))
            return
        refs_status, detail, refs = self.evidence_refs_status(obj.get("evidence_refs"), check_id)
        self.add(check_id, area, refs_status, detail, blocking=blocking, evidence_refs=refs)

    def run(self) -> dict[str, Any]:
        if self.fatal_input_errors:
            return self._result("TOOL_ERROR", "invalid_manifest", self.fatal_input_errors)
        if self.case.get("schema_version") != SCHEMA_VERSION:
            self.add("manifest.schema_version", "manifest", "TOOL_ERROR",
                     f"schema_version must be {SCHEMA_VERSION}", blocking=False)
            return self._result("TOOL_ERROR", "unsupported_schema_version",
                                [f"schema_version must be {SCHEMA_VERSION}"])

        # Skill identity, boundaries and contracts: a skill cannot be qualified on its name alone.
        for key in ("id", "version", "owner", "purpose"):
            value = _get(self.case, f"skill.{key}")
            self.add(f"skill.{key}", "skill_contract", "PASS" if _nonempty(value) else "NOT_ASSESSED",
                     "declared" if _nonempty(value) else "required field is missing", blocking=False)
        for key in ("allowed_paths", "forbidden_paths"):
            value = _get(self.case, f"skill.scope.{key}")
            self.add(f"skill.scope.{key}", "scope", "PASS" if isinstance(value, list) else "NOT_ASSESSED",
                     "explicit scope list supplied" if isinstance(value, list) else "scope list missing", blocking=False)
        for key in ("inputs", "outputs", "limitations", "acceptance_criteria"):
            value = _get(self.case, f"contract.{key}")
            ok = isinstance(value, list) and len(value) > 0 and all(_nonempty(x) for x in value)
            self.add(f"contract.{key}", "skill_contract", "PASS" if ok else "NOT_ASSESSED",
                     "non-empty contract list supplied" if ok else "explicit non-empty list required", blocking=False)

        # Authority is separate from model capability. Any declared overbroad access blocks.
        overbroad = _get(self.case, "permissions.overbroad")
        if overbroad is True:
            self.add("permissions.overbroad", "authority", "FAIL", "permissions marked overbroad", blocking=True)
        elif overbroad is False:
            self.add("permissions.overbroad", "authority", "PASS", "permissions not marked overbroad", blocking=False)
        else:
            self.add("permissions.overbroad", "authority", "NOT_ASSESSED", "explicit overbroad-permission assessment missing", blocking=False)
        for key in ("allowed_actions", "denied_actions", "approval_required_for"):
            value = _get(self.case, f"permissions.{key}")
            ok = isinstance(value, list) and (key == "allowed_actions" or bool(value))
            self.add(f"permissions.{key}", "authority", "PASS" if ok else "NOT_ASSESSED",
                     "explicit action list supplied" if ok else "explicit list required; denied actions cannot be implicit",
                     blocking=False)
        self.evaluate_declared_status("permissions.least_privilege_test", "authority",
                                      _get(self.case, "permissions.least_privilege_test"), blocking=True)

        # Model is qualified for a task profile, not merely named by provider or brand.
        for key in ("provider", "model_id", "task_profile", "required_capabilities"):
            value = _get(self.case, f"model.{key}")
            ok = _nonempty(value) and (key != "required_capabilities" or isinstance(value, list))
            self.add(f"model.{key}", "model_fit", "PASS" if ok else "NOT_ASSESSED",
                     "declared" if ok else "required field is missing", blocking=False)
        qualification = _get(self.case, "model.qualification", {})
        for key in ("suite_version", "known_limits"):
            value = _get(self.case, f"model.qualification.{key}")
            ok = _nonempty(value) and (key != "known_limits" or isinstance(value, list))
            self.add(f"model.qualification.{key}", "model_fit", "PASS" if ok else "NOT_ASSESSED",
                     "declared" if ok else "qualification suite version and explicit limits are required", blocking=False)
        self.evaluate_declared_status("model.qualification", "model_fit", qualification, blocking=True)
        q_eval = _parse_date(_get(self.case, "model.qualification.evaluated_at"))
        q_exp = _parse_date(_get(self.case, "model.qualification.expires_at"))
        if q_eval is None or q_exp is None:
            self.add("model.qualification_window", "model_fit", "NOT_ASSESSED",
                     "evaluated_at and expires_at must be real YYYY-MM-DD dates", blocking=False)
        elif q_eval > self.as_of:
            self.add("model.qualification_window", "model_fit", "NOT_ASSESSED",
                     "qualification evaluation date is in the future", blocking=False)
        elif q_exp < self.as_of:
            self.add("model.qualification_window", "model_fit", "STALE",
                     f"model qualification expired on {q_exp.isoformat()}", blocking=False)
        else:
            self.add("model.qualification_window", "model_fit", "PASS",
                     "model qualification is within its declared validity window", blocking=False)
        required_caps = _get(self.case, "model.required_capabilities", [])
        cap_results = _get(self.case, "model.qualification.capability_results", {})
        if not isinstance(required_caps, list) or not required_caps:
            self.add("model.capability_coverage", "model_fit", "NOT_ASSESSED",
                     "required capability list is missing", blocking=False)
        else:
            missing_caps = [x for x in required_caps if not isinstance(cap_results, dict) or cap_results.get(x) != "PASS"]
            self.add("model.capability_coverage", "model_fit", "PASS" if not missing_caps else "NOT_ASSESSED",
                     "all required capabilities passed" if not missing_caps else f"not qualified: {missing_caps}", blocking=False)
        self.evaluate_declared_status("model.fallback_test", "model_fit", _get(self.case, "model.fallback_test"), blocking=False)
        pinned = _get(self.case, "model.version_pinned")
        self.add("model.version_pinned", "model_fit", "PASS" if pinned is True else "NOT_ASSESSED",
                 "model revision pinned" if pinned is True else "exact model revision/version not pinned", blocking=False)

        # Evaluation design: no single self-authored happy-path test is enough.
        baseline = _get(self.case, "evaluation.baseline_id")
        self.add("evaluation.baseline", "evaluation_design", "PASS" if _nonempty(baseline) else "NOT_ASSESSED",
                 "comparison baseline declared" if _nonempty(baseline) else "baseline/counterfactual not declared", blocking=False)
        holdout = _get(self.case, "evaluation.holdout")
        self.add("evaluation.holdout", "evaluation_design", "PASS" if holdout is True else "NOT_ASSESSED",
                 "holdout/transfer set declared" if holdout is True else "holdout/transfer evaluation not established", blocking=False)
        self.evaluate_declared_status("evaluation.independent_verifier", "evaluation_design",
                                      _get(self.case, "evaluation.independent_verifier"), blocking=True)
        checks = _get(self.case, "evaluation.checks", {})
        for name in self.required_checks:
            obj = checks.get(name) if isinstance(checks, dict) else None
            check_id = f"evaluation.{name}"
            self.evaluate_declared_status(check_id, "evaluation", obj,
                                          blocking=(name in {"security", "privacy", "hazard_analysis", "fail_safe",
                                                            "domain_review", "external_review"}))
        # Unknown check labels in the case are reported rather than silently accepted.
        if isinstance(checks, dict):
            for name in sorted(set(checks) - set(PROFILE_CHECKS.get(self.profile, ()))):
                self.add(f"evaluation.unmapped.{name}", "evaluation_design", "NOT_ASSESSED",
                         "check is declared but is not part of the selected profile policy", blocking=False)

        # Operations controls protect against hangs, runaway costs, data leaks, and unrollable changes.
        timeout = _get(self.case, "operations.timeout_seconds")
        if isinstance(timeout, (int, float)) and not isinstance(timeout, bool) and timeout > 0:
            self.add("operations.timeout", "operations", "PASS", f"bounded timeout: {timeout}s", blocking=False)
        else:
            self.add("operations.timeout", "operations", "NOT_ASSESSED", "positive bounded timeout required", blocking=False)
        retries = _get(self.case, "operations.max_retries")
        if isinstance(retries, int) and not isinstance(retries, bool) and 0 <= retries <= 10:
            self.add("operations.retry_bound", "operations", "PASS", f"bounded retries: {retries}", blocking=False)
        else:
            self.add("operations.retry_bound", "operations", "NOT_ASSESSED", "max_retries must be an integer from 0 to 10", blocking=False)
        budget = _get(self.case, "operations.budget_limit", {})
        budget_ok = isinstance(budget, dict) and any(isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 for v in budget.values())
        self.add("operations.budget_limit", "operations", "PASS" if budget_ok else "NOT_ASSESSED",
                 "at least one positive resource budget is declared" if budget_ok else "positive token/time/cost budget required", blocking=False)
        for check_id, key in (
            ("operations.monitoring", "monitoring"),
            ("operations.redaction", "redaction"),
            ("operations.rollback_test", "rollback_test"),
        ):
            value = _get(self.case, f"operations.{key}")
            if isinstance(value, dict):
                self.evaluate_declared_status(check_id, "operations", value,
                                              blocking=(key == "rollback_test"))
            else:
                self.add(check_id, "operations", "NOT_ASSESSED", f"{key} result is missing",
                         blocking=(key == "rollback_test"))
        for key in ("incident_owner", "rollback_plan", "maintenance_trigger", "rate_limit_policy",
                    "network_egress_policy", "secrets_handling", "human_escalation", "concurrency_limit",
                    "input_size_limit", "user_feedback_channel"):
            value = _get(self.case, f"operations.{key}")
            self.add(f"operations.{key}", "operations", "PASS" if _nonempty(value) else "NOT_ASSESSED",
                     "declared" if _nonempty(value) else "required operating detail missing", blocking=False)
        for key in ("dependencies_pinned", "idempotency_tested", "backup_recovery_tested"):
            value = _get(self.case, f"operations.{key}")
            self.add(f"operations.{key}", "operations", "PASS" if value is True else "NOT_ASSESSED",
                     "confirmed by declaration" if value is True else "control not established", blocking=False)

        # Data and lifecycle governance must be explicit even when no regulated data is expected.
        for key in ("data_classification", "retention_policy", "deletion_policy", "incident_playbook",
                    "intellectual_property_policy", "audit_log_retention", "deployment_region",
                    "support_boundary", "deprecation_policy"):
            value = _get(self.case, f"governance.{key}")
            self.add(f"governance.{key}", "governance", "PASS" if _nonempty(value) else "NOT_ASSESSED",
                     "declared" if _nonempty(value) else "explicit policy required; 'none' must be stated", blocking=False)
        if self.profile == "high_impact":
            for key in ("human_decision_owner", "appeal_or_override_path", "domain_policy_reference"):
                value = _get(self.case, f"governance.{key}")
                self.add(f"governance.{key}", "governance", "PASS" if _nonempty(value) else "NOT_ASSESSED",
                         "declared" if _nonempty(value) else "high-impact governance detail required", blocking=True)
            approval_actions = _get(self.case, "permissions.approval_required_for", [])
            expected = {"final_decision", "irreversible_action", "external_side_effect", "all_high_impact_actions"}
            self.add("permissions.high_impact_human_gate", "authority",
                     "PASS" if isinstance(approval_actions, list) and expected.intersection(approval_actions) else "NOT_ASSESSED",
                     "explicit human approval required for a consequential action" if isinstance(approval_actions, list) and expected.intersection(approval_actions) else "high-impact profile requires an explicit approval gate for consequential actions",
                     blocking=True)

        # Release authorization is independent of technical qualification.
        approval = _get(self.case, "release.approval_status")
        approver = _get(self.case, "release.authorized_by")
        if approval == "APPROVED" and _nonempty(approver):
            refs_status, detail, refs = self.evidence_refs_status(_get(self.case, "release.evidence_refs"), "release.authorization")
            self.add("release.authorization", "release_governance", refs_status, detail,
                     blocking=True, evidence_refs=refs)
        elif approval in {"REJECTED", "REVOKED"}:
            self.add("release.authorization", "release_governance", "FAIL", f"release approval is {approval}", blocking=True)
        else:
            self.add("release.authorization", "release_governance", "NOT_ASSESSED",
                     "release approval must be separately granted by a named authority after qualification", blocking=True)
        if self.profile not in PROFILE_CHECKS:
            self.add("release.profile", "release_governance", "NOT_ASSESSED",
                     f"unsupported release profile {self.profile!r}; choose one of {sorted(PROFILE_CHECKS)}", blocking=False)

        # Every evidence record gets a visible integrity result; hash matching isn't semantic proof.
        for eid in sorted(self.evidence_integrity):
            integ = self.evidence_integrity[eid]
            self.add(f"evidence.integrity.{eid}", "evidence_integrity", integ["status"], integ["detail"],
                     blocking=integ["status"] in {"BLOCKED", "TOOL_ERROR", "FAIL"})

        blocking_failures = [c for c in self.checks if c.blocking and c.status == "FAIL"]
        if blocking_failures or any(c.status == "BLOCKED" for c in self.checks):
            status = "BLOCKED"
            reason = "blocking_control_failed_or_evidence_integrity_blocked"
        elif any(c.status == "TOOL_ERROR" for c in self.checks):
            status, reason = "TOOL_ERROR", "assessment_or_required_check_tool_error"
        elif self.profile not in PROFILE_CHECKS:
            status, reason = "NOT_READY", "unsupported_or_missing_release_profile"
        elif any(c.status in {"NOT_ASSESSED", "STALE"} for c in self.checks):
            status, reason = "NOT_READY", "required_control_or_evidence_not_established"
        elif any(c.status == "FAIL" for c in self.checks):
            status, reason = "BLOCKED", "declared_failure_present"
        elif approval == "APPROVED" and _nonempty(approver):
            status, reason = "RELEASE_ELIGIBLE", "declared_gates_pass_and_named_release_approval_present"
        else:
            status, reason = "QUALIFIED_FOR_REVIEW", "declared_gates_pass_but_release_approval_not_present"
        return self._result(status, reason, [])

    def _result(self, status: str, reason: str, fatal_errors: list[str]) -> dict[str, Any]:
        counts: dict[str, int] = {}
        for check in self.checks:
            counts[check.status] = counts.get(check.status, 0) + 1
        return {
            "harness": "production-readiness-completeness-harness",
            "harness_version": "0.1.0",
            "assessment_type": "manifest_preflight_not_live_execution",
            "as_of": self.as_of.isoformat(),
            "case_id": self.case.get("case_id"),
            "skill": self.case.get("skill", {}),
            "release_profile": self.profile,
            "status": status,
            "reason": reason,
            "counts": counts,
            "fatal_input_errors": fatal_errors,
            "checks": [asdict(c) for c in self.checks],
            "evidence_integrity": self.evidence_integrity,
            "interpretation_limits": [
                "A matching SHA-256 establishes byte integrity against the manifest, not the truth of artifact contents.",
                "Evidence epistemic_status and test statuses are declared inputs in v0.1; adapters must collect them from trusted tools.",
                "This command does not execute tests, prove verifier independence, certify a model generally, or authorize deployment by itself.",
                "RELEASE_ELIGIBLE is a preflight outcome under the declared profile, not a universal claim of production safety.",
            ],
        }


def load_case(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON case: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("case JSON root must be an object")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit a skill production-readiness manifest.")
    parser.add_argument("case", help="path to case JSON; evidence paths are relative to this file's directory")
    parser.add_argument("--as-of", help="assessment date in YYYY-MM-DD; defaults to today's local date")
    args = parser.parse_args(argv)
    case_path = Path(args.case).resolve()
    assessment_date = _parse_date(args.as_of) if args.as_of else date.today()
    if assessment_date is None:
        print(json.dumps({"status": "TOOL_ERROR", "reason": "--as-of must be a real YYYY-MM-DD date"}, indent=2))
        return 2
    try:
        case = load_case(case_path)
    except ValueError as exc:
        print(json.dumps({"status": "TOOL_ERROR", "reason": str(exc)}, indent=2))
        return 2
    result = Auditor(case, case_path.parent, assessment_date).run()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"RELEASE_ELIGIBLE", "QUALIFIED_FOR_REVIEW", "NOT_READY"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
