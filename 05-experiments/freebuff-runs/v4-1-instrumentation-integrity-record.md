---
source: FreeBuff (Buffy) run record from the PZS notebook, 06_ARCHITECTURE/v4-1-instrumentation-integrity-record.md; body copied unchanged except that links to other notebook files are written as plain references
captured: 2026-10-03
status: pending
---

# v4.1 Instrumentation Integrity — Record and Terminal State

Date: 2026-10-03
Status: in-progress

Protocol: *Instrumentation Integrity, Search Validation & Rebaseline Blueprint
v4.1*. Instruments built: `search-detector.mjs`, `gate-mutation.mjs`,
`instrumentation-certification.mjs`.

> **§58 outcome: `BLOCKED`.** Instrumentation ceiling **`NOT_CERTIFIED`**.
> §57 gate **9/18**. `REBASELINE_READY` not reached; PT-2026-10-03-002 **not
> permitted**.

## What v4.1 changed, and why it indicted me

§1 names the failure precisely:

> *The test system applied epistemic controls to the substrate under test while
> failing to apply equivalent controls to the instruments producing those
> measurements.*

That is a description of **my own v4.0 §6 finding**. I ran a negative search for
the v2.0 artifact, got zero matches, and wrote `V2_ARTIFACT_NOT_FOUND` — an
absence claim — from a detector that had **never passed a positive control**, on
a scope searched with a `timeout`, which §14 explicitly prohibits reading as
ABSENT.

Today had already demonstrated *why*: the `.md/.json/.yaml` grep that reported
D13/D20/C-B8-001 as absent when they were sitting in Python.

**The v4.0 §6 finding was inadmissible on its own terms.** It is withdrawn.

## §9/§10/§12 — calibrated search detector

`state/repair/search-detector.mjs` calibrates before it searches, using **one**
detector implementation for controls and the real search (§10 forbids validating
a hand-written "equivalent" search).

| Control | Result |
|---|---|
| positive (§10 fixture, verbatim) | `POSITIVE_CONTROL_PASSED` |
| negative (§12, guards false positives) | `NEGATIVE_CONTROL_PASSED` |
| scope (§11, nested traversal) | `SCOPE_CONTROL_PASSED` |

**A calibration failure withholds the search entirely.** That is the whole point
of §9, and the earlier detector had no such gate.

## The corrected v2.0 search result

| Scope | Coverage | Result |
|---|---|---|
| `~/.claude/projects` | 150 dirs, 0 unreadable, **complete** | `NOT_FOUND_IN_SEARCH_SCOPE` |
| `~/Documents` | 4000 dirs, **truncated** | `NOT_FOUND_IN_SEARCH_SCOPE_PARTIAL_COVERAGE` |
| `~/projects` | 4002 dirs, **truncated** | `NOT_FOUND_IN_SEARCH_SCOPE_PARTIAL_COVERAGE` |
| `$HOME` (whole) | — | **`SEARCH_ERROR`** (grep exit 2, ~230 s) |

Two things worth sitting with:

1. **The whole-home search errors out.** The instrument returns `SEARCH_ERROR`,
   not a negative. It refuses.
2. **Truncated coverage downgrades the verdict automatically** — two of four
   scopes cannot support even a scoped negative.

**Corrected finding: `NOT_FOUND_IN_SEARCH_SCOPE`.** Not `ABSENT`. No scope
achieved declared-universe coverage, so per §14/§16 the instrument is
**forbidden from emitting `ABSENT_IN_DECLARED_UNIVERSE`** — and it never does.
The declared universe is larger than `$HOME`: external storage, remote
repositories, archived vaults, conversation exports.

**Consequence: the v2.0 artifact is formally unavailable under this instrument,
which is not the same as not existing.** Gate 6 now reads *recovered OR formally
unavailable*, and that reading is earned rather than asserted.

## §20/§21/§22 — the gate runner failed its own audit

`state/repair/gate-mutation.mjs`:

- **14/14 gate mutations detected.** Each gate has a mutation targeting its own
  invariant; all fourteen produced `FAIL`.
- **§47 benign control passes** — an all-good state produces zero failures, so
  the harness is not simply always-fail.
- The harness **independently re-implements** each gate verdict, so the test is
  not circular against the runner it audits.

> **Corrected by [v4.2](v4-2-verification-of-verification-record.md) §14.** The
> harness never *executes* `repair-gate.mjs` — it only reads it as text for the
> §21 scan. Re-implementing the logic is non-circular in the obvious way, but it
> means **14/14 says nothing about whether the runner's gates can fail.** The
> harness verified its own reasoning. Status downgraded `VERIFIED` → `PARTIAL`.

Then §21 scanned the runner source for fail-open patterns and found:

```
FAIL-OPEN PATTERNS PRESENT: hardcoded pass: true x6
```

**Six of fourteen gates in `repair-gate.mjs` are hardcoded `pass: true`. Only one
is computed.**

