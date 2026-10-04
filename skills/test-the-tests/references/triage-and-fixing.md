# Triage and fixing survivors

Read this when you have a list of survivors.

## For each survivor, ask

1. **What behavior does the mutation change?** Read the mutated line. If you cannot describe an input where the output differs, it may be equivalent.
2. **Is there such an input that matters?** If yes, it is a real gap.
3. **Is the line dead?** A branch no valid input can reach is a sign of dead logic. Consider deleting it instead of testing it.

## Equivalent mutants (record, do not fix)

- A boundary swap where the boundary value cannot occur: `if n >= 1` versus `if n > 1` when `n` is never exactly 1 by construction.
- A change to a value that is overwritten before use.
- A change inside a branch whose result is unused (logging, a returned message nobody reads).
- `x in {a, b}` versus `x not in {a, b}` in a position where both outcomes fall through to the same result.

Write each as: location, mutation, reason, date. Keep the list with the report.

## Closing a real gap

1. Write the smallest test that exercises the behavior (the input where original and mutant differ).
2. Run it against the original: it must pass.
3. Apply the mutation by hand, or rerun the meta-test: it must fail.
4. If it passes both, the test does not isolate the behavior. Tighten the assertion; do not add more tests of the same shape.

## Common patterns

| Survivor | Likely missing test |
|---|---|
| comparison on a limit (`> 1024`) | a value exactly at the limit and one beyond it |
| `if` branch removed | an input that takes the branch and an assertion on its effect |
| `and` to `or` | cases where only one condition holds |
| return to None | an assertion on the returned value, not only that no exception occurred |
| constant plus one | a test that pins the exact constant (a count, a threshold) |
| rule enforced but nothing asserts the failure | the negative case: invalid input is rejected |

## Do not

- Weaken the mutator or exclude the line to raise the score.
- Edit the code under test so the mutant becomes equivalent.
- Add a test only to cover a line; coverage without assertions is the failure this skill exists to find.
