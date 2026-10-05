---
source: owner-supplied package (The_BAD_IDEA1.zip, uploaded 2026-10-05); body unchanged, front matter added
captured: 2026-10-05
status: pending
---

# Domain-Crossing & Domain-Depth Benchmark v1.0

## Purpose

Measure two things separately:

1. **Breadth:** how many distinct domains the work substantively entered.
2. **Depth:** how far the work progressed inside each domain.

The benchmark is designed for a human-readable and scientific reporting pair. Both lanes must resolve to the same structured ledger.

> **Do not count a domain because it was mentioned. Count it only when the evidence shows substantive engagement.**

## Core Metrics

### Verified Domain Count

A domain counts as **verified breadth** at Level 2 or higher.

`D = count(domains where max_level >= 2 and status != REJECTED)`

Additional reporting buckets:

- `D2+` = domains substantively entered
- `D4+` = source-grounded domains
- `D6+` = domains with a domain-specific artifact
- `D7+` = domains with executed validation
- `D8+` = domains with adversarial/falsification testing
- `D9+` = domains with fresh-run reconstruction
- `D10` = domains with public-record empirical testing

### Depth

For each domain `d`, record one maximum validated level `L(d)` from 0–10.

`Total Depth Points = Σ L(d)`

`Mean Depth = Σ L(d) / D2+`

Do not use mean depth as a substitute for breadth. A program can be broad but shallow, narrow but deep, or both.

### Domain-Depth Equivalents

`DDE = Σ (L(d) / 10)`

This is a derived communication metric, not a scientific claim. It expresses the portfolio as an equivalent number of fully deep domains.

Example: four L10 domains = `4.0 DDE`; ten L5 domains = `5.0 DDE`.

### Velocity

Let `T` be elapsed research time in days from the benchmark start date to the benchmark cutoff.

`Domain Velocity = D2+ / T`

`Depth Velocity = Total Depth Points / T`

Also report:

`L10 Velocity = D10 / T`

Never report velocity without the date window.

---

# The 10-Level Depth Ladder

## Level 1 — Encountered

The domain is encountered or correctly identified.

Required evidence:

- a domain-specific artifact, question, source, or task;
- enough context to show the domain was not merely named in passing.

Not enough:

- a random word in a document;
- a generic reference with no substantive interaction.

## Level 2 — Domain Question

A domain-specific question or problem is explicitly formulated.

Required evidence:

- domain-specific referent;
- concrete proposition/problem;
- scope and desired outcome.

This is the minimum level for counting breadth.

## Level 3 — Domain Framing

The work identifies domain-specific concepts, rules, constraints, variables, or failure conditions.

Required evidence:

- domain vocabulary used correctly;
- relevant constraints or governing relationships;
- explicit assumptions or boundaries.

## Level 4 — Public-Source Grounding

The work is grounded in public records, primary sources, public datasets, published standards, or other externally inspectable evidence appropriate to the domain.

Required evidence:

- source references;
- source role;
- provenance connecting source material to the domain claim.

## Level 5 — Structured Domain Analysis

The work performs substantive analysis using domain logic.

Examples:

- quantitative calculation;
- legal/technical framework application;
- structured empirical comparison;
- model construction;
- formal argument analysis.

Required evidence:

- inputs;
- method;
- output;
- domain-specific interpretation.

## Level 6 — Domain Artifact

The work produces a material artifact that belongs to the domain.

Examples:

- mission design;
- proof/verification package;
- executable domain model;
- market analysis;
- security analysis;
- speech/voice pipeline;
- research report with domain-specific computation.

Required evidence:

- artifact identity;
- artifact contents or repository location;
- clear domain relationship.

## Level 7 — Executed Validation

A domain-specific model, calculation, program, or verification procedure is actually executed.

Required evidence:

- execution record;
- inputs/environment;
- output;
- exit status or equivalent result.

A documented command that was never run does not qualify.

## Level 8 — Adversarial / Falsification Test

The work deliberately attempts to break, falsify, mutate, or defeat the domain result or its verification mechanism.

Examples:

- counterexample search;
- mutation testing;
- contradictory evidence;
- boundary-condition attack;
- false-green/false-positive test.

Required evidence:

- attack specification;
- mutation/attack input;
- observed result;
- disposition.

## Level 9 — Reproducible Reconstruction

The material result can be reconstructed from preserved inputs, instructions, and evidence without relying on hidden conversational state.

Required evidence:

- frozen inputs or source references;
- exact method/commands;
- reconstruction run;
- comparison of reconstructed vs original result.

A second assertion by the same author is not enough.

## Level 10 — Public-Record Empirical Test

The work performs an actual empirical test using public records or public datasets as the evidence base, with an explicit research question and an observable result.

Minimum requirements:

- preregistered or frozen question/hypothesis;
- identified public records/dataset;
- defined sample or population;
- executable analysis/test;
- observed result;
- limitations and falsifiers;
- preserved evidence package.

