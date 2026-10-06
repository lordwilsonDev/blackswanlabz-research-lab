---
source: author-supplied text (Lord Wilson), pasted into a working session 2026-10-06; reproduced verbatim below the banner. The counterpart table at the end is Claude's addition and is not part of the source text.
captured: 2026-10-06
status: pending
---

# META-HARNESS skill registry (author-supplied design)

> **Record status:** A design document, not a result. It describes a registry of skills for a meta-harness that builds and improves governed software-production harnesses. Nothing here is evidence that the described skills exist as named, and no claim row depends on it ([AGENTS.md](../AGENTS.md) rule 10). Many of the capabilities it names are built under other names; see "Counterparts found locally" at the end, which is an unverified mapping by function. The meta-skill that this registry serves is in [meta-harness.md](meta-harness.md).

---

META-HARNESS SKILL REGISTRY

Skill Architecture

```text
                         META-HARNESS
                              │
              ┌───────────────┼────────────────┐
              │               │                │
          DISCOVER          BUILD            LEARN
              │               │                │
        ┌─────┴─────┐    ┌────┴─────┐    ┌────┴─────┐
        │           │    │          │    │          │
     Inspect     Diagnose  Contract  Verify       Analyze
     Factory     Factory   Factory   Factory      Failures

```

The skills should be divided into five families:

1. Discovery
2. Execution
3. Verification
4. Governance
5. Meta-improvement

1. DISCOVERY SKILLS
These reconstruct the environment before anything is changed.
`factory-inspector`
Purpose: Reverse-engineer the existing software factory.
Can inspect:

* repository structure
* build system
* CI/CD
* tests
* agents
* tools
* skills
* permissions
* deployment
* observability
* human intervention points

Output:

```yaml
factory_map:
  control_plane:
  agents:
  tools:
  skills:
  inner_loop:
  outer_loop:
  meta_loop:
  evidence:
  authority:
  bottlenecks:

```

`repository-archaeologist`
Purpose: Understand an unfamiliar codebase before an agent modifies it.
Capabilities:

* architecture reconstruction
* dependency mapping
* entry-point discovery
* test discovery
* configuration discovery
* dead-code detection
* convention extraction

Critical rule:
Never modify architecture you have not first mapped.
`capability-auditor`
Determines:

```text
What can the agent do?
What can it not do?
What tools exist?
What tools are missing?
What permissions exist?
What permissions are excessive?

```

Output:

```text
CAPABILITY
AUTHORITY
TOOL
SKILL
MISSING
UNUSED
DANGEROUS

```

`bottleneck-detector`
Determines the actual limiting factor.
Tests:

```text
agent reasoning
context
tool availability
verification
human review
environment
latency
permissions
deployment

```

Rule:
Do not add architecture until the bottleneck has evidence.
2. CONTRACT SKILLS
These define what the factory is actually supposed to accomplish.
`mission-contract`
Converts an objective into a machine-readable mission.
Produces:

```text
objective
scope
requirements
constraints
authority
verification
termination
evidence

```

`scope-guardian`
Prevents agents from silently expanding their task.
Checks:

```text
allowed files
forbidden files
allowed dependencies
allowed tools
allowed side effects
allowed network access

```

`authority-policy`
Separates:

```text
CAN_READ
CAN_WRITE
CAN_EXECUTE
CAN_COMMIT
CAN_PR
CAN_MERGE
CAN_DEPLOY
CAN_CHANGE_POLICY
CAN_CHANGE_AUTHORITY

```

This should be a dedicated skill because capability and authority are not the same thing.
`requirement-resolver`
Takes ambiguous human requirements and identifies:

```text
known
unknown
assumption
conflict
missing authority
missing evidence

```

It should be able to stop the factory rather than manufacture certainty.
3. AGENT EXECUTION SKILLS
These are the skills that let the agent actually operate.
`sandbox-manager`
Creates and destroys isolated execution environments.
Handles:

