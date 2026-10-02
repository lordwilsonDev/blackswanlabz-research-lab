---
source: pre-registration written in this repo during research session 2026-10-02
captured: 2026-10-02
status: pending
---

# CVT-1 run sheet and pre-registration

**Not run.** Nothing on this page is a result. It fixes what will be run and how it will be judged, so the outcome cannot be argued afterward. The idea behind it is in [the proposal](../../07-next/cheap-verification-test.md).

## What it tests

Whether a small free model, checked by running tests and shown the failure message, solves more held-out problems than the same model that is only re-sampled from scratch, at the same attempt limit. This separates two things that are easy to confuse: the effect of a verifier (an oracle that says pass or fail) and the effect of feedback (telling the model why it failed).

## Exactly what to do

1. Open Google Colab and create a notebook, or upload [cvt1.ipynb](cvt1.ipynb) (File, Upload notebook).
2. Runtime, Change runtime type, choose **T4 GPU**.
3. Run the cells top to bottom. The `selfcheck()` call runs first; if it fails, stop and send me the message.
4. Optional cloud arms A and D: add `ANTHROPIC_API_KEY` under the key icon (Secrets) and set it in the environment before the last cell, `import os; os.environ["ANTHROPIC_API_KEY"] = "..."`. Edit `cloud_price_per_mtok` in the config cell to the current price **before** running. Without a key, only the loop-versus-resample question is tested and no cost comparison is made.
5. Do not edit the config after the first real run. If you must change something, change it, delete `cvt1_results.jsonl`, and note the change.
6. Bring back: the printed summary table, the "REGISTERED DECISION" line, the file `cvt1_results.jsonl`, the Colab GPU type shown in the notebook, and the commit hash of this folder you used.

Expect roughly 30 to 90 minutes on a free T4 for the local arms. Free sessions can disconnect; results are appended to `cvt1_results.jsonl` as they finish, so download it if the session dies, and say so.

## Design

| Item | Value |
|---|---|
| Tasks | 24 small Python functions, each with 3 visible and 3 to 7 hidden tests, plus a reference solution used only by the self-check |
| Seeds | 0, 1, 2 (72 task-runs per arm) |
| Attempts | up to 4 per task-run |
| Local model | Qwen/Qwen2.5-Coder-1.5B-Instruct, sampled at temperature 0.7, top-p 0.95, 384 new tokens |
| Cloud model (optional) | claude-haiku-4-5-20251001 |

Arms, with attempt 1 shared per task and seed so the comparison is paired:

| Arm | What it does |
|---|---|
| B | attempt 1 only |
| B-n | attempt 1, then fresh independent samples until one passes the visible tests |
| C | attempt 1, then fixes that see the failure message, until one passes the visible tests |
| A, D | the same as B and C using the cloud model (only if a key is set) |

The loop sees only the visible tests. The hidden tests judge the final answer. A **false pass** is a final answer that passes the visible tests and fails the hidden ones.

## Registered decision

Using the mean hidden-test pass rate per task (averaged over the three seeds):

- **Supported** only if C beats B-n by at least **0.10** AND the 95% bootstrap interval (5,000 resamples over tasks) of the difference has a lower bound above 0.
- Otherwise **not supported**. A tie is not supported.

All other numbers (visible pass, false-pass rate, attempts, tokens, seconds, cloud cost) are descriptive and support no claim by themselves.

## Limits, stated now

- The tasks are small and the same author wrote the visible and hidden tests, so the result says little about real software work. It measures the effect of feedback on a small model under this oracle, nothing wider.
- Local cost on free Colab is recorded as 0 dollars, which is not an energy or capacity cost. Compare tokens and seconds before drawing a cost conclusion.
- 24 tasks is a small sample. A supported result is a direction, not an established effect.
- The hypothesis in the proposal compares a small model in a loop with a large model's single attempt (arm C against arm A). That needs the cloud arms and a price check, and it is not part of the registered decision above.
- No claim is added to [CLAIMS.md](../../CLAIMS.md) until results exist and have been checked.
