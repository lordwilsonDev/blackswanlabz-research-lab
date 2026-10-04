# Versioning and changelog

Read this at step 8 and whenever a skill changes.

## Version rules

| Change | Bump | Examples |
|---|---|---|
| Wording only; no directive, checkpoint, template field or trigger changes meaning | patch | typo, clearer example, corrected locator |
| Something added that nothing existing depends on | minor | a new reference file, a new optional directive, a new template |
| A directive, checkpoint, schema field or trigger changes meaning or is removed, or the source's own new edition changes a framework | major | a rule reversed, a scoring scale changed, a template field removed |

`config.toml` and `metadata.version` in SKILL.md must carry the same number; the validator fails a mismatch.

## What a major change invalidates

List these in the Changelog entry:

- Outputs produced under the old behavior that users may be relying on.
- Other skills that cite this one's directives or templates.
- Evals whose expected answers change; rerun them.

Do not edit an old Changelog entry. Add a new one that corrects it.

## When the source updates

Treat a new edition as a new source: redo intake (terms may differ), diff the new source against the source map, mark directives whose locators changed or vanished, and classify the result. Update `review_by`.

## Changelog entry format

`- **vX.Y.Z (YYYY-MM-DD)**: what changed, in one or two sentences; for a major, "Invalidates: ...".`