* filesystem isolation
* environment variables
* dependencies
* credentials
* network policy
* resource limits
* cleanup

`tool-discovery`
Determines what tools are available for a task.
Rather than dumping every tool into context:

```text
Mission
   ↓
Required capability
   ↓
Relevant tools
   ↓
Minimal tool set

```

This reduces tool/context noise.
`agent-runner`
Executes the agent against the mission contract.
Tracks:

```text
run_id
agent
model
version
tools
skills
iterations
duration
actions
files
failures
result

```

`agent-repair`
Provides structured feedback when the agent fails.
Instead of:

```text
"Try again."

```

produce:

```yaml
failure:
  type:
  evidence:
  expected:
  actual:
  affected_files:
  allowed_actions:

```

Then allow bounded repair.
`iteration-controller`
Controls:

```text
maximum iterations
maximum repair attempts
failure thresholds
timeout
escalation
termination

```

Prevents infinite agent loops.
4. INNER-LOOP VERIFICATION SKILLS
These optimize autonomy.
`lint-gate`
Runs deterministic static checks.
`typecheck-gate`
Checks type correctness.
`unit-test-gate`
Runs relevant unit tests.
`contract-test-gate`
Tests explicit interface contracts.
`scope-integrity-gate`
Detects unauthorized modifications.
`dependency-integrity-gate`
Checks dependency changes and compatibility.
`security-preflight`
Fast security checks before expensive verification.
`inner-loop-orchestrator`
Combines those skills:

```text
CHANGE
 ↓
LINT
 ↓
TYPECHECK
 ↓
UNIT
 ↓
CONTRACT
 ↓
SCOPE
 ↓
SECURITY
 ↓
PASS / REPAIR / BLOCK

```

The inner loop should be fast enough that the agent can use it continuously.
5. OUTER-LOOP VERIFICATION SKILLS
These optimize automation.
`integration-verifier`
Runs cross-component verification.
`e2e-verifier`
Tests actual user/system flows.
`regression-verifier`
Determines whether existing behavior was broken.
`mutation-verifier`
Tests whether the tests actually detect meaningful failures.
This is important because:
Passing tests ≠ strong tests.
`negative-test-verifier`
Tests:

```text
invalid input
missing permissions
malformed data
unexpected state
boundary conditions
failure paths

```

`security-verifier`
Performs deeper security validation.
`architecture-verifier`
Checks architectural invariants.
Examples:

```text
dependency direction
forbidden imports
layer boundaries
API contracts
database boundaries
permission boundaries

```

`evidence-verifier`
Checks whether the claimed result is actually supported by evidence.
`outer-loop-orchestrator`
Runs the expensive verification stack and returns:

```text
PASS
FAIL
BLOCKED
UNRESOLVED
HUMAN_REQUIRED

```

6. EVIDENCE SKILLS
This family is particularly important for your architecture.
`evidence-collector`
Captures:

```text
diff
files
commands
tests
logs
environment
versions
artifacts
receipts

```

`claim-evidence-mapper`
Maps:

```text
CLAIM → REQUIRED EVIDENCE → ACTUAL EVIDENCE

```

Example:

```text
Claim:
"Feature works."

Required:
functional test

Evidence:
test #381 PASS

Verdict:
SUPPORTED

```

`evidence-integrity`
Detects:

```text
missing evidence
stale evidence
modified evidence
contradictory evidence
incorrect provenance

```

`receipt-generator`
Creates the final machine-readable execution receipt.

```yaml
receipt:
  mission:
  agent:
  changes:
  tests:
  verification:
  evidence:
  policy:
  verdict:

```

`audit-ledger`
Records the factory's activity.
This becomes the historical memory of:

```text
what happened
when
by whom
with what authority
using what tools
producing what evidence

```

7. HUMAN-INTERVENTION SKILLS
This is where the meta-loop begins.
`intervention-recorder`
Records every human takeover.
`intervention-classifier`
Classifies it:

