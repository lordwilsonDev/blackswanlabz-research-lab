---
source: Codex creation-session validation output and Sites native deployment/access receipts
captured: 2026-10-12
status: active
---

# BlackSwanLabz Evidence Explorer v1

**Built and privately deployed on 2026-10-12 by Codex (ChatGPT), at Lord Wilson's direction.** This records a new working artifact of the lab, not a proposed website. Its scoped creation claim is [C-055](../CLAIMS.md).

[Open the private explorer](https://blackswanlabz-proof.docilehawk8.chatgpt.site). The Site is owner-only; the URL does not grant access. Publishing this creation record to GitHub does not make the Site public.

## What was created

A small, buildless HTML/CSS/JavaScript website turns the lab's existing repository evidence into an interactive collection:

- Browse 17 selected artifacts and methods by domain.
- Search and filter the complete captured 54-row claim register: 29 verified, 24 pending, and 1 retracted.
- Open individual evidence receipts with the ledger's exact claim, evidence, how-to-check, status, and checked-date fields.
- Inspect artifact stages separately from associated claim states; documents without a ledger claim row retain that distinction.
- Follow pinned GitHub source links and read captured source text with recorded hashes.
- Copy filtered views and open direct links to a claim or artifact.

The captured claim register is pinned to lab commit `a7ac9a6ce392a251c72310e4b411fa88ac81cdb3`. It preserves C-045 as retracted and C-048 as pending. Adding this creation record and C-055 does not retroactively change the website's input snapshot; v1 has no automatic ingestion.

## What was checked

At Site source commit `da14fd341f3d837b0b37d63ef41036656d048a94`, `node scripts/validate.mjs` completed all 12 validation checks. The [captured output](evidence/evidence-explorer-2026-10-12/validation.txt) records the successful run.

The checks cover exact preservation of all ledger fields, unique claim IDs and state counts, all 23 captured source files matching their pinned repository Git blob hashes, valid artifact-to-claim associations, explicit source banners, combined domain/state/text filtering, empty results, unsafe URL rejection, pinned source links, UI event wiring for filters and evidence dialogs, and restored filtered URLs and deep links. UI wiring was exercised in a minimal DOM harness, not a browser.

Sites returned a successful deployment and owner-only access with no added viewers, editors, or groups. The [creation and deployment receipt](evidence/evidence-explorer-2026-10-12/creation-receipt.json) records the deployment/version identifiers, as-of access summary, source commits, and verification limits. Credentials, account identifiers, and personal contact details are omitted.

## Evidence files

- [Creation / deployment receipt](evidence/evidence-explorer-2026-10-12/creation-receipt.json): selected native tool response fields, recorded by the creating assistant; not a separately signed attestation.
- [Validation output](evidence/evidence-explorer-2026-10-12/validation.txt): the executed check results.
- [Build manifest](evidence/evidence-explorer-2026-10-12/build-manifest.json): file hashes and sizes for the created implementation and evidence.
- [Input source manifest](evidence/evidence-explorer-2026-10-12/source-manifest.json): the pinned lab input revision and captured document hashes.

The implementation source remains in the private Sites source repository at the recorded Site commit. This lab repository publishes the creation record and receipts. An owner can reopen that Site checkout, compare the build hashes, and rerun `node scripts/validate.mjs`. An unauthorised visitor can inspect these public receipts but cannot independently inspect or execute the private Site source from this record alone.

## Limits

- Browser-based visual QA was unavailable; layout, rendered browser behavior, and browser accessibility have not been independently checked.
- The underlying experiments were not rerun. Existing verified, pending, and retracted research claims keep their recorded states.
- Artifact badges summarize associated claim rows. A verified row does not certify a whole system, a method's comparative superiority, or independent reproduction.
- The artifact list is a curated selection, not a complete inventory of every lab repository, branch, or local project. Domains and associations are editorial navigation.
- This record establishes creation-session checks and deployment as of its recorded date. It does not guarantee future availability, current access configuration, or unchanged live content.
