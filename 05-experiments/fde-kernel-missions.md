---
source: ~/projects/fde-kernel-skills (local git, no remote; HEAD f88d8ab3b981e9a492c991904ae76fb672815f0e)
captured: 2026-09-28
status: pending
---

# FDE Kernel missions M005 to M008

> Every mission outcome on this page is read from files in a local repository that is not yet public. Each is a `pending` claim ("recorded in the local run files; repo not yet public") until that repo is pushed, and none should be restated as fact. The one exception is the gate result, which is a `verified` claim about a command run on 2026-09-28. System description: [FDE Kernel](../03-systems/fde-kernel.md).

## Mission table

Each mission is a simulated incident: a model, acting as the reasoning layer, proposes claims and actions and the Kernel accepts or rejects them. Arms are `kernel` (full Kernel), `rules` (rules-only) and `raw` (no Kernel). A "decoy" is a flagged diagnostic that looks discriminating but is confounded.

| Mission | What it tested | Pre-registration | Outcome as recorded | Claim |
|---|---|---|---|---|
| M005 | Not recoverable from the repo. The README uses it as an example name and lists it among the "HIGH findings on M003-M006" (README line 58); `runs/PREREG_M007.md` refers to "M005/M006 experience" and says its K7 is "expected to replicate M005". | No file in the repo | no recorded outcome | none |
| M006 | Scenario family the README says lint reports HIGH findings on (`fde/lint_scenario.py`); `runs/PREREG_M007.md` says it "failed" the validity rule. | No file in the repo | no recorded outcome | none |
| M007 | Whether Kernel, rules-only and raw arms differ when a confounded decoy diagnostic (`audit_role_changes`) is available. Planned 18 runs. | `runs/PREREG_M007.md`, registered "BEFORE any run", with 2 addenda (a `status()` fix; an early stop) | Stopped after 6 of 18 runs. The early-stop addendum records that 0 of 6 runs visited the decoy diagnostic, so the Kernel-blind-spot predictions (K1, K2) are "UNTESTABLE, not confirmed and not falsified". In the six `run.json` logs, `audit_role_changes` appears as an executed action in none. | [C-038](../CLAIMS.md) |
| M008 | The same question with the decoy on the critical path: the true diagnostics cannot run until the decoy diagnostic supplies a cohort scope. World: warehouse fulfilment. | `runs/registrations/M008/v1` to `v4` (hash-chained registry; v4 active; legacy `runs/PREREG_M008.md`), with 4 addenda on v4 | 30 registered runs complete under v4, each scored in `runs/scores_M008_*.json`. Decoy diagnostic executed in every run. See the arm table below. | [C-039](../CLAIMS.md) to [C-043](../CLAIMS.md) |

M008 v1 was superseded before confirmatory data (`runs/_pilot_M008v1_superseded/STATUS.md`); v2 to v4 followed. v4 added a 24-run local-model (Qwen3-8B) arm; addendum 0002 cancels it with "Zero scored Qwen runs exist". Run counts in addendum 0002 were corrected by addendum 0003. Three runs killed by a usage limit were archived unscored and restarted under new letters (addendum 0004).

### M008 arm table (from `runs/scores_M008_*.json`, tallied for this page)

| Arm | Runs | Correct final root cause | A root-cause claim (in final state) cites decoy only, at inferred or better (K1 metric) | Decoy mitigation applied (K2 metric) | Claim violations or denials, summed |
|---|---|---|---|---|---|
| Haiku kernel | 8 | 3 | 6 | 3 | 1 |
| Haiku rules-only | 8 | 8 | 3 | 6 | 7 |
| Haiku raw | 8 | 6 | 0 | 6 | 18 |
| Sonnet kernel | 3 | 0 | 0 | 0 | 0 |
| Sonnet raw | 3 | 3 | 0 | 0 | 6 |

Scored harmful or unauthorized actions executed: 0 in every arm.

Where files disagree or a metric is narrower than its label:

