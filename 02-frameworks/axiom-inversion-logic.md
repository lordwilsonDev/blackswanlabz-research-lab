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

## Existing cross-domain evidence and open comparative questions

**Cross-domain artifact production is documented; do not confuse that with an unrun comparative benchmark.** The [Doctoral Artifact Battery](../docs/doctoral-artifact-battery-v1.md) inventories pre-existing work in AI systems, software engineering, formal verification, mathematics, security/governance, research methods, automation, question engineering, and other fields. The record includes actual repositories such as [MSB v3](../03-systems/msb-v3.md) and [FCVE](../03-systems/fcve.md); it does not start from an empty capability baseline. Count exact domains from a domain-to-artifact matrix, not from overlapping category names.

The [Q2B-MBEDDR-001 state-machine run](../05-experiments/learning-trajectory/runs/q2b-mbeddr-001-state-machine.md) also records **a bounded structural-transfer demonstration**: six initial behavior checks passed, three verifier challenges passed after a documented correction, four fresh traffic-light-controller transfer checks passed after an instrumentation correction, and five pedestrian-capability extension checks passed after a further instrumentation correction. That run labels L4 transfer demonstrated, L5 extension provisional, and independent reconstruction and retention pending. These are author-side recorded results, not a universal transfer-rate estimate.

### Distinguish three questions

1. **Were artifacts built and tested in multiple domains?** Yes: the linked portfolio and run records document multiple domain-specific artifacts and tests. Assess each artifact by its actual evidence status; do not downgrade the entire portfolio to an untested proposal.
2. **Has any concrete cross-domain/structural transfer been demonstrated?** Yes, in bounded recorded exercises such as Q2B-MBEDDR-001. This does not by itself establish transfer by independent human operators across every domain or expertise level.
3. **Does AIL+MoIE outperform a compute-matched best-of-n baseline, and is there a documented 100% success rate across 23+ domains?** These are separate quantitative claims. The original `MoIE_Complete_Operating_System.docx` package did not include underlying run records for its 23+ domains / 100% assertions. That limitation is **scoped to that package**; it does not negate the other artifacts linked above. The [Hermes12 comparison](../05-experiments/hermes12-benchmark.md) has not been run, so the comparative advantage tracked by [C-004](../CLAIMS.md) remains **pending**.

**Evidence rule:** distinguish demonstrated artifact breadth, bounded transfer results, broad operator-to-operator generalization, and compute-matched causal advantage. Neither the absence of records in one package nor the status of one benchmark determines the status of the whole research program.

## Sources

- `~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/Axiom-Forge-Director.md`
- `~/acts_mixture_of_inversion_experts/01_AIL_ACT/000_README_FIRST.md`
- `~/projects/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE/ail_research_loop/spec.md` (§7, "AIL Procedure")
- `~/acts_mixture_of_inversion_experts/09_META/000_ASSESSMENT_AND_HONEST_STATUS.md`
