---
source: BlackSwanLabz Research Lab record - CRT-1 — Context Reconstruction Test
captured: 2026-10-02
status: pending
---

# CRT-1 — Context Reconstruction Test

## Purpose

Test whether a fresh large language model can reconstruct the research program from its evidence substrate.

CRT-1 is not a learner benchmark. It measures transmission and reconstruction of the research specification.

## Context bundle

The investigator may receive selected chat history, GitHub repositories, repository snapshots, commit history, papers, experiments, benchmark specifications, claims ledger, evidence links, corrections, and retractions.

## Evidence-status vocabulary

Every extracted claim must be classified as:

VERIFIED
REPRODUCED
OBSERVED
AUTHOR-REPORTED
HYPOTHESIS
INTERPRETATION
SUPERSEDED
RETRACTED
UNRESOLVED

## Reconstruction tasks

The model must reconstruct:

1. Research chronology
2. Method genealogy
3. Benchmark definitions
4. Metric dictionary
5. Claim and evidence matrix
6. Benchmark dependencies
7. Experimental arms
8. Verification rules
9. Falsification rules
10. Resource-normalization rules

## Epistemic firewall

The investigator model must not convert hypotheses into results, treat README claims as independently verified without evidence status, infer learning from correctness alone, infer novelty from absence of search hits, interpret TCR as an intelligence quotient, infer that rater divergence is inherently meaningful, equate calendar duration with effort, or treat model-generated explanations as proof.

## Scoring

CRT-1 reports recovery of definitions, metrics, dependencies, chronology, evidence states, and benchmark logic.

False inferences and omissions are reported separately.

The test asks whether the research specification survives transmission, not whether the model can summarize the documents.
