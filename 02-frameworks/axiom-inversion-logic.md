---
source: ~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/Axiom-Forge-Director.md
vault-date: 2026-08-25
captured: 2026-09-28
status: active
---

# Axiom Inversion Logic (AIL)

AIL is the reasoning operator behind the "Axiom Forge" hypothesis-generation engine: it finds an assumption a field treats as settled, inverts it, and asks what would have to be true for the inversion to hold.

## The move

The formal spec (`ail_research_loop/spec.md` §7, "AIL Procedure") states the operator as six steps:

1. Identify at least one load-bearing assumption.
2. State why the assumption matters.
3. Construct a meaningful inversion.
4. Derive the alternative mechanism.
5. State the observable consequence.
6. Identify at least one condition where the inversion should fail.

The spec is explicit about what an inversion is not:

> **`INVERSION != PROOF`**
>
> An inversion can only create a candidate explanation.

The Axiom Forge Director doc states the same limit as an operating law: "Inversion is a generator, not evidence — every inversion must earn credibility through evidence and prediction," alongside "Consensus is a prior, not a fact" and "Don't confuse novelty with truth — a strange idea isn't a breakthrough unless it improves explanation, prediction, capability, or understanding."

## The Axiom Forge phases

The Axiom Forge Director spec runs the move through 11 phases, in order:

0. Problem Reconstruction — rewrite the input as a precise research problem and define what "breakthrough" means for the domain.
1. Consensus Map — build the strongest fair version of the mainstream model.
2. Inversion Field — generate 7–12 candidate inversions across named types (polarity, conditional, level, measurement, causal, population, timescale, resource, boundary) and score/select the top three.
3. Neglected-Evidence Retrieval — search for what an ordinary consensus-oriented answer would omit; label each finding verified anomaly / conditional exception / unresolved contradiction / weak signal / not an anomaly.
4. Cross-Domain Transfer — search adjacent domains for structurally similar mechanisms.
5. Mechanism Construction — build competing models and select a provisional one without forcing a single model onto unrelated anomalies.
6. Breakthrough Candidate — state the claim in five forms and score it; label it a "promising hypothesis" rather than a breakthrough if it misses the domain's minimum threshold.
7. Adversarial Red Team — attack the candidate as if disproving it were the goal; revise once, preserving the original.
8. Prediction Engine — generate falsifiable predictions, at least three "risky" under the consensus model.
9. Minimal Test — design the smallest ethical, affordable, reversible test with explicit stop conditions.
10. Final Output — an ordered report ending in a confidence label (Established / Supported / Promising / Speculative / Rejected) and three closing sentences: the deepest overlooked pattern, why it matters, and the fastest way to find out if it's real.

## What keeps it honest

The AIL ACT operating skill states the posture directly: "Be permissive about generating hypotheses and strict about characterizing claims." The formal spec makes falsifiability a hard requirement: "every active hypothesis has at least one explicit failure condition," predictions are frozen once a research cycle reaches the `PREREGISTERED` state, and a hypothesis with a materially new, unrepresented observation is routed to `NOVEL` rather than silently absorbed. Evidence quality is weighted, not just counted — executed code and real datasets carry a 1.00 source-reliability multiplier in the JEV decision procedure, while an unexecuted model assertion carries 0.20.

## What is not yet shown

The package's own self-assessment is direct about the gap between the method's design and its evidence base:

> **"'100% success rate' and '23+ domains' are not evidenced in the package."** The MoIE_Complete_Operating_System.docx makes those claims directly. The package does not include the underlying run record for 23 domains, and the benchmark companion (hermes12) explicitly says the experiment is not yet run. So the strongest empirical claim in the package is unsupported by anything inside the package. Read it as the author's stated thesis, not as established fact.

Whether AIL+MoIE actually outperforms a compute-matched baseline is the open, pre-registered question tracked as [C-004](../CLAIMS.md) — status pending.

## Sources

- `~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/Axiom-Forge-Director.md`
- `~/acts_mixture_of_inversion_experts/01_AIL_ACT/000_README_FIRST.md`
- `~/projects/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE/ail_research_loop/spec.md` (§7, "AIL Procedure")
- `~/acts_mixture_of_inversion_experts/09_META/000_ASSESSMENT_AND_HONEST_STATUS.md`
