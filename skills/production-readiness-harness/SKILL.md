---
name: production-readiness-harness
version: 1.0.0
status: designed-and-prototype-backed
---

# Production Readiness Harness Skill

## Purpose
Move an existing skill from an honestly reconstructed state to a profile-specific release decision. Use this skill as the operator workflow; use `scripts/production_readiness_harness.py` for deterministic manifest preflight. Neither a written skill nor a green preflight proves production readiness by itself.

## Prime directive
**Discover before building. Specify before modifying. Qualify the model and tools in context. Execute within explicit authority. Verify independently. Preserve evidence. Never self-authorize release.**

## Procedure

### 1. Reconstruct the existing environment
Inspect manifests, readmes, instructions, code, tests, CI, release workflows, skills, tool adapters, model routing, permissions, environment configuration, evidence stores, issue/incident history and deployment paths. Follow the repository reading order and linked/pinned repositories where access permits. Record exact search scope, time, access limits and queries.

Use these discovery states: `FOUND`, `NOT_FOUND_IN_SEARCHED_SCOPE`, `ACCESS_LIMITED`, `NOT_SEARCHED`, and `CONFLICTING_RECORDS`. Never infer absence from a missing filename. Map functional counterparts and mark unverified equivalence as provisional.

### 2. Compile the user specification
Record outcome, user, acceptance example, scope/non-goals, preconditions, inputs/outputs, invariants, failure modes, limitations, authority, data classification, operating profile, budget/latency bounds, evaluation criteria, oracle, baseline, holdout, rollback, monitoring, support and ownership. For each field, record source and state: `KNOWN`, `ASSUMED`, `UNKNOWN`, `CONFLICTED`, `NOT_APPLICABLE` with rationale, or `REQUIRES_AUTHORIZATION`.

Ask the smallest question whose answer could change permission, architecture, evaluation, cost or release. Do not repeat questions already answered. Unknown critical details block execution rather than being guessed.

### 3. Map requirements to existing capability
Map each requirement to existing skills, tools, model capability, policies, tests, and evidence. Classify gaps as capability, authority, tool, knowledge, contract, verification, observability, infrastructure, governance, model fit, operations, user acceptance or unknown. Before adding anything, check for a functionally equivalent capability under another name.

For every gap, ask: Was the relevant scope searched? Can a deterministic control close it? What is the smallest falsifiable change? What might regress? How will closure be proven?

### 4. Qualify the model and tools
Qualify the exact model revision and tool configuration against the real task distribution and data boundary. Test instruction/schema fidelity, long context, domain correctness, tool calls, argument validity, evidence discipline, uncertainty/abstention, prompt-injection resilience, recovery, fallback, latency and cost. Record suite version, results, known limits, qualification expiry and retest triggers. Provider reputation or model name is not qualification.

### 5. Implement with bounded authority
Use a sandbox, least privilege, pinned dependencies, bounded input/context, time, retries, tokens, cost and concurrency. Keep secrets out of prompts, logs, fixtures and reports. Journal actions, checkpoint before risky operations, and define idempotency and recovery.

Separate read, write, execute, commit, merge, deploy, delete, send, policy-change and authority-change permissions. The skill may not grant itself authority. Require action-specific approval for irreversible or external side effects.

### 6. Evaluate independently
Run profile-appropriate unit, contract, integration, E2E, negative, boundary, adversarial, regression, security/privacy, mutation, reproducibility and user-acceptance tests. Include a meaningful baseline and holdout/transfer set. The executor's self-check is not the independent verifier.

For AIL, MoIE and question-engineering claims, preregister the hypothesis, primary metric, falsification condition and stopping rule; run ablations and matched baselines where relevant. An inversion creates a candidate, not evidence. A successful example is not a general result.

### 7. Preserve evidence
Map each requirement and readiness claim to the raw receipt, source, date, hash, verifier, scope, limitations and exact coverage. Keep raw evidence separate from interpretation and release decision. A matching hash establishes byte integrity against a declared digest—not truth or evaluator independence. Model-authored status fields remain assertions until validated against trusted runner receipts.

### 8. Apply the gate
Run:

```bash
python3 scripts/production_readiness_harness.py path/to/production_readiness_case.json
```

The case file is a relative-evidence manifest. Review each check and limitation, not just the terminal state. `BLOCKED` means a blocking failure or integrity issue. `NOT_READY` means something required is missing, unrun, stale or unresolved. `TOOL_ERROR` means the assessment itself did not complete reliably. `QUALIFIED_FOR_REVIEW` is separate from a release decision. `RELEASE_ELIGIBLE` is profile-relative and not a universal guarantee.

### 9. Monitor and requalify
After release, monitor errors, user outcomes, human overrides/takeovers, latency/cost, drift, dependency changes and incidents. Define stop/rollback signals before rollout. Material changes to model, prompt/skill, tool, policy, data distribution or environment trigger impact analysis and targeted requalification.

Mine interventions as candidate controls; retain changes only after baseline and guardrail measurements. Do not let the meta-loop silently change its evaluator, authorization policy or release criteria.

## Required report
1. Search scope and limitations.
2. Existing functional counterparts and confidence.
3. User contract, assumptions, unknowns and acceptance criteria.
4. Requirement-to-skill/tool/model/test/evidence graph.
5. Model qualification, exact revision, limits and fallback.
6. Authority, security, data governance and blast radius.
7. Tests, baseline, holdout, adversarial findings and what was not run.
8. Evidence integrity, provenance, freshness and contradictions.
9. Verdict: `BLOCKED`, `NOT_READY`, `QUALIFIED_FOR_REVIEW`, `RELEASE_ELIGIBLE`, or `TOOL_ERROR`.
10. Limitations, owner, rollback, retest triggers and highest-value next action.

## Hard rules
- Design is not build; build is not run; run is not reproduction; reproduction is not independent verification.
- `NOT_READY` is not `FAIL`; `NOT_RUN` is not `PASS`; `TOOL_ERROR` is not task failure.
- Autonomy, automation, quality, safety, user value and cost remain separate dimensions.
- Human review is not removed merely because it is expensive.
- The harness cannot be the sole judge of its own success.
- If required evidence is absent or contradictory, say so precisely.
