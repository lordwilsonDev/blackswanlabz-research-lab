---
source: curated index of existing BlackSwanLabz repository resources
captured: 2026-10-12
status: active
---

# BlackSwanLabz — Agent & Operator Resource Directory

**Purpose:** A navigational entry point for people and AI agents using the existing lab methods to discover requirements, choose skills, define procedures, propose measurements, and operate a governed feedback loop. This index links to source documents; it does not replace them or imply that designs are executable.

## Start here (for Claude Code, Codex, and other repository-reading agents)

1. Read [README](../README.md), [AGENTS.md](../AGENTS.md), [llms.txt](../llms.txt), and [CLAIMS.md](../CLAIMS.md). Follow the full reading order and the evidence rules.
2. Read the [50-Question OS Bootstrap](../08-operations/50-question-os-bootstrap-v1.md). Ask its questions **one at a time**; record YES, NO, or UNKNOWN as appropriate. Do not invent missing facts.
3. Inspect [People-Centered Research Operating System](../08-operations/black-swan-labs-research-group.md) for the owner-intent compiler, research operating loops, authority, and people model.
4. Use [Question Engineering](../04-papers/epistemic-state-transition-question-engineering.md), [AIL](../02-frameworks/axiom-inversion-logic.md), and [MoIE](../02-frameworks/moie.md) to clarify assumptions and test alternatives. Inversion generates hypotheses, not proof.
5. Discover and inspect **actual available skills** before invoking them. Match the capability to the task and check execution prerequisites; do not assume that a design registry is an installed skill.
6. Compile the answers into: confirmed state, uncertainties, dependencies, required roles and SOPs, proposed KPIs and OKRs, relevant available skills/harnesses, approval gates, and the smallest justified next task.
7. Obtain human authorization for consequential actions. Execute only within accessible tools and permissions. Verify results, measure outcomes, record failures, and use feedback to determine the next question or improvement.

**Suggested instruction to the agent:** “Read the BlackSwanLabz repository instructions and this resource directory. Inspect the actual available skills and harnesses, then start the 50-Question OS Bootstrap at Question 1. Ask one question at a time. Do not build replacement infrastructure before inspecting what already exists.”

## Resource map

