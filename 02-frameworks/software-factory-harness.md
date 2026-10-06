---
source: author-supplied text (Lord Wilson), pasted into a working session 2026-10-06; reproduced verbatim below the banner
captured: 2026-10-06
status: pending
---

# Software Factory Harness (author-supplied architecture design)

> **Record status:** A design document, not a result. It describes a governed three-loop harness (inner loop, outer loop, meta loop) for autonomous software production. Nothing here is evidence that the described harness exists as a single system. Many of its parts are built under other names on the author's machine; see the [counterpart table in the skill registry page](meta-harness-skill-registry.md), which is an unverified mapping by function. Related designs: [META-HARNESS](meta-harness.md) and the [skill registry](meta-harness-skill-registry.md). No claim row depends on this page ([AGENTS.md](../AGENTS.md) rule 10). Numbers inside the examples, such as iteration counts and task counts, are illustrations in the source, not measurements.

---

Software Factory Harness
A Governed Three-Loop Harness for Autonomous Software Production
1. Purpose
The Software Factory Harness converts an AI coding agent from a conversational programmer into a participant in a controlled software-production system.
The harness does not assume that an agent is trustworthy.
Instead:
The agent produces changes. The harness produces evidence. Gates determine whether the changes may advance.
The system optimizes three independent properties:

1. Autonomy — how far the agent can progress without human intervention.
2. Automation — how much verification and review can occur without human labor.
3. Quality — whether the resulting software remains correct, maintainable, observable, and useful.

These metrics must not be collapsed into a single "success" score.
2. Core Architecture

```text
                         SOFTWARE FACTORY HARNESS

┌─────────────────────────────────────────────────────────────────────┐
│                         CONTROL PLANE                               │
│                                                                     │
│  Mission → Contract → Agent Assignment → Sandbox → Evidence Ledger  │
│                         ↓                                           │
│                    Execution Policy                                │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         INNER LOOP                                  │
│                                                                     │
│  Agent → Inspect → Plan → Implement → Test → Repair → Retest        │
│                                                                     │
│  Fast checks:                                                       │
│    • syntax                                                       │
│    • type checking                                                │
│    • linting                                                      │
│    • unit tests                                                   │
│    • contract tests                                               │
│    • targeted integration tests                                  │
│                                                                     │
│  Objective: MAXIMIZE AUTONOMY                                     │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                         submission gate
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         OUTER LOOP                                  │
│                                                                     │
│  Independent verification                                           │
│    • full test suite                                                │
│    • integration / E2E                                             │
│    • mutation testing                                               │
│    • security checks                                                │
│    • regression detection                                           │
│    • architectural checks                                           │
│    • evidence verification                                          │
│    • agent-generated QA                                             │
│                                                                     │
│  Objective: MAXIMIZE AUTOMATION                                   │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                         release gate
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         PRODUCTION                                  │
│                                                                     │
│  Runtime telemetry → failures → user feedback → incidents           │
│                         │                                           │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          META LOOP                                  │
│                                                                     │
│  Observe:                                                           │
│    • agent transcripts                                              │
│    • failed tests                                                   │
│    • PR comments                                                    │
│    • human takeovers                                                │
│    • production errors                                              │
│    • recurring repairs                                              │
│    • rejected changes                                               │
│                                                                     │
│  Discover:                                                          │
│    • missing test                                                   │
│    • missing tool                                                   │
│    • missing skill                                                  │
│    • missing policy                                                 │
│    • missing environment                                            │
│    • recurring agent failure                                        │
│                                                                     │
│  Modify:                                                            │
│    • inner-loop checks                                              │
│    • outer-loop checks                                              │
│    • skills                                                         │
│    • contracts                                                      │
│    • policies                                                       │
│    • documentation                                                  │
│                                                                     │
│  Objective: MAXIMIZE QUALITY                                       │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              └──────────────► INNER LOOP

```

3. The Fundamental Object: Mission Contract
Every autonomous run begins with a machine-readable contract.

