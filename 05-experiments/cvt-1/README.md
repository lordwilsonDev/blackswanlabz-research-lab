---
source: pre-registration written in this repo during research session 2026-10-03
captured: 2026-10-03
status: pending
---

# CVT-1 run sheet and pre-registration

**Not run.** Nothing on this page is a result. It fixes what will be run and how it will be judged, so the outcome cannot be argued afterward. The idea is in [the proposal](../../07-next/cheap-verification-test.md). The process is the [lab-verify skill](../../.claude/skills/lab-verify/SKILL.md), which wraps `lab_harness.py`.

## What it tests

Whether a small local model that sees the failure message of a failed attempt (arm C) solves more hidden tests than the same model re-sampled from scratch with the same attempt limit (arm B-n). This separates two effects that are easy to confuse: having a verifier that says pass or fail, and giving the model feedback about why it failed.

## Run it on the Mac mini (local, no cloud)

Hardware to record in the run note: Mac mini M4, 16 GB unified memory (as the captured environment file in msb-v3 and the owner's readout both indicate; the owner should confirm with `system_profiler SPHardwareDataType`).

```bash
ollama pull qwen3:8b
H=.claude/skills/lab-verify/scripts
python3 $H/lab_harness.py lock      05-experiments/cvt-1     # freezes prereg.json and tasks.json
python3 $H/lab_harness.py selfcheck 05-experiments/cvt-1     # must say SELF-CHECK OK
OLLAMA_MODEL=qwen3:8b python3 $H/lab_harness.py run 05-experiments/cvt-1 \
  --adapter "python3 $H/ollama_adapter.py" --note "Mac mini M4 16GB, qwen3:8b via Ollama"
python3 $H/lab_harness.py analyze 05-experiments/cvt-1
python3 $H/lab_harness.py report  05-experiments/cvt-1
```

Or in Claude Code or claude.ai, say: **use the lab-verify skill and run CVT-1 on `05-experiments/cvt-1`**.

Edit `prereg.json` (margin, seeds, limits) before `lock` if you want to; after `lock` the harness refuses to run if either file changed. Expect roughly 30 to 100 minutes on a 16 GB machine (an estimate, not a measurement); results are written as they finish. Bring back the printed table, the registered-decision line, `results.jsonl`, `RUN.json` and `REPORT.md`.

A run with `--adapter fake:0.5` tests the harness only. It is labelled NOT EVIDENCE in the output and report. Do not quote its numbers.

## Design

| Item | Value |
|---|---|
| Tasks | 24 small Python functions in `tasks.json`, each with 3 visible and 3 to 7 hidden tests and a reference solution used only by the self-check |
| Seeds | 0, 1, 2 (72 task-runs per arm) |
| Attempts | up to 4 per task-run |
| Metric | hidden-test pass rate; false passes (visible pass, hidden fail) are counted too |
| Cost | tokens and seconds on one machine; no dollar or energy figure |

Attempt 1 is generated once per task and seed and shared by every arm, which pairs the comparison.

| Arm | What it does |
|---|---|
| B | attempt 1 only |
| B-n | attempt 1, then fresh independent samples until one passes the visible tests |
| C | attempt 1, then fixes that see the failure message, until one passes the visible tests |

The self-check proves, per task, that the reference passes, a stub fails, and a lookup of the visible answers (the auto-cheat) is rejected by the hidden tests.

## Registered decision

Using the mean hidden-test pass rate per task, averaged over seeds: **supported** only if C beats B-n by at least **0.10** and the 95% bootstrap interval (5,000 resamples over tasks) of the difference has a lower bound above 0. Otherwise **not supported**. A tie is not supported. All other numbers are descriptive.

## Limits, stated now

- The same author wrote the visible and hidden tests, and 24 small tasks says little about real software work.
- Local cost is tokens and seconds on one machine, not dollars or energy.
- 24 tasks is a small sample. A supported result is a direction, not an established effect.
- The comparison in the proposal of a small model in a loop against a large model's single attempt is a separate experiment: run the harness again with a different adapter in a new directory.
- No claim is added to [CLAIMS.md](../../CLAIMS.md) until results exist and have been checked.

## Superseded

An earlier Colab version of this test (`cvt1.py` and `cvt1.ipynb`), built on a mistaken assumption about where the test would run, was removed on 2026-10-03 and remains in the git history. The harness pack above replaced it; the 24 tasks were carried over unchanged.
