# How the meta-test works

Read this when configuring a run or interpreting a report.

## Contents
1. Configuration
2. The pipeline
3. Mutation operators
4. Reading the report

## 1. Configuration

`meta-test.toml` at the project root:

```toml
[[suite]]
name = "my_module"
targets = ["src/my_module.py"]          # code under test
tests = ["tests/test_my_module.py"]     # tests that must guard it
timeout = 60                            # seconds per mutant run
```

Every path must exist. A suite names the tests that should guard its targets, so the report can say which tests are responsible for which code.

## 2. The pipeline

1. **Baseline.** Run the suite. If it is red, stop and report; nothing else is meaningful.
2. **Trace.** Run the suite again under a line tracer limited to the target files, and record which lines executed. Statement counts come from the file's syntax tree.
3. **Enumerate** mutation sites in each target. Sites on lines the tests never executed are listed as `NOT_EXERCISED` and left out of the score.
4. **Sample** the executed sites with a fixed seed (`--max-mutants`, `--seed`).
5. **Run each mutant** in an isolated copy of the project with fail-fast pytest. A non-zero exit is `KILLED`, a timeout is `TIMEOUT` (counted as caught), exit zero is `SURVIVED`.
6. **Audit** the test files and write the report.

The original files are never modified; copies are made in a temporary directory and removed.

## 3. Mutation operators

| Operator | Change | Catches tests that miss |
|---|---|---|
| Comparison swap | `==`/`!=`, `<`/`>=`, `>`/`<=`, `is`/`is not`, `in`/`not in` | wrong or missing boundary and equality checks |
| Boolean swap | `and`/`or` | conditions where only one side is exercised |
| Branch removal or forcing | `if cond` becomes `False` or `True` | untested branches |
| `not` removal | drops a negation | inverted logic |
| Return to None | `return x` becomes `return None` | results never checked |
| Constant change | `True`/`False` flipped, integers plus one | magic numbers and limits that nothing pins |

The `if __name__ == "__main__"` guard and f-strings are never mutated.

## 4. Reading the report

- **Statements executed** is coverage of the target by this suite. Low coverage is the first thing to fix.
- **Mutation score** is caught over (caught plus survived), for the sampled executed sites only.
- **Survivors** are listed with file, line and the change made. Open the line and ask what behavior the change alters.
- **Unexercised sites** are not survivors. They are code no test reaches.
- **Audit findings** are test-quality problems independent of the code.

A high score with low coverage means the tests are strict about what they touch and touch little. A high coverage with a low score means the tests run the code but do not check what it does.