```yaml
mission:
  id: "MISSION-0001"
  objective: "Implement feature X"

scope:
  allowed_paths:
    - "src/"
    - "tests/"
  forbidden_paths:
    - ".github/workflows/"
    - "secrets/"

requirements:
  functional:
    - "..."
  non_functional:
    - "..."

verification:
  required:
    - unit_tests
    - typecheck
    - lint
    - integration_tests

authority:
  agent:
    may_modify: true
    may_commit: true
    may_open_pr: true
    may_merge: false
    may_deploy: false

evidence:
  required:
    - changed_files
    - test_results
    - diff
    - verification_receipt

termination:
  max_iterations: 20
  max_failures: 5

```

The agent does not receive unlimited authority simply because it is capable of writing code.
4. State Machine
The harness should have explicit states.

```text
REQUESTED
    │
    ▼
CLASSIFIED
    │
    ▼
AUTHORIZED
    │
    ▼
PLANNED
    │
    ▼
EXECUTING
    │
    ├──────────────► BLOCKED
    │
    ▼
INNER_VERIFIED
    │
    ├──────────────► REPAIR
    │                    │
    │                    └──► EXECUTING
    │
    ▼
SUBMITTED
    │
    ▼
OUTER_VERIFIED
    │
    ├──────────────► REPAIR
    │
    ├──────────────► HUMAN_REVIEW
    │
    ▼
ACCEPTED
    │
    ▼
DEPLOYED
    │
    ▼
OBSERVED
    │
    ▼
META_ANALYSIS
    │
    ├──────────────► HARNESS_CHANGE
    │
    └──────────────► NO_CHANGE

```

Terminal states should be explicit:

```text
PASS
FAIL
BLOCKED
TOOL_ERROR
UNRESOLVED
HUMAN_REQUIRED

```

Do not use:

```text
"probably okay"
"looks good"
"agent says done"

```

as system states.
5. INNER LOOP — Autonomy Harness
The inner loop exists to let the agent resolve ordinary failures itself.
Agent cycle

```text
READ
 ↓
UNDERSTAND
 ↓
PLAN
 ↓
CHANGE
 ↓
TEST
 ↓
INTERPRET FAILURE
 ↓
REPAIR
 ↓
RETEST

```

The harness records every cycle.
Example:

```json
{
  "run_id": "R-1042",
  "iteration": 7,
  "action": "repair",
  "failure": "type_error",
  "files_changed": 3,
  "tests_before": 142,
  "tests_after": 142,
  "result": "PASS"
}

```

Inner-loop gate
The agent may proceed automatically when:

* required tests pass;
* required static checks pass;
* scope has not been violated;
* no unauthorized files changed;
* no policy violation occurred;
* evidence was successfully recorded.

Otherwise:

```text
REPAIR
or
BLOCK

```

6. OUTER LOOP — Independent Verification
The outer loop must be more independent than the agent's own reasoning.
This is critical.
If the same agent writes the code and declares the code correct, that is not independent verification.
Outer verification should include:
Functional

* complete test suite
* integration tests
* E2E tests
* regression tests

Structural

* type checking
* dependency validation
* API compatibility
* schema compatibility

Adversarial

* mutation testing
* negative tests
* malformed inputs
* boundary conditions
* permission violations

Security

* secret detection
* dependency vulnerabilities
* unsafe configuration
* unauthorized capability usage

Evidence

* changed-file manifest
* test receipt
* diff
* environment
* tool versions
* agent identity
* mission contract
* verification result

The outer loop answers:
"Can we independently establish that this change satisfies the contract?"
Not:
"Does the agent think it is finished?"
7. META LOOP — Harness Improvement
This is the part that turns an automated pipeline into a learning software factory.
Every failure becomes classified evidence.

```text
FAILURE
   │
   ├── Agent reasoning failure
   ├── Missing test
   ├── Missing tool
   ├── Missing skill
   ├── Bad contract
   ├── Bad environment
   ├── Infrastructure failure
   ├── Security policy failure
   └── Unknown

```

