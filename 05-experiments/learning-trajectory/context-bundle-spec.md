---
source: BlackSwanLabz Research Lab record - Research Context Bundle Specification
captured: 2026-10-02
status: pending
---

# Research Context Bundle Specification

## Purpose

Provide any investigating large language model with enough structured evidence to understand the research program, reconstruct its history, implement the benchmark, and interpret its metrics without relying on unstated context.

## Inputs

The context bundle may include chat history, GitHub repositories, repository file snapshots, commit metadata, experiment logs, white papers, benchmark specifications, claims ledger, evidence links, corrections, and retractions.

## Source manifest

Each source records:

- source_id
- source_type
- URI or repository reference
- snapshot date
- commit or version when applicable
- provenance status
- confidentiality class
- extraction status

## Reconstruction sequence

1. Build a chronology.
2. Extract claims.
3. Bind claims to evidence.
4. Classify epistemic status.
5. Reconstruct method genealogy.
6. Reconstruct benchmark dependencies.
7. Recover metric contracts.
8. Recover experimental conditions.
9. Identify known confounds and unresolved defects.
10. Reconstruct implementation requirements.

## Source and evidence rule

Raw conversation is historical evidence, not automatic truth.

Repository README text is an author claim unless independently verified.

Experiment output is a result only under the conditions documented by the experiment.

## Learner-context separation

The full research context may be available to the investigator.

The participant receives only preregistered benchmark inputs.

The context bundle must never become accidental hidden assistance to the benchmark participant.

## Reproducibility target

A fresh investigator model should recover the benchmark family, metric definitions, experimental arms, verification rules, falsification criteria, and current version intended for execution.

CRT-1 is the formal test of this reconstruction property.