```text
CLARIFICATION
PLANNING
IMPLEMENTATION
TESTING
ENVIRONMENT
SECURITY
POLICY
ARCHITECTURE
RELEASE

```

`intervention-cost`
Measures:

```text
frequency
duration
complexity
repetition
production impact

```

`intervention-miner`
Asks:
"Is this human intervention actually a missing factory capability?"
8. META-LEARNING SKILLS
This is the heart of META-HARNESS.
`failure-analyzer`
Turns raw failures into structured patterns.

```text
failure
 ↓
classification
 ↓
frequency
 ↓
recurrence
 ↓
root-cause hypothesis

```

`pattern-detector`
Finds recurring failures across runs.
Example:

```text
Run 12 → migration test missing
Run 19 → migration test missing
Run 27 → migration test missing
Run 31 → migration test missing

```

Output:

```text
RECURRING FACTORY DEFICIENCY

```

`root-cause-analyzer`
Separates:

```text
agent failure
from
harness failure
from
environment failure
from
requirement failure
from
verification failure

```

This is critical.
Otherwise the factory can "fix" the wrong layer.
`improvement-generator`
Generates candidate interventions:

```text
ADD TEST
ADD GATE
ADD SKILL
ADD TOOL
CHANGE CONTRACT
CHANGE POLICY
CHANGE ENVIRONMENT
CHANGE CONTEXT
ADD OBSERVABILITY

```

`improvement-prioritizer`
Ranks candidate changes by something like:

```text
frequency
× impact
× preventability
× confidence
÷ implementation cost

```

9. EXPERIMENT SKILLS
The factory needs to test its own changes.
`baseline-builder`
Establishes pre-change performance.
`experiment-designer`
Defines:

```text
hypothesis
baseline
intervention
metric
sample
duration
success criteria

```

`experiment-runner`
Runs the changed factory against comparable tasks.
`delta-analyzer`
Compares:

```text
before
vs.
after

```

`change-validator`
Determines:

```text
IMPROVED
NO_CHANGE
REGRESSED
INCONCLUSIVE

```

`rollback-manager`
Reverts ineffective or harmful factory changes.
10. METRIC SKILLS
`autonomy-measurer`
Tracks:

```text
takeover rate
iterations
successful autonomous runs
repair success
blocked runs

```

`automation-measurer`
Tracks:

```text
manual review minutes
human PR comments
automated PR rate
human corrections

```

`quality-measurer`
Tracks:

```text
regressions
escaped defects
mutation score
security findings
production incidents
rollback rate

```

`metric-integrity`
Protects against Goodhart effects.
It asks:
"Did the metric improve, or did the system learn to game the metric?"
11. PRODUCTION FEEDBACK SKILLS
`runtime-observer`
Consumes:

```text
logs
metrics
traces
errors
incidents

```

`production-failure-correlator`
Connects:

```text
production failure
→ deployment
→ PR
→ agent run
→ code change
→ verification

```

This gives the meta-loop causal evidence.
`incident-miner`
Determines whether production incidents expose a missing factory control.
`user-feedback-analyzer`
Converts actual user feedback into potential:

```text
requirement
test
skill
verification rule

```

12. FACTORY-GOVERNANCE SKILLS
`policy-verifier`
Ensures factory changes remain within policy.
`authority-verifier`
Checks whether the actor making a change actually has authority.
`change-risk-classifier`
Classifies changes:

```text
LOW
MEDIUM
HIGH
CRITICAL

```

`human-escalation`
Determines when the factory must stop.

```text
UNKNOWN
+
HIGH CONSEQUENCE
=
HUMAN REQUIRED

```

`self-modification-guard`
Prevents the meta-loop from silently modifying:

```text
its own authority
security boundaries
approval requirements
evidence rules
audit mechanisms

```