Then ask:
"What change to the factory would make this class of failure less likely next time?"
Example:

```text
Agent repeatedly forgets migration tests
        ↓
Meta-loop detects recurrence
        ↓
Add migration verification to inner loop
        ↓
Next agent receives immediate feedback
        ↓
Human review requirement decreases

```

That is actual harness engineering.
8. Skills Registry
Skills should be treated as versioned executable capabilities.

```yaml
skill:
  id: database-migration
  version: 3

  purpose:
    "Safely modify database schemas."

  prerequisites:
    - database_available

  tools:
    - migration_cli
    - schema_diff

  required_checks:
    - migration_up
    - migration_down
    - schema_consistency

  prohibited:
    - production_database_write

  evidence:
    - migration_receipt
    - schema_diff

```

Skills should have:

```text
OWNER
VERSION
INPUT CONTRACT
OUTPUT CONTRACT
TOOLS
PERMISSIONS
TESTS
FAILURE MODES
EVIDENCE REQUIREMENTS

```

A skill is therefore not merely a prompt.
It is a capability contract.
9. Control Plane
The control plane coordinates the factory.
Minimum objects:

```text
Mission
Contract
Agent
Skill
Sandbox
Tool
Run
Iteration
Artifact
Test
Evidence
Receipt
Policy
Failure
PR
Deployment
Observation

```

Every run should produce an immutable-ish audit trail:

```text
Mission
  ↓
Authorization
  ↓
Agent
  ↓
Environment
  ↓
Actions
  ↓
Files
  ↓
Tests
  ↓
Verification
  ↓
PR
  ↓
Deployment
  ↓
Runtime outcome

```

This creates causal traceability.
10. Metrics
Do not simply report "AI productivity."
Track the three dimensions independently.
Autonomy

```text
Autonomy Rate =
successful agent runs without human takeover
/
total agent runs

```

Also track:

```text
Human Takeover Rate
Mean Agent Iterations
Agent Repair Success Rate
Blocked Run Rate

```

Automation

```text
Automation Rate =
PRs accepted without manual corrective intervention
/
total PRs

```

Track:

```text
PR Human Comment Volume
Manual Review Minutes
Automated PR Initiation Rate
Human Corrections / PR

```

Quality
Quality must not be inferred from autonomy.
Track:

```text
Test pass rate
Regression rate
Defect escape rate
Mutation score
Production incident rate
Rollback rate
Security findings
User-facing error rate

```

The factory can therefore produce:

```text
HIGH AUTONOMY
LOW AUTOMATION
HIGH QUALITY

```

or:

```text
HIGH AUTONOMY
HIGH AUTOMATION
LOW QUALITY

```

The second condition is a failure, even though the factory appears productive.
11. The Critical Metric: Human Intervention Taxonomy
"Human takeover" is too coarse.
Classify intervention.

```text
H1 — Clarification
H2 — Planning correction
H3 — Code correction
H4 — Test correction
H5 — Environment repair
H6 — Security intervention
H7 — Policy intervention
H8 — Architectural intervention
H9 — Release intervention

```

Now the meta-loop can distinguish:

```text
10 human interventions

```

from:

```text
10 fundamentally different failure modes

```

That distinction matters.
12. Failure Learning
Each intervention becomes a candidate factory improvement.

```yaml
failure:
  category: H4
  frequency: 17
  recurring_pattern:
    "Agent implements feature but omits regression test."

  proposed_change:
    type: "inner_loop_check"

  change:
    "Require test-delta evidence for feature-class missions."

  validation:
    baseline: 17
    experiment: 50

  result:
    recurrence_after_change: 2

```

Now the factory can demonstrate:
"We changed the harness, and the failure rate dropped."
That is stronger evidence than claiming the model became smarter.
13. Anti-Gaming Layer
The factory must defend against Goodhart's Law.
An agent can improve apparent autonomy by:

