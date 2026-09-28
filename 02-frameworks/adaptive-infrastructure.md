---
source: ~/projects/AI-Agents/msb-v3/docs/blueprints/2026-08-11-adaptive-build-environment.md
repo: lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE
commit: 765979bda8b7fb5be123261578fdd4cf0d943c53
captured: 2026-09-28
status: active
---

# Adaptive Infrastructure

## The thesis: the system owns the workflow, the model is a swappable worker

A vault architecture note on msb-v3's "Meta-System" states the core thesis directly:

> "the system, not the model, owns the intelligence of the workflow; the model is an interchangeable worker."

The design keeps three levels of intelligence separate: **Strategic** (human / architect / meta-planner — what are we building) → **Translation** (how to express this so *this* worker can execute it) → **Execution** (the model — what action right now). Stated invariants include: the project plan, tasks, and task language are model-independent; models receive translated tasks, never raw project intent; models never define completion — verification does; a model can be swapped without rewriting the project plan; and project memory lives outside the model's context.

## Meta-System

The proposed net-new subsystems that carry this thesis include:

- **MSL** — a formal, model-independent task language and schema, one artifact per task.
- **Context Compiler** — a relevance-scoring pipeline meant to reduce a large codebase to a small set of high-signal tokens for a given task.
- **Failure Compiler** — turns a structured execution failure into a diagnosis and a repair task, rather than a raw error.
- **Recursive decomposition** — a task may be broken down further whenever its estimated complexity exceeds the assigned worker's capacity.

A vault note reports a small-model scoreboard from early Meta-System runs: across three runs, qwen3:8b (a local 8B model, run by hand through the driver) got 8 of 9 delegated functions correct (7 on the first pass), with the two misses attributed to one task that needed escalation past an 8B-class model and one case where the model's own code was correct but the run's driver assembled it without its dependencies. This is an author-reported figure from a vault note, not a run record held in this lab — tracked as [C-028](../CLAIMS.md), status pending. (Qwen 3B is a separate, smaller hypothesized target named in the thesis statement below, not the model actually run in this scoreboard.)

The same vault note records a later, single-job test of the amplification thesis directly: neither qwen3:8b nor a second small model (Qwen2.5-Coder-1.5B) passed a real, well-specified job under the same harness, each failing all 3 of 3 attempts, while the strong model passed 1 of 1 direct. The note states the conclusion plainly: "the burden of proof the assessment doc set (does cheap-model-plus-harness beat strong-model-direct?) was not met here, on either candidate model." This is tracked as [C-029](../CLAIMS.md), status pending — the 8/9 scoreboard above covers small, decomposed functions built by hand through the driver; this later test is one real job, end to end, and its result was negative.

## Generate → verify: the research loop and audit chain

The public [blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE](https://github.com/lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE) repository splits AIL+MoIE into two halves — one that generates, one that verifies:

- **`ail_research_loop/`** — the generation half: problem → AIL assumptions → inversion → MoIE competing mechanisms → hypothesis → preregistered prediction → experiment → evidence → JEV routing → updated theory → re-entry.
- **`ail_audit_chain/`** — the verification half: a "Composable Skill Mesh" of ordered audit skills that decomposes a task, gathers evidence, tests claims, exposes omissions, and assembles only what passes. Its own stated core rule: "The model proposes; source material and tests decide," and a citation is not validation unless "the source must exist *and* support the exact claim."

Output moves from the research loop into the audit chain before release. The audit chain's release gates move through named stages — `DRAFT` → `EVIDENCE-CHECKED` → `CALCULATION-CHECKED` → `ADVERSARIAL-REVIEWED` → `FINAL-READY`, or `BLOCKED` — and the repo states plainly: "Nothing is called 'proven,' 'court-ready,' or 'publication-ready' unless that external review has actually happened."

## Open

The repository documents its own unresolved inconsistency between two descriptions of the research loop's state machine. `ail_research_loop/spec.md` defines 12 non-exceptional states plus 3 exceptional states (`BLOCKED`, `FAILED_EXECUTION`, `INVALIDATED`); the repo's own `execution-plan.md` separately describes a different, finer-grained 15-state machine that makes the AIL and MoIE steps explicit states in their own right. The `ail_research_loop/README.md` records this directly:

> "**Known inconsistency:** `execution-plan.md` ('State machine') lists a different, finer-grained set of 15 states (`INTAKE`, `ASSUMPTIONS`, `INVERSION`, `MECHANISMS`, …, `ARCHIVED`) that makes the AIL and MoIE steps explicit states. The spec and code do not yet have those states; AIL and MoIE happen inside `PROBLEM_DEFINED → HYPOTHESIS_FORMED`. Reconciling the two is open work."

## Sources

- `~/projects/AI-Agents/msb-v3/docs/blueprints/2026-08-11-adaptive-build-environment.md`
- `~/Documents/Vault/10_Projects/msb-v3/MSB-v3.md` (section "Meta-System: Project Compiler above the Kernel")
- `https://github.com/lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE` (root `README.md`, `ail_research_loop/README.md`, `ail_audit_chain/README.md`) at commit `765979bda8b7fb5be123261578fdd4cf0d943c53`
