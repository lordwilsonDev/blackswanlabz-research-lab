---
source: ~/Documents/Vault/10_Projects/BlackSwanLabz/BlackSwanLabz-North-Star-Architecture.md
vault-date: 2026-09-22
captured: 2026-09-28
status: active
---

# North Star

BlackSwanLabz's North Star, stated as one sentence:

> **"Help businesses continuously improve by finding operational truth, proving it with measurement, and intervening where it matters — so the business gets better and the people inside it get better at what they do."**

Everything else in the architecture is described as "how we deliver it."

## The five parts

The source note breaks the sentence into five moves:

1. **Find operational truth** — what's actually happening, not what people assume. Evidence before conclusion.
2. **Prove it with measurement** — baseline → change → observation → comparison → result, "applied honestly."
3. **Intervene where it matters** — not everywhere. Automation is optional; decision comes first.
4. **So the business gets better** — measurable improvement, not activity.
5. **And the people inside it get better at what they do** — augmentation over replacement; skills compound toward the direction the business wants to go.

The note is explicit that this is not "sell automation," "be an AI company," or "sell tools" — it frames those as means, and states the North Star as the outcome itself.

## Decision before automation

Every opportunity is scored on five dimensions (evidence, impact, readiness, economics, risk) and routed to one of three outcomes:

- **DO NOTHING** — with a written reason, what was learned, what would change the conclusion, and what to monitor. The source calls this "professional advice," not a failed sale.
- **IMPROVE** — a non-automation intervention: process redesign, training, role change, or a tooling change inside the existing stack.
- **AUTOMATE** — technology reliably handles a defined workflow, with human approval points where consequential.

The source frames automation as one outcome among three, chosen "when the evidence, readiness, and economics support it" — not the default.

## The control loop

A companion architecture note reframes the North Star, together with BlackSwanLabz's internal FDE protocol and a cybernetic-control lens, as "one feedback loop seen from three altitudes" rather than three separate frameworks:

| Altitude | Answers | 
|---|---|
| North Star | *Why*, and what counts as better — the setpoint and the sensing rules |
| FDE protocol | *How* the state is known and who may act — the controller |
| Cybernetic loop | *Whether the loop is actually closed* — the diagnostic |

In control-theory terms: the North Star supplies the **setpoint** (the desired state) and the rule that a baseline must be measured before anything else (the **state estimate**). The controller compares observed state against that setpoint, routes the resulting gap to a capability, gates it by authority, and either executes, recommends, escalates, blocks, or does nothing. Feedback closes the loop by asking whether the gap shrank *because of* the action taken — not merely whether activity occurred. The note also names a **second loop**, above the first: periodically questioning the setpoint itself rather than only adjusting the action, and states that KPIs are designed to "cross-check each other" so a single number cannot be gamed in isolation (an anti-Goodhart safeguard).

## Sources

- `~/Documents/Vault/10_Projects/BlackSwanLabz/BlackSwanLabz-North-Star-Architecture.md`
- `~/Documents/Vault/30_Architecture/North-Star-FDE-Cybernetic-Loop.md`
