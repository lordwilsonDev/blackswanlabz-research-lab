---
source: https://github.com/lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE/blob/765979bda8b7fb5be123261578fdd4cf0d943c53/AIL_MoIE_Recursive_Research_Protocol.pdf
repo: lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE
commit: 765979bda8b7fb5be123261578fdd4cf0d943c53
captured: 2026-09-28
status: active
---

# AIL + MoIE Recursive Research Protocol

A 6-page PDF: *AIL + MoIE Recursive Research Re-Entry Protocol — A production-ready specification for evidence-governed, AI-assisted research and engineering*. It is the design document for the evidence-in/theory-update-out loop that [ACTS](../02-frameworks/acts-5-act-research.md) and the [AIL research loop](../02-frameworks/axiom-inversion-logic.md) implement.

Governing rule stated on page 1: *"The experiment decides. The evidence updates the system. The updated system asks the next question."*

Read it at the pinned commit: [AIL_MoIE_Recursive_Research_Protocol.pdf](https://github.com/lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE/blob/765979bda8b7fb5be123261578fdd4cf0d943c53/AIL_MoIE_Recursive_Research_Protocol.pdf).

The machine-readable version of the same protocol — the one the reference implementation actually runs — is [`ail_research_loop/spec.md`](https://github.com/lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE/blob/765979bda8b7fb5be123261578fdd4cf0d943c53/ail_research_loop/spec.md).

## Section headings (extracted with pypdf from the PDF's own text, no bookmarks/outline present)

1. Purpose and scope
2. Complete research loop
3. Non-negotiable rules
4. Research state model
5. Evidence package
6. Typed evidence record
7. JEV evidence-relation analysis
8. Theory update protocol
9. Experiment selection
10. Quality gates
11. Stop, escalate, or continue
12. Research memory and audit trail
13. Minimum artifact set
14. Final operating statement

## What it covers, in brief

The research loop it specifies: `Problem → Axioms and assumptions → Inversion → Competing mechanisms → Hypothesis → Prediction → Experiment design → Execution → Results → Evidence synthesis → JEV analysis → Theory update → Next hypothesis / test`.

Non-negotiable rules (§3) require separating observation, derived result, interpretation, and causal conclusion; forbid promoting a causal claim solely because an observation is consistent with it; require every major claim to point to a source dataset, experiment ID, analysis method, and execution environment; and require a failed hypothesis to be retained as evidence.

§7 defines JEV (the evidence-relation classifier used elsewhere in this lab) with relations `EQUAL | NOT_EQUAL | PARTIAL | CONDITIONAL | CONFOUND | UNKNOWN | NOVEL`, each with a required next action rather than a verdict.

§13 lists the minimum artifact set a completed research cycle must produce: research brief, assumption/inversion register, mechanism map, hypothesis/prediction ledger, experiment protocol, evidence package with provenance manifest, JEV adjudication record, theory-update record, next-test decision memo, and a final white paper.
