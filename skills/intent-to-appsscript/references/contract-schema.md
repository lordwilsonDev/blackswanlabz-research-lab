# Contract schema (version 3)

Read this when writing or checking a contract or a receipt. `scripts/validate_contract.py` enforces everything below.

## Contents
1. Fields
2. Status ladder
3. Receipt
4. What the validator cannot tell you

## 1. Fields

Text fields must be non-empty strings: `source_utterance` (the user's exact words), `intent` (your reading), `owner`, `trigger`, `input`, `predicate` (the eligibility rule), `transformation`, `action`, `destination`, `identity` (the account the script runs as), `idempotency`, `failure_policy`, `audit_log`, `data_retention`, `quota`, `success_measure` (how you will know it did what was intended), `rollback` (how its effects are undone), `disable`.

Text means real text: at least one letter or digit, and not a placeholder (`TODO`, `TBD`, `N/A`, `fixme`, `xxx`, `none yet`, or anything starting with todo/tbd/fixme). Short honest answers such as `none kept` are fine.

List fields: `exclusions` (may be empty), `permissions` (not empty), `tests` (not empty, unique), `missing_critical_facts` (may be empty). Every entry must be real text.

Flags: `dry_run` must be exactly `true`. `deployment_authorized` is true only when the owner has said so.

Conditional fields: `scope_justification` when a broad scope is requested: `https://mail.google.com`, `.../auth/drive`, `.../auth/drive.readonly`, `.../auth/gmail.modify`, `.../auth/gmail.readonly` (compared case-insensitively, ignoring a trailing slash; narrower scopes such as `drive.file` are not flagged). `consent_policy` and `rate_limit` when the `action` name contains any of: send, post, publish, notify, forward, reply, broadcast, invite (any spelling or case). `reason` for FAILED and BLOCKED. `deployed_version` for DEPLOYED_UNVERIFIED. `test_results` for LOCAL_TESTED. `execution_receipt` for VERIFIED_IN_SCOPE.

## 2. Status ladder

| Status | Requires |
|---|---|
| DESIGNED | a valid contract |
| LOCAL_TESTED | `test_results` with a PASS for every entry in `tests` |
| DEPLOYED_UNVERIFIED | `deployment_authorized: true` and `deployed_version` |
| VERIFIED_IN_SCOPE | `deployment_authorized: true`, `deployed_version`, and a valid receipt file (below) |
| FAILED, BLOCKED | `reason` |

Do not skip rungs by editing the status. Each rung asks for evidence the one before it did not.

## 3. Receipt

`execution_receipt` is a path to a JSON file inside the contract's directory:

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
  "checks": [{"name": "<each contract test>", "status": "PASS", "evidence": "execution log reference"}]  // names unique; PASS needs evidence
}
```

Every contract test needs a PASS check; any FAIL or NOT_RUN check fails the receipt. A receipt marked `"example": true` is rejected. For a contract whose entry point is manual (a menu item or button), `trigger_fired` means that specified entry point was used. Contract and receipt files may not repeat a JSON key. The hash covers the contract's substance and excludes status and evidence fields, so changing the design invalidates old receipts.

## 4. What the validator cannot tell you

It cannot tell whether the execution happened. A receipt can be written by hand. The validator guarantees it is well formed, names this exact contract, and claims every test passed. Open the evidence it points to (the execution log, the created draft) before you call anything verified.