This is one of the most important skills in the entire system.
13. SKILL ENGINEERING SKILLS
META-HARNESS eventually needs to create new skills.
`skill-discovery`
Identifies repeated behavior that deserves abstraction.
`skill-specification`
Creates:

```text
purpose
inputs
outputs
tools
permissions
preconditions
postconditions
failure modes
verification

```

`skill-builder`
Implements the skill.
`skill-tester`
Tests the skill independently.
`skill-versioner`
Tracks:

```text
version
changes
performance
compatibility

```

`skill-deprecator`
Removes skills that no longer provide value.
`skill-registry-manager`
Maintains the complete registry.
14. THE MINIMUM VIABLE SET
Do not build all of these first.
The first real META-HARNESS should require only:

```text
01 factory-inspector
02 mission-contract
03 scope-guardian
04 sandbox-manager
05 agent-runner
06 iteration-controller

07 inner-loop-orchestrator
08 outer-loop-orchestrator

09 evidence-collector
10 evidence-verifier
11 receipt-generator
12 audit-ledger

13 intervention-recorder
14 intervention-classifier
15 failure-analyzer
16 pattern-detector

17 improvement-generator
18 experiment-designer
19 delta-analyzer
20 change-validator

21 autonomy-measurer
22 automation-measurer
23 quality-measurer

24 authority-verifier
25 self-modification-guard

```

25 skills is the practical core.
Everything else can be added when evidence says the factory needs it.
15. THE COMPOSITION
The important architecture is not:

```text
25 independent agents

```

It is:

```text
                    META-HARNESS
                         │
        ┌────────────────┼─────────────────┐
        │                │                 │
    DISCOVERY         EXECUTION         LEARNING
        │                │                 │
   factory-inspector   agent-runner     failure-analyzer
   capability-auditor  sandbox          pattern-detector
   bottleneck          inner-loop       improvement-generator
                       outer-loop       experiment
        │                │                 │
        └────────────────┼─────────────────┘
                         │
                     GOVERNANCE
                         │
              authority-verifier
              self-modification-guard

```

The skills are capabilities. The harness is the orchestration. The meta-skill decides which capability is required.
16. THE RECURSIVE PROPERTY
Eventually:

```text
Agent
  ↓
uses skills
  ↓
produces software
  ↓
factory observes production
  ↓
META-HARNESS identifies missing capability
  ↓
skill-discovery
  ↓
skill-specification
  ↓
skill-builder
  ↓
skill-tester
  ↓
skill-versioner
  ↓
factory gets new capability
  ↓
future agents operate differently

```

That is the actual recursive loop.
The key invariant:
A repeated human intervention should eventually become either a deterministic control, a reusable skill, an explicit policy, or evidence that the task genuinely requires human judgment.
That gives you a very clean test of whether the factory is actually learning.
If intervention #1 requires a human, that's normal.
If intervention #37 is the same intervention and humans are still doing it manually, the factory has failed to learn from its own history.

---

## Counterparts found locally (Claude's mapping, not part of the source text)

**Read this as a map, not a verdict.** Written 2026-10-06 by matching each registry skill to the descriptions of 122 skills found in five places on the author's machine (the personal skills folder, the Claude skills folder, the question-engineering harness repository, and this repository's two skill folders). The match is by function from the descriptions only. Nothing here was run against this design, so no row says that a counterpart meets the registry skill's specification. "None found" means none found in that scope and by that keyword search, not that none exists. The skills named live on the author's machine and are not in this repository unless stated.

