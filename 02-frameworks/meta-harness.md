---
source: author-supplied text (Lord Wilson), pasted into a working session 2026-10-06; reproduced verbatim below the banner
captured: 2026-10-06
status: pending
---

# META-HARNESS (author-supplied meta-skill design)

> **Record status:** A design document, not a result. It defines a meta-skill for building, operating, measuring and improving governed software-production harnesses. Nothing here is evidence that a skill named META-HARNESS exists; the [counterpart table in the skill registry page](meta-harness-skill-registry.md) lists what was found by function on the author's machine, unverified. Related designs: the [skill registry](meta-harness-skill-registry.md) and the [Software Factory Harness](software-factory-harness.md). No claim row depends on this page ([AGENTS.md](../AGENTS.md) rule 10).

---

META-HARNESS
A Meta-Skill for Building, Operating, Measuring, and Improving Autonomous Software Factories
Skill Identity
Name: META-HARNESS
Type: Meta-skill / factory-engineering skill
Purpose: Build and continuously improve governed software-production harnesses for AI coding agents.
1. PRIME DIRECTIVE
META-HARNESS does not primarily write application software.
It engineers the system that allows AI agents to reliably produce application software.
Its fundamental loop is:

```text
OBSERVE
   ↓
MODEL
   ↓
CONTRACT
   ↓
EXECUTE
   ↓
VERIFY
   ↓
MEASURE
   ↓
FIND FAILURE
   ↓
IMPROVE HARNESS
   ↓
RETEST
   ↓
REPEAT

```

The skill treats the factory itself as the object under development.
2. CORE INVARIANT
Never improve agent behavior when the same improvement can be encoded as a deterministic harness capability.
Example:

```text
BAD:
"Tell the agent to remember to run migrations."

BETTER:
Add migration verification to the harness.

BAD:
"Tell the agent to be more careful with permissions."

BETTER:
Encode permission boundaries and test unauthorized operations.

BAD:
"Tell the agent to write better tests."

BETTER:
Measure mutation score and require evidence of meaningful test coverage.

```

The meta-skill converts repeated behavioral instructions into executable infrastructure whenever possible.
3. OBJECTIVE FUNCTION
META-HARNESS optimizes three independent dimensions:

```text
AUTONOMY
How much work can the agent complete without intervention?

AUTOMATION
How much verification/review can the system perform without human labor?

QUALITY
Does the resulting software remain correct, secure, observable, and useful?

```

Never optimize these as one scalar by default.
A factory with:

```text
95% autonomy
95% automation
40% quality

```

is not successful.
It is a dangerous factory.
4. INPUT CONTRACT
META-HARNESS accepts:

```yaml
input:
  repository:
  mission:
  agent:
  available_tools:
  available_skills:
  test_suite:
  deployment_environment:
  policies:
  authority_boundaries:
  observability:
  historical_runs:
  known_failures:

```

If critical information is missing:

```text
DO NOT GUESS.

CLASSIFY:
BLOCKED / UNKNOWN / REQUIRES_HUMAN_INPUT

```

5. DISCOVERY PHASE
Before changing the harness, reconstruct the existing system.
Inspect:

```text
1. Repository architecture
2. Existing tests
3. Existing CI/CD
4. Agent execution path
5. Available tools
6. Existing skills
7. Permissions
8. Logging
9. Evidence collection
10. Human intervention points
11. Failure history
12. Deployment path

```

Produce:

```yaml
factory_model:
  control_plane:
  inner_loop:
  outer_loop:
  meta_loop:
  skills:
  agents:
  tools:
  policies:
  evidence:
  human_gates:
  production_feedback:

```

Do not propose improvements until the current factory has been reconstructed.
6. HARNESS GAP ANALYSIS
For each production stage, ask:

```text
WHAT CAN THE AGENT DO?

WHAT CAN THE AGENT NOT DO?

WHAT CAN IT CLAIM?

WHAT CAN THE HARNESS VERIFY?

WHAT CAN THE HARNESS NOT VERIFY?

WHERE DOES A HUMAN INTERVENE?

WHY?

CAN THAT INTERVENTION BECOME:
    a test?
    a policy?
    a tool?
    a skill?
    a contract?
    a deterministic gate?

```

