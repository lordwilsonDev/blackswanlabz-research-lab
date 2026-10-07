# Meta Router Skill

## Skill Identity

**Name:** Meta Router  
**Purpose:** Select, compose, challenge, and revise the reasoning/control apparatus used to solve a task.

## Trigger

Use this skill when:

- a task may require multiple reasoning frameworks;
- the correct investigative method is unclear;
- the user asks which harness/process should be used;
- a prior approach appears inadequate;
- evidence requirements are uncertain;
- the task spans multiple domains;
- the task asks whether a system, harness, benchmark, or reasoning process itself is working;
- routing errors could materially affect the result.

## Operating Principle

> Route before reasoning; challenge the route during reasoning; re-route when evidence demands it.

## Procedure

### Step 1 — Normalize

Convert the request into:

- objective
- deliverable
- constraints
- domain
- stakeholders
- authority
- time horizon
- risk

### Step 2 — Separate Epistemic States

Tag important information as:

- KNOWN
- REPORTED
- INFERRED
- HYPOTHESIZED
- UNKNOWN
- DISPUTED

Never promote a lower-confidence state merely because it is convenient.

### Step 3 — Determine the Primary Problem

Choose the dominant problem type:

- understanding
- question formulation
- failure/recovery
- evidence/verification
- competing hypotheses
- specialized domain
- meta-system evaluation
- consequential decision

### Step 4 — Select Routes

Choose a primary route and any required secondary routes.

Available routes:

- R0 Direct
- R1 Understanding
- R2 Failure & Recovery
- R3 Question Engineering
- R4 AIL/MoIE
- R5 Evidence/Verification
- R6 Domain-Specific
- R7 Meta
- R8 Human/Authorized Escalation

### Step 5 — Test Route Sufficiency

Ask:

1. Does the selected route answer the actual question?
2. Can it meet the evidence requirement?
3. Does it respect authority boundaries?
4. Can its output be verified?
5. What failure would indicate that this route is wrong?

### Step 6 — Execute the Smallest Sufficient Apparatus

Do not invoke every framework simply because it exists.

Use the smallest combination that can reliably answer the question.

Add apparatus only when evidence or failure requires it.

### Step 7 — Monitor

During execution, watch for:

- scope drift
- missing evidence
- contradictions
- unexplained anomalies
- repeated rework
- wrong-domain assumptions
- authority mismatch
- inability to verify
- recurring need for another route

### Step 8 — Re-Route

If the route fails:

1. stop extending the failed approach;
2. preserve useful work;
3. identify why the route failed;
4. select the new route;
5. continue from preserved evidence;
6. record the routing correction.

### Step 9 — Verify

The skill must distinguish:

**route was appropriate**

from

**conclusion was correct**.

A correct answer reached through an invalid or unauditable route is not equivalent to a verified result.

### Step 10 — Learn

Record:

- original route
- route confidence
- route failure, if any
- successful route
- evidence that justified the change
- reusable routing rule

This becomes institutional memory for future routing.

## Compact Decision Logic

```
IF task is simple + low-risk + well-defined
    → R0

ELSE IF question is malformed
    → R3

ELSE IF organizational/process understanding is required
    → R1

IF active failure/incident
    → add R2

IF competing explanations matter
    → add R4

IF evidence/provenance/verification matters
    → add R5

IF specialized domain controls dominate
    → add R6

IF the task evaluates the reasoning apparatus itself
    → R7

IF authority/consequence exceeds system authority
    → R8
```

## Anti-Patterns

Never:

- route by keyword alone;
- assume the user's first framing is the root problem;
- use the most sophisticated harness by default;
- equate multiple models agreeing with verification;
- let routing confidence substitute for evidence;
- continue a failed route merely because work has already been invested;
- silently change routes;
- conceal routing failures.

## Output

Return a concise routing record:

```yaml
route:
  primary: <R0-R8>
  secondary: []
confidence: <HIGH|MEDIUM|LOW|UNKNOWN>
objective: <normalized objective>
reason: <routing rationale>
evidence_standard: <standard>
escalation: <condition or NONE>
next_action: <first action>
```

## Success Criterion

The skill succeeds when:

1. the selected apparatus matches the actual problem;
2. the evidence standard matches the consequence of error;
3. the route can be verified;
4. route failure is detectable;
5. re-routing preserves useful work;
6. successful routing rules become reusable knowledge.

## Core Invariant

> **Do not merely solve the task. Ensure that the method used to solve the task was appropriate, sufficient, auditable, and capable of correcting itself.**
