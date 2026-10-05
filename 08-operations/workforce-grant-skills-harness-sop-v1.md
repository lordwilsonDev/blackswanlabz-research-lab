# Workforce Grant Skills and Harness SOP v1

## Skill SOP
When creating or modifying a workforce skill:
1. State purpose and invariant.
2. Define inputs and evidence states.
3. Define operating modes.
4. Define decision states.
5. Define failure semantics.
6. Define anti-gaming and anti-consulting rules.
7. Define required outputs.
8. Connect the skill to the Meta-Skill.
9. Connect mechanically testable rules to the harness.
10. Add adversarial tests.
11. Validate.
12. Commit and record the result.

A skill is complete only when:
instruction -> execution path -> evidence -> test -> failure semantics.

## Training skill construction
For every proposed skill:
1. Define the occupational behavior.
2. Define the worker baseline.
3. Define the target behavior.
4. Create a realistic task.
5. Define constraints.
6. Define assessment.
7. Define deterministic pass criteria where possible.
8. Add a novel holdout.
9. Test employer transfer.
10. Preserve the evidence artifact.

Capability progression:
Taught -> Practiced -> Tested -> Passed -> Held-out -> Transferred -> Verified

## Harness SOP
The harness is a mechanical boundary. It must:
- consume structured case data;
- apply explicit rules;
- report missing mandatory gates;
- preserve unknowns;
- report contradictions;
- calculate scores deterministically;
- never infer missing facts;
- never rewrite evidence;
- never tune rules after seeing outcomes.

Mandatory gates:
eligible applicant; eligible employer; documented employer need; eligible trainees; occupational mapping; required match; customized occupational training; measurable outcomes; required employer commitments.

States:
BLOCKED = mandatory failure or fatal contradiction.
NOT_READY = no mandatory failure, but evidence or score is insufficient.
GRANT_READY_PARTNER_REQUIRED = structurally viable but a partner is required for an unmet condition.
GRANT_READY = gates, evidence, score, and adversarial review pass.

NOT_READY is not FAIL.

## Harness test protocol
For every harness change:
1. Run the example fixture.
2. Test every gate with a positive case.
3. Test every gate with a negative case.
4. Test unknown fields.
5. Test contradictions.
6. Test rubric boundaries.
7. Test threshold behavior.
8. Test deterministic repeatability.
9. Confirm exit codes.
10. Confirm no inference from missing data.
11. Confirm machine-readable output.
12. Run repository tests and static checks.
13. Record results.

Minimum matrix:
- all gates false -> BLOCKED
- one gate false -> BLOCKED
- unknown gate -> never silently true
- contradiction -> BLOCKED
- score below threshold -> NOT_READY
- score above threshold with unresolved evidence -> not GRANT_READY
- complete passing case -> GRANT_READY
- identical input repeated -> identical output

## Required case artifacts
A mature case should contain:
eligibility matrix; employer-demand ledger; occupational mapping; trainee matrix; skills-gap baseline; competency map; training map; assessment specification; holdout/transfer tests; wage/outcome model; employer commitments; equity plan; capacity plan; budget/match model; provenance ledger; rubric score; MoIE report; contradiction register; adversarial findings; harness output; readiness decision; unresolved evidence list; post-training outcome; capability extraction.

## Research-to-workforce loop
Employer Problem -> Question -> Research -> Experiment -> Skill -> Training -> Assessment -> Worker Capability -> Employer Outcome -> Evidence -> Capability Extraction -> Reusable Skill -> Reusable Harness -> Curriculum Update

## Final gate
GRANT_READY requires eligibility, employer need, occupational mapping, measurable skills gap, customized occupational training, objective competency assessment, employer pathway, outcome measurement, sourced wage claims, defensible budget/match, evidence-backed equity and capacity claims, resolved contradictions, completed adversarial review, passing harness, rubric threshold, and required human review.

Otherwise remain BLOCKED, NOT_READY, or GRANT_READY_PARTNER_REQUIRED.
