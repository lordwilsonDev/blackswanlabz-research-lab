---
source: operator smoke test of lab-forge + lab-verify, run in this repo's cloud sandbox
captured: 2026-10-03
status: pending
---

# Operator smoke test: do the pieces come together?

Question asked by the owner: with a person in the loop, do the forge scaffold, the lock, the self-check, the run, the analysis and the report fit together?

## What was done

An AI model acted as the operator, in a scratch copy of the two skills (not in this repo's experiments).

| Step | Command | Result |
|---|---|---|
| Scaffold | `forge.py new smoke-1 --type executable` | pack, prereg, tasks and run-skill created |
| Gate | `forge.py check` | **NOT READY**: FILL markers, 0 tasks. The pipeline stopped and waited for the operator. |
| Operator | filled prereg, wrote 5 tasks | `check`: READY TO LOCK |
| Lock, self-check | `lab_harness.py lock`, `selfcheck` | locked; cheat caught on 5/5 tasks |
| Run | Haiku via `claude_adapter.py` | 5 tasks, completed in under 1 minute |
| Analyze, report | `analyze`, `report` | NOT SUPPORTED (C minus B-n +0.000, CI [0,0]); suggested claim row written |
| Rerun | `run` a second time | **REFUSED**: results already exist |

## Findings

- The pieces fit. Every stage consumed the previous stage's output with no manual fix-up.
- Each guard fired where designed: incomplete prereg blocked, run-once refused.
- The decision points are the operator's (see "What needs a human operator" in both SKILL.md files).
- The tasks were too easy. All three arms are identical: Haiku passed the visible tests on the first try, so the retry arm never retried. One false pass (`rev_words`, hidden test with double spaces) is the only signal. A run like this cannot tell the arms apart. The instrument does not warn about ceiling effects; it reports a tie, and a tie counts as failure.
- Not tested here: the rubric engine (covered by the Haiku AIL+MoIE run), the FCVE skill (see the clean-room page).

The numbers are not evidence about self-repair. They show only that the plumbing works with a real model.
