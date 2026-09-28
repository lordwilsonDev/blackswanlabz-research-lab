# Claims

Every number or factual claim in this lab has a row here. **Status** is one of `verified` (checked, evidence linked), `pending` (not yet checked — never restate as fact), `retracted` (checked and found wrong — kept, not deleted).

Re-run the mechanical checks with `scripts/verify.sh`. Cells never contain the `|` character.

| ID | Claim | Evidence | How to check | Status | Checked |
|---|---|---|---|---|---|
| C-001 | 32,543,981 lines were added to GITHUB_AI_PROJECTS_PACKAGE in the week starting 2025-12-14 (net 32,543,027 to date) | [code-frequency.json](01-cornerstone/evidence/code-frequency.json) and Wilson's Insights export | `scripts/verify.sh` (online) compares the live API to 32,543,981 | verified | 2026-09-28 |
| C-002 | Breakdown of C-001 into own source code vs vendored code vs data | tokei run at a pinned commit | Task 15 of the v1 plan | pending | 2026-09-28 |
| C-003 | The package holds 208+ projects in 35 categories with 19,864 Python files and 649 external dependencies | the package's own README (self-reported) | recount from a checkout | pending | 2026-09-28 |
| C-004 | AIL+MoIE produces more novel hypotheses than compute-matched best-of-n baselines (H1c) | Hermes12 pre-registered benchmark | run the benchmark; experiment not yet run | pending | 2026-09-28 |
| C-005 | Adaptive Infrastructure `reproduce.py` reproduces `reproduce_results.txt` byte-for-byte | [blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE](https://github.com/lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE) (local write-up added in Task 11) | `python reproduce.py > out.txt; diff out.txt reproduce_results.txt` | verified | 2026-09-28 |
| C-006 | The Adaptive Infrastructure published numbers are correct: SSO inclination 97.59 deg at 550 km, period 95.65 min, 10 deg plane change 1,322 m/s, HHI 1864 to 3106, outbreak RR 7.39 and OR 18.42 | independent hand recomputation | recompute from the formulas in reproduce.py | verified | 2026-09-28 |