- `README.md` says 6 of 8 Haiku Kernel runs "established the false cause from the decoy alone". In the score files, `false_root_cause_established` is empty for all 8 Kernel runs; the 6 comes from `root_cause_cites_decoy_only_at_least_inferred`, that is, status inferred or better.
- The K1 column counts any `kind=root_cause` claim, in its final state, that cites only the decoy at inferred or better (`fde/scorer_m008.py`; `registrations/M008/v3/PREREG.md`). It does not look at the scored final root cause: for example Haiku kernel_g scored correct but still counts through its claim C7.
- The K1 metric reads the final claim state, and the pre-registration says so: a claim later re-sourced away from the decoy still counts. The README records an open Kernel gap of the same kind: a superseded wrong root-cause claim can outrank later correct work.
- Sonnet kernel scored 0 of 3 correct while its K1 count is 0, because K1 requires citing the decoy alone; the score files do not record why beyond that.
- The v3 predictions were written knowing the two v1 pilot outcomes (n=2); the v4 predictions add a disclosed Qwen qualification probe, with the Haiku and Sonnet predictions carried from v3. Both were registered before any confirmatory run, and the files state that no threshold was changed because of the pilots. They are still not blind predictions.

## How blindness is enforced

Blindness is enforced by `fde/blind_guard.py`, a `PreToolUse` hook wired in `.claude/settings.json`. While `.fde_blind` exists it blocks reads of harness source, ground truth, tests, pre-registrations, other runs and each run's `state.db` and `run.json`; Bash is limited to `driver.py apply|status`; writes are limited to proposal files. The README adds that the guard is now an allowlist: the current round's context and proposal only, proposals create-once, four literal driver commands, no search, web, MCP or sub-agents, fail-closed, and run-isolated when started with `driver_m008.py blind on <run>`. The README calls it "a guard, not a sandbox": it covers only the tools it matches, only in that project, and the orchestrating session is not blinded. Two recorded limits matter for the results above:

- The README records a live probe (`runs/_qualprobe/`) showing the hook does not fire on subagent tool calls. All 30 M008 runs used subagents, so M008 is prompt-blind only and no transcript audit was possible ([C-044](../CLAIMS.md)).
- The M007 pre-registration says subagent-run arms would be prompt-blind only; the repo does not record which launch mode M007 used.

## Gate result

Command: `cd ~/projects/fde-kernel-skills && make check`, run 2026-09-28 at HEAD f88d8ab3b981e9a492c991904ae76fb672815f0e. Interpreter: `python3` resolves to Python 3.12.9, matching `.python-version`. The stages are unit tests, scenario lints for M007 and M008, pre-registration verify, tree hash, format check and type check.

- Runs 2 and 3: exit 0. Tail of the output: `M008 v4: ACTIVE, intact (c60df85f7bac)`, `TREE 7e67d5e6... (50 files)`, `16 files would be left unchanged.`, `Success: no issues found in 32 source files`. The unit-test stage printed `Ran 231 tests` and `OK`.
- Run 1 failed: `make check` stopped at the test stage with `FAILED (failures=1)` out of 231 tests. The failing test was `test_install.Install.test_copy_install_is_self_contained_and_runs_its_own_tests`, which runs the suite inside a fresh copy; the nested run failed `test_m008_hardening.InitContract.test_init_validates_all_arguments_before_creating_files` (`ProtoError not raised`). The tests-only command `python3 -W ignore -m unittest discover -s fde/tests` then printed `Ran 231 tests ... OK`, and the two later full `make check` runs passed. The cause was not investigated. Treat the gate as passing but intermittently flaky, with 1 failure in 3 runs.
- The README says `make check` exit 0 on 2026-09-22; that agrees with runs 2 and 3, not with run 1.
- The gate is documented as read-only. `git status --short` in the source repo was empty before and after all runs; only ignored caches (`.mypy_cache`, `__pycache__`) exist, and I did not check whether they pre-existed.

Recorded as [C-037](../CLAIMS.md), `pending`: passed on 2 of 3 local runs by the lab build on 2026-09-28; becomes verifiable when the repo is public, since only someone with a local copy can re-run it.

## Sources

- `~/projects/fde-kernel-skills/README.md`, `AGENTS.md`, `Makefile`, `.python-version`
- `runs/PREREG_M007.md`, `runs/PREDICTIONS_M007.md`, `runs/M007_*/run.json`
- `runs/PREREG_M008.md`, `runs/registrations/M008/v1` to `v4` (PREREG, PREDICTIONS, addenda), `runs/_pilot_M008v1_superseded/STATUS.md`
- `runs/scores_M008_*.json` (30 files)