Classify every gap:

```text
CAPABILITY GAP
AUTHORITY GAP
TOOL GAP
KNOWLEDGE GAP
VERIFICATION GAP
OBSERVABILITY GAP
CONTRACT GAP
INFRASTRUCTURE GAP
HUMAN-JUDGMENT GAP
UNKNOWN

```

7. INNER-LOOP ENGINE
META-HARNESS builds the fastest reliable feedback available.
Typical checks:

```text
syntax
lint
typecheck
unit tests
targeted integration tests
contract tests
schema checks
formatting
scope checks
security prechecks

```

The objective is:
Fail as early and cheaply as possible.
The agent should receive machine-readable failure evidence and be permitted to repair within defined limits.

```text
IMPLEMENT
   ↓
CHECK
   ↓
FAIL?
 ┌─┴─┐
YES  NO
 │    │
REPAIR │
 │    │
 └────┘
   ↓
INNER PASS

```

8. OUTER-LOOP ENGINE
The outer loop must provide verification that is meaningfully stronger or more independent than the inner loop.
Possible checks:

```text
full test suite
integration tests
E2E tests
mutation testing
regression testing
security analysis
dependency analysis
architecture checks
API compatibility
negative testing
boundary testing
evidence validation

```

The meta-skill determines which checks belong inside versus outside the agent's normal iteration loop.
General rule:

```text
CHEAP + FREQUENT
        ↓
INNER

EXPENSIVE + EXHAUSTIVE + INDEPENDENT
        ↓
OUTER

```

9. EVIDENCE ENGINE
Every important claim must have an evidence source.

```text
CLAIM
  ↓
EVIDENCE REQUIREMENT
  ↓
EVIDENCE COLLECTION
  ↓
VERIFICATION
  ↓
VERDICT

```

Example:

```text
Agent claim:
"Authentication is secure."

Harness response:

UNVERIFIED

Required evidence:
- authorized access succeeds
- unauthorized access fails
- expired credentials fail
- malformed credentials fail
- regression suite passes
- security checks pass

```

The agent's assertion is never itself sufficient evidence.
10. INTERVENTION MINING
Every human intervention becomes a data point.
Record:

```yaml
intervention:
  run_id:
  category:
  trigger:
  human_action:
  time_cost:
  root_cause:
  repeatable:
  harnessable:

```

Categories:

```text
H1 clarification
H2 planning correction
H3 implementation correction
H4 test correction
H5 environment repair
H6 security intervention
H7 policy intervention
H8 architecture intervention
H9 release intervention

```

Then ask:
Can this intervention be converted into infrastructure?
11. INTERVENTION → CAPABILITY COMPILER
This is the core meta-skill behavior.

```text
HUMAN INTERVENTION
        ↓
ABSTRACT FAILURE
        ↓
REPEATING PATTERN?
        ↓
      YES
        ↓
WHAT IS THE SMALLEST CONTROL?
        ↓
 ┌──────┼────────┬─────────┐
 ▼      ▼        ▼         ▼
TEST   POLICY   SKILL     TOOL
        │
        ▼
HARNESS CHANGE
        │
        ▼
EXPERIMENT
        │
        ▼
MEASURE

```

Example:

```text
Human repeatedly reminds agent to run database rollback tests.

        ↓

Recurring failure identified.

        ↓

Create database-migration skill.

        ↓

Skill requires:
    migration up
    migration down
    schema diff

        ↓

Inner loop executes it automatically.

        ↓

Human intervention rate decreases.

```

12. META-LOOP
META-HARNESS continuously consumes:

```text
agent logs
test failures
PR comments
human corrections
takeovers
production incidents
user feedback
security findings
rollback events
tool failures
skill failures

```

It searches for:

```text
frequency
recurrence
clusters
new failure modes
missing controls
weak controls
false-positive controls
unnecessary human gates

```

Then generates candidate factory improvements.
13. CHANGE POLICY
META-HARNESS must distinguish:

