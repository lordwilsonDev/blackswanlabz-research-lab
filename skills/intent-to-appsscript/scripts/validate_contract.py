#!/usr/bin/env python3
"""Validate an automation contract (and, for VERIFIED_IN_SCOPE, its execution receipt).

Standard library only. This checks structure, internal consistency and the status ladder.
It does NOT execute Apps Script, verify OAuth scopes, or prove that anything ran: a receipt
is a self-reported file, so VERIFIED_IN_SCOPE means "a well-formed receipt bound to this exact
contract and deployed version says a live run passed every test, with evidence", not "it is
true". Open the evidence yourself.

    validate_contract.py contract.json          validate
    validate_contract.py --hash contract.json   print the hash a receipt must carry

Exit code: 0 pass, 1 problems found, 2 could not read the file or it is not a JSON object.
The validator never raises on malformed input; anything it cannot make sense of is a problem.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_TEXT = ("source_utterance", "intent", "owner", "trigger", "input", "predicate", "transformation",
                 "action", "destination", "identity", "idempotency", "failure_policy", "audit_log",
                 "data_retention", "quota", "success_measure", "rollback", "disable")
REQUIRED_LISTS = ("exclusions", "permissions", "tests", "missing_critical_facts")
STATUSES = ("DESIGNED", "LOCAL_TESTED", "DEPLOYED_UNVERIFIED", "VERIFIED_IN_SCOPE", "FAILED", "BLOCKED")
CHECK_STATES = ("PASS", "FAIL", "NOT_RUN")
# Words in an action name that mean the automation reaches outside the owner's own data.
SENDING_WORDS = frozenset({"send", "post", "publish", "notify", "forward", "reply", "broadcast", "invite"})
# Words that usually mean sending too, unless the action is clearly only a draft ("create_email_draft").
SOFT_SENDING_WORDS = frozenset({"mail", "email", "dispatch", "message", "sms", "tweet", "dm"})
EXTERNAL_WORDS = SENDING_WORDS | SOFT_SENDING_WORDS | {"delete", "purchase", "buy", "pay", "charge", "share", "modify", "external"}
# Scopes that expose a whole mailbox or drive. Compared after lower-casing and dropping a trailing slash.
BROAD_SCOPES = frozenset({
    "https://mail.google.com",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/contacts",
})
HASH_EXCLUDED = ("status", "deployment_authorized", "execution_receipt", "test_results",
                 "deployed_version", "reason", "contract_hash")
PLACEHOLDERS = frozenset({"todo", "tbd", "tba", "n/a", "na", "fixme", "xxx", "none yet"})
PLACEHOLDER_PREFIXES = ("todo", "tbd", "fixme")


def is_text(value) -> bool:
    """Real text: a string with at least one letter or digit that is not a placeholder."""
    if not isinstance(value, str):
        return False
    s = unicodedata.normalize("NFKC", value).strip().lower()     # fullwidth and compatibility forms count as plain letters
    if not any(ch.isalnum() for ch in s):
        return False
    return s not in PLACEHOLDERS and not s.startswith(PLACEHOLDER_PREFIXES)


def load_json(text: str):
    """json.loads that refuses duplicate keys, which would otherwise let the last one win silently."""
    def no_duplicates(pairs):
        keys = [k for k, _ in pairs]
        dup = sorted({k for k in keys if keys.count(k) > 1})
        if dup:
            raise ValueError(f"duplicate JSON key {dup[0]!r}")
        return dict(pairs)
    return json.loads(text, object_pairs_hook=no_duplicates)


def contract_hash(doc: dict) -> str:
    """Hash of the contract's substance. Status and evidence fields are excluded so a receipt
    can name the contract it was produced against without being circular."""
    if not isinstance(doc, dict):
        raise ValueError("contract must be a JSON object")
    body = {k: v for k, v in doc.items() if k not in HASH_EXCLUDED}
    return "sha256:" + hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def normalize_scope(scope: str) -> str:
    return scope.strip().lower().rstrip("/")


def sends(words: set[str]) -> bool:
    """True when an action name reads as sending something outward. Over-flagging is the safe direction."""
    return bool(words & SENDING_WORDS) or (bool(words & SOFT_SENDING_WORDS) and "draft" not in words)


def action_words(action) -> set[str]:
    return set(re.split(r"[^a-z0-9]+", action.lower())) - {""} if isinstance(action, str) else set()


def _checks_by_name(items, problems: list[str], label: str, need_evidence: bool = False) -> dict[str, str]:
    """Map check name to status. Records a problem for anything malformed, duplicated or, when
    evidence is required, passing without it."""
    out: dict[str, str] = {}
    if not isinstance(items, list) or not items:
        problems.append(f"{label} must be a non-empty list")
        return out
    for i, item in enumerate(items):
        if not isinstance(item, dict) or not is_text(item.get("name")) or item.get("status") not in CHECK_STATES:
            problems.append(f"{label}[{i}] needs a name and a status of {'/'.join(CHECK_STATES)}")
            continue
        name = item["name"]
        if name in out:
            problems.append(f"{label} has a duplicate check name {name!r}")
            continue
        if need_evidence and item["status"] == "PASS" and not is_text(item.get("evidence")):
            problems.append(f"{label}[{i}] {name!r} is PASS but needs evidence")
        out[name] = item["status"]
    return out


def validate_receipt(doc: dict, receipt: dict, now: datetime | None = None) -> list[str]:
    problems: list[str] = []
    if receipt.get("example") is True:
        problems.append("receipt is marked as an example, not a real execution")
    if receipt.get("contract_hash") != contract_hash(doc):
        problems.append("receipt contract_hash does not match this contract (it was produced for a different version)")
    for key in ("executed_by", "environment", "observed_outcome"):
        if not is_text(receipt.get(key)):
            problems.append(f"receipt missing {key}")
    if receipt.get("mode") != "live":
        problems.append("receipt mode must be 'live': a dry run cannot verify an automation's real effects")
    if not is_text(receipt.get("deployed_version")) or receipt.get("deployed_version") != doc.get("deployed_version"):
        problems.append("receipt deployed_version does not match the contract's deployed_version")
    if receipt.get("trigger_fired") is not True:
        problems.append("receipt must record trigger_fired: true (the contract's real entry point, not a manual run in the editor)")
    try:
        when = datetime.fromisoformat(str(receipt.get("executed_at")).replace("Z", "+00:00"))
        if when.tzinfo is None:
            problems.append("receipt executed_at needs a timezone")
        elif when > (now or datetime.now(timezone.utc)):
            problems.append("receipt executed_at is in the future")
    except ValueError:
        problems.append("receipt executed_at is not an ISO 8601 time")
    states = _checks_by_name(receipt.get("checks"), problems, "receipt checks", need_evidence=True)
    for t in doc.get("tests", []) if isinstance(doc.get("tests"), list) else []:
        if isinstance(t, str) and t not in states:
            problems.append(f"receipt has no check for contract test {t!r}")
    for name, st in states.items():                       # every recorded check must pass, contract tests included
        if st != "PASS":
            problems.append(f"receipt check {name!r} is {st}")
    return problems


def _validate(doc, base_dir: Path | None, now: datetime | None) -> list[str]:
    if not isinstance(doc, dict):
        return ["contract must be a JSON object"]
    problems: list[str] = []
    for key in REQUIRED_TEXT:
        if key not in doc:
            problems.append(f"missing {key}")
        elif not is_text(doc[key]):
            problems.append(f"{key} must be non-empty text")
    for key in REQUIRED_LISTS:
        if key not in doc:
            problems.append(f"missing {key}")
        elif not isinstance(doc[key], list):
            problems.append(f"{key} must be a list")
        elif key in ("permissions", "tests") and not doc[key]:
            problems.append(f"{key} must not be empty")
        elif not all(is_text(x) for x in doc[key]):
            problems.append(f"{key} must be non-empty text entries")
        elif key == "tests" and len(set(doc[key])) != len(doc[key]):
            problems.append("tests must be unique")
    if doc.get("dry_run") is not True:
        problems.append("dry_run must default true")
    status = doc.get("status")
    if status not in STATUSES:
        problems.append("invalid status")

    tests = [t for t in doc["tests"] if isinstance(t, str)] if isinstance(doc.get("tests"), list) else []
    perms = [p for p in doc["permissions"] if isinstance(p, str)] if isinstance(doc.get("permissions"), list) else []
    broad = [p for p in perms if normalize_scope(p) in BROAD_SCOPES]
    if broad and not is_text(doc.get("scope_justification")):
        problems.append(f"broad scope {broad[0].strip()} needs a scope_justification")

    words = action_words(doc.get("action"))
    if sends(words) and (not is_text(doc.get("consent_policy")) or not is_text(doc.get("rate_limit"))):
        problems.append("sending needs a consent_policy and a rate_limit")

    deployed = status in ("DEPLOYED_UNVERIFIED", "VERIFIED_IN_SCOPE")
    if deployed and doc.get("deployment_authorized") is not True:
        problems.append("deployed status requires deployment_authorized: true"
                        + (" (external side effect deployed without authorization)" if words & EXTERNAL_WORDS else ""))
    if deployed and not is_text(doc.get("deployed_version")):
        problems.append(f"{status} requires deployed_version")
    if status in ("FAILED", "BLOCKED") and not is_text(doc.get("reason")):
        problems.append(f"{status} requires a reason")
    if status == "LOCAL_TESTED":
        got = _checks_by_name(doc.get("test_results"), problems, "test_results")
        for t in tests:
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
                    receipt = load_json(path.read_text(encoding="utf-8"))
                except (OSError, ValueError) as e:
                    problems.append(f"execution_receipt is not readable JSON: {e}")
                else:
                    problems += validate_receipt(doc, receipt if isinstance(receipt, dict) else {}, now)
    return problems


def validate(doc, base_dir: Path | None = None, now: datetime | None = None) -> list[str]:
    """Return the list of problems. Never raises: an input the validator cannot handle is a problem."""
    try:
        return _validate(doc, base_dir, now)
    except Exception as e:  # unknown state is never a pass
        return [f"validator could not process this input ({type(e).__name__}); treat it as invalid"]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("contract", type=Path)
    ap.add_argument("--hash", action="store_true", help="print the hash a receipt must carry")
    args = ap.parse_args(argv)
    try:
        doc = load_json(args.contract.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"cannot read contract: {e}", file=sys.stderr)
        return 2
    if args.hash:
        if not isinstance(doc, dict):
            print("cannot hash: the contract must be a JSON object", file=sys.stderr)
            return 2
        print(contract_hash(doc))
        return 0
    problems = validate(doc, base_dir=args.contract.resolve().parent)
    for p in problems:
        print("ERROR:", p)
    print("PASS" if not problems else "FAIL")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
