---
name: skill-forge
description: Turn a book, framework, blueprint, SOP, or research corpus into a faithful, attributed, validated Claude skill package (SKILL.md plus references, templates, config and a source map), the way a framework such as ExO 3.0 was packaged as a skill. Use whenever the user wants to encode a body of knowledge as a skill, turn a document or methodology into a skill, build a skill generator, package someone else's framework for Claude, or update or version an existing knowledge skill, even if they never say the word skill. Settles source rights and attribution first, maps every directive to where the source says it, and validates the result. For a skill built from a repeatable workflow rather than a body of source knowledge, use skill-creator instead.
metadata:
  version: 0.1.0
---

# Skill Forge

A skill that encodes a body of knowledge is a lossy copy of its source. It can drop a name, harden a hedge into a rule, or quietly add the skill author's opinions under the source author's name. Skill Forge exists to make those failures visible: it settles rights and credit before drafting, ties every directive to its source, and checks the package mechanically before anyone relies on it.

It builds on `skill-creator` (draft, test, iterate, package). Use skill-creator for the evaluation loop and description tuning. Use this skill for the part skill-creator leaves open: faithfully turning someone's knowledge into a skill.

## Attribution

This skill's structure is derived from studying the `building-an-exo` package (author Kent Langley, MIT declared in its config; encodes Salim Ismail and contributors' *The Organizational Singularity*, OS Outline v25), and from the `skill-creator` guidance. It encodes none of their domain content. See `references/case-study-building-an-exo.md` and `source-map.md`.

## When to use this skill

- The user hands over a book, paper, blueprint, SOP, wiki or notes and wants Claude to apply it consistently.
- The user wants to repackage, update or version an existing knowledge skill.
- The user asks for a skill generator or "a skill that makes skills".

Do not use it for a skill that captures a workflow the user just performed (use skill-creator), or when the source is not the user's and its rights are unknown and the user wants it published (see D-02).

## Workflow

1. **Intake.** Copy `templates/intake.md.tmpl` into the new skill as `intake.md` (the scaffolder does this) and fill it in with the user. Read `references/source-intake-and-rights.md` when rights are unclear.
2. **Scaffold.** Run `scripts/scaffold_skill.py --name <kebab-name> --out <dir> --author <maintainer> --source-title <title> --source-author <authors as credited>`. It refuses to overwrite.
3. **Decompose the source.** List the source's distinct frameworks, rules, procedures, diagnostics and vocabulary. Decide which become directives, which become reference files and which fill-in templates. Read `references/anatomy.md` for the package shape and when each part earns its place.
4. **Draft SKILL.md.** Keep it short and put depth in references. Give each directive an ID (D-01...) and write the reason after the rule.
5. **Map every directive.** Fill `source-map.md`. Read `references/fidelity-and-source-mapping.md` for how to cite and how to label author additions.
6. **Validate.** Run `scripts/validate_skill.py <skill-dir> --draft` while working, then without `--draft`, then `--release` before publishing. Fix errors; read warnings.
7. **Test.** Write trigger evals from `templates/trigger-evals.json.tmpl` and 2 or 3 realistic task evals, and run them with skill-creator against a no-skill baseline. Record the outcome in `evals/results.md`. Do not claim the skill works without it (D-15).
8. **Release and maintain.** Set `review_by`, add a Changelog entry for every change, and classify each change as patch, minor or major per `references/versioning-and-changelog.md`.

## Core Directives

Every directive has a row in `source-map.md`. The reasons are part of the directive; if a reason does not apply to a case, use judgment instead of the letter.

