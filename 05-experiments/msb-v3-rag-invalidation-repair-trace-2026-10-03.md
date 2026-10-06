---
source: session trace reconstructed from tool outputs and carried-forward handoff
repo: lordwilsonDev/msb-v3 (implementation worktree; changes were not committed there)
captured: 2026-10-03
status: pending
record-type: provisional-run-record
---

# MSB-v3 RAG invalidation repair — engineering trace, 2026-10-03

> **Record status:** Provisional session record, not an independent review, production migration receipt, or proof of ongoing runtime behavior. The starting failure below is carried forward from an earlier session summary; it was not independently reproduced before changes in this session. The live verification performed here used real Qdrant and Ollama through FastAPI `TestClient`, a disposable tenant, a temporary source tree and a scratch SQLite database. It did not reindex the production vault.

## Evidence labels

- **USER-DIRECTED** — requested or expressly selected by Wilson.
- **SYSTEM-DERIVED** — inspection, hypothesis, design, or test selected to serve the request.
- **TEST-DERIVED** — evidence produced by an executed test or check.
- **ENVIRONMENT-DERIVED** — repository, tool, or service state observed in the environment.

These labels identify the origin of decisions and observations; they do not convert an inference into a verified fact.

## 1. Starting state and task boundary

- **USER-DIRECTED:** “Run it again … make all the fixes with the same rigor as the original prompt,” referring to an end-to-end memory/search lifecycle: create a known marker, index and retrieve it, verify provenance, modify/delete the source, reindex, and establish that stale content cannot look current.
- **USER-DIRECTED:** A pasted Autonomous Self-Observing Engineering Blueprint v1.0 supplied methodological guidance: distinguish observation from interpretation, seek adversarial failure modes, preserve uncertainty, and report the next question. It was treated as scope/methodology, not as authorization to build the entire blueprint.
- **ENVIRONMENT-DERIVED — carried forward, not re-probed at the start of this run:** The prior live experiment reportedly found that a deleted/omitted source remained retrievable from Qdrant after reindex. The handoff said an earlier disposable test used tenant `live_test_buffymem_fe6bb178ca42`, temporary service port `8767`, and a scratch database, then removed the collection and stopped the service. It also said Ollama `:11434` and Qdrant `:6333` were reachable and normal MSB `:8766` was down at that time. Those are historical inputs to this run, not fresh checks made here.
- **ENVIRONMENT-DERIVED:** The `projects/AI-Agents/msb-v3` repository already had unrelated dirty tracked and untracked files. I inspected its status and preserved those changes; no reset, checkout, or cleanup of that pre-existing work was done.
- **SYSTEM-DERIVED:** Scope was limited to source-currentness and stale-result handling in the RAG path, related reindex clients, tests, and the status checker. Production vault data and the legacy production Qdrant collection were out of scope absent explicit authorization.

## 2. Inspection and initial anomalies

