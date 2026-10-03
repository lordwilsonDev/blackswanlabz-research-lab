---
name: lab-forge
description: Turn an idea or claim into a pre-registered experiment pack, a run sheet and a one-sentence run-skill, using the lab's harnesses. Use when the user says "forge", "make a new experiment", "turn this into a harness and a skill", "build a test for this claim", or wants a process that others can run by saying "run the skill". Does not run the experiment or lock it; the owner locks.
---

# lab-forge

This skill reproduces the process that produced the lab's experiments: it takes a claim, scaffolds a locked-ready pack with the right engine, writes a run sheet and a `run-NAME` skill, adds a pending ledger row and the index entries, and gates the pack with a completeness check. The scripts are in this skill's `scripts/` folder. In a repo checkout: `python3 .claude/skills/lab-forge/scripts/forge.py --help`.

Never describe results as peer reviewed, externally validated or independently confirmed. Read `AGENTS.md` and `CLAIMS.md` first. Run `forge.py process` to print the eleven stages this tool encodes; the page `02-frameworks/forge-process.md` explains where each one came from.

## Ask the user for these (do not guess)

1. **The claim**, one sentence that can fail.
2. **How anyone would know.** If code can check it, the type is `executable` (engine `lab_harness.py`: tasks with visible and hidden tests). If it needs a judgement of quality, the type is `rubric` (engine `lab_rubric.py`: a blind judge from a different model family, with a second judge). If neither is possible, say so and write the same registration by hand at a weaker level, labelled as weaker.
3. **What would count as failure**, including that a tie fails, and the margin that counts as support. Fix it now, not after the data.
4. **Resources.** The hardware, the generator model, the judge models, and how much time the owner can spend.

## Steps

1. `forge.py new NAME --type executable|rubric --claim "..."`. It creates the pack, a run sheet, a `run-NAME` skill, a pending claim row and the index entries. It refuses to overwrite an existing pack.
2. Fill every `FILL` marker in `prereg.json` (and `prompts.json` for rubric packs) with the user. Add the tasks or questions. Write hidden tests with a model other than the one under test.
3. For an executable pack, `lab_harness.py selfcheck` must pass (reference passes, stub fails, a visible-only cheat is caught). For a rubric pack, run `lab_rubric.py controls --out controls.json` and record the power the decision rule has at the planned sample size. Tell the user plainly if the power is low.
4. Look for validity traps before locking: a context window shorter than the longest prompt, a hard-coded system prompt, a judge from the generator's family, tests the generator can see, any file that will be edited later. Make the adapter fail closed.
5. `forge.py check NAME`. Resolve everything it reports. It ends with `READY TO LOCK` when the pack is complete.
6. **Stop.** The owner runs `lock`, then the run commands from the run sheet, on their own machine. You do not lock, and you do not run a real model on the owner's behalf unless they ask. A fake adapter proves plumbing only.
7. After a real run exists, follow the `run-NAME` skill's report step. The claim stays `pending` until someone else reproduces it.
8. Run `scripts/verify.sh --offline` and the tests. New pages need headers and an `llms.txt` link (the scaffold adds both).

## Stopping rule

One revision pass after the controls pass, then freeze. The lab's known failure is building the measuring tool forever.

## Limits to tell the user

- The rubric engine fixes the rated dimensions as novelty and coherence. Other qualities need an extension.
- The harness judges Python functions only for executable packs.
- A pack that passes `check` is complete, not good. The same author usually writes the questions and the rubric.
- Nothing here has been run by a third party yet.
