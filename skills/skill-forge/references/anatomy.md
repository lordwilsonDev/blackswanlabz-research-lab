# Anatomy of a knowledge-encoding skill

Read this when deciding what goes where. The shape below is derived from a real framework skill (see `case-study-building-an-exo.md`) and from skill-creator's guidance on progressive disclosure.

## Contents
1. The parts and when each earns its place
2. Sizing rules
3. What to leave out

## 1. The parts

| Part | Holds | Add it when |
|---|---|---|
| `SKILL.md` | Frontmatter, Attribution, when to use, workflow, Core Directives, Validation Checkpoints, References, Not covered, Changelog | always |
| `references/*.md` | Depth: the source's frameworks, evidence, worked cases, vocabulary | a topic needs more than a few paragraphs, or only some tasks need it |
| `templates/*.md` | Fill-in artifacts the user completes (scorecards, specs, canvases) | the source defines an artifact people produce |
| `source-map.md` | Directive ID, source locator, status, note | always (this is the fidelity mechanism) |
| `config.toml` | Version, maintainer, license, source terms, redistribution, review_by | always |
| `intake.md` | The rights and scope record from step 1 | always |
| `schema.json` | Input and output shape, when a program or pipeline calls the skill | the skill is invoked by code and needs a stable contract |
| `evals/` | Trigger queries, task prompts, `results.md` | always for release |
| `traces/` | Records of past use | only if opt-in and free of personal or client data |
| `scripts/` | Deterministic helpers | the same code would otherwise be rewritten each run |

## 2. Sizing rules

- SKILL.md: 500 lines or fewer. It is loaded whenever the skill triggers, so every line costs every use.
- Reference files over about 300 lines get a table of contents.
- Every reference and template is named in SKILL.md with a "read this when" cue. The validator fails a file nobody points to.
- Description: 1024 characters at most. It is always in context.

## 3. What to leave out

- Trigger lists in frontmatter. The platform allows only name, description, license, allowed-tools, metadata and compatibility; put the phrases that matter inside the description.
- A long version-by-version narrative in SKILL.md. Put the summary in the Changelog and the detail in a reference file if it is worth keeping.
- Anything that is the skill author's opinion presented as the source's. It belongs in `source-map.md` with status `AUTHOR-ADDITION`, or nowhere.