- **SYSTEM-DERIVED:** Read the draft `src/msb_v3/api/rag.py`, `rag_index_state.py`, new state tests, existing RAG ID/cleanup tests, retrieval-router tests, app config/startup, `tests/conftest.py`, `pyproject.toml`, and relevant Makefile commands. Purpose: locate state ownership, preserve existing tenant behavior, and match test/lint/typecheck conventions.
- **SYSTEM-DERIVED:** Inspected `bin/vault-reindex.py`, `Documents/Vault/80_Tools/scripts/vault-semantic-index/index_vault.py`, `projects/Infrastructure/vault-search-mcp/server.py`, its `tool_manifest.json`, and `bin/vault-check.py`. Purpose: compare all producers of index data with the server's source-verification contract.
- **SYSTEM-DERIVED:** The draft invoked `_snapshot_matches_live_vault()` in status and search, but inspection found no definition. Hypothesis: source-currentness handling was unfinished and the API would either fail at runtime or be unable to establish currentness.
- **SYSTEM-DERIVED:** Snapshot records had a `verify_sources` bit, but did not persist a `source_root`; draft verification referenced `state["source_root"]`. Hypothesis: source verification could not reliably bind a snapshot to the configured source tree.
- **SYSTEM-DERIVED:** Draft `_tree_manifest()` attempted to use chunk boundaries that were not present in stored manifest rows, had an unused `boundaries` placeholder, and did not share a correct chunking contract. Hypothesis: a matching point count could mask changed source bytes or mismatched segmentation.
- **SYSTEM-DERIVED:** Snapshot manifests were caller-supplied. Hypothesis tested by design review: a self-consistent caller-supplied hash proves only internal consistency, not that the claimed text exists in the source of truth. Server-side filesystem verification is needed for source-currentness claims.
- **SYSTEM-DERIVED:** Empty manifests were accepted. Hypothesis: an empty or failed source walk could publish a complete-looking empty generation and remove all searchable content.
- **SYSTEM-DERIVED:** `vault-check.py` inferred freshness from a point-count threshold (90% of an estimated chunk count). Hypothesis: counts can agree while the wrong, stale, or tampered points remain indexed.
- **SYSTEM-DERIVED:** Reindexers skipped unreadable files and the MCP exclusion list differed from other clients. Hypothesis: clients might declare a partial or inconsistent source inventory as a full reindex.
- **SYSTEM-DERIVED:** In-place upserts do not remove omitted source points or trailing chunks and are vulnerable to partial-build corruption. Hypothesis/architecture decision: build a separate immutable generation, verify it completely, then atomically change the active pointer.

## 3. Repairs and changes, with observed results

### Snapshot state and activation

- **SYSTEM-DERIVED:** Added `src/msb_v3/api/rag_index_state.py` with SQLite state for managed tenants, snapshots, exact source/chunk manifests, upload reservations, and the active-index pointer. Added migration checks for `verify_sources` and `source_root` columns.
- **SYSTEM-DERIVED:** Made manifest validation reject unsafe POSIX paths, duplicate `(source, chunk)` entries, inconsistent whole-source hashes, non-contiguous chunks, and empty manifests. Persisted the configured source root in snapshot state; active lookup joins to generation state.
- **SYSTEM-DERIVED:** Snapshot commit verifies all expected uploads and point counts and rejects a builder whose base snapshot is no longer active. Activation switches the SQLite pointer transactionally; only the active generation is routable for managed tenants.
- **SYSTEM-DERIVED:** Marked a tenant managed as part of successful commit, not at staging start. This preserves the old collection/routing until a verified first generation is active.
- **SYSTEM-DERIVED:** Made abort idempotent for an already-aborted build so a retried cleanup can finish.

### Server-side RAG implementation

- **SYSTEM-DERIVED:** Implemented shared 3,000-character chunks with 200-character overlap; the source walk independently rebuilds content and whole-source SHA-256 values. It checks the configured source root, excludes the agreed directory-name segments, fails on walk/read errors, and rejects file symlinks resolving outside the root.
- **SYSTEM-DERIVED:** For `wilson-vault`, source verification uses `settings.vault_path`; disposable `live_test_*` and `r02_eval_*` tenants use the same configured root. Arbitrary request-provided source roots were considered, then removed: accepting a caller-selected root would let the requester choose what counts as the source of truth. Generic tenants may build a manifest-only snapshot but cannot be called source-current.
- **SYSTEM-DERIVED:** Snapshot indexing now creates a unique staging Qdrant collection, validates and reserves manifest entries, embeds and uploads stable source/chunk IDs with content/source/snapshot metadata, verifies the entire Qdrant point set against the frozen manifest, rechecks source currentness, and commits only after verification. Managed tenants and `wilson-vault` reject in-place legacy writes.
- **SYSTEM-DERIVED:** Search routes to the active snapshot, verifies result content and metadata hashes, verifies active-snapshot identity, and checks the configured source before and after query execution. Stale source results are rejected; source-currentness unknown and legacy vault results are withheld.
- **SYSTEM-DERIVED:** Status distinguishes `VERIFIED_CURRENT`, `STALE`, `INTEGRITY_ERROR`, `LEGACY_UNVERIFIED`, `SOURCE_CURRENTNESS_UNKNOWN`, and not-yet-published states rather than collapsing them into a count-based pass.
- **SYSTEM-DERIVED:** Retired snapshot collection deletion is best-effort after successful activation and its result is returned. The legacy `tenant_wilson-vault` collection is intentionally retained during first migration because it may contain operator-owned data. It is no longer the active managed search route after a snapshot commits.

