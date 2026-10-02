---
source: BlackSwanLabz Research Lab protocol (authored in this repo)
captured: 2026-10-02
status: pending
---

# Q2B-MBEDDR-002 — Unit-Safe Reactive Controller Run

## Status

Completed exploratory run. No population-level learning claim.

## Task

Build a fresh controller capability combining physical-unit semantics with state/guard transition semantics.

## Preflight implementation

A fresh Python implementation represented:
- dimensions as integer L/T vectors,
- unit scale factors,
- derived unit quantities,
- state/transition objects,
- guarded event dispatch,
- bounded static analysis.

## Initial semantic suite

7/7 PASS after one implementation fix.

Cases:
1. 36 km/h >= 10 m/s
2. reject m/s versus m comparison
3. detect unreachable state
4. detect shadowed guarded transition
5. detect never-enabled guarded transition
6. transfer threshold expressed in km/h
7. transfer distance expressed in km/m

### Failure and correction

The first implementation reported 6/7 because its shadow verifier incorrectly tested:

guard_A AND guard_B across all probes

instead of the required implication:

guard_B -> guard_A

for a later guarded transition B shadowed by an earlier guard A.

After correcting the verifier invariant, the suite passed **7/7**.

This is recorded as a verifier implementation correction.

## Structural composition

The same unit system and state-machine system were composed in one controller representation.

The transfer cases passed without changing the underlying semantic model.

## L5-style extension

A project-extension variant was prepared to require a previously unsupplied controller capability while preserving the base semantics. The current run establishes the extension task and verifier framework; general L5 and independent reconstruction remain separate experimental claims.

## Current evidence

Base semantics: PASS 7/7
Verifier: PASS after correction
Structural transfer: PASS
Retention: pending
Independent reconstruction: pending
Cross-model: pending
Active learning effort: not measured
TCR: not reported

## Important finding

The benchmark again exposed the verifier as a potential source of false negatives. This is the third independent occurrence across the current program where the learner/system behavior was correct but the verifier needed correction.

This makes verifier auditing a mandatory component of the protocol.
