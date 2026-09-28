---
source: vault:30_Architecture/North-Star-FDE-Cybernetic-Loop.md
vault-date: 2026-09-22
captured: 2026-09-28
status: active
---


# North Star × FDE Protocol × Cybernetic Loop: one control system

**Claim:** these are not three frameworks. They are **one feedback loop seen from
three altitudes**:

| Altitude | Answers | Source |
|---|---|---|
| **North Star** | *Why*, and *what counts as better* (the setpoint and the rules for sensing) | BlackSwanLabz-North-Star-Architecture |
| **FDE protocol** | *How* the state is known and *who may act* (the controller) | BlackSwanLabz-Universal-FDE-Lifecycle-Harness-v1.0, FDE Kernel v0.3 |
| **Cybernetic loop** | *Whether the loop is actually closed* (the diagnostic) | Intent-to-Control-Loop Engineering (Wilson, 2026-09-22) + additions tested the same day |

---

## The loop

```text
            ┌───────────────────── NORTH STAR ─────────────────────┐
            │  "find operational truth, prove it with measurement,  │
            │   intervene where it matters"                         │
            │  → DESIRED STATE (setpoint) + measurement discipline  │
            └──────────────────────────┬────────────────────────────┘
                                       ▼
  ┌──────────── FDE PROTOCOL (controller) ─────────────────────────────┐
  │ Engagement Charter ─► Kernel state (known / unknown / contested)   │
  │   ─► COMPARE observed vs desired  ◄── added by this integration    │
  │   ─► highest-consequence gap ─► required capability ─► provider    │
  │   ─► authority gate (approved / approval-required / prohibited)    │
  │   ─► EXECUTE | RECOMMEND | ESCALATE | BLOCK | DO NOTHING           │
  └──────────────────────────┬─────────────────────────────────────────┘
                             ▼
                  REALITY (client business / our business / our tools)
                             │
                             ▼
  ┌──────────── SENSING (North Star rules, FDE evidence ledger) ───────┐
  │ baseline → same method after → explicit before/after → paired      │
  │ guardrails → score from records, never from self-report           │
  └──────────────────────────┬─────────────────────────────────────────┘
                             ▼
        FEEDBACK: did the gap shrink *because of* the action?
                             │
          ┌──────────────────┴───────────────────┐
          ▼                                      ▼
  FIRST LOOP: adjust the action          SECOND LOOP: question the setpoint
  (revalidate, re-plan, new provider)    (stage transition, target change,
                                          audited: registry / decision record)
```

---

## Element-by-element mapping

| Cybernetic element | North Star provides | FDE protocol provides | Proven in a run? |
|---|---|---|---|
| **Setpoint** | The North Star + client's goal in their own terms | `mission.objective`, `success_metrics` | ✅ Primary metric: milestone 3 baselines |
| **State estimate** | "Baseline before anything else" | `epistemic_state` (known / unknown / contested / stale) | ✅ FDE M007/M008: state-controlled runs beat raw on discipline |
| **Error** | Before → after → difference, explicit | **Missing.** The discovery loop ranks *unknowns*, not the *outcome gap* | ❌ Gap 1 |
| **Controller policy** | Decision cards; DO NOTHING is a real outcome | Kernel transitions + human gate | ✅ Kernel gate, 221 tests |
| **Control authority** | Client approves interventions | `authority` block, policy result states | ✅ 0 harmful / unauthorized actions in 30 M008 runs |
| **Requisite variety** (Ashby) | — | Capability routing: required → qualified provider → acquire / escalate | ✅ Workbench: 4 worker types behind one registry |
| **Actuation** | Intervention layer | Execute under authority | ✅ Workbench handoff OpenCode→dsh on Ornith |
| **Sensor** | 10 measurement categories | Evidence ledger, telemetry | ✅ Today: "did the repo change" beat exit code 0 |
| **Paired metrics** (anti-Goodhart) | "KPIs cross-check each other" | Contradiction tracking | ✅ Pilot sim: contact + booking guardrail + callback age |
| **Delay / stability** | Measurement continues during care | Revalidation triggers, TTLs | ✅ Primary metric: 2-week review cadence |
| **Feedback: causation, not activity** | Value-conversion engine ("capacity released ≠ money") | `VERIFIED` only by the verification layer, never the executor | ✅ Pilot sim retracted a fix that approved a do-nothing system 13–32% of the time |
| **Second loop** (update the setpoint) | "Test against the first three clients" | Registry versioning; decision records | ✅ Primary metric's stage-transition rule |
| **Observer effect** | Measurement available to the client | Blindness guard | ⚠️ Blind guard does not fire on subagents (M008 finding) |

---

## Where the lens finds real gaps (for Wilson to decide on)

1. **The FDE discovery loop has no explicit error step.** It asks "which unknown has
   the highest consequence?", which reduces *uncertainty*. It never asks "how far is
   the observed state from the desired state?", which reduces the *outcome gap*. A mission
   can shrink every unknown and still not move the client's number. Proposed: add
   `COMPARE (observed vs success_metrics)` between UPDATE STATE and REPEAT, with the
   baseline as its input.
2. **Stale state estimate = the M008 finding, restated.** A superseded wrong
   `root_cause` claim can outrank correct later work. In control terms the controller is acting
   on a state estimate it never corrected. Same fix as the open follow-up:
   force explicit disposition of a claim before a new one on the same investigation.
3. **Sensors lie in the same way at every level.** The same failure turned up
   independently four times: subagent narratives (M008), OpenCode exit 0 on a crash, `shutil.which` on
   a broken Codex, an OKR marked MET whose audit events are no longer in the DB. The
   shared rule is **score from records the actor cannot write**. It's already the practice
   in the FDE driver. It isn't yet a stated North Star measurement rule.
4. **The North Star had sensors but no primary signal** (100+ metrics, none designated).
   Fixed for the current stage by BlackSwanLabz-Primary-Metric.

---

## The same loop runs at three levels (recursion)

| Level | Setpoint | Sensor | Controller | Today's instance |
|---|---|---|---|---|
| **Client** | Client's number (e.g. missed calls recovered) | Pilot measurement design | FDE mission | Pilot proposal → decision rule → simulation → retraction |
| **BlackSwanLabz** | North Star, current stage | Baselines Captured + G1–G3 | Wilson's decisions at 2-week reviews | BlackSwanLabz-Primary-Metric |
| **Tools** | "The worker did the task" | Repo changed + tests pass | Workbench runner, governance gate | Qwen → Ornith; context clipping found and fixed |

A loop at one level is only trustworthy if the level below it is closed. A pilot readout
is only as good as the tools that ran it, and a business metric is only as good as the
pilot readouts feeding it.

---

## Master test (from the cybernetic card, applied to every level)

An independent observer can reconstruct: **what was intended → what state existed →
what action occurred → what changed → whether the change was desired → what happens next**,
from records alone, without asking anyone.

- Client level: pilot ledger + decision rule (designed; no client yet).
- Business level: `metrics/baseline-ledger.csv` + `primary_metric.py`. **Passes today**, at 0.
- Tool level: worktree commits with `Worker:` trailers + stored handoff packets. **Passed** in the
  2026-09-22 probe.
