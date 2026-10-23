# Results for intent-to-appsscript v0.3.0

Recorded 2026-10-25. This lists what was measured and, just as important, what was not.

## Measured

| Check | Result |
|---|---|
| Platform validator (`quick_validate.py`) | Pass (v0.1.0 failed: `version` is not an allowed frontmatter key) |
| skill-forge validator | Pass |
| Unit tests (`tests/test_validator.py`) | 29 tests, all pass |
| Adversarial probes (`tests/test_adversarial.py`) | 29 tests, all pass; 17 of the first 24 probes (15 failures, 2 errors) failed against v0.2.0, which is how the defects were found (`inversion-review.md`) |
| Mutation test of the validator (every mutant) | 191 caught, 0 survived (v0.1.0's 6 tests caught 22 of 24 mutants) |
| Statements executed by the tests | 179 of 180 (the `__main__` guard) |
| Google behavior claims (script edits do not fire edit triggers, installable triggers run as their creator, time-driven jitter, 20 triggers per user per script, 100/1,500 email recipients per day, least-privilege scopes) | Confirmed by a fetch of the Google documentation on 2026-10-24, partly from summaries of truncated pages |

## Not measured

- **Trigger evals** (`trigger-evals.json`, 9 queries) have not been run, so it is unknown how reliably the description triggers.
- **No model has been run on a task with this skill** against a no-skill baseline, so it is unknown whether the instructions produce better automations.
- **No Apps Script was generated, deployed or executed.** The skill ships no `Code.gs` template.
- **Draft-creation quota**: the fetched documentation does not state one.
- **Receipts are self-reported.** The validator cannot tell whether an execution really happened (`inversion-review.md`, section 5).

Until the model-run evals exist, the honest status is: drafted, structurally validated, and its validator is heavily tested.
