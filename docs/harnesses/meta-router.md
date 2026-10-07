# Meta Router

## Purpose

The Meta Router decides **which reasoning/control apparatus should handle a request** and whether the selected apparatus is sufficient.

It sits above the regular understanding harness.

**Regular harness:** understand the situation.

**Meta Router:** determine how the situation should be understood, which harnesses are required, what evidence standard applies, and when the selected approach must be challenged or escalated.

## Core Invariant

> **Route before reasoning, test the route while reasoning, and re-route when the evidence shows the current apparatus is insufficient.**

## Routing Pipeline

```
INPUT
 ↓
NORMALIZE
 ↓
CLASSIFY
 ↓
IDENTIFY DOMAIN
 ↓
IDENTIFY STAKEHOLDERS / AUTHORITY
 ↓
IDENTIFY RISK
 ↓
IDENTIFY EVIDENCE REQUIREMENT
 ↓
SELECT HARNESS / SKILL
 ↓
CHECK COVERAGE
 ↓
EXECUTE
 ↓
MONITOR FOR ROUTING FAILURE
 ↓
RE-ROUTE / ESCALATE
 ↓
VERIFY
 ↓
RECORD ROUTING DECISION
```

## Route Classes

### R0 — Direct Answer

Use when the request is low-risk, well-defined, evidence requirements are simple, and no external state needs to be changed.

### R1 — Understanding Harness

Use for ambiguous organizational/process questions, complaints, operational bottlenecks, workflow analysis, institutional-memory questions, and process improvement.

### R2 — Failure & Recovery Harness

Use when the primary problem is an observed failure, incident, recurring breakdown, or recovery weakness.

### R3 — Question Engineering

Use when the main problem is that the question itself is underspecified, ambiguous, improperly scoped, or mixes multiple propositions.

### R4 — AIL / MoIE

Use when competing explanations, assumptions, anomalies, inversion, or adversarial hypothesis testing are required.

### R5 — Evidence / Verification

Use when a consequential conclusion depends on source quality, independent verification, contradiction handling, provenance, or auditability.

### R6 — Domain-Specific Harness

Use when specialized technical, legal, financial, safety, scientific, medical, or other domain constraints dominate.

### R7 — Meta Harness

Use when the question concerns whether the current reasoning process, harness, routing decision, evidence standard, or system design is itself working correctly.

### R8 — Human / Authorized Escalation

Use when authority, privacy, safety, legal obligations, employment consequences, financial permissions, or other consequential decisions exceed the system's authority.

## Routing Questions

Before selecting a route:

1. What is the user actually trying to accomplish?
2. What is the deliverable?
3. What domain is involved?
4. What is known?
5. What is merely reported?
6. What is uncertain?
7. What evidence is required?
8. Who has authority over the decision?
9. What could go wrong?
10. What is the consequence of being wrong?
11. Does the regular harness cover the problem?
12. Does another specialized harness need to run first?
13. Is this actually a meta-level problem?

## Route Selection Matrix

| Condition | Primary Route | Add |
|---|---|---|
| Ambiguous organizational problem | R1 | R3 |
| Complaint / allegation | R1 | R5 |
| Active incident | R2 | R5 |
| Competing explanations | R4 | R5 |
| Weak question | R3 | R1 |
| Evidence-sensitive conclusion | R5 | R1 |
| Specialized domain | R6 | R5 |
| System/harness critique | R7 | R3/R5 |
| Consequential decision beyond authority | R8 | Relevant route |
| Simple low-risk request | R0 | None |

Routes may be composed. The router must not force a single route when the problem is inherently multi-harness.

## Route Confidence

Every routing decision gets:

- route
- confidence
- reason
- alternatives considered
- evidence required
- escalation condition

Confidence states:

- HIGH
- MEDIUM
- LOW
- UNKNOWN

Low-confidence routing should trigger broader analysis rather than false precision.

## Routing Failure Detection

The router must watch for:

- unanswered core questions
- evidence requirements discovered late
- contradictory findings
- repeated rework
- unexplained exceptions
- scope drift
- wrong-domain assumptions
- authority mismatch
- inability to verify outcomes
- repeated need for a different harness

If detected:

```
ROUTING FAILURE
 ↓
STOP
 ↓
IDENTIFY MISROUTE
 ↓
PRESERVE WORK
 ↓
SELECT NEW ROUTE
 ↓
CONTINUE
```

Do not discard valid work merely because the initial route was wrong.

## Meta-Routing Rule

If the same class of failure repeatedly causes the router to choose the wrong apparatus, the problem is no longer only the underlying task.

It is a **routing-system defect**.

That defect becomes a Meta Harness investigation.

## Output Contract

The Meta Router returns:

```yaml
route:
  primary: R1
  secondary: [R3, R5]
confidence: MEDIUM
objective: "<normalized objective>"
domain: "<domain>"
risk: "<risk class>"
evidence_standard: "<required standard>"
authority: "<authorized decision maker>"
reason: "<why this route>"
alternatives:
  - "<alternative route>"
escalate_if:
  - "<condition>"
next_action:
  - "<first executable step>"
```

## Non-Negotiables

1. Never confuse a route with a conclusion.
2. Never let confidence in routing become confidence in facts.
3. Never suppress a competing route solely for convenience.
4. Never bypass a higher-risk evidence standard because a lower-risk route is easier.
5. Preserve work produced before a route correction.
6. Escalate when authority is exceeded.
7. Record routing decisions so routing itself becomes institutional memory.

## Relationship to the Regular Harness

```
META ROUTER
    ↓
SELECT / COMPOSE
    ↓
REGULAR UNDERSTANDING HARNESS
    ↓
SPECIALIZED HARNESS / SKILLS
    ↓
EVIDENCE + ACTION
    ↓
VERIFICATION
    ↓
META FEEDBACK
    ↺
```

The router is therefore a **control layer above reasoning**, not merely a classifier.
