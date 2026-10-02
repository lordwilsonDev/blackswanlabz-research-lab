# Three-Process Learning Research Protocol v0.1

## Purpose

This document is the operating protocol that connects the three core measurement processes:

1. INV-LTB — characterize the problem resistance terrain.
2. LTB — measure the learner capability trajectory.
3. Q2B-LTB — integrate terrain, learning, construction, verification, transfer, retention, and reference effort.

CRT-1 is a reproducibility gate for the protocol, not a fourth measurement process.

No new experimental run is permitted while this protocol or one of its three core processes has an unresolved readiness defect.

## Process 0 — Registration and Evidence Firewall

This gate happens before any of the three measurement processes.

### P0.1 Freeze the instrument

Record benchmark family version, exact Git commit, task/project version, verifier version, analysis version, resource budget, stopping rules, and contamination controls.

### P0.2 Separate roles

Maintain four distinct roles:
- Investigator: can inspect the full research context and maintain the benchmark.
- Learner: receives only preregistered benchmark inputs and permitted resources.
- Verifier: independently evaluates correctness.
- Analyst: interprets the preserved records.

A single system may technically perform more than one role only when the protocol explicitly labels the role transition and prevents hidden-context leakage.

### P0.3 Freeze the evidence boundary

The learner must not receive hidden reference solutions, investigator-only context, unpublished interpretation of its own trajectory, post hoc benchmark revisions, or hidden verifier assumptions.

### P0.4 CRT-1 readiness gate

A fresh investigator context must reconstruct the three processes, their order, metric contracts, verification split, terrain dimensions, arms, resource ledger, falsification rules, and change-control rules.

CRT-1 failure blocks experimental execution.

# Process 1 — INV-LTB: Problem Terrain Characterization

## Question

What demands does the problem impose, independent of any single learner interpretation of those demands?

## Step 1. Define the problem

Freeze the initial problem statement, required outcome, constraints, public source material, correctness criteria, and candidate transfer structures.

## Step 2. Define terrain dimensions

### T1 — Entry cost
Active effort/resources before coherent engagement.

### T2 — Extraction demand
Information that must be extracted before meaningful progress. Record necessary, optional, and disputed extraction.

### T3 — Generalization demand
Structural transformations required before an existing strategy stops being sufficient. Use a structurally manipulated instance ladder; item number is not difficulty.

### T4 — Exhaustion gradient
Where additional effort stops producing proportional progress. Record plateau location and between-run variance.

### T5 — Destruction requirement
Prior representations that causally obstruct progress. A candidate destruction requirement requires intervention: retain representation → outcome; remove representation → outcome; restore representation → outcome.

## Step 3. Use learner/model arrays as probes

Terrain is not defined from one learner subjective map. Preserve each map, shared features, unique features, disagreements, unresolved features, and reasons for disagreement where known.

Map divergence is data. It is not automatically good, bad, deep, shallow, rich, or erroneous.

## Step 4. Terrain arms

- DESTROY
- CONSTRUCT
- TERRAIN-INHERIT

Do not silently mix terrain mapping with capability scoring.

## Step 5. Terrain output

Output is a structured profile:
problem → T1/T2/T3/T4/T5 → evidence → divergence → stability → unresolved claims

There is no single terrain score.

## Process-1 completion gate

Process 1 is complete only when terrain definitions are frozen, the T3 ladder is structurally justified, destruction candidates have intervention designs, map divergence is preserved, boundedness of each verification procedure is documented, and unresolved terrain claims are explicitly marked.

# Process 2 — LTB: Learner Capability Trajectory

## Question

How does a learner move from unfamiliarity to independently verified transferable capability?

## Step 1. Establish baseline

Record initial capability on fresh tasks. Do not infer capability from self-report, correct explanation alone, exposure to examples, or benchmark familiarity.

## Step 2. Acquire capability

Use only the registered condition: capability-first, instruction-first, or another preregistered condition. Log all assistance.

## Step 3. Record level transitions

- L1 recognition
- L2 mechanism modeling
- L3 fresh in-domain application
- L4 structural transfer
- L5 generation of an unsupplied method/artifact

Every L-level crossing requires both:

Verification A — Capability: the learner independently performs on a fresh instance.

Verification B — Correctness: an independent mechanism establishes that the performance is correct.

One without the other is not a verified level crossing.

## Step 4. Record trajectory events

Record active effort to engage, model, architect, build, function, verify, transfer, and retain.

Wall-clock duration is not substituted for active effort.

## Step 5. Audit the verifier

