---
source: ~/acts_mixture_of_inversion_experts/98_HERMES12_BENCHMARK/README.md
captured: 2026-09-28
status: pending
---

# Hermes12 benchmark

Pre-registered replication package for *Axiom Inversion Logic and the Mixture of Inversion Experts* (AIL-WP-2026-08-005) — the paper this package tests is itself **not located** in this machine or in any repo checked as of 2026-09-28 (see [04-papers/README.md](../04-papers/README.md)). The package is local-only: `~/acts_mixture_of_inversion_experts/98_HERMES12_BENCHMARK/`. ACTS has no git remote, so there is no `repo`/`commit` pin for this page — the package is not yet published anywhere else.

> **Harness validated; experiment not yet run. No result exists.** See [C-004](../CLAIMS.md).

## The claim being tested

Not "AIL+MoIE beats a single pass" — that is unsurprising and proves nothing on its own. The primary test is whether MoIE beats **compute-matched** baselines: best-of-n single-pass prompting given the same token budget as MoIE used. If the advantage disappears under compute matching, the protocol is an expensive way to buy what temperature and resampling buy cheaply.

## Conditions and compute-matched arms

| ID | Condition |
|---|---|
| C1 | baseline few-shot |
| C2 | chain-of-thought |
| C3 | tree-of-thoughts (branch → evaluate → expand) |
| C4 | AIL+MoIE, internal knowledge only |
| C5 | AIL+MoIE + retrieval-backed anomaly search |
| C1-bon / C2-bon / C3-bon | compute-matched best-of-n versions of C1–C3 |

Compute matching: per question, run C4 and C5, take budget `B = mean(tokens)`. For each baseline, measure single-pass cost `s`, set `n = round(B/s)`, re-run as best-of-n; the best-of-n selector call is charged to the baseline's own budget (deliberately conservative against the MoIE hypothesis).

## Pre-registered hypotheses

- **H1** — novelty(C4,C5) > novelty(C1,C2,C3). Weak test; passing H1 alone is not evidence.
- **H1c** — novelty(C4,C5) > novelty(C1-bon,C2-bon,C3-bon). **PRIMARY.**
- **H2** — novelty(C5) > novelty(C4).
- **H3** — coherence(C4,C5) not materially lower than matched baselines (TOST, margin 0.5).

## Success criterion

Holm-adjusted p < 0.05 **and** Hedges' g > 0.5 on H1c.

## Binding falsification condition (quoted verbatim from the package README)

> "if H1c fails across two independent replications, the paper's integration claim is false and must be reported as such. This commitment is binding regardless of outcome."

## What has and has not happened

The package contains a harness (`harness.py`), blinding/sealing tooling (`blind.py`), and a frozen analysis plan (`analyze.py` — Krippendorff's α, Hedges' g, Holm-Bonferroni, TOST). The `validation/` directory holds only synthetic pipeline controls (null test, positive test, near-threshold controls) used to verify the analysis code behaves correctly before spending API budget or rater time — **none of these say anything about whether MoIE works**, and none is a run of the actual 16-question pilot set against real conditions.

The README also records dated audit notes (2026-09-19) about defects found and fixed in the analysis scripts themselves (a p-value range assertion, an under-specified effect-size standardizer, and under-specified contrast-family/alpha/reliability-caveat handling) — those are process/tooling corrections to the frozen plan, not experimental results, and they do not change the fact that no confirmatory run has happened.

**No experiment has been run. No number in this page is a result.**