### Reindex clients and freshness checker

- **SYSTEM-DERIVED:** Updated `bin/vault-reindex.py`, `Documents/Vault/80_Tools/scripts/vault-semantic-index/index_vault.py`, and `projects/Infrastructure/vault-search-mcp/server.py` to construct a manifest, stage batches, commit after upload, and abort a failed build. Their vault root now honors `MSB_VAULT_PATH`; exclusion checks use path components; unreadable files and empty inventories fail closed.
- **SYSTEM-DERIVED:** Updated MCP tool text and `tool_manifest.json` to describe verified staging and stale-result withholding rather than the old upsert-only semantics.
- **SYSTEM-DERIVED:** Changed `bin/vault-check.py` to query `/rag/index/status` and map server labels to exit behavior; it no longer regards a 90%-of-count heuristic as proof of freshness.

## 4. Test trajectory, failures, and corrections

### Tests created or modified

- **SYSTEM-DERIVED:** Created `tests/api/test_rag_index_state.py`. It tests manifest canonicalization/path validation, upload claims/retries, incomplete builds, atomic activation, stale concurrent builders, source-root persistence, empty/noncontiguous manifests, abort retry, and retrieval hash/provenance validation.
- **SYSTEM-DERIVED:** Created `tests/api/test_rag_snapshot_api.py`. It uses fake Qdrant plus a temporary source root and scratch SQLite DB for API lifecycle tests, and includes a separately marked live test for real Qdrant/Ollama.
- **TEST-DERIVED / SYSTEM-DERIVED:** Modified two expectations/patches in `tests/api/test_rag_index_ids.py` for cleanup behavior and test doubles.
- **ENVIRONMENT-DERIVED:** Added a temporary `test_vault_check_status.py` attempt, but its computed script path resolved to the wrong directory and collection failed. I removed that test file rather than retain a broken test. Therefore the checker has compile/Ruff validation in this trace, but no retained dedicated unit test.
- **ENVIRONMENT-DERIVED:** The existing `tests/api/test_retrieval_router.py` was not modified; it was run as regression coverage.

### Failures and responses