Important distinction:

> **L10 does not automatically mean causal experiment, scientific proof, or universal validity.**

A public-record observational study must be labeled observational; a quasi-experiment must be labeled quasi-experimental; a randomized experiment must meet its own design requirements.

Synthetic data alone cannot qualify for Level 10.

---

# Anti-Inflation Rules

### Rule A — Mention is not breadth

A domain mention with no substantive artifact cannot count above Level 0.

### Rule B — Evidence is local to the level

An L6 artifact does not automatically prove L7 execution.

An L8 attack does not automatically prove L9 reconstruction.

### Rule C — No skipped levels

A domain may only claim Level `n` when all required conditions through `n` are satisfied.

Higher-level evidence may also satisfy lower-level conditions, but those lower-level conditions must still be explicitly checkable.

### Rule D — One domain, one canonical identity

Synonyms and subfields must not inflate breadth.

For example, `network science` and `epidemiology` may be separate only when the ledger's domain taxonomy establishes that they are substantively distinct for the benchmark.

### Rule E — Domain name does not prove depth

A sophisticated title does not establish a high level.

### Rule F — Artifact generation is not execution

A file containing code or calculations is not an executed result.

### Rule G — Execution is not empirical validation

A simulation can qualify for Level 7 or 8 without qualifying for Level 10.

### Rule H — Public source ≠ public experiment

Using a citation at Level 4 does not make the work Level 10.

### Rule I — Correlated observations stay correlated

Repeated observations produced through one discovery path cannot establish independent replication by themselves.

### Rule J — Unknown is a valid result

If the evidence cannot establish a level, record `UNKNOWN` or the highest defensible lower level.

---

# Domain Ledger Schema

```yaml
domain_id: D-001
domain_name: formal_mathematics_verification
status: CANDIDATE | ACTIVE | VERIFIED | REJECTED
max_level: 0-10
level_evidence:
  - level: 4
    evidence_ids: [E-001, E-002]
    verdict: SUPPORTED
    note: "..."
provenance:
  discovery_path: "..."
  primary_artifacts: ["..."]
  independent_observers: ["..."]
  domain_parent: null
  taxonomy_note: "..."
temporal:
  first_entry: 2026-07-14
  latest_evidence: 2026-10-03
```

`max_level` is derived from evidence. It is not an author-entered prestige score.

---

# Benchmark Run Protocol

1. Freeze benchmark start date and cutoff date.
2. Enumerate candidate domains from the complete corpus.
3. Normalize names and merge aliases.
4. Assign stable domain IDs.
5. For each domain, locate evidence for Levels 1–10.
6. Score only the highest level fully satisfied.
7. Run anti-inflation validation.
8. Calculate breadth, depth, DDE, and velocity.
9. Generate the scientific report.
10. Generate the plain-language report from the same ledger.
11. Compare the two reports for semantic agreement.
12. Preserve unresolved domains and missing evidence instead of deleting them.

---

# Scientific Benchmark Output

Required summary:

```text
Benchmark window: START → CUTOFF
Verified domains (L2+): N
Source-grounded domains (L4+): N
Artifact domains (L6+): N
Executed domains (L7+): N
Adversarial domains (L8+): N
Reconstructed domains (L9+): N
Public-record empirical domains (L10): N
Total depth points: N
Mean depth: N
Domain-depth equivalents: N.N
Domain velocity: N/day
Depth velocity: N/day
L10 velocity: N/day
```

Every number must be reproducible from the domain ledger.

# Layperson Benchmark Output

The plain-language version must answer exactly the same underlying questions:

```text
How many different fields did we actually work in?
How deeply did we work in each field?
How many fields reached real source-backed research?
How many produced something that actually ran?
How many were tested to see if they were wrong?
How many could be reproduced?
How many reached real public-record empirical testing?
How long did all of that take?
What is still unproven?
```

The lay report must never introduce a stronger claim than the scientific ledger supports.

---

# Human-Comprehension Test

Give a person only the lay report.

Ask them to recover:

1. verified domain count;
2. number of L7+ domains;
3. number of L10 domains;
4. total elapsed time;
5. the deepest domain(s);
6. one thing that remains unproven.

Score:

`Human Comprehension Fidelity = correct recovered answers / required answers`

The scientific and lay reports have passed the communication-fidelity test only when the numbers and epistemic labels agree.

---

# Research Interpretation Rules

Do not use this benchmark to claim:

- mastery of every counted domain;
- expertise equivalent to professional credentialing;
- causal superiority of the methodology;
- scientific proof merely from breadth or depth;
- universal generalization.

The benchmark measures **documented depth of engagement and evidence production**, not professional licensure or omniscience.

## Terminal Question

> **How many domains did we actually enter, how deeply did we go in each one, how quickly did we move between them, and how much of that work survived execution and evidence checks?**
