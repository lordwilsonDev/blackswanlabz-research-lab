---
source: BlackSwanLabz Research Lab record - Q2B-MBEDDR-001 — State-Machine Capability Tranche
captured: 2026-10-02
status: pending
---

# Q2B-MBEDDR-001 — State-Machine Capability Tranche

## Source basis
mbeddr documents state machines with events, variables, states, transitions, guards, entry/exit/actions, hierarchical states, testing, and verification for unreachable and shadowed transitions.
Sources:
- https://mbeddr.com/userguide/UserGuideExport.html
- https://mbeddr.com/

## Starting question
Build a state-machine capability with event-triggered transitions, guards, entry/exit actions, transition actions, runtime state, and static verification.

## Initial behavior suite
6/6 PASS:
- takeoff/landing sequence
- transition action penalty
- crash transition
- reset
- static reachability
- entry/exit ordering

## Verifier challenge
Three hidden verifier checks:
1. unreachable state
2. guarded transition completely shadowed by an earlier broad guard
3. never-enabled guarded transition

Initial result: 1/3.
The existing verifier detected unreachable states but missed the two guarded cases.

## Verifier correction
Added a bounded finite guard-probe analysis.
Important boundary: this is a bounded diagnostic, not a general proof of satisfiability or non-shadowing.
Corrected verifier result: 3/3.
Original 6/6 behavior remained intact.

## L4 transfer
The same state/guard/transition mechanism was applied to a structurally different domain: a traffic-light controller.
Fresh cases:
- red → green → yellow → red cycle
- emergency from green
- guarded transition priority
- static analysis

Initial static transfer failed because the verifier probe schema lacked the timer input.
After making the probe schema context-aware: 4/4 PASS.
The failure was classified as verifier instrumentation failure, not learner/model capability failure.

## L5 generation
Generated a new pedestrian-walk capability without re-teaching the original state-machine model.
Extension:
- new walk state
- pedestrian request event
- timed return to red
- emergency return
- preservation of prior behavior

Initial L5 suite: 4/5.
The implementation behaved correctly; the verifier failed because its finite probe schema lacked the boolean button input.
After adding boolean inputs to the probe generator: 5/5 PASS.

## Current capability evidence
For this bounded tranche:
- L1/L2/L3-style state-machine behavior: demonstrated
- L4 structural transfer: demonstrated
- L5-style project extension: demonstrated provisionally
- retention: pending
- independent reconstruction: pending
- population terrain: not estimable
- full mbeddr reconstruction: not attempted

## Terrain candidates
Observed demands:
- explicit state representation
- event/guard separation
- ordered transition semantics
- action sequencing
- static reachability
- guard satisfiability/shadow analysis

Observed architectural corrections repeatedly moved from local/special-case logic toward explicit state-machine representation. This is recorded as an observed correction, not a universal causal law.

## Measurement limits
No active learner-effort clock was available that would validly estimate model cognition. Therefore no T_Q2V or TCR is reported.

## Main result
The protocol exposed a recurring distinction between system-under-test defects and verifier defects. Multiple false failures were caused by inadequate verifier input coverage. Verifier audit is therefore a first-class component of Q2B-LTB rather than a postscript.