Every failed result receives an initial failure classification:
LEARNER_FAILURE | ARTIFACT_FAILURE | VERIFIER_FAILURE | PROTOCOL_FAILURE | DATA_RESOURCE_FAILURE | UNRESOLVED

A verifier failure is corrected as an instrument defect and does not count as learner failure. Verifier corrections remain part of the trajectory record.

## Step 6. Retention

Re-test on fresh instances at +1 day, +7 days, and +30 days. Stable capability is the highest level satisfying the preregistered retention rule.

## Process-2 completion gate

Process 2 is complete only when every claimed level has A+B verification, active effort is recorded, assistance is logged, verifier status is separated from learner status, transfer is fresh, retention policy is executed or explicitly pending, and no hidden-context dependency remains.

# Process 3 — Q2B-LTB: Question-to-Build Integration

## Question

Given a real problem and required outcome, how efficiently can the intelligence acquire the capabilities needed to produce an independently verified working artifact?

Process 3 does not replace Processes 1 or 2. It composes their outputs.

## Step 1. Select a real project

The project must have a concrete starting question, concrete required output, public documentation, interacting requirements, independent verification, defensible reference effort, and transfer opportunities.

## Step 2. Reconstruct the reference trajectory

Reference effort must represent active effort, not calendar duration.

Evidence tiers:
- A — direct labor records
- B — published staffing/duration
- C — reconstructed project effort
- D — expert estimate

Do not calculate TCR when the reference denominator is not comparable.

## Step 3. Execute the learner trajectory

Capture Q0 → Q1 → Q2 → Q3 → Q4 → Q5 → Q6 → Q7 → Q8 → Q9:
- Q0 problem comprehension
- Q1 mechanism identification
- Q2 architecture
- Q3 first executable prototype
- Q4 functional implementation
- Q5 robust implementation
- Q6 independent verification
- Q7 independent reconstruction
- Q8 structural transfer
- Q9 novel extension

## Step 4. Maintain the resource ledger

Record active effort, tokens, tool calls, human intervention, external references, compute, and setup time when relevant.

No resource-normalized claim is made without a complete enough ledger.

## Step 5. Verify the artifact

Correctness requires an independent verifier. The verification record states what was checked, how it was checked, what was not checked, verifier version, verifier defects encountered, and whether verification is bounded or proof-level.

## Step 6. Transfer

Supply a structurally different problem without supplying its solution procedure. Transfer failure is evidence about capability, not automatically evidence about terrain.

## Step 7. Reconstruction

Strip original context and evaluate whether another intelligence can reconstruct the demonstrated capability from the specified evidence package. Reconstruction is distinct from ordinary transfer.

## Step 8. TCR

TCR = E_reference / E_learner

TCR is a trajectory-compression statistic. It must never be translated into IQ, intelligence ranking, years of knowledge acquired, or universal learning speed.

## Process-3 completion gate

A Q2B run is complete only when the project reference is defensible, active effort is normalized, artifact correctness is independently verified, transfer is fresh, reconstruction conditions are documented, retention status is known, hidden assistance has been audited, and interpretation scope is explicit.

# Cross-Process Analysis

The three processes remain analytically distinct:

INV-LTB → terrain profile
LTB → learner trajectory
Q2B-LTB → integrated question-to-verified-build trajectory

Do not collapse terrain into learner difficulty, correctness into learning, speed into intelligence, transfer into broad expertise, TCR into IQ, map agreement into truth, map divergence into richness, calendar duration into active effort, or verifier success into proof unless proof-level checking was actually performed.

## Failure taxonomy

Every material failure is classified before interpretation:
1. Learner failure
2. Artifact/implementation failure
3. Verifier failure
4. Protocol failure
5. Data/resource failure
6. Unresolved

## Change loop

run → observe → classify → record issue → adversarial review → version → rerun

Existing runs remain pinned to their original instrument version.

# Stop Rule

No new experimental test starts until all three processes pass the readiness checklist.

Readiness requires definitions frozen, sequence fixed, inputs/outputs specified, role separation defined, evidence firewall defined, verifier audit defined, resource ledger defined, failure taxonomy defined, retention policy defined, transfer policy defined, reconstruction policy defined, change-control linkage defined, preregistration fields sufficient, and run-record schema sufficient.

A missing process element is a protocol defect, not a reason to improvise during a live experiment.

# Current State

The existing Python and mbeddr runs remain historical/provisional records. No new run should be interpreted as evidence under this protocol until the readiness gate is formally marked READY in version-controlled documentation.