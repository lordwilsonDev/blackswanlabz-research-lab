---
name: run-cvt-1
description: "Run the cvt-1 experiment (On 24 small Python tasks, does a small local model that sees the failure message of a failed attempt (arm C) solve more hidden tests than ...). Use when the user says run cvt-1, use the run-cvt-1 skill, or asks to reproduce this test. Follows the registered pre-registration exactly and never edits it."
---

# run-cvt-1

This skill runs one registered experiment, `05-experiments/cvt-1`. First read `.claude/skills/lab-verify/SKILL.md` for the rules. Then follow this sheet.

## Rules that apply

- Never describe a result as peer reviewed, externally validated or independently confirmed.
- Never edit `prereg.json`, `tasks.json` after the lock, and never edit result files. The harness refuses to run if they changed.
- The owner locks. If the pack is not locked yet, show the owner the pre-registration and ask them to run `lock`.
- A fake adapter is a harness test: say it is not evidence and do not quote its numbers.
- Report the registered decision first, then the numbers, then the limits. Results against the hypothesis get the same prominence.

## Ask the user first

1. The adapter command for the model under test (for Ollama: `python3 .claude/skills/lab-verify/scripts/ollama_adapter.py` with `OLLAMA_MODEL`).
2. A run note: the hardware and the model. Do not guess them.

## Steps

```bash
H=.claude/skills/lab-verify/scripts
python3 $H/lab_harness.py selfcheck 05-experiments/cvt-1      # after you lock; must say SELF-CHECK OK
python3 $H/lab_harness.py lock      05-experiments/cvt-1      # freezes prereg.json and tasks.json (the owner does this)
python3 $H/lab_harness.py selfcheck 05-experiments/cvt-1
python3 $H/lab_harness.py run 05-experiments/cvt-1 --adapter "python3 $H/ollama_adapter.py" --note "HARDWARE and MODEL"
python3 $H/lab_harness.py analyze 05-experiments/cvt-1
python3 $H/lab_harness.py report  05-experiments/cvt-1
```
(Run `selfcheck` once before locking to catch bad tasks, and again after.)

## Return to the user

What was run and its output; the registered decision; the suggested ledger row (add it to `CLAIMS.md` as `pending`); what could not be verified. Add nothing as `verified` until someone else has reproduced it.
