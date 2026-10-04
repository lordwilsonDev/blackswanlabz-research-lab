# Cleanup record — 2026-10-04

**Who:** Claude (Sonnet 5.5, in Claude Code), working at Lord Wilson's request. This is a record that a different model than the one that built the learning-trajectory runs came in afterwards, reviewed the repository, and tidied the bookkeeping. I did not build, run or alter any experiment.

**Why:** `verify` had been failing on `master` since 2026-10-02 (26 errors), so the README badge was red, and the learning-trajectory results had no rows in `CLAIMS.md`.

## What I changed

1. **Front-matter headers (24 files).**
   - 22 files under `05-experiments/` had no header at all: the whole `learning-trajectory/` tree (specs, runs, tasks, the readiness audit) and the causal-audit-loop page. Each now has `source: authored in this lab (first committed <sha>)`, `captured:` set to the date of the commit that first added it, and `status: active`. These values come from git history, not from me.
   - `08-operations/black-swan-labs-research-group.md` had a status value outside the allowed set (`active design / implementation blueprint`) and no `captured`. The status is now `active`; the "design and implementation blueprint, not evidence that the described processes run" wording moved into `source`. `captured: 2026-10-03` is its first-commit date.
   - `08-operations/competitive-architecture-absorption-v1.md` lacked `source` and `captured`. Added, `captured: 2026-10-03`.
2. **Six new claim rows, C-048 to C-053**, all `pending`. They cover the Python 2.0 slice pilot, its L5 extension, the mbeddr units / transfer / state-machine tranche, the unit-safe controller run, the "verifier was wrong, learner was right" pattern, and the readiness audit result. They record what the run files say. I did not re-run anything, and the interpreter and suite code are not in this repository, so none of them can be marked `verified` from here.

## What I did not change

- No result, run record, score, or wording of any experiment page was edited. The headers sit above the existing text.
- No claim was promoted to `verified`. No existing claim row was edited.
- G19 and G20 stay pending and the stop state `BLOCKED_FOR_NEW_RUNS` stands. Nothing here counts as an independent reconstruction.
- Branches, other commits and the `cool-knuth` branch (clone-traffic notice, skills, meta-test harness) were not touched or merged. Whether to keep them is the owner's decision.

## Things I noticed and left for the owner

- `q2b-ltb-pilot-001-record.json` names the learner as "GPT-5.6 Luna"; the other runs do not name a learner model. Confirm which model produced each run before anyone cites them.
- The C-018 to C-027 citations (Epoch AI, Anthropic, Stargate, FT) are still pending with no links.
- `build/v1` and `showcase` are still on origin; the thesis header, SOP prices and author emails are still public.

## Checks run

`scripts/verify.sh --offline`: OK (was FAIL with 26 errors). `pytest`: 38 passed. The online checks run in CI.
