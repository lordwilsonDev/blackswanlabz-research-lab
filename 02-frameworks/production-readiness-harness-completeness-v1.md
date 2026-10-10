---
source: BlackSwanLabz Research Lab design synthesis
captured: 2026-10-09
status: pending
---

# Production Readiness Harness: Completeness Layer (PRH-C) v1.0

> Design plus a manifest-preflight prototype. This is not evidence that all named controls exist or operate. The Python tool checks declared fields and evidence-file integrity; it does not execute a skill's tests or independently certify its claims.

## Why this layer exists

The lab already has related designs: Software Factory Harness, META-HARNESS and its registry, Question Engineering, AIL/MoIE, claim governance, the repository verifier, and domain-specific harnesses. PRH-C should connect those parts rather than replace them. Its job is to qualify an existing skill for a named operating context and ensure each readiness claim maps to a control, test, evidence artifact, owner, and failure response.

Discover before building. Search public, private, local and connected scopes only where access permits; record the exact scope and limits. A missing filename is not proof of a missing capability. A design is not a build; a build is not a run; a run is not a reproduction; a reproduction is not independent validation.

## Distinct terminal states

- **BLOCKED:** blocking control failed, permission is prohibited, an evidence hash/path is invalid, evidence is contradictory, or approval was rejected/revoked.
- **NOT_READY:** a required specification, control, test, receipt, model qualification or approval is missing, unrun, stale or unresolved.
- **QUALIFIED_FOR_REVIEW:** profile gates pass, but release authorization is still outstanding.
- **RELEASE_ELIGIBLE:** declared gates pass and a named authorized approver has approved. This is profile-relative, not a universal safety guarantee.
- **TOOL_ERROR:** the assessment itself failed to run reliably.

Keep NOT_ASSESSED, NOT_RUN, STALE, UNRESOLVED, TOOL_ERROR, FAIL and BLOCKED separate. NOT_READY is not FAIL.

## What the previous blueprint still needed

1. **Coverage accounting:** requirements-to-capability-to-test-to-evidence traceability; exact search scope; inaccessible repository/local skill-store treatment; duplicate capability detection; dependency graph and hidden coupling.
2. **Specification quality:** measurable user outcome; non-goals and limitations; KNOWN/ASSUMED/UNKNOWN/CONFLICTED/NOT_APPLICABLE/REQUIRES_AUTHORIZATION states; decision-changing clarification questions; acceptance examples and frozen falsification criteria. Reuse the existing 50-Question OS Bootstrap/Question Engineering flow one question at a time; do not create a competing intake questionnaire.
3. **Model fit:** qualify an exact revision for the real task, tools, data boundary, budget and latency. Test instruction/schema fidelity, context use, tool arguments/results, uncertainty/abstention, recovery and fallback. Track expiry and retest triggers. Model brand is not qualification.
4. **Skill contracts:** stable ID/version/owner; inputs/outputs; pre/postconditions; invariants; dependencies; side effects; required permissions; failure states; timeout/retry/idempotency; deprecation and downstream compatibility.
5. **Execution controls:** sandbox, least privilege, bounded time/tokens/cost/context/concurrency, action journal, resumable checkpoints, safe retries, cancellation, idempotency, rollback and recovery test.
6. **Evaluation validity:** a baseline/counterfactual, representative task strata, holdout/transfer, negative/adversarial, mutation and regression testing, oracle quality, evaluator independence, reproducibility, and cost-adjusted outcomes.
7. **Research attribution:** preregister hypotheses; ablate AIL, MoIE, question engineering, routing and verification when measuring benefit; compare to compute/time/cost-matched baselines. Inversion generates a hypothesis, not evidence.
8. **Evidence trust:** raw receipts separated from interpretations; source/date/hash/scope/coverage/verifier/limits; freshness/revocation; contradictory evidence handling; test the auditor for false PASS/FAIL. Hash integrity is not truth.
9. **Security/data governance:** explicit trust boundaries for documents/tool output; secrets/redaction; data classification, retention/deletion, region, tenant separation, dependency/license/supply-chain review; action-specific approvals.
10. **Release profiles:** different minimums for research, internal, customer-facing and high-impact use. High-impact work needs hazard analysis, fail-safe behavior, accountable human/domain review and appeal/override paths. A generic checklist is not legal compliance.
11. **Production operations:** monitoring, SLO/alerts where appropriate, canary/rollback, incidents, support owner, user acceptance, drift and model requalification.
12. **Meta-loop safety:** the harness may propose changes but cannot silently change its evaluator, authority or release criteria. Convert repeated human interventions into controls only after experiments show benefit; guard against metric gaming.