* avoiding difficult tasks;
* weakening tests;
* deleting failing tests;
* reducing scope;
* declaring ambiguity;
* manipulating metrics;
* avoiding PR creation;
* generating superficial changes.

Therefore the harness must separately measure:

```text
Task difficulty
Task completion
Verification strength
Scope preservation
Evidence integrity
Production outcome

```

A successful run is not:

```text
agent said PASS

```

It is:

```text
contract satisfied
+
scope preserved
+
independent verification passed
+
evidence exists
+
no policy violation

```

14. Evidence Firewall
The agent's claim and the verifier's evidence should remain separate.

```text
AGENT CLAIM
"I implemented authentication."

             │
             ▼

INDEPENDENT EVIDENCE

✓ expected files changed
✓ tests added
✓ tests pass
✓ unauthorized access rejected
✓ authorized access succeeds
✓ regression suite passes
✓ security checks pass

             │
             ▼

VERDICT
PASS

```

The agent may provide hypotheses about correctness.
It does not get final authority over correctness.
15. Experimental Harness
Before attempting full autonomy, establish a baseline.
Run 50–100 representative tasks.
Measure:

```text
                BASELINE

Human Takeover Rate
PR Correction Rate
Manual Review Minutes
Test Failure Rate
Defect Escape Rate
Agent Iterations
Blocked Rate

```

Then change one harness component at a time.
Example:

```text
Experiment A
Add missing API contract tests.

Experiment B
Add automated PR mutation testing.

Experiment C
Add skill for database migrations.

Experiment D
Add production-log feedback.

Experiment E
Add automatic regression-test generation.

```

Measure the delta.
This prevents "we added 17 agents and everything got better" architecture theater.
16. Minimum Viable Harness
You do NOT need the complete factory initially.
The smallest useful implementation is:

```text
1. Mission Contract
2. Sandbox
3. Agent Runner
4. Inner Test Gate
5. Outer Verification Gate
6. Evidence Ledger
7. Human Intervention Logger
8. Meta-Loop Failure Classifier

```

Everything else can grow around those primitives.
17. The Recursive Property
The most important property of the system is:

```text
Software
   ↓
Factory produces software
   ↓
Factory observes software production
   ↓
Factory identifies weaknesses
   ↓
Factory modifies itself
   ↓
Improved factory produces software

```

The meta-loop therefore operates on the production system itself.
But it must not have unrestricted authority to rewrite its own authority model.
Separate:

```text
CAPABILITY
from
AUTHORITY

```

The system may discover:
"We need a new capability."
That does not automatically mean:
"The system is authorized to grant itself that capability."
That boundary is where governance belongs.
18. Final Factory Model
The complete system becomes:

```text
                    HUMAN
                      │
                Mission / Intent
                      │
                      ▼
              ┌───────────────┐
              │ CONTROL PLANE │
              └───────┬───────┘
                      │
                Contract + Policy
                      │
                      ▼
              ┌───────────────┐
              │     AGENT     │
              └───────┬───────┘
                      │
              ┌───────▼───────┐
              │  INNER LOOP   │
              │  AUTONOMY     │
              └───────┬───────┘
                      │
                Evidence Gate
                      │
              ┌───────▼───────┐
              │  OUTER LOOP   │
              │  AUTOMATION   │
              └───────┬───────┘
                      │
                Release Gate
                      │
                      ▼
                 PRODUCTION
                      │
                Observability
                      │
              ┌───────▼───────┐
              │   META LOOP   │
              │    QUALITY    │
              └───────┬───────┘
                      │
             Harness Improvements
                      │
                      └──────────────►
                              INNER / OUTER

```

The invariant
Agents write software.
Harnesses constrain and verify agents.
Evidence establishes what happened.
Metrics expose where the system fails.
The meta-loop modifies the factory in response to evidence.
Humans retain authority over consequential capability and policy changes.
That is the Software Factory.
And the key distinction from a normal "AI coding setup" is that the product is no longer merely the software being generated. The product is the production system that can repeatedly generate, verify, observe, and improve software.
