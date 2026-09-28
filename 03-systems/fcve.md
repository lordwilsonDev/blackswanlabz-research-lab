---
source: github.com/lordwilsonDev/fcve
repo: lordwilsonDev/fcve
commit: c3704cdb7333bfaa5bc5be7b20f8a9ca0a4c2624
captured: 2026-09-28
status: archived
---

# FCVE — Formal Claim Verification Engine (archived 2026-09-19)

## What it did

FCVE turned a mathematical claim into an auditable evidence package instead of a one-word "verified." A claim moved through a fixed chain of gates — source, claims extraction, normalization, Lean 4 formalization, build, axiom audit, semantic re-audit, computational tests, an independent check, evidence graph, report, governance decision — with every gate's result recorded in an append-only, hash-chained ledger (`evidence/event-ledger.jsonl`), one JSON event per gate, each hashed with its parent.

The project's own stated philosophy: "the model can propose, the experiment decides" — reasoning is not evidence. States are never collapsed: `PASS` means the check ran and held, `FAIL` means it ran and rejected the proof, `BLOCKED`/`TOOL_ERROR`/`UNRESOLVED` all mean no verdict was reached, and "not PASS is not FAIL." A correction never overwrites a prior run — it is a new run recorded beside it, with the superseded events and reports kept, so decisions are recorded as superseding events rather than rewritten history. The automated path (`scripts/audit.sh`) tops out at `PROVISIONAL`; `TRUSTED` requires two rows no code path can produce — a named human confirming the Lean statement means what the source paper claims, and a kernel-vulnerability review needing live web access — and the test suite itself asserts that no automated run can emit `TRUSTED`. Reports state what the evidence permits to say; the decision itself lives in a separate `governance-decision.md`, made by a named human, not asserted by the report.

## What it produced

Two theorems were run through the full engine and issued as deliverables, each corrected at least once (a "rev r" repair revision, then a "rev s" superseding revision):

- **VCE-001** — Eliahou, Theorem 1.1 (a bound on the length of a nontrivial Collatz cycle; explicitly does not resolve the Collatz conjecture). Deliverables: `VCE-001-rev-r`, `VCE-001-rev-s`. Decision recorded: **PROMOTE** (rev s).
- **VCE-002** — every power of two reaches 1 under the Collatz map. Deliverables: `VCE-002-rev-r`, `VCE-002-rev-s`. Decision recorded: **PROMOTE** (rev s).

Both PROMOTE decisions are Wilson's, recorded in each package's own `governance-decision.md`, not asserted by this lab. Each issued deliverable directory carries `ISSUE-NOTE.md` (what it supersedes and its stated limitations), `MANIFEST.sha256`, `correction-ledger.md`, `event-ledger.jsonl`, `governance-decision.md`, `receipt.json`, `report.tex`/`report.pdf`, and `verification-receipt.md` — see [C-034](../CLAIMS.md), status verified, listing re-run against the GitHub API at the pinned commit.

The repository at the pinned commit contains 13 files matching a `test_*.py` pattern (a file count, not a count of test functions or a collected/passed total) — see [C-035](../CLAIMS.md), status verified.

## Upstream contributions

FCVE's independent-check gate (row 10) needed huge decimal Nat literals to be tractable in two upstream tools; the project's own two small patches were submitted upstream as pull requests, and their real state as of 2026-09-28 is:

- `leanprover/lean4export#52` — "Print huge natVal literals in sub-quadratic time" — **open**, not merged.
- `ammkrn/nanoda_lib#36` — "Parse huge decimal nat literals in sub-quadratic time" — **closed and merged**.

See [C-033](../CLAIMS.md), status verified, checked against the GitHub API.

## Why it is archived

Wilson closed FCVE on 2026-09-19 to focus on MSB v3. The repository remains public on GitHub and is restorable — nothing was deleted, and its own README states the repo is meant to be self-bootstrapping (a fresh clone carries the instructions, skill, scripts, manifest, and tests needed to reconstruct the working environment without relying on anyone's memory). It was validated on exactly one machine (a specific Mac mini configuration) and run on two real theorems plus fixtures, by one person — the README states this directly as a known limitation, not a claim of general-purpose verification.

## Sources

- `README.md`, github.com/lordwilsonDev/fcve @ `c3704cdb7333bfaa5bc5be7b20f8a9ca0a4c2624`
- GitHub API: repo, commits, tree, contents/deliverables, and the two upstream pull requests, all queried 2026-09-28
