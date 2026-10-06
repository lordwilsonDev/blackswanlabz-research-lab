---
source: authored in this repository (commit f93c653, 2026-10-03): attributed competitive architecture absorption register; original working location not recorded
captured: 2026-10-03
status: active
version: 1.0
purpose: competitive architecture absorption and attribution
---

# Competitive Architecture Absorption Register v1.0

## Operating rule

BlackSwanLabz does not compete by rebuilding every wheel.

When a public system exposes a useful architectural primitive, the lab:

1. identifies the primitive;
2. verifies what is publicly observable;
3. records provenance and license;
4. maps the primitive to an existing BlackSwanLabz substrate;
5. re-implements the behavior through BlackSwanLabz interfaces;
6. adds local tests and governance;
7. attributes the source.

Architecture is absorbed; source code is not copied unless its license and attribution requirements permit it.

For unlicensed projects, only independently re-derived ideas/patterns are considered; no source-code reuse.

## 1. OneManCompany — organizational execution primitives

Source: https://github.com/1mancompany/OneManCompany
License observed: Apache-2.0.

Publicly described primitives include a unified runtime, hierarchical agents, task scheduling, retries/fault tolerance, multi-agent meetings, hiring/onboarding, 1-on-1 coaching, performance reviews, task versioning, cost accounting, and Vessel/Talent separation.

### Absorb

**A1 — Vessel / Talent separation**

Separate execution substrate, worker identity, role, skill set, and task assignment.

Mapping:
MSB execution substrate -> Agent/Role/Skill registry -> governed task.

**A2 — Persistent coaching ledger**

COACHING_EVENT -> BEHAVIOR_CHANGE -> NEXT_TASK_TEST -> RETAINED/PENDING.

**A3 — Agent performance review**

Use evidence-backed review records covering work completed, verification yield, defect rate, rework, transfer performance, policy violations, useful capability created, and unresolved limitations.

**A4 — Multi-agent meeting protocol**

Meetings become structured artifacts containing purpose, participants, claims, disagreements, decisions, action owners, evidence, and unresolved questions.

**A5 — Cost ledger**

Track model, tokens where available, tool calls, human interventions, external services, elapsed time, direct cash cost, and setup cost at task/project level.

**A6 — Retrospective -> workflow compiler**

REPEATED WORK -> RETROSPECTIVE -> PATTERN -> SKILL/HARNESS -> TEST -> REUSE.

## 2. OPOS — Git-native company operating primitives

Source: https://github.com/Koroqe/OPOS
License observed: MIT.

Publicly described primitives include the company as a Git repository, department/role/policy files, a chief-of-staff steward, parallel workstreams, a graduated permission ladder, Copier scaffolding, and a setup skill.

### Absorb

**B1 — Organization-as-repository contract**

MISSION / VALUES / POLICIES / ROLES / DEPARTMENTS / WORK / DECISIONS are represented as versioned files.

**B2 — Department charter schema**

Each department gets mission, authority, inputs, outputs, owner, tools, skills, permissions, KPIs, failure modes, and escalation rules.

**B3 — Chief-of-staff workstream steward**

Registers active workstreams, prevents ambiguous ownership, routes tasks, tracks blocked/paused/resumed state, and preserves current-task state.

**B4 — Graduated permission ladder**

AUTO -> NOTICE -> CONFIRM -> EXPLICIT APPROVAL -> HARD REFUSE.

**B5 — Parallel workstream registry**

Every concurrent workstream receives an ID, owner, objective, task reference, current state, dependencies, next action, and blocking authority.

**B6 — CORE/STARTER separation**

Separate reusable institutional primitives from organization-specific content so the operating system can be instantiated repeatedly.

## 3. Robin / FutureHouse — specialized research primitives

Source: https://github.com/Future-House/robin
License observed: Apache-2.0 for the repository.

Publicly described primitives include specialized literature agents, a scientific data-analysis agent, continuous hypothesis/experiment/data-analysis feedback, ablation experiments, blinded human reference checking, and statistical comparison.

### Absorb

**C1 — Specialized research lanes**

Define explicit interfaces for concise literature discovery, deep literature synthesis, evidence extraction, data analysis, experiment interpretation, hypothesis generation, and adversarial critique.

**C2 — Continuous hypothesis loop**

QUESTION -> LITERATURE -> HYPOTHESIS -> EXPERIMENT -> DATA -> ANALYSIS -> UPDATED HYPOTHESIS.

**C3 — Agent ablation harness**

Compare FULL SYSTEM vs ABLATED SYSTEM under a prespecified metric when a specialist's contribution is consequential.

**C4 — Blinded reference verification**

Where practical, separate system-generated results from evaluator identity/source identity.

**C5 — Statistical comparison primitive**

For appropriate repeated comparisons, freeze the metric and null hypothesis, preserve raw observations, and use permutation/randomization testing where assumptions fit.

## 4. PHOBOS — multimodal/local capability pattern

Source: https://github.com/armyofbear136/PHOBOS
License observed: no standard open-source license identified in public repository metadata.

No PHOBOS source code is copied.

The independently re-derived architectural patterns are local/self-hosted execution, broad modality adapters, task queues, production-oriented tool integration, skills as capability modules, and heterogeneous workers.

### Absorb

**D1 — Modality capability registry**

Each tool/worker records modality, capability, local/remote status, prerequisites, cost, data boundary, verification, failure class, and owner.

**D2 — Tool-class capability routing**

Route tasks by required capability/modality rather than model brand.

**D3 — Governed production capability queue**

Use one governed queue for research, coding, media, analysis, documentation, and verification.

## 5. Integrated BlackSwanLabz target

OWNER INTENT
-> CHIEF-OF-STAFF / WORKSTREAM STEWARD
-> QUESTION ENGINE
-> DEPARTMENT / RESEARCH LANE
-> SPECIALIZED AGENT / SKILL / HARNESS
-> VESSEL + TALENT
-> MSB GOVERNED EXECUTION
-> EVIDENCE + COST + DECISION RECEIPT
-> VERIFICATION
-> ABLATION / ADVERSARIAL TEST
-> HUMAN DECISION
-> CAPABILITY EXTRACTION
-> COACHING / RETROSPECTIVE
-> SKILL/HARNESS UPDATE
-> PERSISTENT MEMORY
-> NEXT WORKSTREAM

## 6. Attribution and licensing

Architectural inspiration is attributed at the primitive level.

This register does not claim that the source projects invented every underlying concept independently. It records the public implementation pattern that informed the BlackSwanLabz absorption.

Sources:
- OneManCompany — https://github.com/1mancompany/OneManCompany
- OPOS — https://github.com/Koroqe/OPOS
- Robin / FutureHouse — https://github.com/Future-House/robin
- PHOBOS — https://github.com/armyofbear136/PHOBOS

Observed licenses:
- OneManCompany: Apache-2.0
- OPOS: MIT
- Robin repository: Apache-2.0
- PHOBOS: no standard open-source license observed in public repository metadata

Published papers/documentation may carry different terms from repository code. Use the applicable license for each artifact.

## 7. Non-negotiable absorption gate

PROPOSED
-> IMPLEMENTED
-> TESTED
-> VERIFIED
-> REUSABLE
-> PROMOTED

Competitor documentation establishes that a competitor claims a capability. It does not establish that the same capability works in BlackSwanlabz.

The BlackSwanlabz implementation must establish its own evidence.

## 8. Strategic rule

observe -> abstract -> attribute -> re-implement -> test -> integrate -> improve

The external ecosystem becomes an architecture-discovery feed while BlackSwanlabz governance, evidence, memory, verification, and intent-fidelity rules remain the controlling substrate.
