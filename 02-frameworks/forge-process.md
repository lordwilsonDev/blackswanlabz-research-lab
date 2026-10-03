---
source: process page drafted by an AI model in this repo during research session 2026-10-03, from the lab's own build history
captured: 2026-10-03
status: pending
---

# How the lab makes an experiment: the process that produced the process

This page describes the procedure the lab converged on while building its experiments, and the tool that now encodes it: the [lab-forge skill](../.claude/skills/lab-forge/SKILL.md). The procedure is the lab's own convention, drafted from what happened, and it has not been used by anyone else. Nothing here is externally validated.

## The eleven stages

Run `python3 .claude/skills/lab-forge/scripts/forge.py process` to print them. In order: claim, standard, instrument, pre-registration, instrument controls, validity traps, lock, run once, report, ledger, package.

Each stage exists because skipping it caused a real failure or a near miss while the lab's experiments were being built:

| Stage | What went wrong without it, in this repo's history |
|---|---|
| Standard | Claims with no declared standard were argued after the fact; the lab's independence ladder now names the level reached and says that the top level is unreachable. |
| Pre-registration | A measuring tool was tightened in about 80 commits with no measurement run; the registered margin and stopping rule now come first. |
| Instrument controls | Hidden tests that add nothing beyond the visible ones cannot detect a cheat; the harness builds a visible-only cheat and refuses tasks it cannot catch. A rubric engine whose decision rule has never seen a null dataset has unknown error rates, so it is run on null and planted-effect data first. |
| Validity traps | A local model server silently truncates a prompt that fills its context window, which would have corrupted the multi-stage arm of a method test; an adapter had a hard-coded code-writing system prompt that was wrong for a non-code experiment; a test that rewrote a locked file in a different format correctly tripped the byte-level lock. |
| Lock | Goalposts can move silently; a hash of the registration and inputs makes any change visible and makes the run refuse. |
| Run once | A partial or repeated run invites cherry-picking; the harness refuses a second run and does not splice partial results. |
| Report | Reporting numbers first lets the reader and the author pick a favourable one; the registered decision comes first. |
| Ledger | Several claims were restated as fact before anyone checked them; every claim enters as pending with a re-check command. |
| Package | A process that only its author can run is not reproducible; the run sheet and a `run-NAME` skill make it one sentence. |

## What the tool does and does not do

`forge.py new` scaffolds the pack for either engine (executable-oracle or blind-rubric), the run sheet, a `run-NAME` skill, a pending ledger row and the index entries. `forge.py check` is a completeness gate, ending in READY TO LOCK. It does not lock, does not run a real model, and cannot tell a good experiment from a complete one. The owner locks and runs.

## Limits

- The procedure was derived from this lab's own experience by its own tooling and assistant, so it can share that experience's blind spots.
- The rubric engine fixes the rated dimensions (novelty and coherence); the executable engine judges Python functions only.
- Two packs have been scaffolded or retro-fitted with it ([CVT-1](../05-experiments/cvt-1/README.md) and [AIL-H1c-001](../05-experiments/ail-moie-h1c-001/README.md)). Neither has been run on a real model.
