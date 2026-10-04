---
source: D1 — Failure-to-Leverage Compiler experiment protocol
captured: 2026-10-04
status: active
---

# D1 — Failure-to-Leverage Compiler Experiment

## Question

Can a research failure be converted into a reusable control and a higher-value next question without losing the original failure provenance?

## Test

Run scripts/d1_failure_to_leverage_compiler.py self-test.

Expected result:

status = PASS

The self-test includes:

1. hidden/shared multimodal capability;
2. false-failure attribution;
3. clean leverage capture.

## Primary behavior

Given a structured D1 dossier, the harness must:

- preserve the failure;
- identify unresolved influential variables;
- identify shared influential variables;
- block causal attribution when necessary;
- detect explicit downstream propagation;
- rank candidate reusable controls;
- generate additional questions;
- produce a next research action.

## Acceptance conditions

### A. No silent variable collapse

UNKNOWN remains UNKNOWN.

### B. Attribution firewall

An influential unresolved variable blocks definitive causal attribution.

### C. Cascade detection

A downstream artifact explicitly dependent on an unresolved/shared variable produces CASCADE_DETECTED.

### D. Leverage extraction

A candidate control with impact, recurrence, generality, and cost receives a deterministic priority score.

### E. Question generation

The harness produces follow-up questions from the unresolved variable and the downstream cascade.

### F. Recursive use

The output contains sufficient information to become the input boundary for the next research cycle.

## Example use

python scripts/d1_failure_to_leverage_compiler.py init /tmp/d1.json
# populate /tmp/d1.json
python scripts/d1_failure_to_leverage_compiler.py analyze /tmp/d1.json
python scripts/d1_failure_to_leverage_compiler.py self-test

## Interpretation

A D1 PASS does not mean the research claim passed.

It means the harness successfully performed its job as a meta-instrument.

A CASCADE_DETECTED result is a successful detection outcome when the dossier accurately records the discovered cascade.

A BLOCKED attribution is an epistemic control, not evidence that the underlying system is false.


## Steel regression suite

The D1 self-test now includes hardening cases for:

- missing required environment/boundary/measurement/independence sections;
- hidden shared multimodal capability;
- measurement-context drift;
- observer intervention that changes the measured environment;
- boundary violation;
- canonical multimodal cascade fixture;
- MSB environment/observer cascade fixture.

The lab verification script invokes the D1 self-test automatically.

The two canonical fixtures are deliberately different:

1. `cascade-multimodal-verification.json` exercises shared multimodal capability and verification-independence failure.
2. `msb-environment-cascade.json` exercises software-engineering environment drift, observer mutation, supervisor topology, CI configuration, and restore-semantics cascades.

A future D1 implementation change that stops detecting these cases must fail the lab verification gate.
