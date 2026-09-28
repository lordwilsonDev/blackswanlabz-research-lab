---
source: lordwilsonDev/fcve deliverables + lordwilsonDev/ico-collatz-verification
repo: lordwilsonDev/ico-collatz-verification
commit: 409c4c3b6f0179ae9131ac2450998e59a7fb1132
captured: 2026-09-28
status: archived
---

# Proofs

Two theorems were run end-to-end through [FCVE](../03-systems/fcve.md), FCVE's own Formal Claim Verification Engine, and issued as deliverable packages. Each was corrected once and superseded, never overwritten — the repair revision ("rev r") stays in the repo alongside the superseding revision ("rev s") that carries the final governance decision.

## VCE-001 — Eliahou bound on nontrivial Collatz cycle length

Claim verified: Eliahou, Theorem 1.1 — a bound on the length of a nontrivial Collatz cycle. This does **not** resolve the Collatz conjecture itself; it bounds a hypothetical cycle's length, nothing more.

Decision recorded: **PROMOTE** (rev s), in `governance-decision.md` inside the rev-s package.

- [VCE-001-rev-r](https://github.com/lordwilsonDev/fcve/tree/c3704cdb7333bfaa5bc5be7b20f8a9ca0a4c2624/deliverables/VCE-001-rev-r) — repair revision.
- [VCE-001-rev-s](https://github.com/lordwilsonDev/fcve/tree/c3704cdb7333bfaa5bc5be7b20f8a9ca0a4c2624/deliverables/VCE-001-rev-s) — superseding revision, PROMOTE.

The FCVE README's own account of this run: the independent-check gate first recorded VCE-001's headline proof as "checker incompatible: `lean4export` stalls (memoization bug)" — a hypothesis that was later found to be wrong. Sampling the stalled process showed the real cause was quadratic-time decimal conversion of natural-number literals up to 25.6 million digits, in the exporter and then in the independent checker. The project's own patches (below, under Upstream patches) fixed it; the theorem then checked (17,464 declarations, with the checker's axiom set matching the Lean-side audit), a deliberately corrupted literal was still correctly rejected, and earlier passes reproduced.

## VCE-002 — every power of two reaches 1 under the Collatz map

Claim verified: every power of two reaches 1 under the Collatz map — a small, fully decidable slice of the Collatz conjecture, not the conjecture itself.

Decision recorded: **PROMOTE** (rev s), in `governance-decision.md` inside the rev-s package.

- [VCE-002-rev-r](https://github.com/lordwilsonDev/fcve/tree/c3704cdb7333bfaa5bc5be7b20f8a9ca0a4c2624/deliverables/VCE-002-rev-r) — repair revision.
- [VCE-002-rev-s](https://github.com/lordwilsonDev/fcve/tree/c3704cdb7333bfaa5bc5be7b20f8a9ca0a4c2624/deliverables/VCE-002-rev-s) — superseding revision, PROMOTE.

## Lean / Collatz verification

The formal statement and Lean 4 proof for VCE-002 live in a separate, dedicated repository: [ico-collatz-verification](https://github.com/lordwilsonDev/ico-collatz-verification), described in its own repo metadata as "Lean project for FCVE VCE-002 (powers_of_two_reach_one)." At the pinned commit above, the repo holds a single Lean source file (`IcoCollatzVerification.lean`) plus its supporting `IcoCollatzVerification/` module directory, a `lakefile.toml` and `lean-toolchain` pinning the Lean/Lake toolchain versions, and a `lake-manifest.json` pinning its dependency set (including Mathlib) — the reproducibility contract FCVE's audit gates check against. This repository is what FCVE's Lean-build and axiom-audit gates (gates 5–6) ran against for VCE-002; FCVE itself holds the evidence ledger, receipts, and governance decision.

## Upstream patches

FCVE's independent-check gate needed two small patches to upstream Lean tooling to make huge decimal Nat literals tractable (up to 25.6 million digits in one proof; the unpatched tools are quadratic in both printing and parsing). Both patches were submitted upstream. Real state as of 2026-09-28, checked against the GitHub API:

- `leanprover/lean4export#52` ("Print huge natVal literals in sub-quadratic time") — **open**, not merged.
- `ammkrn/nanoda_lib#36` ("Parse huge decimal nat literals in sub-quadratic time") — **closed and merged**.

Both patches are disclosed on every verdict that used them: FCVE's README states each such verdict names the upstream commit, patch hash, build result, equivalence-test result, negative-control result, export validation, and output hashes. See [C-033](../CLAIMS.md).