- **ENVIRONMENT-DERIVED:** An oversized `str_replace` response was cut off; the tool reported it was not applied. I did not assume the file was truncated or resend the same oversized call; I inspected and made smaller edits.
- **ENVIRONMENT-DERIVED:** A `code_search` call used a file path as its cwd and failed with `ENOTDIR`; subsequent reads/searches used valid project directories.
- **TEST-DERIVED:** State tests initially had two incorrect expectations in the earlier in-progress work (different source hashes on chunks of one file, and in-flight batch semantics). Those expectations were corrected before this run’s reported 26-test checkpoint.
- **TEST-DERIVED:** Adding snapshot-ID validation broke an existing test fixture lacking `_rag_snapshot_id`; the fixture was updated to represent a valid hit.
- **TEST-DERIVED:** Abort retry test failed because a second abort raised on status `aborted`; abort became idempotent.
- **TEST-DERIVED:** An error-text assertion no longer matched after provenance validation was made more explicit; expected text was updated.
- **TEST-DERIVED:** API tests exposed that an empty batch response omitted the snapshot manifest digest/counts needed by a client opening a snapshot and committing later. The API now returns that metadata even when the upload batch is empty.
- **TEST-DERIVED:** One incomplete-build fixture tried to hash `new.md` before creating it; the fixture was corrected.
- **TEST-DERIVED:** A forged-source test expected the old index to remain current after an extra source file had been placed in the configured tree. That was a misleading expectation: the old index should remain active but report stale. The test was corrected to assert `STALE` and unchanged active snapshot ID.
- **TEST-DERIVED:** A production-tenant test showed `wilson-vault` could still use legacy direct indexing before management state existed. The guard was widened to reject that path unconditionally.
- **TEST-DERIVED:** First live pytest command deselected the test under the repository’s default live-tier policy and exited 5 because zero tests ran. Rerun with `MSB_RUN_TIERS=1` executed it successfully.
- **TEST-DERIVED:** Mypy found optional-source typing problems and an untyped local; an initial annotation fix created a duplicate-definition error. A single explicit annotation and path type assertions fixed the diagnostics.
- **ENVIRONMENT-DERIVED:** Several compile commands used paths relative to the wrong repository root and failed with “No such file or directory.” They were rerun in the correct script directories. These were command-path errors, not compile failures.
- **ENVIRONMENT-DERIVED:** Ruff initially found import ordering and an undocumented broad exception catch in the MCP server; imports and the intentional cleanup catch were corrected. The final direct Ruff run passed.
- **ENVIRONMENT-DERIVED:** A temporary wrong indentation was visible in `rag.py` during diff review and was corrected. Several replacement attempts for strings that did not match returned no change; file reads were used to confirm actual content instead of assuming those edits applied.

## 5. Verification evidence actually obtained

- **TEST-DERIVED:** Focused suite at the end: `60 passed, 1 deselected` across RAG ID/state/snapshot API and retrieval-router tests.
- **TEST-DERIVED:** Ruff passed on the changed RAG source and state/test files; mypy passed on `rag.py` and `rag_index_state.py`.
- **TEST-DERIVED:** `bin/vault-reindex.py` and `bin/vault-check.py` compiled and passed Ruff in `bin/`.
- **TEST-DERIVED:** `index_vault.py` compiled. MCP `server.py` compiled, its JSON manifest parsed, and Ruff passed in the MCP project directory.
- **TEST-DERIVED:** Explicit live command `MSB_RUN_TIERS=1 python3 -m pytest tests/api/test_rag_snapshot_api.py -q -m live` passed: `1 passed, 7 deselected`. It was run multiple times; the final run passed.
- **TEST-DERIVED:** The live test used real Qdrant/Ollama, unique `live_test_snapshot_<random>` tenant, temporary source files/root, and scratch SQLite. It checked create/read, source edit → stale status and HTTP 409 result withholding, verified update → new text only, source deletion → stale/withheld → replacement snapshot without deleted marker, recreate → new marker and no old marker, and cleanup assertions for the test collections and SQLite tenant state.
- **TEST-DERIVED:** The live test verified status as `VERIFIED_CURRENT` for its configured temporary source before/after committed generations and `STALE` after edit/delete. It verified returned `_rag_snapshot_id` for results.
- **ENVIRONMENT-DERIVED:** Live validation exercised the FastAPI endpoints using in-process `TestClient`; it did not start a separate MSB HTTP server process.

## 6. Scope boundaries and deliberate non-actions

