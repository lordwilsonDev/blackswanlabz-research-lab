#!/usr/bin/env python3
"""Validate an automation contract (and, for VERIFIED_IN_SCOPE, its execution receipt).

Standard library only. This checks structure, internal consistency and the status ladder.
It does NOT execute Apps Script, verify OAuth scopes, or prove that anything ran: a receipt
is a self-reported file, so VERIFIED_IN_SCOPE means "a well-formed receipt bound to this exact
contract says every check passed", not "it is true". Read the receipt's evidence yourself.

    validate_contract.py contract.json          validate
    validate_contract.py --hash contract.json   print the hash a receipt must carry

Exit code: 0 pass, 1 problems found, 2 could not read the file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_TEXT = ("source_utterance", "intent", "owner", "trigger", "input", "predicate", "transformation",
                 "action", "destination", "identity", "idempotency", "failure_policy", "audit_log",
                 "data_retention", "quota", "disable")
REQUIRED_LISTS = ("exclusions", "permissions", "tests", "missing_critical_facts")
STATUSES = ("DESIGNED", "LOCAL_TESTED", "DEPLOYED_UNVERIFIED", "VERIFIED_IN_SCOPE", "FAILED", "BLOCKED")
EXTERNAL_ACTIONS = ("send_email", "send_message", "delete", "modify_external", "purchase", "share", "publish")
BROAD_SCOPES = ("https://mail.google.com/", "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/gmail.modify")
HASH_EXCLUDED = ("status", "deployment_authorized", "execution_receipt", "test_results",
                 "deployed_version", "reason", "contract_hash")
CHECK_STATES = ("PASS", "FAIL", "NOT_RUN")


def contract_hash(doc: dict) -> str:
    """Hash of the contract's substance. Status and evidence fields are excluded so a receipt
    can name the contract it was produced against without being circular."""
    body = {k: v for k, v in doc.items() if k not in HASH_EXCLUDED}
    return "sha256:" + hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _text(doc: dict, key: str) -> bool:
    return isinstance(doc.get(key), str) and bool(doc[key].strip())


def _checks_by_name(items, problems: list[str], label: str) -> dict[str, str]:
    out: dict[str, str] = {}
    if not isinstance(items, list) or not items:
        problems.append(f"{label} must be a non-empty list")
        return out
    for i, item in enumerate(items):
        if not isinstance(item, dict) or not _text(item, "name") or item.get("status") not in CHECK_STATES:
            problems.append(f"{label}[{i}] needs a name and a status of {'/'.join(CHECK_STATES)}")
            continue
        out[item["name"]] = item["status"]
    return out


def validate_receipt(doc: dict, receipt: dict, now: datetime | None = None) -> list[str]:
    problems: list[str] = []
    if receipt.get("example") is True:
        problems.append("receipt is marked as an example, not a real execution")
    if receipt.get("contract_hash") != contract_hash(doc):
        problems.append("receipt contract_hash does not match this contract (it was produced for a different version)")
    for key in ("executed_by", "environment", "observed_outcome"):
        if not _text(receipt, key):
            problems.append(f"receipt missing {key}")
    if receipt.get("trigger_fired") is not True:
        problems.append("receipt must record trigger_fired: true (a manual function run is not the trigger)")
    try:
        when = datetime.fromisoformat(str(receipt.get("executed_at")).replace("Z", "+00:00"))
        if when.tzinfo is None:
            problems.append("receipt executed_at needs a timezone")
        elif when > (now or datetime.now(timezone.utc)):
            problems.append("receipt executed_at is in the future")
    except ValueError:
        problems.append("receipt executed_at is not an ISO 8601 time")
    states = _checks_by_name(receipt.get("checks"), problems, "receipt checks")
    for t in doc.get("tests", []) if isinstance(doc.get("tests"), list) else []:
        if t not in states:
            problems.append(f"receipt has no check for contract test {t!r}")
    for name, st in states.items():                       # every recorded check must pass, contract tests included
        if st != "PASS":
            problems.append(f"receipt check {name!r} is {st}")
    return problems


def validate(doc: dict, base_dir: Path | None = None, now: datetime | None = None) -> list[str]:
    if not isinstance(doc, dict):
        return ["contract must be a JSON object"]
    problems: list[str] = []
    for key in REQUIRED_TEXT:
        if key not in doc:
            problems.append(f"missing {key}")
        elif not _text(doc, key):
            problems.append(f"{key} must be non-empty text")
    for key in REQUIRED_LISTS:
        if key not in doc:
            problems.append(f"missing {key}")
        elif not isinstance(doc[key], list):
            problems.append(f"{key} must be a list")
        elif key in ("permissions", "tests") and not doc[key]:
            problems.append(f"{key} must not be empty")
    if doc.get("dry_run") is not True:
        problems.append("dry_run must default true")
    status = doc.get("status")
    if status not in STATUSES:
        problems.append("invalid status")

    perms = doc.get("permissions") if isinstance(doc.get("permissions"), list) else []
    broad = [p for p in perms if p in BROAD_SCOPES]
    if broad and not _text(doc, "scope_justification"):
        problems.append(f"broad scope {broad[0]} needs a scope_justification")

    action = doc.get("action") if isinstance(doc.get("action"), str) else ""
    if action.startswith("send_") and (not _text(doc, "consent_policy") or not _text(doc, "rate_limit")):
        problems.append("sending needs a consent_policy and a rate_limit")

    deployed = status in ("DEPLOYED_UNVERIFIED", "VERIFIED_IN_SCOPE")
    if deployed and doc.get("deployment_authorized") is not True:
        problems.append("deployed status requires deployment_authorized: true"
                        + (" (external side effect deployed without authorization)" if action in EXTERNAL_ACTIONS else ""))
    if status == "DEPLOYED_UNVERIFIED" and not _text(doc, "deployed_version"):
        problems.append("DEPLOYED_UNVERIFIED requires deployed_version")
    if status in ("FAILED", "BLOCKED") and not _text(doc, "reason"):
        problems.append(f"{status} requires a reason")
    if status == "LOCAL_TESTED":
        got = _checks_by_name(doc.get("test_results"), problems, "test_results")
        for t in doc.get("tests", []) if isinstance(doc.get("tests"), list) else []:
            if got.get(t) != "PASS":
                problems.append(f"LOCAL_TESTED needs a PASS test result for {t!r}")
    if status == "VERIFIED_IN_SCOPE":
        ref = doc.get("execution_receipt")
        if not isinstance(ref, str) or not ref.strip():
            problems.append("VERIFIED_IN_SCOPE requires execution_receipt: a path to a receipt file")
        elif base_dir is None:
            problems.append("cannot resolve execution_receipt without the contract's directory")
        else:
            path = (base_dir / ref).resolve()
            if base_dir.resolve() not in path.parents:
                problems.append("execution_receipt must be inside the contract's directory")
            elif not path.is_file():
                problems.append(f"execution_receipt {ref} does not exist")
            else:
                try:
                    receipt = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as e:
                    problems.append(f"execution_receipt is not readable JSON: {e}")
                else:
                    problems += validate_receipt(doc, receipt if isinstance(receipt, dict) else {}, now)
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("contract", type=Path)
    ap.add_argument("--hash", action="store_true", help="print the hash a receipt must carry")
    args = ap.parse_args(argv)
    try:
        doc = json.loads(args.contract.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"cannot read contract: {e}", file=sys.stderr)
        return 2
    if args.hash:
        print(contract_hash(doc))
        return 0
    problems = validate(doc, base_dir=args.contract.resolve().parent)
    for p in problems:
        print("ERROR:", p)
    print("PASS" if not problems else "FAIL")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
