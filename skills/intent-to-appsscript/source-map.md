# Source map for intent-to-appsscript

Sources: **V1** = the v0.1.0 package's SKILL.md and references (BlackSwanLabz), cited by section. **GD** = Google Apps Script documentation, fetched 2026-10-24 (see `references/OFFICIAL_APPS_SCRIPT.md`). **SC** = the skill-creator platform validator. **REV** = the v0.2.0 to v0.4.0 revisions. **OWNER** = the lab owner's direction in this session on 2026-10-25: "make it so that the user and the AI work through it; we're giving the baseline of what they need, but everyone's situation is different."

| Directive | Source locator | Status | Note |
|---|---|---|---|
| D-01 | V1 SKILL.md, "Scope and routing" | SOURCE-CLAIM | |
| D-02 | V1 SKILL.md, "Construction flow" step 0; "Scope and routing" (no new automation if covered) | SOURCE-CLAIM | |
| D-03 | V1 SKILL.md, "Mission" and "Scope and routing" (do not invoke an LLM for deterministic work) | SOURCE-CLAIM | |
| D-04 | V1 SKILL.md, "Contract from natural language" | SOURCE-CLAIM | v0.2 enforces the split with separate fields. |
| D-05 | V1 SKILL.md, "Construction flow" step 2; "Hard safety / acceptance gates" | SOURCE-CLAIM | |
| D-06 | V1 SKILL.md, "Construction flow" step 4 | SOURCE-CLAIM | |
| D-07 | V1 SKILL.md, "Construction flow" step 5 | SOURCE-CLAIM | |
| D-08 | V1 SKILL.md, "Hard safety / acceptance gates"; GD scopes page ("narrowest scopes possible") | SOURCE-CLAIM | |
| D-09 | V1 SKILL.md, "Hard safety / acceptance gates" and "MoIE distinct passes" (security) | SOURCE-CLAIM | |
| D-10 | V1 SKILL.md, "Hard safety / acceptance gates"; GD triggers pages | SOURCE-CLAIM | Rechecked 2026-10-24 from page summaries; see reference. |
| D-11 | V1 SKILL.md, "Hard safety / acceptance gates" (statuses, VERIFIED needs a real run) | SOURCE-CLAIM | v0.1's gate accepted any non-empty receipt string; REV closes that. |
| D-12 | V1 SKILL.md, "Mission" and "Construction flow" step 7 | SOURCE-CLAIM | |
| D-13 | V1 SKILL.md, "AIL: Invert hidden assumptions" | SOURCE-CLAIM | Moved to `references/inversions-and-passes.md`. |
| D-14 | V1 SKILL.md, "Beginner script" | SOURCE-CLAIM | |
| D-15 | V1 SKILL.md, "Existing BlackSwanLabz integration" | SOURCE-CLAIM | |
| D-16 | REV: receipt validation design and the lab's "pending is not verified" rule | AUTHOR-ADDITION | A self-reported receipt is not proof; stated so no one over-trusts it. |
| D-17 | V1 references/OFFICIAL_APPS_SCRIPT.md ("quotas can change, so recheck at deployment") | SOURCE-CLAIM | |
| D-18 | V1 SKILL.md, "Mission" (rollback procedure) and "MoIE distinct passes" (cybernetics: desired outcome, measurement, stop switch) | SOURCE-CLAIM | v0.1 promised both but the contract had no field for either; v0.3 adds them. |
| D-19 | REV: found by AIL review (inversion of "a PASS receipt means it ran for real"); V1 references/WHY_THE_PROPERTIES.md three levels of certainty | AUTHOR-ADDITION | |
| D-20 | OWNER (the user and the AI work through it); V1 SKILL.md "Hard safety / acceptance gates" (no inferred authorization) | AUTHOR-ADDITION | Enforced in the validator: `decided_by` must be a user value. |
| D-21 | OWNER (a baseline, but everyone's situation is different); REV contract split into baseline and situational fields | AUTHOR-ADDITION | Waivers need a real reason; idempotency and audit_log cannot be waived when the action reaches outward. |
| D-22 | OWNER; V1 SKILL.md "Teaching expert" pass and "Beginner script" | AUTHOR-ADDITION | |
| D-23 | V1 SKILL.md "Contract from natural language" ("missing critical facts"; "do not fabricate") | SOURCE-CLAIM | |
