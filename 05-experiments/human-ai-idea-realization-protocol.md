# Human–AI Idea Realization Protocol v0.1

## Purpose

Measure how effectively a human-originated idea becomes a working, verified, reusable artifact through AI-assisted production.

This is an instrument study, not a learner benchmark.

It does not alter the frozen Learning Trajectory protocol or reopen its experimental gates.

## Stage 1 — Capture intent

Record the earliest materially meaningful human statement.

Do not clean it before preserving the raw form.

## Stage 2 — Build three representations

Create:

- Raw Intent (L0)
- Structured Intent (L1)
- Executable Contract (L2)

Each representation must preserve lineage to the prior form.

## Stage 3 — Freeze model condition

Record:
- provider
- model
- version
- context policy
- tools
- memory state
- system instructions.

A model comparison is invalid when these uncontrolled variables materially differ.

## Stage 4 — Build

For each model/intent arm:
- provide only registered materials,
- execute the same task,
- capture the first artifact,
- record all model-visible corrections.

## Stage 5 — Verify

Use executable acceptance tests whenever possible.

Classify every failure as:
- intent ambiguity
- model realization failure
- tool/harness failure
- verifier defect
- external dependency failure
- unresolved.

## Stage 6 — Repair accounting

Separate:
- human clarification,
- model self-repair,
- verifier-triggered repair,
- human direct code/edit intervention.

This is critical.

A final perfect artifact with 40 hidden human repairs is not equivalent to a first-pass artifact that required none.

## Stage 7 — Final fidelity

Compare final artifact against the intent contract.

Record:
- requirements satisfied
- omitted requirements
- contradictory behavior
- invented scope
- unrequested changes.

## Stage 8 — Retained capability

Record whether the resulting artifact became:
- a reusable procedure,
- a reusable skill,
- a reusable harness,
- a reusable library,
- a published method,
- a new product/system component.

## Primary metrics

### Intent Fidelity (F)

Satisfied registered requirements / registered requirements.

### First-Pass Realization (P)

Requirements satisfied before corrective intervention / registered requirements.

### Repair Burden (B)

Human clarification + direct human edits + model-repair cycles, each reported separately.

### Verification Closure (V)

Verified claims or requirements / claimed requirements.

### Transfer (T)

Fresh structurally changed task performance.

### Accumulation (A)

Reusable capabilities produced from the task.

### Realization Cost (C)

Wall time, active human effort, model calls/tokens, and tool calls.

## Required evidence

Every measured arm should retain:
- raw intent
- structured intent
- executable contract
- model metadata
- prompt/context record
- first artifact
- repair log
- verifier output
- final artifact
- retained-capability record.

## Peer comparison

The preferred external comparison population is public AI-assisted software projects with:
- inspectable version history,
- declared AI involvement where available,
- executable artifacts,
- tests or other verification evidence.

Do not infer private prompting quality from a public repository alone.

## Falsifiers

This framework would be weakened if:
- improvements disappear when model capability is controlled,
- apparent articulation gains are explained entirely by task selection,
- artifact improvements do not survive verification,
- historical output cannot be reconstructed from preserved records,
- peer-normalized comparisons are dominated by confounds.

## Stop rule

No ranking or superiority claim should be made from one historical trajectory.

A minimum controlled study requires at least:
- one frozen task family,
- one controlled model,
- multiple intent representations,
- executable verification,
- explicit repair accounting.

## Relationship to existing lab

This protocol sits underneath:
- IBX discovery
- AIL inversion
- MoIE
- SD-BP build discipline
- Green-Gate verification
- capability fabric
- institutional memory
- Adaptive Infrastructure.

The existing systems become components of the realization pipeline rather than separate phenomena.
