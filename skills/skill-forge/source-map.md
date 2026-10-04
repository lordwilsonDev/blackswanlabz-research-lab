# Source map for skill-forge

Sources: **EXO** = the building-an-exo package v1.5.0 as observed 2026-10-04 (`third-party/building-an-exo/`); **SC** = the skill-creator SKILL.md and `quick_validate.py` as installed in the session; **LAB** = BlackSwanLabz `AGENTS.md` and the FreeBuff v1.1 question blueprint; **ME** = the skill author.

| Directive | Source locator | Status | Note |
|---|---|---|---|
| D-01 | LAB AGENTS.md rules 1-2 (claims need a recorded status); EXO config.toml + SKILL.md Attribution (rights stated in two places) | AUTHOR-ADDITION | Intake step is ours; motivated by the EXO observation. |
| D-02 | EXO config.toml `license = "MIT"` with no LICENSE file; EXO SKILL.md Attribution ("authors' intellectual property") | AUTHOR-ADDITION | Fail-closed rule is ours. |
| D-03 | EXO SKILL.md Attribution section (full contributor list) | AUTHOR-ADDITION | Example of correct credit; the rule is ours. |
| D-04 | ME | AUTHOR-ADDITION | Not checked against any legal source. |
| D-05 | LAB FreeBuff v1.1 Part Ω0 (axioms registered with IDs) | AUTHOR-ADDITION | Pattern borrowed from the lab's own ID discipline. |
| D-06 | LAB AGENTS.md rules 2-3 (pending is not verified; claims keep status) | AUTHOR-ADDITION | Status vocabulary is ours. |
| D-07 | SC scripts/quick_validate.py (ALLOWED_PROPERTIES, 64-char name, 1024-char description, no angle brackets); EXO frontmatter failing that script | SOURCE-CLAIM | Colon-in-description rule is from running the validator on EXO (invalid YAML at char 1008). |
| D-08 | SC SKILL.md "Write the SKILL.md" (description is the triggering mechanism; be a little pushy) | SOURCE-CLAIM | Near-miss exclusions: SC "Description Optimization". |
| D-09 | SC SKILL.md "Progressive Disclosure" (SKILL.md under 500 lines; point to references) | SOURCE-CLAIM | 800-line hard stop is ours. |
| D-10 | SC SKILL.md "Writing Style" (explain why; ALWAYS/NEVER in caps is a yellow flag); EXO uses MUST 68 times | SOURCE-CLAIM | |
| D-11 | LAB FreeBuff v1.1 Part M (checks must be exercised; a test that cannot fail is not evidence) | AUTHOR-ADDITION | |
| D-12 | LAB FreeBuff v1.1 Part Ω3.2 (patch/minor/major and invalidation set); EXO SKILL.md Changelog | AUTHOR-ADDITION | |
| D-13 | LAB FreeBuff v1.1 Part A11, I14 (kill criteria, staleness); PZS `verify_by` | AUTHOR-ADDITION | |
| D-14 | EXO traces/*.jsonl contain real project context; SC "Principle of Lack of Surprise" | AUTHOR-ADDITION | |
| D-15 | SC SKILL.md "Test Cases" and "Running and evaluating test cases" | SOURCE-CLAIM | |
| D-16 | SC SKILL.md "Principle of Lack of Surprise" | SOURCE-CLAIM | |
| D-17 | SC SKILL.md "Updating an existing skill" (preserve name; copy before editing) | SOURCE-CLAIM | |
