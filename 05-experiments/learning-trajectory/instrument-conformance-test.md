# Instrument Conformance Test

## Purpose

This test checks whether the executable run-record contract mechanically enforces the material requirements already stated by:

- `05-experiments/learning-trajectory/protocol-0.1.md`
- `05-experiments/learning-trajectory/preregistration-template.md`
- `05-experiments/learning-trajectory/metric-contracts.md`
- `05-experiments/learning-trajectory/context-bundle-spec.md`

It is an instrument-engineering test, not a learner, terrain, transfer, retention, reconstruction, or cross-condition benchmark.

## Rule

A requirement that exists only in prose but can be omitted from a valid run record is an enforcement gap.

The test therefore uses a closed-world approach for material execution fields:

- protocol identity and exact commit
- verifier identity and scope
- Q0-Q9 milestones
- T1-T5 terrain record
- reference-effort provenance and comparability
- assistance/resource detail
- reconstruction conditions
- retention epochs
- registered condition/arm linkage

## Non-goals

Passing this test does not pass G19 or G20.

It does not establish independent investigator reconstruction or end-to-end future-run reproducibility.

It establishes only that the machine-readable run contract is aligned tightly enough with the written protocol to prevent the tested omissions.

## Change-control relation

This artifact exposes a protocol/enforcement defect. Repair must be versioned; historical runs remain pinned to their prior benchmark/schema versions.
