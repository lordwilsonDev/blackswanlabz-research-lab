# Q2B-LTB-1 — Final Learning Trajectory Benchmark

## Purpose

Measure the complete path:

Question → engagement → learning → capability → build → verification → transfer → retention.

Q2B-LTB integrates LTB and INV-LTB and adds a reference-effort axis.

## Core question

Given a real problem and a required outcome, how rapidly can an intelligence acquire the capabilities necessary to produce an independently verified working artifact?

## Required project

A benchmark project must have a concrete initial problem, concrete required outcome, public documentation, nontrivial interacting requirements, independent verification criteria, a defensible reference-effort estimate, and enough structure to define transfer tests.

## Reference effort

Reference effort is measured in active effort units such as person-hours or person-months.

Calendar duration is not treated as equivalent to labor effort.

Evidence tiers:

- Tier A: direct labor records
- Tier B: published staffing and duration records
- Tier C: reconstructed effort from documented project stages
- Tier D: expert estimate, explicitly labeled

## Arms

### Capability-first

Question and outcome first; learning is acquired on demand.

### Instruction-first

Structured instruction precedes construction.

### Model-assisted capability-first

AI may research, explain, critique, build, and debug; all assistance is logged.

## Project milestones

Q0 problem comprehension
Q1 domain mechanism identification
Q2 architecture
Q3 first executable prototype
Q4 functional implementation
Q5 robust implementation
Q6 independent verification
Q7 independent reconstruction
Q8 structural transfer
Q9 novel extension

Q-levels are project-specific. L-levels are general capability levels.

## Core timing events

T_engage
T_model
T_architecture
T_first_build
T_functional
T_verified
T_transfer
T_retained

Primary time outcome: T_Q2V, active effort from question to verified capability.

## Trajectory Compression Ratio

TCR = E_reference / E_learner

TCR is a relative trajectory-compression statistic, not an IQ score and not a literal claim that a learner acquired ten calendar years of knowledge in a few hours.

## Transfer

After verified construction, supply a structurally different task without supplying a new solution procedure.

## Reconstruction

Strip the original learner or model context. Give a second learner or model the artifact and specification and test whether capability can be reconstructed.

## Retention

Re-test on fresh instances at T+1 day, T+7 days, and T+30 days.

## Resource ledger

Record active time, model and token use, tool use, human interventions, external references, compute, and relevant setup time.

## Completion states

COMPLETE, PROVISIONAL, INCOMPLETE, FAILED, UNRESOLVED.

## Falsification

The central learning-trajectory hypothesis is weakened if speed advantages disappear after resource normalization, fast builds fail independent verification, transfer or retention collapses, results depend on hidden context, historical reference effort proves non-comparable, or the effect fails on independent projects or learners.
