# Human–AI Idea Realization Framework v0.1

## Core unit

The unit of analysis is the **human–AI production system**:

`human intent -> model translation/reasoning -> artifact -> verification -> revision -> retained capability`

The framework does not treat the human and model as independent producers when the task itself is collaborative.

The research question is not whether a human is "smart" or whether a model is "smart."

It is:

> **How reliably can a human's intended idea become a working, inspectable, reusable artifact through interaction with an AI system?**

## Decomposition

Observed realization can be decomposed into four experimentally separable contributors:

### M — Model realization capability

Hold the task specification fixed and vary the model.

Measure:
- first-pass requirement satisfaction
- executable correctness
- omission rate
- defect rate
- repair burden
- verification closure
- transfer behavior

### H — Human articulation capability

Hold the model and task family fixed while comparing successive intent specifications or interaction protocols.

Measure:
- requirement recovery
- ambiguity reduction
- instruction completeness
- correction frequency
- model repair burden
- realization fidelity

### J — Joint production capability

Allow both human articulation and model realization to vary.

Measure:
- time/effort to verified artifact
- number of interaction/revision cycles
- first-pass success
- final fidelity
- verification closure
- retained/reusable capability

### S — System/harness contribution

Hold human intent and model constant while varying memory, routing, verification, tooling, or process.

Measure:
- defect escape
- recovery success
- verification latency
- context loss
- artifact persistence
- model substitution sensitivity

## No single composite score by default

Report a **Realization Vector** instead of collapsing the system into one number:

`R = (F, P, B, V, T, A, C)`

Where:

- `F` = intent-to-artifact fidelity
- `P` = first-pass realization
- `B` = human/model repair burden
- `V` = verification closure
- `T` = transfer/generalization
- `A` = artifact accumulation/reusability
- `C` = realization cost/effort

A composite score may be preregistered for a specific study, but never inferred after seeing results.

## Primary distinction

A polished artifact is not enough.

The evaluator asks:

1. What was the intended idea?
2. What requirements were explicitly recoverable?
3. What did the model actually implement?
4. What failed on first pass?
5. What did the human have to repair or clarify?
6. What did verification discover?
7. What survived as a reusable artifact?
8. Can the same idea be reproduced with another model?
9. Can another person's model realize a comparable task?

## Historical vs controlled evidence

Historical trajectory evidence can establish **what changed**, but does not by itself identify causality.

Controlled arms are required to separate:
- model improvement
- human articulation improvement
- harness/process improvement
- task-complexity changes.

## Fair peer comparison

External comparisons should use publicly inspectable artifacts and should normalize for:
- task difficulty
- artifact scope
- verification burden
- model access
- interaction availability
- project age
- declared AI involvement.

A GitHub repository alone does not reveal the hidden human–AI interaction process.

Therefore public-repository comparisons measure **artifact realization**, not private prompting skill, unless interaction logs or equivalent process evidence are available.

## Core hypothesis family

### H1 — Model capability

With intent held fixed, newer/more capable models should change realization metrics.

### H2 — Articulation capability

With model held fixed, improved intent specification should change realization metrics.

### H3 — Joint capability

The human–AI system should improve as both articulation and model capability improve.

### H4 — Harness mediation

Memory, routing, verification, and reusable process can change realization quality even when the underlying model is unchanged.

These are empirical hypotheses. None is assumed true.

## The cleanest experiment

Use one frozen idea represented at three levels:

**L0 — raw human statement**

**L1 — structured specification**

**L2 — executable acceptance contract**

Then run each level through multiple models.

This produces the key matrix:

| Intent level | Model A | Model B | Model C |
|---|---|---|---|
| L0 raw idea | realization vector | realization vector | realization vector |
| L1 structured | realization vector | realization vector | realization vector |
| L2 executable | realization vector | realization vector | realization vector |

That matrix separates:
- model capability
- articulation quality
- translation burden.

## Longitudinal test

For the same human operator, freeze several recurring task classes and compare early vs later intent articulation while controlling model/version where possible.

The result is:

`articulation_gain = R(later intent, same model) - R(earlier intent, same model)`

This is the direct test of whether the human got better at making ideas executable.

## Retrospective trajectory

Historical repositories can then be read as a sequence:

`idea -> specification -> artifact -> test -> reusable system -> new idea`

The trajectory itself is evidence of **realization capacity**, even where causal decomposition remains unresolved.

## Important boundary

The framework does not require a metaphysical claim about humans and AI being one entity.

It only treats their coupled production process as the correct empirical unit when neither side alone constitutes the complete production system.