| Area | Authoritative resource | What it supplies |
| --- | --- | --- |
| Agent instructions | [AGENTS.md](../AGENTS.md), [llms.txt](../llms.txt) | Repository navigation, claims discipline, absence-check rules |
| Use with your own AI | [Use BlackSwanLabz With Your Own AI](using-with-your-ai.md) | Quick start, a copy-paste agent instruction, the closed-loop method, completion criteria |
| Onboarding skill | [blackswanlabz-onboarding](../skills/blackswanlabz-onboarding/SKILL.md) | The whole onboarding as one runnable procedure: discover, 50 questions, scope from the lab |
| User onboarding | [50-Question OS Bootstrap](../08-operations/50-question-os-bootstrap-v1.md) | One-question-at-a-time intent and capability discovery; **pending** bootstrap interface |
| Owner intent and people | [People-Centered Research Operating System](../08-operations/black-swan-labs-research-group.md) | Intent compiler, people operations, research relief, quality, governance; design/implementation blueprint |
| Question methodology | [Epistemic State Transition: Question Engineering](../04-papers/epistemic-state-transition-question-engineering.md) | Question engineering research framework; paper, not a deployed result |
| Question-purpose meta-skill | [Why the Trainer Asks the Question](../skills/workforce-grant-readiness-meta/SKILL.md) | Question → purpose → dependency → evidence → decision → consequence; **workforce-specific**, adapt cautiously |
| Axiom Inversion Logic | [AIL](../02-frameworks/axiom-inversion-logic.md) | Invert assumptions, derive alternatives, specify falsifiers |
| Mixture of Inversion Experts | [MoIE](../02-frameworks/moie.md) | Independent reasoning roles and adversarial hypothesis generation; comparative benchmark not run |
| Skill discovery architecture | [META-HARNESS skill registry](../02-frameworks/meta-harness-skill-registry.md) | Skill families and capability-to-counterpart mapping; **design**, not proof of installed skills |
| Harness improvement | [META-HARNESS](../02-frameworks/meta-harness.md), [Software Factory Harness](../02-frameworks/software-factory-harness.md) | Observe, verify, repair and improve the harness; **designs** |
| Available verification skill | [lab-verify SKILL.md](../.claude/skills/lab-verify/SKILL.md) | Preregister, lock, self-check, run, analyze, report; see skill's executable harness and limitations |
| Available workforce skill | [workforce-grant-readiness SKILL.md](../skills/workforce-grant-readiness/SKILL.md) | Workforce evidence, eligibility, competency and outcome mapping; domain-specific |
| Available workforce harness | [Workforce grant harness](../scripts/workforce-grant-harness.md) | Deterministic preflight and example case |
| Evidence-gated check (external repo) | [AIL CSM Harness skillpack](https://github.com/lordwilsonDev/ail-csm-harness-skillpack) | A 20-step check an AI runs on its own deliverable before release: evidence ledger, unknowns register, release gate. Four worked examples; run on small tasks, not benchmarked |
| Software analysis skill (third party) | [leanrea](https://github.com/aicodeking/leanrea), bundled in that pack under `extras/` | AICodeKing, MIT. Plain command-line reverse engineering of software; use only on software you own or may analyze |
| Skill Foundry (external repo, working preview) | [blackswanlabz-skill-foundry](https://github.com/lordwilsonDev/blackswanlabz-skill-foundry) | A local app that turns a question and authorized sources into a bounded, cited, reviewable skill, teaching plan or second-brain answer, run in an OS sandbox with receipts. Re-tested 2026-10-19: 162 tests pass. Ready for one operator on one machine; enterprise gates are out of scope by design; no independent reviewer has approved any generated skill |
| SOP directory | [Operations index](../08-operations/README.md) | SOP map, status notes, held-back document locations |
| Operating architecture | [North Star Architecture](../08-operations/north-star-architecture.md) | Intelligence → decision → intervention/verification → compounding; measurement discipline |
| Control-loop operations | [North Star FDE Cybernetic Loop](../08-operations/north-star-fde-cybernetic-loop.md) | Feedback, state and operational improvement |
| People-centered HR | [People-Centered Research Operating System](../08-operations/black-swan-labs-research-group.md) §§27–29, 44–45 | Staffing, employee care, relief, people KPIs and quality guardrails |
| Day-to-day business | [Day-to-Day Operating Manual](../08-operations/day-to-day-operating-manual.md) | Workflow signals, employee friction, baselines, exception-first operations; read current-state warning |
| Claim evidence | [CLAIMS.md](../CLAIMS.md), [Experiments index](../05-experiments/README.md), [Proofs](../06-proofs/README.md) | Verified/pending/retracted distinctions and inspectable records |
| Mechanical repository checks | [verify.sh](../scripts/verify.sh), [verify.py](../scripts/verify.py) | Structural verification; not proof of operational outcomes |
| Full-system inspection | [Freebot audit prompt](../docs/prompts/freebot-full-system-audit.md) | Read-only inspection protocol, not a completed audit |

## Skill availability and routing

**Confirmed public skill files in this repository:** `.claude/skills/lab-verify/SKILL.md`, `skills/workforce-grant-readiness/SKILL.md`, and `skills/workforce-grant-readiness-meta/SKILL.md`.

**Referenced local counterparts:** The main README reports a local question-engineering harness with question gate, intent-reality check, and skill router, plus a larger local skill library. These are **not made executable by this index**. Agents with access to the author's local environment should inspect them by function and exact path before deciding what is available.

**Registry caution:** The META-HARNESS registry includes proposed skill names and an unverified functional mapping to local counterparts. Treat it as a discovery guide, not an installation manifest.

Route by need:
- General onboarding → 50-question bootstrap + owner-intent architecture.
- Clarification or contradictory answers → question engineering + linguistic/requirement analysis.
- Alternative assumptions → AIL + MoIE; then independent evidence.
- Workforce grants → workforce skills and deterministic grant harness.
- Experimental claim verification → lab-verify skill and its documented run prerequisites.
- SOP, KPI, OKR and HR design → operations documents + North Star + people model.
- Checking a finished deliverable before release, or taking apart software you own → AIL CSM Harness skillpack (and its leanrea extra).
- Recurring execution failures → meta-harness design and any **actually accessible** matching implementation.

## Closed-loop output contract

For each onboarding or operational cycle, produce a concise record:

1. **Intent and authority:** objective, beneficiary, scope, constraints, owner, approvals.
2. **State and evidence:** confirmed facts, unknowns, contradictions, accessible sources.
3. **Capability map:** exact file/path, availability, trigger, inputs, outputs, tests, dependencies.
4. **Process:** required SOPs, handoffs, exception handling and human safeguards.
5. **Measurement:** proposed KPI definitions, baselines, data sources, owners; proposed OKRs and human approval status.
6. **Action:** next smallest justified step, preconditions, acceptance criteria and stop conditions.
7. **Observation:** what actually ran, what changed, what evidence supports the outcome.
8. **Feedback:** deviation, root-cause hypotheses, corrections, reusable learning, next question.

**Loop:** Intent → Question → State → Plan → Authorize → Execute → Observe → Verify → Measure → Improve → Next Question.

Do not mark a suggested KPI as measured, a drafted SOP as deployed, or a planned harness as tested. Protect employee data and require authorization for HR decisions and production changes.

## Maintenance

Add links to existing source-of-truth files instead of duplicating their content. Update this directory when skills are published, moved, or verified. Preserve the original status banners, follow [AGENTS.md](../AGENTS.md), and check [CLAIMS.md](../CLAIMS.md) before describing outcomes. If a source is held back or local-only, say so. The directory is navigation, **not a new research claim**.