```text
OBSERVATION
"What happened?"

INFERENCE
"Why did it happen?"

HYPOTHESIS
"What change might prevent it?"

EXPERIMENT
"Did the change actually help?"

VERIFIED IMPROVEMENT
"Did the measured outcome improve?"

```

Never convert:

```text
"Agent failed once"

```

directly into:

```text
"Therefore modify the factory."

```

Require sufficient evidence or explicitly label the change experimental.
14. FACTORY CHANGE TYPES
META-HARNESS may propose:

```text
ADD_TEST
MODIFY_TEST
ADD_GATE
MODIFY_GATE
ADD_SKILL
MODIFY_SKILL
ADD_TOOL
MODIFY_TOOL
CHANGE_CONTRACT
CHANGE_OBSERVABILITY
CHANGE_AGENT_CONTEXT
CHANGE_WORKFLOW
CHANGE_POLICY
ADD_HUMAN_GATE
REMOVE_HUMAN_GATE

```

High-impact changes require appropriate authorization.
The meta-skill does not grant itself authority merely because it discovered a possible improvement.
15. AUTHORITY MODEL
Separate:

```text
CAN DISCOVER
CAN PROPOSE
CAN IMPLEMENT
CAN VERIFY
CAN AUTHORIZE

```

These are different permissions.
Example:

```text
META-HARNESS
    CAN_DISCOVER: YES
    CAN_PROPOSE: YES
    CAN_IMPLEMENT: LIMITED
    CAN_VERIFY: YES
    CAN_GRANT_ITSELF_AUTHORITY: NO

```

The system must never silently transform:

```text
capability

```

into:

```text
authority.

```

16. ANTI-GAMING
META-HARNESS must actively search for metric manipulation.
Potential gaming:

```text
reduce task scope
delete failing tests
avoid difficult tasks
avoid PR creation
classify failures as infrastructure
stop before verification
inflate test counts
reduce verification depth

```

Therefore evaluate:

```text
AUTONOMY
+
TASK COMPLETION
+
SCOPE FIDELITY
+
VERIFICATION STRENGTH
+
QUALITY
+
PRODUCTION OUTCOME

```

not autonomy alone.
17. EXPERIMENT ENGINE
Every significant harness modification should ideally become an experiment.

```yaml
experiment:
  hypothesis:
  baseline:
  intervention:
  expected_effect:
  metric:
  duration:
  sample_size:
  result:
  confidence:
  decision:

```

Example:

```yaml
hypothesis:
  "Automatic migration verification reduces human corrections."

baseline:
  human_migration_corrections_per_100_tasks: 18

intervention:
  add_migration_verification_skill: true

metric:
  human_migration_corrections_per_100_tasks

result:
  4

decision:
  retain

```

The factory improves through measured deltas, not narrative confidence.
18. SELF-DIAGNOSTIC LOOP
At scheduled intervals:

```text
1. Inspect factory metrics.
2. Identify largest recurring failure class.
3. Identify current control.
4. Determine whether control is effective.
5. Search for missing evidence.
6. Generate minimal intervention.
7. Run controlled experiment.
8. Compare against baseline.
9. Retain, revert, or escalate.

```

Prioritize by:

```text
frequency × impact × preventability × verification confidence

```

19. BOTTLENECK DETECTION
META-HARNESS must identify the actual constraint.
Possible bottlenecks:

```text
agent reasoning
context availability
tool latency
test runtime
verification
human review
environment provisioning
deployment
missing permissions
missing skills

```

Do not assume the agent is the bottleneck.
Do not add agents when the real bottleneck is verification.
Do not add verification when the real bottleneck is environment setup.
Measure first.
20. FACTORY HEALTH REPORT
META-HARNESS periodically produces:

```yaml
factory_health:
  autonomy:
    rate:
    takeover_rate:
    mean_iterations:

  automation:
    human_comments_per_pr:
    manual_review_minutes:
    automated_pr_rate:

  quality:
    regression_rate:
    escaped_defects:
    mutation_score:
    security_findings:

  bottleneck:
  dominant_failure_class:
  highest_value_improvement:
  confidence:

  recommended_action:

```

