# Independent Verifier Artifact Contract v0.1

## Purpose

Define the executable correctness-verification layer required by the Three-Process Learning Research Protocol.

This document is an instrument specification. It is not a learner result and does not satisfy G20 by itself.

## Required verifier properties

A future task-specific verifier artifact must:

1. Be versioned and addressable at an exact Git commit or immutable release.
2. Accept the learner artifact and the registered task specification.
3. Execute registered correctness checks without using the learner's hidden reasoning or investigator-only conversation context.
4. Separate checked scope from unchecked scope.
5. State whether verification is bounded test-based or proof-level.
6. Emit machine-readable verdicts for each registered success criterion.
7. Record verifier defects independently of learner failures.
8. Preserve the exact verifier version in the run record.
9. Be rerunnable from the run's artifact references and commit.
10. Not silently change expected outputs after observing the learner result.

## Independence basis

The verifier implementation must declare one of:

- INDEPENDENT_EXECUTION — separate implementation/runtime from learner.
- SAME_SYSTEM_LABELED_TRANSITION — same model/system is used, but the transition is explicit and hidden-context leakage is prevented.
- NOT_INDEPENDENT — not acceptable for an independent correctness claim.

A run claiming independent correctness may not use NOT_INDEPENDENT.

## Output contract

Each verification result should include:

- run_id
- verifier_version
- task_id
- criterion_id
- verdict: PASS | FAIL | NOT_CHECKED | VERIFIER_ERROR
- checked_scope
- unchecked_scope
- verification_level
- evidence_reference
- failure_classification when verdict is FAIL or VERIFIER_ERROR

## Defect rule

If the verifier's expected behavior is found to be wrong, the event is a verifier defect.

The verifier must be corrected, versioned, and rerun. The original failure remains preserved as historical evidence.

## G20 consequence

A future-run replay is BLOCKED until the run record points to a concrete verifier artifact satisfying this contract.

A verifier version string, hidden-test output file, or prose assertion alone is insufficient.