- **USER-DIRECTED / SAFETY:** No production `wilson-vault` reindex, source write, or production collection deletion was performed.
- **SYSTEM-DERIVED:** The old production collection is retained on first migration, not auto-deleted. Cleanup requires an explicit reviewed maintenance action.
- **SYSTEM-DERIVED:** No full autonomous-engineering blueprint platform, defect registry, recurring loop, or evidence database was built; that would exceed the defect-fix request.
- **ENVIRONMENT-DERIVED:** No standalone server process was started for the final live test. The previously failed temporary process attempt came from the carried-forward history, not a new attempt in this run.
- **ENVIRONMENT-DERIVED:** No full project test suite, all-source mypy, performance test on the full vault, or independent human/model code review was performed.
- **SAFETY:** No user changes were reverted; no commit or push was made to the msb-v3 repository.
- **ENVIRONMENT-DERIVED:** The reindexer/checker and MCP/vault client files were edited outside the `msb-v3` repository root. They were syntax/lint checked where available, but their separate Git status/diffs were not audited in this session. The main `msb-v3` dirty status therefore does not enumerate those external paths.

## 7. Remaining unknowns, risks, and next questions

- **UNKNOWN:** Production migration has not occurred. Legacy vault data is retained but is not marked verified; under the new guard, vault retrieval is withheld until a verified snapshot is published.
- **UNKNOWN:** Behavior through a separately running MSB server, including startup, middleware, environment propagation, and shutdown, was not verified.
- **UNKNOWN:** Concurrent builders and source edits at every precise activation/search race point were tested in state/unit reasoning but not exhaustively under concurrent live HTTP/Qdrant load.
- **UNKNOWN:** Qdrant ambiguous upsert outcomes, service outage during status/retirement cleanup, and cleanup retry under a real outage were not fault-injected.
- **UNKNOWN:** Cost/latency of hashing and walking the entire configured production vault on status/search was not benchmarked.
- **UNKNOWN:** Each external reindex client was compiled but not run against an actual configured full vault; their source-walk contract was reviewed, not end-to-end tested as separate commands.
- **LIMITATION:** SHA-256 binds indexed bytes to the configured local source during verification; it is not external authenticity. An actor controlling both source tree and local SQLite/Qdrant state can alter them.
- **SYSTEM-DERIVED NEXT QUESTIONS:** Does the separately running server reproduce the same stale-withholding behavior under a scratch configuration? What is the measured full-vault verification cost? Should the operator authorize a production snapshot migration, and what review is required before eventual legacy collection cleanup?

## 8. Decisions by origin

| Decision/action | Origin | Evidence or rationale |
|---|---|---|
| Repair deleted/stale-source search; use the pasted blueprint’s rigor | USER-DIRECTED | User request and blueprint |
| Keep production vault untouched; preserve dirty worktree; no push | USER-DIRECTED / SAFETY | Production reindex had not been authorized; worktree had unrelated edits |
| Use staged collections + atomic pointer rather than in-place deletion | SYSTEM-DERIVED | Partial failures and omitted-source stale data make in-place mutation unsafe |
| Verify source against server-configured root; do not trust client hash alone | SYSTEM-DERIVED | Caller-controlled manifest is not independent source evidence |
| Refuse empty manifests; fail on unreadable source | SYSTEM-DERIVED | Prevent accidental empty/partial generation being treated as a successful full index |
| Label generic manifest-only index `SOURCE_CURRENTNESS_UNKNOWN`; withhold search | SYSTEM-DERIVED | Manifest integrity does not establish live-source currentness |
| Preserve legacy production collection at first migration | SYSTEM-DERIVED / SAFETY | Avoid destructive deletion of potentially operator-owned data |
| Add fake-Qdrant API tests and a marked live lifecycle test | SYSTEM-DERIVED | Verify endpoints and external vector/embedding behavior without using production tenant |
| Correct fixtures and expected behavior after observed failures | TEST-DERIVED | Failures revealed mismatched expectations or a missing safety check |
| Explicitly enable the live tier after default deselection | SYSTEM-DERIVED | First command ran zero tests; repository requires `MSB_RUN_TIERS=1` |

## 9. Stopping point

The bounded code repair passed the focused unit/API suite, static checks, and the live disposable lifecycle. The session stopped before production migration and before a separate-server test. That stopping point is a boundary, not evidence that every deployment path or every race condition is closed.
