# Instrument Conformance / Replay Audit — 2026-10-02

## Scope

Instrument engineering only. No learner, terrain, transfer, retention, reconstruction, or cross-condition benchmark run was initiated.

Historical records remain pinned to their original versions. The frozen v0.2 run-record schema was restored unchanged on this branch.

## Test A — Baseline schema conformance

The pinned v0.2 schema was compared against material requirements in:

- protocol-0.1.md
- preregistration-template.md
- metric-contracts.md
- context-bundle-spec.md

Result:

- 11 enforcement gaps identified.
- The most consequential gaps were optional exact-commit pinning, optional verifier identity, open-ended Q milestones, optional terrain fields, count-only assistance accounting, unstructured reconstruction conditions, unstructured retention, missing reference-effort comparability, free-text verifier scope, and free-text condition/arm identity.
- A minimal synthetic run record omitted material protocol fields and still satisfied the old schema's required-field surface.

## Test B — Candidate repair

A separate conformance candidate schema was created as:

`run-record.schema.conformance-candidate.json`

The frozen v0.2 schema was restored at:

`run-record.schema.json`

Candidate enforcement adds:

- run-record schema version
- exact Git commit
- task/preregistration/verifier/analysis versions
- concrete artifact references
- resource budget and stopping rules
- contamination controls and evidence firewall
- explicit role separation
- registered condition identifier
- closed Q0-Q9 milestones
- closed T1-T5 terrain fields when terrain is run
- reference-effort source and comparability
- structured assistance log
- structured verifier scope and verification level
- reconstruction conditions
- explicit +1/+7/+30 retention records
- conditional material-process payload requirements

## Test C — Negative-control / mutation suite

A complete synthetic record passed the current candidate contract.

Direct negative-control tests across the repair iterations covered deliberate regressions including:

1. remove Git commit requirement
2. remove Q9
3. allow arbitrary Q milestone keys
4. remove verifier version
5. remove one retention epoch
6. remove assistance log
7. remove task artifact reference
8. remove the T5 intervention structure
9. remove per-level A+B capability evidence
10. supply a transfer solution procedure
11. claim shared-system roles without a transition log

All tested regressions were detected by the candidate constraints.

This is a meta-test of the conformance gate itself: the gate detects the classes of omissions it claims to prevent.

## Test D — Replay preflight

A stronger G20 sub-gate was added.

The future-run replay preflight requires every registered run to identify concrete protocol, benchmark, task, preregistration, verifier, and analysis artifacts and verifies those references against the recorded Git commit in a local checkout.

Current repository finding:

- protocol artifact exists
- benchmark artifact exists
- task artifact exists
- metric/analysis artifact exists
- a preregistration template exists
- a concrete future-run preregistration instance is not currently present in the benchmark directory
- no versioned executable learner-correctness verifier artifact is currently present in the benchmark directory

Therefore G20 remains blocked.

A result note or hidden-test output is not treated as equivalent to an independently executable verifier.

## Test E — CI enforcement

The existing `.github/workflows/verify.yml` now invokes:

- `check_instrument_conformance.py`
- `test_conformance_mutations.py`

Observed CI behavior:

- repository pytest step passed
- the first conformance-enabled run failed because the isolated candidate schema was one revision behind the intended repair
- that defect was corrected
- the next run was queued against the corrected branch state

The CI failure was therefore used as another feedback signal rather than interpreted as a benchmark failure.

## Interpretation

The research instrument currently has a specification/enforcement gap, not a demonstrated invalidation of its measurement concepts.

The builder/cleaner pattern is becoming testable as an engineering process:

builder or editor -> machine conformance gate -> mutation test -> repair -> CI recheck

That process is not evidence that any named model is universally better at building or cleaning. A controlled builder/cleaner model comparison would be a separate study.

## Readiness impact

Official experimental readiness remains:

`BLOCKED_FOR_NEW_RUNS`

No G19 or G20 pass is claimed.

The candidate branch is an instrument-repair branch, not a new experimental version being silently applied to historical records.


## Final engineering pass

### Instrument-specific execution evidence

CI run `37073487889` executed the instrument-specific sequence successfully before the legacy repository verifier:

- pytest: PASS
- instrument conformance: PASS
- conformance mutation suite: PASS
- Q2B-MBEDDR-002 verifier tests: PASS
- replay preflight: PASS

The run then failed only in the separate legacy `scripts/verify.sh` step.

The legacy repository verifier was independently observed failing at the pinned pre-repair commit `5fa37688d7557a6e6026824b1aba8629d76f1997`, so that failure is not attributed to the new instrument machinery.

### CI separation

The instrument checks are now isolated in:

`.github/workflows/learning-trajectory-instrument.yml`

The legacy `.github/workflows/verify.yml` was restored to its pre-repair contents.

The dedicated instrument workflow was also corrected to install pytest and use a full-history checkout.

A dedicated run was then created at head `c4a2f88aca43370a67549511b9c23fe65f902b90`; its earlier environment issue was the missing pytest installation and has been corrected in the workflow.

### Current readiness interpretation

This pass establishes a mechanically testable instrument-enforcement layer.

It does not establish:

- G19 independent investigator reconstruction
- G20 end-to-end reproducibility of a completed learner run
- any learner/model performance result
- superiority of one model over another

The experimental hard stop remains in force.
