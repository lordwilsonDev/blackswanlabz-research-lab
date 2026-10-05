# Doctoral Artifact Battery — v1.0

## Purpose

A preregistered-style artifact battery for testing whether AI-mediated, self-directed learning can enable a person without conventional domain training to produce artifacts comparable in function to those expected from advanced doctoral researchers.

The unit of evaluation is the artifact, not the author's biography.

## Core rule

Freeze requirements before construction. Evaluate the finished artifact independently. Do not use educational background to inflate or lower artifact scores.

## Ten artifacts

### 1. Original Research Dissertation
Produce a doctoral-style dissertation in one chosen field.

Required: title, abstract, research problem, research questions, literature review, state of the field, research gap, hypotheses/propositions, methodology, experiments, results, statistical analysis where applicable, threats to validity, alternative explanations, limitations, original contribution, future work, references, reproducibility appendix, complete research repository.

Verification: independent literature check, methodological review, blind evaluation, reproduction attempt.

### 2. Original Computer Science System
Build a nontrivial research system.

Required: requirements, architecture, threat model, interfaces, implementation, unit/integration/adversarial tests, performance evaluation, failure analysis, security analysis, reproducibility environment, documentation, benchmark, source repository.

Verification: independent operator runs the system from the instructions.

### 3. Formal Mathematics Artifact
Investigate a nontrivial proposition, conjecture, proof, or counterexample.

Required: definitions, known results, proposition/conjecture, proof attempt, counterexample search, computational exploration, formalization, machine-checked proof when possible, failed approaches, boundary conditions, final status.

Allowed final statuses: PROVED, DISPROVED, COUNTEREXAMPLE, UNRESOLVED, PARTIAL, BLOCKED.

### 4. Experimental Science Paper
Conduct a controlled empirical experiment.

Required: research question, hypothesis, preregistration, variables, controls, sample design, measurement protocol, data, analysis plan, results, uncertainty, negative results, limitations, replication package.

Rule: freeze the analysis plan before examining final results.

### 5. Cybersecurity Research Artifact
Build and evaluate a defensive security system.

Required: threat model, assets, attack surfaces, defensive mechanism, false-positive/false-negative tests, bypass attempts, adversarial inputs, performance, degradation and failure analysis, research paper.

Verification: independent tester attempts to defeat the defense.

### 6. Linguistics / Communication Research
Conduct an original empirical study of language or communication.

Required: research question, theoretical framework, corpus/dataset, annotation scheme, coding rules, inter-rater agreement, analysis, competing hypotheses, results, limitations, reproducible dataset and paper.

Verification: independent researcher applies the annotation rules to unseen examples.

### 7. Economics / Decision Science Study
Conduct a quantitative investigation of a real economic or decision question.

Required: research question, theoretical model, assumptions, dataset, variable definitions, identification strategy, statistical model, robustness checks, alternative explanations, sensitivity analysis, results, limitations, reproducibility package.

Adversarial requirement: attempt to produce evidence against the preferred explanation.

### 8. Engineering Verification & Validation Package
Demonstrate that a system satisfies an explicit specification.

Required: requirements R1..Rn, architecture, implementation, verification matrix, tests, evidence, validation, boundary conditions, fault injection, recovery, degraded operation, traceability matrix, final verification and validation reports.

Key distinction: demonstrate not merely that the system was built, but that it satisfies defined requirements.

### 9. Independent Replication
Select an external published result and attempt to reproduce it.

Required: original claim, original methodology, required inputs, independent implementation, deviations, reproduction results, statistical comparison, discrepancy analysis, final replication verdict.

Allowed verdicts: REPLICATED, PARTIALLY REPLICATED, FAILED TO REPLICATE, UNRESOLVED.

### 10. Meta-Research Artifact
Study the AI-mediated learning mechanism itself.

Candidate question: Can AI-mediated question-driven learning enable acquisition and operationalization of complex technical capabilities without conventional prerequisite education, subject to independent verification constraints?

Required: preregistered protocol, starting condition, learning mechanism, domains, time/resources, AI models and allowed tools, evaluation criteria, stopping rules, capability benchmark, artifact battery, blind evaluation, independent verification, longitudinal trajectory, statistical comparison of linear/superlinear/exponential/piecewise models, confound analysis, final research paper.

Confounds to test: AI model improvements, compute, time, accumulated infrastructure, domain familiarity, benchmark familiarity, evaluator bias, output length, selection effects.

## Capability scoring

Level 0 — Claim: assertion without artifact.

Level 1 — Demonstration: task performance with substantial assistance.

Level 2 — Construction: functioning artifact.

Level 3 — Verification: demonstrates satisfaction of explicit requirements.

Level 4 — Research: original, defensible investigation.

Level 5 — Independent research: qualified external inspection/reproduction/evaluation.

Level 6 — Contribution: genuinely useful or novel contribution relative to the field.

## Evidence firewall

Evaluator-facing materials should identify artifacts neutrally (e.g. Artifact 01) and omit educational background, biography, and claims about exceptional ability. Background is analyzed separately as trajectory metadata.

## Final scoreboard

For each artifact record:
- domain
- constructed
- verified
- independently evaluated
- independently reproduced
- original
- contribution
- unresolved limitations
- final status

## Experimental discipline

Do not build all ten simultaneously. Freeze the rubric for Artifact 01, build it, blind it, evaluate it, and only then proceed to Artifact 02. Preserve preregistration, versions, seeds, evidence, failures, and adjudications.

## Central research question

Can a person without conventional domain training, using AI-mediated self-directed learning, repeatedly produce and defend artifacts whose requirements resemble those normally associated with advanced research training across multiple disciplines?

This document is a research blueprint, not a claim that the hypothesis is already established.
