---
source: pre-registration and run sheet written in this repo during research session 2026-10-03
captured: 2026-10-03
status: pending
---

# AIL-H1c-001: does AIL+MoIE beat compute-matched best-of-n?

**Not run.** This is the lab's second instrument for the primary hypothesis of the Hermes12 pre-registration (H1c; claim [C-004](../../CLAIMS.md)). The original Hermes12 package lives only on the owner's machine and could not be read from the session that built this one. This instrument is built from the lab's framework pages ([AIL](../../02-frameworks/axiom-inversion-logic.md), [MoIE](../../02-frameworks/moie.md), [Hermes12](../hermes12-benchmark.md)). Whether it counts as one of the two independent replications the original pre-registration requires is the lab's call. Process: [lab-verify skill](../../.claude/skills/lab-verify/SKILL.md), engine `lab_rubric.py`.

## The question

On 12 open research questions, does the AIL+MoIE five-stage procedure (arm C4) produce hypotheses that a blind judge rates more novel than compute-matched best-of-n versions of few-shot, chain-of-thought and tree-of-thoughts prompting (arms C1-bon, C2-bon, C3-bon), using the same model and the same total token budget?

## What has been run, and what has not

| Step | Status |
|---|---|
| Analysis rule validated on synthetic data | **Run.** [controls.json](controls.json): 500 simulated datasets per case, 12 questions. No effect: decision SUPPORTED in 0 of 500. Planted effect of 1.0 rating point: 216 of 500 (43%). Planted effect of 2.0 points: 498 of 500 (99.6%). Perfect rater agreement gives alpha 1.000; independent ratings give 0.045. ([C-054](../../CLAIMS.md)) |
| Full pipeline with fake model and fake judge | **Run**, plumbing only, results stamped NOT EVIDENCE. Compute matching landed within 0.89 to 0.97 of the treatment's budget. |
| Real generation, blind judging, registered decision | **Not run.** It needs a local generator model (hours of generation) and a judge of a different model family. The session that built this instrument had neither, and using one model as both generator and judge would break the registered independence requirement. |

The 43% figure matters: the registered rule is strict (all three contrasts must be significant after Holm correction and each effect size must exceed 0.5), so with 12 questions a modest real effect will often not be detected. A "not supported" result is therefore weaker evidence against AIL+MoIE than a "supported" result is for it. The report states this.

## Run it on the Mac mini

Hardware to record in the run note: Mac mini M4, 16 GB unified memory. Use two different model families, one to generate and one to judge.

```bash
ollama pull qwen3:8b          # generator
ollama pull llama3.1:8b       # judge: a different family from the generator (any other family works)
H=.claude/skills/lab-verify/scripts
D=05-experiments/ail-moie-h1c-001
export OLLAMA_SYSTEM="You are a careful research assistant."
export OLLAMA_NUM_PREDICT=700 OLLAMA_NUM_CTX=8192     # MoIE stage prompts accumulate; a short window would truncate them

python3 $H/lab_rubric.py lock $D                       # freezes prereg.json, questions.json, prompts.json
OLLAMA_MODEL=qwen3:8b python3 $H/lab_rubric.py run $D --adapter "python3 $H/ollama_adapter.py" \
   --note "Mac mini M4 16GB, qwen3:8b via Ollama"       # about 2 to 4 hours (an estimate); resumes are not supported
python3 $H/lab_rubric.py blind $D                       # shuffles texts; never show judges blind_key.json
OLLAMA_MODEL=llama3.1:8b python3 $H/lab_rubric.py judge $D --adapter "python3 $H/ollama_adapter.py" --judge-id J1
# second judge J2: a model of a third family, or a human: rate blind_items.csv and run
#   python3 $H/lab_rubric.py import-ratings $D filled.csv --judge-id J2
python3 $H/lab_rubric.py analyze $D
python3 $H/lab_rubric.py report $D
```

The adapter fails closed if a prompt fills the context window, so a truncated MoIE stage cannot corrupt arm C4 silently. If the run dies partway, move `gen.jsonl` aside, note why, and start again; partial results are not spliced.

Or in Claude Code, say: **use the lab-verify skill and run AIL-H1c-001** (the skill runs the commands above and asks you for the judge model).

## What the report will contain

The registered decision first (SUPPORTED, NOT SUPPORTED, or INCONCLUSIVE when judge agreement alpha is below 0.4), then the three contrasts with Holm-adjusted p, Hedges g and coherence non-inferiority, then tokens and words per arm, then flags: judge not independent, one judge only, compute match outside 0.85 to 1.15, length differing by more than 30%. It ends with a suggested `pending` ledger row.

## Registered limits

See `limits` in [prereg.json](prereg.json). In short: a rubric judged by a model is a weaker standard than an executable check; the sample is small; one generator model; the scout stage uses the model's own knowledge so cited anomalies are unverified; blinding hides labels but not style.
