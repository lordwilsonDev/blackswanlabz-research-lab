---
source: pre-registration and run record written in this repo during research session 2026-10-03
captured: 2026-10-03
status: pending
---

# AIL-H1c-002: AIL+MoIE against compute-matched best-of-n, Claude Haiku generator

The same question, questions, prompts and decision rule as [ail-moie-h1c-001](../ail-moie-h1c-001/README.md), configured to run in a cloud session that has only Claude models: a **Claude Haiku generator** and **Claude Sonnet and Claude Opus judges**, called through the `claude` CLI. The owner asked for this run ("just use a haiku model"). The registration was locked and committed to git before any generation call; the assistant ran the lock at the owner's instruction.

## What differs from 001, and why it matters

| | 001 (not run) | 002 (this run) |
|---|---|---|
| Generator | a local model on the owner's Mac mini | Claude Haiku (resolved model id recorded in the adapter log) |
| Judges | models or humans of a different family from the generator | Claude Sonnet and Claude Opus: **same vendor as the generator, independence not met** |
| Seed and temperature | controlled through Ollama | not controllable through the CLI; runs are not exactly reproducible |
| Token accounting | reported by Ollama | output tokens reported by the API; input tokens estimated as characters / 4 |

Because independence is not met, the registered falsification condition says: a NOT SUPPORTED result stands, and a SUPPORTED result does not establish the claim and needs replication with judges from another family or human raters. The decision rule, margins, sample size and controls are unchanged; its power at 12 questions is in [controls.json](controls.json) (a 1-point effect is detected 43% of the time).

## How it is run

```bash
H=.claude/skills/lab-verify/scripts
D=05-experiments/ail-moie-h1c-002
python3 $H/lab_rubric.py lock $D
export CLAUDE_ADAPTER_LOG=$D/adapter.log CLAUDE_SYSTEM="You are a careful research assistant."
CLAUDE_MODEL=haiku python3 $H/lab_rubric.py run $D --adapter "python3 $H/claude_adapter.py" --note "..."
python3 $H/lab_rubric.py blind $D
CLAUDE_MODEL=sonnet python3 $H/lab_rubric.py judge $D --adapter "python3 $H/claude_adapter.py" --judge-id J1
CLAUDE_MODEL=opus   python3 $H/lab_rubric.py judge $D --adapter "python3 $H/claude_adapter.py" --judge-id J2
python3 $H/lab_rubric.py analyze $D && python3 $H/lab_rubric.py report $D
```

## Status

Locked; run in progress. Results, if any, are recorded below by the assistant exactly as the harness reports them, whichever way they fall. Status stays **pending** until someone other than the run's author has reproduced it.
