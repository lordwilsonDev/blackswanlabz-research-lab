# Contract schema (version 4)

Read this when writing or checking a contract or a receipt. `scripts/validate_contract.py` enforces everything below. The idea behind the structure: a small **baseline** that every automation gets, **situational** items decided with the person, and a record of the person's **decisions**.

## Contents
1. Baseline fields
2. Situational fields
3. Lists, flags and conditional fields
4. Decisions
5. Status ladder
6. Receipt
7. What the validator cannot tell you

## 1. Baseline fields (cannot be waived)

Text, real and non-empty: `source_utterance` (the user's exact words), `intent` (your reading), `owner`, `trigger`, `input`, `action`, `destination`, `identity` (the account it runs as), `failure_policy`, `success_measure` (how you will know it did what was intended), `rollback` (how its effects are undone; for a read-only automation, say there is nothing to undo), `disable`.

Real text means at least one letter or digit, and not a placeholder (`TODO`, `TBD`, `N/A`, `fixme`, `xxx`, `none yet`, or anything starting todo/tbd/fixme). Short honest answers such as `none kept` are fine.

## 2. Situational fields (a value, or a reasoned waiver)

`predicate`, `transformation`, `idempotency`, `audit_log`, `data_retention`, `quota`.

Each is either real text, or, if the person and the AI agree it does not apply in this case, exactly:

```json
{"not_applicable": "a real reason, in the person's situation"}
```

A missing situational field is a problem; nothing is skipped silently. `idempotency` and `audit_log` cannot be waived when the `action` name reaches outside the owner's own data (it contains send, post, publish, notify, forward, reply, broadcast, invite, mail, email, dispatch, message, sms, tweet, dm, delete, purchase, buy, pay, charge, share, modify or external), because repeated or untraceable side effects are the harm they prevent.

## 3. Lists, flags and conditional fields

Lists of real text: `exclusions` (may be empty), `permissions` (not empty), `tests` (not empty, unique), `missing_critical_facts` (may be empty).

`dry_run` must be exactly `true`. `deployment_authorized` is true only when the owner has said so.

Conditional: `scope_justification` when a broad scope is requested: `https://mail.google.com`, `.../auth/drive`, `.../auth/drive.readonly`, `.../auth/gmail.modify`, `.../auth/gmail.readonly`, `.../auth/calendar`, `.../auth/contacts` (compared case-insensitively, ignoring a trailing slash; narrower scopes such as `drive.file` are not flagged). `consent_policy` and `rate_limit` when the action reads as sending, unless it is clearly only a draft. `reason` for FAILED and BLOCKED. `deployed_version` for DEPLOYED_UNVERIFIED and VERIFIED_IN_SCOPE. `test_results` for LOCAL_TESTED. `execution_receipt` for VERIFIED_IN_SCOPE.

## 4. Decisions

`decisions` is a non-empty list. Each entry:

```json
{"topic": "sending", "choice": "drafts only, never send", "reason": "the owner wants to read every email",
 "decided_by": "user"}
```

`decided_by` is `user` or `user_after_ai_recommendation`. The AI may recommend; it may not decide, and the validator rejects any other value. Record routing, permissions, sending, which situational items do not apply, anything irreversible, and deployment.

A deployed status (DEPLOYED_UNVERIFIED or VERIFIED_IN_SCOPE) needs a decision whose `topic` is `deployment`, decided by the user, with a `quote` of their own words authorizing it. Decisions are not part of the contract hash, so the deployment decision can be recorded just before the live run without invalidating anything.

## 5. Status ladder

| Status | Requires |
|---|---|
| DESIGNED | a valid contract |
| LOCAL_TESTED | `test_results` with a PASS for every entry in `tests` |
| DEPLOYED_UNVERIFIED | `deployment_authorized: true`, `deployed_version`, a user `deployment` decision with a quote |
| VERIFIED_IN_SCOPE | the same, plus a valid receipt file (below) |
| FAILED, BLOCKED | `reason` |

Do not skip rungs by editing the status. Each rung asks for evidence the one before it did not.

## 6. Receipt

`execution_receipt` is a path to a JSON file inside the contract's directory. The comments are illustration; real JSON has none.

```json
{
  "contract_hash": "sha256:...",          // from validate_contract.py --hash
  "executed_at": "2026-10-23T10:00:00Z",  // ISO 8601 with a timezone, not in the future
  "executed_by": "account that ran it",
  "environment": "script project",
  "mode": "live",                         // a dry run cannot verify real effects
  "deployed_version": "v7",               // must equal the contract's deployed_version
  "trigger_fired": true,                  // the contract's real entry point, not a manual run in the editor
  "observed_outcome": "what actually happened",
  "checks": [{"name": "<each contract test>", "status": "PASS", "evidence": "execution log reference"}]
}
```

Every contract test needs a PASS check with evidence; check names are unique; any FAIL or NOT_RUN check fails the receipt. A receipt marked `"example": true` is rejected. For a contract whose entry point is manual (a menu item or button), `trigger_fired` means that specified entry point was used. Contract and receipt files may not repeat a JSON key. The hash covers the contract's substance and excludes status, evidence and decisions, so changing the design invalidates old receipts.

## 7. What the validator cannot tell you

- **Whether a receipt is true.** A receipt can be written by hand. The validator guarantees it is well formed, names this exact contract and version, and claims a live run with evidence. Open the evidence (the execution log, the created draft) before you call anything verified.
- **Whether a decision was really the person's.** `decided_by` and `quote` are self-reported. The conversation is the safeguard: ask in plain words and record what they actually said.
- **Whether a field's content is meaningful.** `"asdf"` is text. The validator checks shape, not sense.
