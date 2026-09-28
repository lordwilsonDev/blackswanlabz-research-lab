---
source: ~/projects/fde-kernel-skills (local git, no remote; HEAD f88d8ab3b981e9a492c991904ae76fb672815f0e)
captured: 2026-09-28
status: active
---

# FDE Kernel skills

> Not yet public. The source is a local git repository with no remote, so a reader of this lab cannot open it. Every claim below is pending a public push, including the gate result (pending, C-037), which is checkable only by someone who has the repo. See [the missions page](../05-experiments/fde-kernel-missions.md) and the claims [C-037](../CLAIMS.md) to [C-044](../CLAIMS.md).

## What the Kernel is

The README describes the FDE Kernel v0.3.2 as a harness packaged as Claude Code skills, plus the scripts behind them. The skill file `fde-kernel` describes it as a persistent mission state machine and bounded Gateway between a model and a mission: the model proposes, the Kernel decides, and state lives in one SQLite `state.db` per run. Its checks cover claim-status monotonicity, contradiction objects, an authority gate, a human-gate path and revalidation forcing. The worlds it is exercised on are simulated incident missions in `fde/simulator*.py`, not live systems.

## The three skills

| Skill | Use |
|---|---|
| `fde-kernel` | understand, extend or debug the Kernel |
| `fde-mission` | run one closed-loop mission as the reasoning layer |
| `fde-eval` | design, lint, pre-register, run and report an experiment; red-team the Kernel |

The README also lists `bs-*` skills; they are not covered here.

## Enforced blindness

While a run is being scored, the model must not read the harness source, ground truth, tests or other runs. `fde/blind_guard.py` is a `PreToolUse` hook that, while a `.fde_blind` file exists, blocks those reads and limits Bash and writes to a small allowlist. The README states its own limit: "a guard, not a sandbox".

Two caveats are in the README itself:

- The README records that the guard was not observed to fire on Claude Code subagent tool calls (probe in `runs/_qualprobe/`). All 30 M008 runs were driven through subagents, so M008 is prompt-blind only, not hook-enforced.
- Not verified, per the README: the skills loading in a live session, the hook firing in a top-level interactive session, and the headless scripts end to end (they stopped at a credit-balance error).

## Vault persistence split

`fde/vault_sync.py` keeps human-readable memory in the author's Obsidian vault: lessons, gap records and regression tests under `40_Memory/FDE-Lessons/`, and run notes and arm tables under `50_Experiments/FDE-Kernel/`. Notes for humans are create-only; generated notes carry `fde_generated: true`. SQLite stays the live projection, and it can be rebuilt from the vault notes. The vault is private, so this split is described, not evidenced, here.

## Gate result

`make check` at the pinned HEAD passed on 2 of 3 runs, with 231 unit tests OK, plus scenario lints, pre-registration verify, format check and type check (pending: [C-037](../CLAIMS.md), becomes verifiable when the repo is public). Details, including one earlier failed run, are on the [missions page](../05-experiments/fde-kernel-missions.md#gate-result).

## Sources

- `~/projects/fde-kernel-skills/README.md` and `AGENTS.md` at HEAD f88d8ab3b981e9a492c991904ae76fb672815f0e.
- `~/projects/fde-kernel-skills/.claude/skills/fde-kernel/SKILL.md`, `fde-mission/SKILL.md`, `fde-eval/SKILL.md`.
- `~/projects/fde-kernel-skills/fde/vault_sync.py` (docstring) and `fde/blind_guard.py`.
