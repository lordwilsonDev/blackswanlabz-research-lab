# Case study: the building-an-exo package

Read this for a concrete example of a framework skill. Everything below was observed in the package as supplied on 2026-10-04 (version 1.5.0; see `third-party/building-an-exo/` in the BlackSwanLabz research lab for the unmodified file and its attribution). This is a description of its structure, not of its subject matter, and not a judgment of the framework it encodes.

## What it does well

- **Layered depth.** One SKILL.md plus 14 reference files, 11 fill-in templates, a JSON schema, a config file and dated traces. Detail loads only when needed.
- **Artifacts, not only advice.** Templates are scorecards and specifications a person completes.
- **Checkpoints and workflows.** A Validation Checkpoints checklist, named cross-skill workflows, and a version-by-version Changelog (six entries, 1.0.0 to 1.5.0).
- **Visible credit.** An Attribution section naming the book, its author and 16 named contributors, and the external sources it borrows from.
- **A machine contract.** `schema.json` defines input and output shapes.

## Problems observed

| Observation | Why it matters | Forge response |
|---|---|---|
| Frontmatter has top-level `version` and a 234-entry `triggers` list. The platform's `quick_validate.py` rejects it: invalid YAML at the description (an unquoted colon at character 1008), and `version`/`triggers` are not allowed keys. | A package that fails the upload validator cannot be installed through the normal path. | D-07; the validator checks keys, length and colons. |
| Description is 1021 characters. | One character from the 1024 limit; any edit breaks it. | Validator warns near the limit through the hard check. |
| SKILL.md is 599 lines (about 87 KB) with 68 uses of MUST. | Everything loads on every trigger; heavy imperatives leave no room for judgment. | D-09, D-10. |
| `config.toml` says `license = "MIT"`, no LICENSE file or copyright line ships, and the Attribution section says the frameworks are the authors' intellectual property. | Terms are ambiguous for anyone redistributing. | D-02; `redistribution` field. |
| Directives have no IDs and no source locators. | A reader cannot tell what the source says from what the skill added. | D-05, D-06; `source-map.md`. |
| Trace files carry project context from real work (for example a client venture name). | A shared skill should not carry someone's work log. | D-14; validator scans traces. |

## What to copy

The layered shape, the artifact templates, the checkpoint list, the changelog, and the visible attribution. Add what it lacks: IDs and a source map, rights recording, platform-valid frontmatter, a size ceiling and measured evals.