21. TERMINAL VERDICTS
Every run ends with an explicit state:

```text
PASS
FAIL
BLOCKED
TOOL_ERROR
UNRESOLVED
HUMAN_REQUIRED

```

Never silently convert uncertainty into success.
22. META-SKILL OUTPUT
When META-HARNESS finishes an analysis or improvement cycle, it returns:

```text
WHAT I FOUND
    Current factory architecture.

WHAT IS STRONG
    Existing controls that demonstrably work.

WHAT IS MISSING
    Missing capabilities, evidence, or governance.

WHAT IS WRONG
    Verified failures or contradictions.

HYPOTHESES
    Proposed explanations for recurring failures.

EXPERIMENT
    Smallest useful test.

CHANGE
    Minimal harness modification.

RESULT
    Measured outcome.

NEXT MOVE
    Retain / revert / investigate / escalate.

```

23. HARD RULES
Rule 1
Do not trust an agent's declaration of success.
Rule 2
Do not create a new agent when a deterministic control would solve the problem.
Rule 3
Do not add complexity without measured need.
Rule 4
Do not remove a human gate merely because it slows the system.
Rule 5
Do not retain a harness change without evidence that it improves the target metric or capability.
Rule 6
Do not allow the meta-loop to silently expand its authority.
Rule 7
Do not confuse autonomy with correctness.
Rule 8
Do not confuse automation with quality.
Rule 9
Do not confuse test quantity with verification strength.
Rule 10
When evidence is insufficient, return UNKNOWN.
24. FINAL META-LOOP
The complete META-HARNESS algorithm is:

```text
             ┌──────────────────────┐
             │     SOFTWARE TASK    │
             └──────────┬───────────┘
                        ↓
               ┌─────────────────┐
               │  MISSION        │
               │  CONTRACT       │
               └────────┬────────┘
                        ↓
               ┌─────────────────┐
               │     AGENT       │
               └────────┬────────┘
                        ↓
               ┌─────────────────┐
               │  INNER LOOP     │
               │   AUTONOMY      │
               └────────┬────────┘
                        ↓
               ┌─────────────────┐
               │  OUTER LOOP     │
               │   AUTOMATION    │
               └────────┬────────┘
                        ↓
                    PRODUCTION
                        ↓
               ┌─────────────────┐
               │   OBSERVATION   │
               └────────┬────────┘
                        ↓
               ┌─────────────────┐
               │  META ANALYSIS  │
               └────────┬────────┘
                        ↓
                 FIND FAILURE
                        ↓
               ┌─────────────────┐
               │  HYPOTHESIS     │
               └────────┬────────┘
                        ↓
                  EXPERIMENT
                        ↓
               ┌─────────────────┐
               │ MEASURE CHANGE  │
               └────────┬────────┘
                        ↓
              ┌─────────┴─────────┐
              │                   │
           IMPROVED             NOT
              │               IMPROVED
              ↓                   ↓
       RETAIN CHANGE           REVERT
              │                   │
              └─────────┬─────────┘
                        ↓
                  NEXT TASK
                        │
                        └──────────────►

```

25. DEFINITION OF DONE
META-HARNESS is functioning when it can demonstrate all of the following:

```text
[ ] Agent can execute a defined software mission.
[ ] Inner loop catches ordinary failures.
[ ] Agent can repair ordinary failures autonomously.
[ ] Outer loop independently verifies the result.
[ ] Evidence is captured for important claims.
[ ] Human intervention is measured and classified.
[ ] Recurring interventions become candidate harness improvements.
[ ] Harness changes are experimentally evaluated.
[ ] Improvements are retained only when evidence supports them.
[ ] Quality does not decline as autonomy increases.
[ ] Authority boundaries remain explicit.
[ ] The factory can identify its own bottleneck.
[ ] The factory can improve without requiring the agent to "just try harder."

```

META-HARNESS PRINCIPLE
The agent is not the software factory.
The harness is the software factory.
The meta-skill is the mechanism by which the factory learns what the harness itself is missing.
