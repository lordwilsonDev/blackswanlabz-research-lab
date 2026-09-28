---
source: https://github.com/lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE/blob/765979bda8b7fb5be123261578fdd4cf0d943c53/ail_research_loop/test_reference.py
repo: lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE
commit: 765979bda8b7fb5be123261578fdd4cf0d943c53
captured: 2026-09-28
status: active
---

# AIL research-loop reference-implementation tests

`ail_research_loop/test_reference.py` is the unit-test suite for `reference_implementation.py`, the standard-library-only state machine + JEV decision procedure + evidence weighting + theory update that implements the [AIL + MoIE Recursive Research Protocol](../04-papers/ail-moie-recursive-research-protocol.md) spec.

## The 8 tests

- `test_unknown_without_evidence`
- `test_strong_support`
- `test_conditional_support_when_scope_bounded`
- `test_not_equal`
- `test_confound_preserves_disagreement`
- `test_illegal_jump_rejected`
- `test_preregistration_freezes_predictions`
- `test_negative_evidence_cycle_can_finish`

## Command and result

```bash
PY=/opt/homebrew/Caskroom/miniforge/base/bin/python
cd ~/projects/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE/ail_research_loop
$PY -m unittest test_reference.py
```

Re-run 2026-09-28 at commit `765979bda8b7fb5be123261578fdd4cf0d943c53`: **OK** (8 tests, 0 failures).

## The smoke-run fix (PR #1)

PR #1 (`restructure/research-loop-and-audit-chain`, merged 2026-09-28) fixed a crash in `reference_implementation.py`'s smoke example: the script ended with `print(to_json(cycle.as_dict()))`, which passed a plain dict into `dataclasses.asdict()` and raised `TypeError`. The fix changed it to `print(to_json(cycle))`. Verified in that PR: `python reference_implementation.py` completes where it previously crashed.

## Open state-machine inconsistency

`ail_research_loop/README.md` documents an unreconciled discrepancy between the two state-machine descriptions in this package:

> "`execution-plan.md` ('State machine') lists a different, finer-grained set of 15 states (`INTAKE`, `ASSUMPTIONS`, `INVERSION`, `MECHANISMS`, …, `ARCHIVED`) that makes the AIL and MoIE steps explicit states. The spec and code do not yet have those states; AIL and MoIE happen inside `PROBLEM_DEFINED → HYPOTHESIS_FORMED`. Reconciling the two is open work."

`spec.md` §5 and the code implement a 12-state machine (`DRAFT → PROBLEM_DEFINED → HYPOTHESIS_FORMED → PREREGISTERED → READY_TO_EXECUTE → EXECUTING → RESULTS_AVAILABLE → EVIDENCE_SYNTHESIZED → JEV_EVALUATED → THEORY_UPDATED → REENTRY_READY → COMPLETE`, plus exceptional states `BLOCKED · FAILED_EXECUTION · INVALIDATED`). `execution-plan.md`'s 15-state list is not implemented. This is unresolved, not fixed here.
