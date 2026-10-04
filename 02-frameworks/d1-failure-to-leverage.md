---
source: D1 — Failure-to-Leverage Compiler
captured: 2026-10-04
status: active
---

# D1 — Failure-to-Leverage Harness

## Purpose

D1 captures the Black Swan Labs principle:

> **Turn every discovered problem into the highest-leverage reusable capability available from that discovery.**

The harness does not treat a discovered failure as the terminal state.

It asks:

**Problem → Failure → Inversion → Hidden variable → Causal attribution → Leverage → Reusable control → Next test**

The unit of progress is therefore not merely a solved problem.

It is a **better research instrument produced by the problem**.

## Doctrine

### D1.1 Failure is evidence

A failure is retained as an observation.

Do not erase the failed path because a later run succeeds.

### D1.2 Invert the failure

Ask what assumption produced the failure.

Then invert it.

Example:

> Multiple models agreed, therefore verification was independent.

becomes:

> Multiple models may share an upstream capability, therefore agreement may not establish independence.

### D1.3 Find the missing variable

Ask:

> **What existed in the system that the experiment failed to represent as a variable?**

UNKNOWN is a first-class state.

UNKNOWN is never silently converted to ABSENT.

### D1.4 Find causal attribution

Separate:

- observed result;
- capability;
- responsible component;
- environment contribution;
- verification contribution.

A correct result with incorrect attribution remains an attribution failure.

### D1.5 Convert to reusable leverage

A discovered failure should produce a candidate control that applies beyond the original incident.

D1 ranks candidate controls by:

**impact × recurrence × generality ÷ cost**

This score is a prioritization heuristic, not a scientific law.

### D1.6 Generate the next question

The highest-value output of D1 may be a question that did not exist before the failure.

The harness therefore persists generated questions.

## Status model

- LEVERAGE_CAPTURED — a reusable control and new questions were extracted.
- DISCOVERY_CAPTURED — a research discovery was preserved but leverage is not yet instantiated.
- ATTRIBUTION_BLOCKED — an influential unresolved variable prevents causal attribution.
- CASCADE_DETECTED — an unresolved/shared variable has propagated into downstream artifacts.
- HARNESS_INPUT_INVALID — the dossier itself is structurally invalid.
- NO_NEW_DISCOVERY — the run did not expose a new reusable finding.

## Minimal dossier

A D1 dossier records:

- research ID;
- problem;
- observed event;
- assumptions;
- variables and provenance;
- failure;
- inversion;
- candidate controls;
- downstream dependencies;
- tests;
- new questions.

Run:

python scripts/d1_failure_to_leverage.py init <dossier.json>

then:

python scripts/d1_failure_to_leverage.py analyze <dossier.json>

and:

python scripts/d1_failure_to_leverage.py self-test

The harness is standard-library only.

## The meta loop

D1 is recursive.

After extracting a control, ask:

> What failure could this new control itself miss?

Then create the next D1 dossier.

That yields:

D1_1 → D1_2 → D1_3 → …

The stopping condition is not "nothing else could ever be missed."

It is:

> **No currently identified influential unknown remains untested at the stated research boundary, and the next question is explicitly recorded.**

## Canonical multimodal use

For multimodal verification, the first control should normally be a **Capability Provenance Preflight**:

1. inventory model-native capabilities;
2. inventory preprocessing;
3. inventory OCR/captioning/vision services;
4. inventory retrieval;
5. inventory memory;
6. inventory tools;
7. inventory system context;
8. inventory judge inputs;
9. map shared pathways;
10. isolate or ablate relevant upstream capabilities;
11. then interpret multi-model agreement.

This directly targets the Cascade Mistake and Multimodal Verification Misidentification.

## Research principle

> **Do not merely solve the problem. Extract the mechanism that prevents the same class of problem from being solved badly again.**

That mechanism is the leverage.

## Core formula

Problem
  ↓
Failure
  ↓
Invert
  ↓
Missing Variable
  ↓
Causal Attribution
  ↓
Highest-Leverage Control
  ↓
Reusable Test
  ↓
New Question
  ↓
Next Experiment

The harness exists to make that loop executable rather than rhetorical.
