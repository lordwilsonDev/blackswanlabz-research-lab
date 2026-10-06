# Workforce Grant Readiness Skill

## Purpose

Convert BlackSwanLabz research, curriculum, skills, harnesses, employer evidence, and worker outcomes into a defensible workforce-grant application package.

This skill is a governance and evidence skill, not a grant-writing shortcut.

## Core invariant

Employer Need -> Occupational Need -> Skills Gap -> Training Intervention -> Demonstrated Competency -> Employment / Retention / Advancement -> Wage / Productivity Outcome -> Employer Economic Impact -> Persistent Workforce Capacity

A missing link is an evidence gap, not an invitation to invent a claim.

## Operating modes

### 1. DISCOVER
Identify the current funding program, applicant/employer/trainee eligibility, occupational classification, employer commitments, match, eligible costs, outcomes, rubric, and deadline. Never rely on memory for current funding rules; retrieve authoritative program documents first.

### 2. EVIDENCE
Build separate evidence records for employer demand, occupational demand, regional/state demand, skills gap, trainee eligibility, baseline/target wages, placement, retention, advancement, credentials, employer commitment, match, curriculum, competency assessments, and capacity building.

Evidence states: VERIFIED | SUPPORTED | PROVISIONAL | INFERRED | UNKNOWN | CONTRADICTED.

Never silently promote PROVISIONAL, INFERRED, or UNKNOWN into verified evidence.

### 3. OCCUPATION MAP
Map the actual worker function to an established occupational classification. Record employer title, actual duties, classification/SOC when applicable, rationale, competencies, wage source, and evidence state. Do not invent occupational categories merely because BlackSwanLabz uses a novel internal title.

### 4. TRAINING MAP
For each module define occupational competency, objective, practice task, assessment, passing rule, employer application, evidence artifact, and transfer/holdout test. BlackSwanLabz L1-L10 is a capability framework, not an occupational classification.

### 5. OUTCOME MAP
For each trainee/cohort define starting status, starting wage when available, target function, target wage, completion, placement, retention, advancement, credential target, measurement source/date, and evidence state. Never fabricate wages, placements, retention, or commitments.

### 6. EMPLOYER COMMITMENT
Require explicit employer evidence for Wisconsin presence when required, named trainee population, documented skills need, hiring/retention/advancement/wage/hours commitment, match contribution, and post-training use of competency. General statements such as AI is important are not employer commitments.

### 7. RUBRIC
Score independently from eligibility. Default WFF-aligned internal mirror: Project Need 10; Economic Impact 10; Training Objectives & Outcomes 20; Training Program Design, Cost & Implementation 20; Capacity Building 20; Equity & Economic Opportunity Enhancements 20. Total 100. Mandatory eligibility failure is BLOCKED, not a low score.

### 8. ADVERSARIAL REVIEW
Attack applicant eligibility, employer commitment, employer-specific need, occupational mapping, wage sourcing, trainee eligibility, new/customized training, worker competency acquisition, objective assessment, measurable outcomes, match, budget, capacity-building claims, equity claims, and every central evaluator-facing claim. Any unresolved contradiction blocks readiness.

## Anti-consulting rule
A funded activity counts as training only when a worker acquires and demonstrates an occupationally relevant competency. Client strategy, implementation, research, or automation work without worker capability development must not be relabeled as training.

## Decision states
DISCOVERY; EVIDENCE_COLLECTION; ELIGIBILITY_CHECK; EMPLOYER_VALIDATION; OCCUPATIONAL_MAPPING; CURRICULUM_MAPPING; OUTCOME_MODEL; BUDGET_MATCH; RUBRIC_SCORING; ADVERSARIAL_REVIEW; GRANT_READY; GRANT_READY_PARTNER_REQUIRED; BLOCKED_ELIGIBILITY; BLOCKED_EVIDENCE; BLOCKED_EMPLOYER; BLOCKED_FUNDING; DO_NOT_APPLY.

## Harness
Run: python3 scripts/workforce_grant_harness.py scripts/fixtures/workforce_grant_case.example.json. The harness must remain deterministic and must not infer missing facts.

## Research-to-workforce loop
Employer Problem -> Question -> Research -> Skill -> Training -> Assessment -> Worker Capability -> Employer Outcome -> Evidence -> Capability Extraction -> Reusable Skill/Harness -> Curriculum Update

## North-star metric
Verified Workforce Capability Produced. Count only competencies explicitly defined, trained, assessed, passed, and demonstrated in an occupational or employer-relevant context.

## Evidence discipline
Prefer: official program rules/solicitation; employer-signed evidence; authoritative labor-market data; documented training records; independently reproducible assessment results; secondary sources; model-generated inference. Model inference identifies what needs verification; it cannot substitute for required evidence.

## Failure principle
NOT_READY != FAIL. BLOCKED = mandatory condition fails. NOT_READY = more evidence/improvement needed. GRANT_READY_PARTNER_REQUIRED = structurally viable but current applicant cannot independently satisfy a required condition. GRANT_READY = mandatory gates, evidence, score, and adversarial review pass.

## Output contract
Produce or update: eligibility matrix; employer-demand evidence ledger; occupational mapping; trainee eligibility matrix; competency/training map; wage/outcome model; employer commitment matrix; budget/match model; rubric score; adversarial findings; readiness state; unresolved evidence list.

Never present a polished application as ready when the evidence system says otherwise.