| Registry skill or family | Counterparts found by function |
|---|---|
| factory-inspector, repository-archaeologist | `sovereign-project-lifecycle-orchestrator` (reconstructs where a project is from evidence, with an archaeology step), `navigation-layer` (deterministic index of every system under the home folder), `auditing-solo-repos`, `closer` |
| capability-auditor, bottleneck-detector | `skill-corpus-audit`, `navigation-layer`; the lifecycle orchestrator can return a "MEASURE" verdict when evidence is thin. No dedicated bottleneck detector found |
| mission-contract, requirement-resolver | `freebuff-question-engineering` (turns a request into a governed question that can pass or block), `governed-intent-capture`, `s10-ask`, `s10-understand`, `surfacing-unasked-questions` |
| scope-guardian, authority-policy | `governed-scope-governance`, `s10-govern`; the Ethos System (allow, pause or refuse) and the governance brakes described in [03-systems/msb-v3.md](../03-systems/msb-v3.md) |
| sandbox-manager, tool-discovery | `interchangeable-components` (capability seams for tools, sandboxes and storage), `agentic-architectural-engineering`. No dedicated sandbox manager found |
| agent-runner, agent-repair, iteration-controller | `agent-harness` (a bounded agentic loop with a task plan, verification, capped retries and escalation), `loop-library`, `harness-skill-router` (ordered chain: question gate, domain skills, fidelity check) |
| inner-loop and outer-loop gates and orchestrators | `ship-gate`, `closer`, `s10-check`, `intent-reality-fidelity`, `landed-vs-live`; project-level gate scripts, for example the lint, type, test and mutation gate in the local tamper-evident ledger project |
| mutation-verifier | `mutating-skill` (mutation-tests the skill gates), the generic mutate-the-checker runner in `failure-to-control` |
| evidence-collector, claim-evidence-mapper, evidence-integrity, evidence-verifier | `intent-reality-fidelity`, `sovereign-verification` (claim, evidence, freshness, verdict ledger), `s10-verify`, `governed-evidence-builder`, `foundations-to-doctorate-integrity-checker`; this repository's [CLAIMS.md](../CLAIMS.md) |
| receipt-generator, audit-ledger | the local tamper-evident ledger project (see [the A02 page](../05-experiments/doctoral-artifact-battery-a02.md)), the evidence chain described in [03-systems/msb-v3.md](../03-systems/msb-v3.md) |
| intervention-recorder, classifier, cost, miner | partial: `failure-to-control` keeps a failure ledger that includes handoff and human-correction failures. No dedicated intervention recorder or classifier found |
| failure-analyzer, pattern-detector, improvement-generator, improvement-prioritizer | `failure-to-control`, the [D1 Failure-to-Leverage Compiler](d1-failure-to-leverage.md) (its leverage score is impact times recurrence times generality divided by cost), `agent-platform-eval-flywheel` |
| baseline-builder, experiment-designer, experiment-runner, delta-analyzer, change-validator | `independent-experimental-engineer`, `srse-designing-experiments`, [ACTS](acts-5-act-research.md), the pre-registered designs in [05-experiments](../05-experiments/README.md). No rollback manager found |
| autonomy, automation and quality measurers, metric-integrity | none found as dedicated skills; `agent-harness` and `building-a-business` mention metrics for other purposes |
| runtime-observer, production-failure-correlator, incident-miner, user-feedback-analyzer | none found as dedicated skills; `s10-deliver` and `ship-gate` touch production readiness |
| policy-verifier, authority-verifier, change-risk-classifier, human-escalation | `governed-quality-review`, `s10-govern`, the Ethos System, the D1 compiler's rule that destructive failure actions are never deployable. No dedicated risk classifier found |
| self-modification-guard | closest found: frozen-test rules in the ledger project and the D1 compiler's controls. No dedicated skill found |
| skill-discovery, specification, builder, tester, versioner, deprecator, registry-manager | `skill-creator`, `skill-normalizer`, `skill-corpus-audit`, `mutating-skill`, `find-skills`; `failure-to-control` was packaged with these. No deprecator found |
| the meta-skill itself ([meta-harness.md](meta-harness.md)) | no skill named meta-harness was found; the loop is spread across `sovereign-project-lifecycle-orchestrator`, `harness-skill-router`, `agent-harness`, `failure-to-control` and the D1 compiler |
