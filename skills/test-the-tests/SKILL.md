---
name: test-the-tests
description: Find out whether a test suite actually catches bugs. Use whenever the user asks how good or trustworthy their tests are, wants mutation testing, a test audit, or to find tests that pass without exercising the code, or says things like meta test, test the tests, do my tests mean anything, or break my code on purpose and see what the tests miss. Runs the suite, traces which lines the tests execute, generates mutants of the code and reports the ones no test notices, audits tests for missing assertions, then helps write the tests that close the gaps. Python and pytest out of the box. Not for writing a first test suite from scratch or debugging one failing test.
metadata:
  version: 0.1.0
---

# Test the Tests

A green test suite only says the code passed the tests. It does not say the tests would fail if the code were wrong. This skill measures that second thing: it breaks the code on purpose, many small ways, and counts how many breaks the suite notices. The breaks nobody notices point at the tests worth writing.

## Attribution

The method (a test is not evidence unless it exercises the target; mutation classes; checking the checker) comes from the BlackSwanLabz FreeBuff blueprint, Part M of `docs/specs/2026-10-03-freebuff-question-blueprint-v1.1.md`, by the lab owner. Mutation testing as a technique is long established in the testing literature; this skill implements a small version and claims nothing new about it.

## When to use this skill

- The user wants to know whether tests are trustworthy, or has just built tests and wants them stress-tested.
- A suite is green but the user does not believe it.
- Before relying on a validator, gate or checker, where a false pass is costly.

Do not use it to write a first suite (write tests first, then come back) or to debug one failing test.

## Workflow

1. **Configure.** List each suite in `meta-test.toml` as the code under test plus the tests that should guard it. See `references/how-it-works.md` for the format.
2. **Audit.** Run `scripts/meta_test.py audit --root .`. It is fast and finds tests with no assertion, tautologies, and test files that never import their target.
3. **Run.** `scripts/meta_test.py run --root . --max-mutants 160 --out <dir>`. Allow minutes, not seconds. It requires a green baseline, traces executed lines, mutates executed lines in isolated copies, and writes `meta-test-report.md` and `.json`.
4. **Triage.** Read the survivors one at a time. Read `references/triage-and-fixing.md`: each is either a real gap, an equivalent mutant (cannot change behavior), or a sign the code has dead logic.
5. **Fix.** For a real gap, write a test that fails on the mutant and passes on the original, then confirm both. Never edit the code to dodge a mutant.
6. **Rerun** with the same seed to see the survivors disappear, and with a different seed before claiming a score.
7. **Record** the numbers with their context in a report the user can keep (coverage, sample size, seed, survivors left and why).

## Core Directives

Every directive has a row in `source-map.md`. Reasons are part of the rule.

- **D-01 Require a green baseline first.** If the suite already fails, every mutant "fails" too and the score means nothing.
- **D-02 Measure execution before mutation score.** A test that never runs the target proves nothing about it however green it is, so report which lines the suite executes and treat the rest as unevidenced.
- **D-03 Mutate only executed lines, and report the rest separately.** A mutant on a line no test touches survives trivially. Mixing those into the score hides the real problem, which is missing coverage, not weak assertions.
- **D-04 Treat survivors as leads, not verdicts.** Some mutants are equivalent (for example `>=` versus `>` where the boundary value cannot occur). Triage each; do not chase 100 percent.
- **D-05 Close a gap with a test that fails on the mutant and passes on the original.** Check both directions. A test that passes either way did not close the gap.
- **D-06 Mutate copies, never the working tree.** The user's code must be unchanged after a run, even if the run is interrupted.
- **D-07 Bound the cost.** Sample with a fixed seed, parallelize, and set a timeout. A mutant that makes the code loop forever is caught, and a timeout is reported as such.
- **D-08 Report coverage, score, sample size and seed together.** A single number lets a weak suite look strong; a sample is not the whole population, so rerun with another seed before claiming a score.
- **D-09 Audit the tests themselves.** A test with no assertion, an assertion that is always true, or a comparison of a value with itself passes while checking nothing.
- **D-10 State the known limits.** A mutant can be "caught" because it broke the import and every test failed, not because a test checks that behavior. Say this when interpreting a high score.
- **D-11 Record equivalent mutants with a reason.** Dropping a survivor silently turns a judgment into an invisible one.

## Validation Checkpoints

- [ ] The baseline suite is green before any mutation result is read.
- [ ] The report gives, per suite, statements executed, mutants caught, survivors and unexercised sites.
- [ ] Every survivor is either fixed by a new test or listed with a reason it is equivalent.
- [ ] The user's working tree is unchanged by the run (`git status` shows only intended edits).
- [ ] After fixes, a rerun with the same seed shows the fixed survivors gone and the suite still green.
- [ ] The score was checked with at least one other seed before it is quoted.

## References

- `references/how-it-works.md`: the pipeline, the mutation operators, the config format and how to read the report. Read at step 1 and when interpreting results.
- `references/triage-and-fixing.md`: how to decide whether a survivor is real, patterns for killing common survivors, and examples of equivalent mutants. Read at step 4.

Script:

- `scripts/meta_test.py` runs `audit` and `run`; it needs only Python 3.11 and pytest.

## Not covered

- Languages other than Python. The method transfers; the AST mutator here does not.
- Mutation operators beyond comparison, boolean, branch, return and constant changes. Statement deletion, string and call-argument mutations are not generated.
- Whether the tests are well designed or the code is correct. A suite can have a perfect mutation score and still miss a requirement nobody wrote down.
- Flaky tests. A flaky suite makes the baseline and the mutant results unreliable; fix flakiness first.

## Changelog

- **v0.1.0 (2026-10-04)**: initial version. Audit, execution tracing, AST mutation, parallel isolated runs, report. Built and exercised on the BlackSwanLabz scripts; not yet evaluated on other codebases.
