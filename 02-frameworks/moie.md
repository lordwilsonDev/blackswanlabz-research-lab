---
source: ~/Documents/Vault/30_Architecture/diagrams/Sovereign-Stack-Tooling/wiki/MoIE-Framework-2.0-revised.md
vault-date: 2026-09-15
captured: 2026-09-28
status: active
---

# Mixture of Inversion Experts (MoIE)

MoIE is a five-agent sequence that turns an AIL inversion into a falsifiable, evidence-grounded hypothesis. The revised framework note states the honest scope directly: MoIE "produces *novel hypotheses* by construction — it does not, on its own, produce *correct* ones. Correctness still requires the evidence-gathering and adversarial-testing stages built into the five-agent process below, and ultimately the same empirical validation any hypothesis needs."

## The five experts

1. **Inversion Critic** — identifies and inverts consensus assumptions. Purely generative; no validation at this stage.
2. **Positive Deviant Scout** — hunts for real, documented anomalies that violate the consensus. This is where empirical grounding actually happens; if no real anomalies exist for an inversion, the framework is supposed to say so immediately.
3. **Mechanism Synthesizer** — builds one unified framework that explains all the documented anomalies, not only convenient ones.
4. **Red Team** — adversarially attacks the synthesis: steelmans the consensus position, finds edge cases the model can't explain, anticipates expert objections.
5. **Prediction Generator** — derives falsifiable predictions from the model, specifying exactly what would disprove it.

## Crystal: from hypothesis to test

MoIE-Crystal is the implementation engine that sits downstream of the five agents and asks a different question — not "what hypothesis can be generated?" but "what is the smallest ethical, reversible test or implementation plan that can tell whether it deserves confidence?" It runs the MoIE output through a compression-and-clarity pass, a minimal implementation blueprint, a scenario sweep over key uncertainties, a risk/ethics/blast-radius review with kill-switch criteria, a staged execution ladder with a scale-or-archive decision fixed in advance, and a final crystallization into one operating thesis.

## The open question

Whether AIL+MoIE produces more novel hypotheses than a **compute-matched** best-of-n baseline — the same token budget spent on repeated single-pass sampling instead of the five-agent process — is an open, pre-registered empirical question, tracked here as [C-004](../CLAIMS.md), status pending. The benchmark package that would answer it states the stakes and its binding falsification condition:

> "If MoIE's advantage disappears under compute matching, the protocol is an expensive way to buy what temperature and resampling buy cheaply, and the paper's integration claim is false."
>
> "**Falsification condition:** if H1c fails across two independent replications, the paper's integration claim is false and must be reported as such. This commitment is binding regardless of outcome."

As of this capture, the benchmark package's own status line reads: "harness validated, experiment NOT YET RUN. No result in this package is experimental evidence."

## Sources

- `~/Documents/Vault/30_Architecture/diagrams/Sovereign-Stack-Tooling/wiki/MoIE-Framework-2.0-revised.md`
- `~/acts_mixture_of_inversion_experts/03_MOIE_CRYSTAL/000_README_FIRST.md`
- `~/projects/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE/ail_research_loop/spec.md` (§8, "MoIE Procedure")
- `~/acts_mixture_of_inversion_experts/09_META/000_ASSESSMENT_AND_HONEST_STATUS.md`
- `~/acts_mixture_of_inversion_experts/98_HERMES12_BENCHMARK/README.md`
