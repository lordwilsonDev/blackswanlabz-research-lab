---
name: lab-verify
description: Run the BlackSwanLabz verification process on a new idea that has no outside standard. Use when the user says "run the skill", "use the harness", "pre-register this", "verify this", "run CVT-1", or asks to test a claim cheaply with a small or local model. Walks through defining the standard, pre-registering, self-checking the instrument, running once, and reporting honestly, using scripts/lab_harness.py. Does not seek or claim peer review.
---

# lab-verify

You are running the lab's own verification process. There is no outside standard for the thing being tested and outside peer review is not the goal. Never describe a result as peer reviewed, externally validated or independently confirmed. The lab writes its standard first, fixes it before looking at results, and reports what it finds either way.

Read `AGENTS.md` and `CLAIMS.md` in the repo first if they exist. A claim is established only when its `CLAIMS.md` row says `verified`. `pending` is never restated as fact. Retracted claims stay visible. Procedures and plans are not evidence.

The harness is `scripts/lab_harness.py` in this skill's folder (stdlib Python, no installs). Run `python3 <skill>/scripts/lab_harness.py --help` to see it. In a repo checkout the path is `.claude/skills/lab-verify/scripts/lab_harness.py`.

## Ask the user for four things (do not guess them)

1. **The question**, one sentence, answerable by running code. If it cannot be checked by running code, say so and use the "No executable oracle" section below.
2. **The tasks.** Each needs a `prompt`, the `function` name, `visible` asserts (shown to the model), `hidden` asserts (never shown), and a `ref` reference solution. If you generate tasks, do not let the model being tested write the hidden tests, and keep the hidden tests out of its prompts.
3. **The adapter**: the shell command that runs the model under test. It reads the prompt on stdin and prints the reply. For Ollama use `python3 <skill>/scripts/ollama_adapter.py` with `OLLAMA_MODEL=qwen3:8b`. Any command works: `claude -p`, a Freebuff wrapper, a script.
4. **A run note**: hardware and model (for example "Mac mini M4, 16 GB, qwen3:8b q4"). Do not guess hardware.

## Steps

1. `new NAME` (or use `05-experiments/cvt-1`, which is already filled). Write `prereg.json` and `tasks.json`.
2. **Fill the pre-registration before anything runs**: question, hypothesis, arms, which two arms are compared, the margin, the falsification condition, honest limits, and a stopping rule. A tie must count as failure. Do not set the margin after seeing numbers.
3. `lock DIR`. This refuses an incomplete pre-registration and fewer than 5 tasks, then hashes the files. After this, changing either file makes `run` refuse. If something must change, make a new experiment directory and say why.
4. `selfcheck DIR`. Every reference must pass its tests, a stub must fail the visible tests, and a visible-only cheat must be caught by the hidden tests. If it fails, fix the tasks and start a new directory if you already locked. Do not run an untested instrument.
5. `run DIR --adapter "..." --note "..."`. It runs once, and refuses to run a second time or after any edit. This can take a long time on a small machine; tell the user and wait. Never edit `results.jsonl`.
6. `analyze DIR`, then `report DIR`. Report the **registered decision first**, then the descriptive numbers, then the limits. Report results against the hypothesis as prominently as results for it. A fake-adapter run is a harness test: say it is not evidence and do not quote its numbers.
7. **Ledger.** Add the suggested row from `REPORT.md` to `CLAIMS.md` as `pending`. Change it to `verified` only after someone other than the run's author has re-run it, or after you have independently checked the evidence. Add any new page to `llms.txt`, give it a front-matter header, and run `scripts/verify.sh --offline` and the tests.
8. **Stop tightening.** The lab's known failure is building the measuring tool forever. After the self-check passes, one revision pass, then freeze and run.

## Return to the user

A short report: what was run, which commands and their output, the registered decision, the claim row you added, and what is still pending and why. State what you could not verify and what you could not reach.

## If you are in claude.ai (no shell access to the user's machine)

You can scaffold, pre-register, lock, self-check, analyze and report, but you cannot run a model on the user's own computer. Have the user run the `run` step on their machine with their adapter, then upload `results.jsonl` and `RUN.json` so you can run `analyze` and `report`. Say that this split happened.

## Rubric-judged experiments (`scripts/lab_rubric.py`)

Use this engine when the claim is about a quality code cannot check (for example, "this method produces more novel hypotheses") and the standard is therefore a rubric applied blind by a judge that is not the generator. Say in every report that this is a weaker standard than an executable check. The worked example is `05-experiments/ail-moie-h1c-001`.

1. The pack holds `prereg.json`, `questions.json` and `prompts.json`. `lock DIR` hashes all three. The prompts are part of the registration: editing a prompt after the lock makes `run` refuse.
2. `run DIR --adapter "..."` generates every arm, sets each best-of-n baseline's size so its total tokens (including the selector call) match the treatment's budget, and writes `gen.jsonl` and `plan.json`.
3. `blind DIR` shuffles the final texts into `blind_items.json` and `blind_items.csv` and writes a private `blind_key.json`. Never show a judge the key or any arm label.
4. `judge DIR --adapter "..." --judge-id J1`, with a model of a different family from the generator. Add a second judge (another family, or a human via `import-ratings`) so agreement can be computed. If a judge shares the generator's adapter, the report says the result is not independent.
5. `analyze DIR`, then `report DIR`. The decision is registered in advance (paired sign-flip test, Holm correction, Hedges g, Krippendorff alpha). Judge agreement below the registered minimum makes the result INCONCLUSIVE, not supported.
6. `controls` runs the decision rule on synthetic null and planted-effect data. Run it before you trust any real result, and record what it shows about the rule's power.
7. Use an adapter that fails closed when a prompt would overflow the model's context window; a silently truncated prompt corrupts the arm that depends on long context.

## No executable oracle

Use the next standard available and label it weaker, never as equivalent: a rubric fixed in advance and applied by a different model, a cross-model reconstruction (a fresh model rebuilds the result from the evidence alone), an adversarial replay, or a dated prediction with a check date. The harness does not run these; write the same pre-registration by hand and keep the same rules.

## Limits to tell the user

- The harness judges Python functions only. Other oracles (shell commands, files, measurements) need an extension.
- The same author usually writes visible and hidden tests, so false passes are only caught for cases the author thought of.
- The auto-cheat is a lookup of the visible asserts. It proves the hidden tests add something, not that they are good.
- Token counts come from the adapter. Without them the harness uses length divided by four.
- Seeds are only honoured if the adapter reads `HARNESS_SEED` (the Ollama adapter does).
