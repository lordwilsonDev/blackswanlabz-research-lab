---
name: run-ail-moie-h1c-001
description: "Run the ail-moie-h1c-001 experiment (On 12 open research questions, does the AIL+MoIE five-stage procedure (C4) produce hypotheses rated more novel by a blind judge than ...). Use when the user says run ail-moie-h1c-001, use the run-ail-moie-h1c-001 skill, or asks to reproduce this test. Follows the registered pre-registration exactly and never edits it."
---

# run-ail-moie-h1c-001

This skill runs one registered experiment, `05-experiments/ail-moie-h1c-001`. First read `.claude/skills/lab-verify/SKILL.md` for the rules. Then follow this sheet.

## Rules that apply

- Never describe a result as peer reviewed, externally validated or independently confirmed.
- Never edit `prereg.json`, `questions.json` or `prompts.json` after the lock, and never edit result files. The harness refuses to run if they changed.
- The owner locks. If the pack is not locked yet, show the owner the pre-registration and ask them to run `lock`.
- A fake adapter is a harness test: say it is not evidence and do not quote its numbers.
- Report the registered decision first, then the numbers, then the limits. Results against the hypothesis get the same prominence.

## Ask the user first

1. The adapter command for the model under test (for Ollama: `python3 .claude/skills/lab-verify/scripts/ollama_adapter.py` with `OLLAMA_MODEL`).
2. A judge model of a different family from the generator, and a second judge (another family or a human).
3. A run note: the hardware and the models. Do not guess them.

## Steps

```bash
H=.claude/skills/lab-verify/scripts
D=05-experiments/ail-moie-h1c-001
python3 $H/lab_rubric.py controls --out $D/controls.json   # validates the decision rule on synthetic data
python3 $H/lab_rubric.py lock  $D                            # freezes prereg.json, questions.json, prompts.json (the owner does this)
OLLAMA_MODEL=GENERATOR python3 $H/lab_rubric.py run $D --adapter "python3 $H/ollama_adapter.py" --note "HARDWARE and GENERATOR"
python3 $H/lab_rubric.py blind $D                            # never show judges blind_key.json
OLLAMA_MODEL=JUDGE python3 $H/lab_rubric.py judge $D --adapter "python3 $H/ollama_adapter.py" --judge-id J1   # a different family
# second judge J2: another family, or a human via: lab_rubric.py import-ratings $D filled.csv --judge-id J2
python3 $H/lab_rubric.py analyze $D
python3 $H/lab_rubric.py report  $D
```
Set `OLLAMA_SYSTEM`, `OLLAMA_NUM_PREDICT` and `OLLAMA_NUM_CTX` for the experiment; the adapter fails closed if a prompt would overflow the context window.

## Return to the user

What was run and its output; the registered decision; the suggested ledger row (add it to `CLAIMS.md` as `pending`); what could not be verified. Add nothing as `verified` until someone else has reproduced it.
