---
source: BlackSwanLabz Research Lab protocol (authored in this repo)
captured: 2026-10-02
status: pending
---

# LTB-0.1 — Learning Trajectory Benchmark

## Purpose

Measure the acquisition of transferable capability rather than a single test score.

## Primary question

How far and how quickly does a learner move from an unfamiliar problem to independently verified capability?

## Capability levels

| Level | Operational definition | Minimum evidence |
|---|---|---|
| L1 | Recognize relevant concepts and structures | Fresh recognition task passes |
| L2 | Model mechanisms and counterfactuals | Mechanism and prediction task passes |
| L3 | Apply to a fresh in-domain problem | Independent solution plus correctness check |
| L4 | Transfer underlying structure | Structurally modified task plus verification |
| L5 | Generate a method or artifact for an unsupplied procedure | Novel method plus hidden evaluation and correctness verification |

L-levels are performance states, not credentials.

## Verification split

Verification A asks whether the learner can independently perform on a fresh instance without the original worked example or hidden reference solution.

Verification B asks whether an independent mechanism establishes that the produced result is correct.

A level crossing requires both.

## Retention

Provisional crossings are retested at T+1 day, T+7 days, and T+30 days.

The highest stable level is the highest level that meets its retention rule.

## Evidence channels

Possible evidence includes executable validation, written explanation, oral defense, transfer, delayed retest, and cross-model reconstruction.

Different channels are not assumed to be statistically independent merely because they are different modalities.

## Output

A trajectory record reports initial state, time and resources, provisional and stable L-levels, transfer, retention, verification, reconstruction, and assistance dependence.

The result is a trajectory, not an aggregate score.
