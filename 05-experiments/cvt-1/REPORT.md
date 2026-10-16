---
source: run of the pre-registration in README.md, locked at e440d9e, executed 2026-10-08 (UTC)
captured: 2026-10-08
status: pending
---

# cvt-1: report

**Registered decision: NOT SUPPORTED.** C minus B-n on hidden tests = +0.000, 95% CI [+0.000, +0.000], registered margin 0.1, 24 tasks.

## Registered question and falsification

On 24 small Python tasks, does a small local model that sees the failure message of a failed attempt (arm C) solve more hidden tests than the same model re-sampled from scratch with the same attempt limit (arm B-n)?

Falsification, fixed before the run: The mean per-task difference (C minus B-n) is below 0.10, or its 95% bootstrap interval includes 0. A tie counts as failure.

## Results (descriptive)

| arm | hidden | visible | false pass | attempts | tokens out | seconds |
|---|---|---|---|---|---|---|
| B | 0.736 | 0.931 | 0.194 | 1.00 | 99 | 6.3 |
| B-n | 0.750 | 0.986 | 0.236 | 1.15 | 120 | 7.6 |
| C | 0.750 | 0.944 | 0.194 | 1.18 | 129 | 8.4 |

## Run record

Adapter `python3 .claude/skills/lab-verify/scripts/ollama_adapter.py`; note: Mac mini M4 (Mac16,10) 16GB, qwen3:8b via Ollama 0.34.4, run by Hark via Desktop Commander; macOS-26.6.2-arm64-arm-64bit; instrument lab-harness-0.1.

## Limits, as registered

- The same author wrote the visible and hidden tests, and 24 small tasks says little about real software work.
- Local cost is measured as tokens and seconds on one machine; there is no dollar or energy figure.
- 24 tasks is a small sample: a supported result is a direction, not an established effect.
- The model's sampling seed is controlled only if the adapter honours HARNESS_SEED.

## Suggested ledger row (add to CLAIMS.md only after you have checked this report)

`| C-??? | Arm C beats arm B-n on hidden-test pass rate by at least the registered margin, because feedback carries information that resampling does not. Result under the registered rule: NOT SUPPORTED (C minus B-n +0.000, n=24 tasks) | 05-experiments/cvt-1/REPORT.md | re-run `lab_harness.py run` with the same adapter; compare ANALYSIS.json | pending | 2026-10-07 |`

Status stays **pending** until someone other than the run's author has re-run it, or the author states plainly that it was not independently re-run.