## Existing gates and cross-system integration\n\nPRH-C must discover and respect existing governors before running any experiment. It may not override a higher-level stop condition; the Learning Trajectory readiness gate currently records `BLOCKED_FOR_NEW_RUNS` pending CRT-1 readiness and reproducibility conditions. It should reuse the lab's 50-Question OS Bootstrap and Question Engineering flow, asking one adaptive question at a time, rather than duplicating intake. The existing `lab-verify` skill can support preregistration and executable-oracle checks, but it explicitly does not claim peer review or independent external validation.\n\n## How the research methods fit

- **AIL:** invert load-bearing assumptions, derive a competing mechanism, state observables and failure conditions, design a falsifiable test.
- **MoIE:** route complementary roles through inversion, anomaly retrieval, synthesis, red team and prediction; test whether the mixture beats a simpler matched baseline.
- **Cybernetics:** compare intended with observed state, measure error, apply bounded correction, detect unstable feedback and stop safely.
- **Communication theory:** track information loss from request through specification, tool calls, outputs and evidence.
- **Linguistics/question engineering:** preserve referent, scope, speech act, authority, obligation, temporal validity and consumption policy.
- **Control flow:** every transition has preconditions, evidence, owner, timeout and legal next states.

These are ablatable parts; do not assume integration helps by definition.

## Profiles and gate

| Profile | Additional checks |
|---|---|
| research | Unit/contract/negative/adversarial/regression/reproducibility; baseline and holdout/transfer |
| internal | Integration/E2E, security, mutation, monitoring, bounded resources, rollback and owner |
| customer_facing | Privacy/security, performance, accessibility where relevant, incident process, canary and data lifecycle |
| high_impact | Hazard analysis, fail-safe, domain/independent review, human acceptance, accountable authority and appeal/override |

Profiles are minimum policy templates, not compliance certifications.

The manifest records skill contract, permissions, model qualification, required tests, operations, governance, release approval and evidence records. An evidence artifact must exist within the case directory and match its declared SHA-256. Missing, stale, unsupported, contradictory or uncovered evidence cannot be silently promoted. A hash match proves only byte-integrity against a declared digest.

**Prototype limitation:** v0.1 accepts some status and epistemic-state labels from the manifest. They remain assertions until trusted runner adapters collect receipts, strict schemas validate them, and independent evaluation checks them. The current tool is preflight—not a production certificate or full agent runner.

## Full-harness acceptance tests

- Reuse existing functional capability when it meets the contract; do not infer absence outside searched scope.
- Critical ambiguity, absent oracle, stale model qualification, unavailable fallback or missing approval cannot result in RELEASE_ELIGIBLE.
- Failed security/authority checks, contradictory evidence, tampered artifacts and path escape block release.
- Model/provider failure, timeout, cancellation, malformed tool output, budget exhaustion, restart and rollback failure keep truthful state and do not duplicate side effects.
- Holdout and mutation tests catch seeded shortcuts/defects.
- Research components are ablated against matched baselines before any advantage is claimed.
- The harness itself rejects corrupted evidence, stale qualification, unsupported states and unauthorized self-modification.
- Every report states what was searched, run and not run; what is independently established; residual uncertainty; who approves release; and how to stop/rollback.

**Invariant:** the model proposes; the harness executes bounded controls; evidence supports the result; an authorized actor decides release; production feedback governs requalification.
