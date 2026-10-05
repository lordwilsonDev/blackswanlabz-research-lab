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

Locked; run complete 2026-10-05. Results are recorded below by the assistant exactly as the harness reports them, whichever way they fall. Status stays **pending** until someone other than the run's author has reproduced it.

## Results (2026-10-05)

**Registered decision (H1c): SUPPORTED**, with the registered caveat that independence is not met, so this does not establish the claim and needs replication with judges from another family or human raters. Full numbers: [REPORT.md](REPORT.md), [ANALYSIS.json](ANALYSIS.json).

| contrast | novelty difference | Hedges g | Holm p | coherence difference | coherence non-inferior |
|---|---|---|---|---|---|
| C4 vs C1-bon | +0.604 | +0.79 | 0.0117 | -0.125 | yes |
| C4 vs C2-bon | +1.208 | +1.74 | 0.0007 | -0.188 | yes |
| C4 vs C3-bon | +0.792 | +1.07 | 0.0024 | -0.458 | **no** |

Judge agreement (Krippendorff alpha, novelty) 0.782; 336 ratings from J1 (Sonnet) and J2 (Opus); generator Haiku.

What weakens it, from the report's own flags:

- **Declared deviation.** Best-of-n was capped at 20 samples (the registered matching needed about 40 to 70 for C1 and C2). C1-bon and C2-bon therefore got 0.375 and 0.353 of the treatment's tokens, not 1.0. The cap was chosen before any baseline output existed and favours the treatment. C3-bon, where the cap rarely bound, got 0.93 of the budget and is the fairest contrast: g +1.07, but its coherence is not non-inferior.
- **Length.** C4's mean answer is 145 words against 74 to 110 for the controls. A judge may rate longer, richer text as more novel.
- **Judges are Claude models** (same vendor as the generator). The report flags possible self-preference.
- 12 questions, one generator, one run, and the CLI gives no seed.

The run was interrupted twice by sandbox restarts and resumed with `--resume`; each resume is in `RUN.json`. Its deviation timestamp was overwritten by the second resume and restored by hand to the first (noted in `RUN.json`); the code now keeps the first declaration. Status stays **pending** until someone other than the run's author has reproduced it.
