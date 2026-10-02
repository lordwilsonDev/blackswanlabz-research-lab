# Future-Run Replay Preflight

This is a deterministic G20 sub-gate. It does not run a learner experiment.

## Replay claim

A future registered run is replayable only when the run record identifies, at minimum:

- exact run-record schema version,
- protocol version,
- benchmark version,
- exact Git commit,
- task version,
- concrete preregistration artifact,
- concrete verifier artifact and version,
- analysis version,
- resource budget,
- stopping rules,
- contamination controls,
- exact artifact references.

## Stronger test

A local checkout must be able to resolve every artifact reference at the run's recorded commit.

A version string without a resolvable artifact is insufficient.

A result log is not a verifier artifact.

A preregistration template is not a preregistration instance.

## Current finding

The repository contains the protocol, benchmark, task, metric contracts, and historical run records.

The current tree does not contain a versioned verifier implementation that can be cited as the independent correctness mechanism for a future run. It also contains a preregistration template but no concrete future-run preregistration record under this benchmark directory.

Therefore this branch does **not** claim G20 PASS.

## Gate behavior

Replay preflight returns BLOCKED when a required artifact reference is missing or cannot be resolved at the recorded commit.

This is intentionally stricter than schema validation.
