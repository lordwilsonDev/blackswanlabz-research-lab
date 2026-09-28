---
source: index of operating documents
captured: 2026-09-28
status: active
---

# 08 Operations

These are the operating standards Wilson wrote for running BlackSwanLabz as an evidence-first research-and-automation practice. Several describe the target system rather than what runs today; their own status notes say what exists now (for example, the Day-to-Day Operating Manual opens with one). They are published as written, with private-note links turned into plain text and a few company names redacted (each affected file says so at the top).

Prices in these documents are the offers as written at capture, not a current price list.

## Reading order

| Doc | Role | Words |
|---|---|---:|
| [master-sop.md](master-sop.md) | The master internal operating standard: North Star, finished state, full end-to-end intelligence, automation and continuous-operations SOP | 4,874 |
| [hardened-blueprint-v2.1.md](hardened-blueprint-v2.1.md) | Current architecture (v2.1): the governing equation and three gates (found is not proven is not improved), plus the founding offer | 2,035 |
| [operator-sop.md](operator-sop.md) | Execution runbook: what an operator or agent does, in order, per phase; hard rules for evidence labelling and the three interventions | 2,969 |
| [day-to-day-operating-manual.md](day-to-day-operating-manual.md) | Daily operations: the control-center queues and the day-to-day loop. Opens with a current-state note: the automation described is the target, not what runs today | 2,160 |
| [complete-client-loop.md](complete-client-loop.md) | Frozen single source of truth for the client lifecycle: every module, data flow and integration point | 1,987 |
| [propulsion-engine-sop.md](propulsion-engine-sop.md) | Domain module for safety-critical physical systems; activated by a domain classifier, not run per engagement | 1,054 |
| [fde-customer-intake-sop-v1.3.md](fde-customer-intake-sop-v1.3.md) | Customer intake and environment-discovery SOP (v1.3, frozen) with North Star measurement overlay | 8,585 |
| [research-manual-v1.md](research-manual-v1.md) | Company research manual (manufacturing edition, pilot): the 12 research lanes, evidence rules, decision engine | 2,915 |
| [research-service.md](research-service.md) | The research-based offer, workflow, pitch scripts and delivery mechanics (draft) | 2,125 |
| [north-star-architecture.md](north-star-architecture.md) | The North Star and the four-layer architecture that serves it, with the measurement discipline | 5,461 |
| [north-star-fde-cybernetic-loop.md](north-star-fde-cybernetic-loop.md) | How the North Star, the FDE protocol and a control-loop view fit together as one feedback loop | 1,085 |

## How these relate

```
Master-SOP ............... the standard (what BlackSwanLabz is + does, in full)
   |-- Hardened-Blueprint-v2.1 ... the architecture (the equation + gates + offer)
   |-- Complete-Client-Loop ...... the lifecycle map (frozen)
   |-- Operator-SOP .............. the runbook (do X then Y, per phase)
   `-- Day-to-Day-Operating-Manual  the daily driver (queues + orchestration)
Propulsion-Engine-SOP ....... a domain module the above call into when the
                              target is a safety-critical physical system
FDE intake SOP + Research Manual + Research Service ... intake, research and offer
North Star Architecture + Cybernetic Loop ............. why, and how the loop closes
```