- **D-01 Do intake before drafting.** Record the source, its exact authors, its version and date, the terms it is under, and what the user wants. Everything later depends on these, and they are cheap to get now and expensive to reconstruct.
- **D-02 When rights are unknown, stop and ask, and keep the skill private.** An encoded skill redistributes someone's work. A package that says "MIT" with no license text, while its own text says the frameworks are the authors' property, is a real example of the ambiguity this guards against. Record `redistribution = "unknown"` and let `--release` refuse until it is resolved.
- **D-03 Credit every named person and every borrowed source, exactly as the source does.** Shortening a credit list to save space is a misattribution. Copy names, titles and dates verbatim into Attribution and `config.toml`.
- **D-04 Encode, do not copy.** Restate the source's ideas in the skill's own structure. Quote only short passages, each with a locator. Long verbatim reproduction needs a recorded license that allows it.
- **D-05 One directive, one ID, one source-map row.** The ID is how a reviewer finds where a rule came from. A directive without a row is unreviewable, and the validator rejects it.
- **D-06 Keep what the source claims separate from what the skill author added.** Label each row `SOURCE-CLAIM`, `AUTHOR-ADDITION` or `UNSOURCED`. Presenting a workflow step or guard as the source's teaching is how a skill drifts from its source.
- **D-07 Make the frontmatter platform-valid.** Only `name`, `description`, `license`, `allowed-tools`, `metadata` and `compatibility` are allowed. The name is kebab-case and at most 64 characters. The description is at most 1024 characters, has no angle brackets, and must not contain a colon followed by a space unless quoted, because plain YAML reads it as a nested mapping. Put `version` under `metadata` and trigger phrases inside the description.
- **D-08 Write a description that triggers when it should and not when it should not.** It is the only text always in context, so say what the skill does, list the situations and phrases that call for it, name the near-misses that do not, and be a little pushy because skills tend to under-trigger. Do not overclaim what the skill can do.
- **D-09 Use progressive disclosure.** Keep SKILL.md at 500 lines or fewer (the validator fails above 800) and move depth into `references/`. Say in SKILL.md when to read each reference, because a file nobody points to is never loaded.
- **D-10 Explain why, and use MUST sparingly.** A model that knows the reason can handle cases the rule did not anticipate. Reserve forceful language for real guardrails.
- **D-11 Make every validation checkpoint observable.** "Directive IDs all appear in source-map.md" can be checked. "The skill is faithful" cannot. If a checkpoint can only be judged by feel, say so and who judges.
- **D-12 Version every change and record it.** Classify each change as patch, minor or major, add a Changelog entry, and for a major change list what it invalidates (users who relied on the old behavior, dependent skills).
- **D-13 State what is not covered, and when to recheck.** Every source has gaps and ages. Add a Not covered section and a `review_by` date so the skill does not present old knowledge as current.
- **D-14 Keep traces and examples free of personal and client data.** Traces are opt-in, synthetic or consented. A skill is shared; a log of someone's real work is not.
- **D-15 Test before claiming the skill helps.** Run trigger evals and task evals against a no-skill baseline and record the results. Without them the honest status is "drafted, unmeasured".
- **D-16 Keep scripts boring and reviewed.** A skill's scripts must do what the skill says and nothing else: no hidden network calls, no reading outside the skill's own task. A user should not be surprised by anything the skill runs.
- **D-17 Never overwrite an existing skill.** Read it, snapshot it, and edit a copy. Preserve its name so updates replace rather than fork.

## Validation Checkpoints

Before calling a skill done:

- [ ] `scripts/validate_skill.py <dir> --release` exits 0 (or, for a private draft, `--draft` exits 0 and the remaining warnings are understood).
- [ ] Every directive ID appears in `source-map.md` and every map row's ID appears in SKILL.md.
- [ ] Every person and source the origin names is in Attribution, spelled as the origin spells it.
- [ ] `config.toml` records the source's terms and `redistribution`; if it says `unknown`, the skill is not published.
- [ ] A reviewer other than the author spot-checked at least five directives against the source locators.
- [ ] `evals/results.md` shows trigger and task outcomes against a baseline, or the skill is labelled unmeasured.
- [ ] `review_by` is set and the Changelog has an entry for the current version.
- [ ] The skill passes the platform's own `quick_validate.py` (from skill-creator).

## References

- `references/anatomy.md`: the package shape (SKILL.md, references, templates, schema, config, traces) and when each part is worth having. Read at step 3.
- `references/source-intake-and-rights.md`: how to establish authorship and terms, what to do when they are unclear, and what to write in `config.toml`. Read at step 1 whenever rights are not obvious.
- `references/fidelity-and-source-mapping.md`: how to write locators, label author additions, and review a skill against its source. Read at step 5.
- `references/versioning-and-changelog.md`: patch, minor and major for a skill, and what a major change invalidates. Read at step 8.
- `references/case-study-building-an-exo.md`: what a real framework skill looks like and the problems found in it, as observed. Read for a concrete example.

Templates the scaffolder uses (read them to see what a field is for):

- `templates/SKILL.md.tmpl`, `templates/config.toml.tmpl`, `templates/source-map.md.tmpl`, `templates/intake.md.tmpl`, `templates/trigger-evals.json.tmpl`

Scripts:

- `scripts/scaffold_skill.py` creates the package skeleton. `scripts/validate_skill.py` checks it (`--draft`, default, `--release`).

## Not covered

- Judging whether a skill is faithful or useful. The validator checks structure and traceability; fidelity needs a human reading the source against the map, and usefulness needs evals.
- Converting source formats (PDF, EPUB, slides) into text. Do that first with the matching tool.
- Legal advice. The skill records what the user says about rights; it does not decide them.
- Packaging and installing the final skill. Use skill-creator's `package_skill.py`.

## Changelog

- **v0.1.0 (2026-10-04)**: initial draft. Intake and rights, source map, platform-valid frontmatter, validator and scaffolder. Evals not yet run.