> Corrected by [v4.2](v4-2-verification-of-verification-record.md): this is a
> **static scan result**, not an execution result. Only gate 5 has execution
> evidence. The other five are `UNKNOWN_UNTIL_MUTATION_TESTED`, not
> `VERIFIER_GAP`. The count of six is accurate; the claim that it proves six
> gate gaps was not.

**Therefore the v4.0 board's "7/14" was a hardcoded diagnostic, not a
measurement.** Six of the seven passes were assertions about the world, written
before running anything. Per §22 the correct label was always
`UNCALIBRATED_DIAGNOSTIC`, and per §21 this is a `VERIFIER_GAP_DEFECT`.

Recorded honestly: `0 of 14` v4.0 gates are certified measurements.

## §25 — an interface defect, confirmed

Feeding a controlled result through two consumers:

| Consumer | Verdict on `{exit 0, system_state: BLOCKED, certified: false}` |
|---|---|
| reads exit code only | **`PASS`** ← interface defect |
| reads `system_state` | `BLOCKED` ← correct |

An exit-code-only consumer reports a blocked system as passing. **I have been
summarising runs tonight in that shape.** v4.1 §3's separation
(`execution_status` / `system_state` / `certified` / `measurement_status`) is the
fix; this run's own output now ends with the statement:

> `execution_status=COMPLETED_EXIT_0` is NOT `system_state=PASS`. This run exited
> 0; its own verdict is `BLOCKED`.

It crashed on its first run with a `TypeError` and **still exited 0** through a
pipe. The separation problem is not hypothetical here; it happened while writing
the fix for it.

## §55/§56 — certification ceiling

| Instrument | Status |
|---|---|
| `search_detector` | `VERIFIED` |
| `gate_mutation_harness` | `VERIFIED` |
| `link_containment_test` | `VERIFIED` |
| `git_porcelain_parser` | `FAILED_THEN_FIXED_UNCALIBRATED` |
| `metric_generators` | `UNCALIBRATED` |
| `authorization_controls` | `BLOCKED` |
| `interface_consumers` | `DEFECT_CONFIRMED` |
| **`gate_runner`** | **`FAILED`** ← ceiling |

> **Two of these are corrected by [v4.2](v4-2-verification-of-verification-record.md).**
>
> - `gate_runner: FAILED` → **`UNKNOWN_UNTIL_MUTATION_TESTED`**. The "6 hardcoded
>   passes" claim came from a **static source scan**, not execution. Only gate 5
>   has executed evidence. v4.2 §12 forbids extrapolating it to the others.
> - `gate_mutation_harness: VERIFIED` → **`PARTIAL`**. It never executes
>   `repair-gate.mjs` — it only `readFileSync`s it. The 14/14 matrix proved the
>   harness's own reasoning, not the runner's behaviour (v4.2 §14).
> - `git_porcelain_parser` → **`VERIFIED`**, 12/12 against real git. The suite
>   found a second real defect (rename/copy orig-path is a second NUL field) in
>   the very technique this record had certified.

**Overall: `NOT_CERTIFIED`.** §56 makes the ceiling the weakest critical
component, so five failing instruments determine the outcome regardless of the
three that pass.

Two findings that only surfaced because the instruments were audited:

- **`AUTHORIZED_EXTERNAL` is self-granted.** The external-link exception is
  authored by the same runner that consumes it — no `authorization_id`,
  `approver_id`, `policy_reference`, or `decision_id` (§26/§27). An authorization
  written only by the actor granting it is not independent authorization.
- **The porcelain parser is fixed but uncalibrated.** Three bugs, three fixed,
  **no regression suite** (§39). A fix nobody re-tests is a fix nobody can rely on.

## §57 — repair gate 9/18

Failing: v2.0 recovered-or-formally-unavailable · no hardcoded-pass gate remains
· gate count certification · exit/state consumer test · `AUTHORIZED_EXTERNAL`
authority binding · complete META set · Git parser regression suite · validator
mutation coverage · artifact provenance ledger.

Passing: the five search-semantics items, 14/14 matrix, scoped counts, validator
target declarations, baseline dimensions classified separately.

## §61, applied to this record

This note reports findings that **weaken my own prior claims** — a wrong absence
claim, a fake gate ratio, a self-granted authorization, an interface that reports
blocked as passing. That is the direction the trust runs. The system does not
earn trust by producing more PASS results; it earns it by demonstrating that it
can detect when PASS is false.

**Unknown remains valid. Blocked remains valid. This phase ends `BLOCKED`.**

## Related

- [v4.0 repair record](v4-0-repair-rebaseline-record.md)
- [PT-2026-10-03-001 — T0 Baseline and HOLD](production-test-pt-2026-10-03-001.md)
- Git porcelain output is whitespace-significant (FreeBuff notebook file `../39_LESSONS/git-porcelain-is-whitespace-significant.md`)
- Search detector (FreeBuff notebook file `../state/repair/search-detector.mjs`) ·
  Gate mutation harness (FreeBuff notebook file `../state/repair/gate-mutation.mjs`) ·
  Instrumentation certification (FreeBuff notebook file `../state/repair/instrumentation-certification.mjs`)