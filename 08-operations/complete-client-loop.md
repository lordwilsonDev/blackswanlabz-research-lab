---
source: vault:10_Projects/BlackSwanLabz/SOPs/Complete-Client-Loop.md
vault-date: 2026-09-01
captured: 2026-09-28
status: active
---

> Redacted for publication: 2 mentions of 2 company names replaced with [company] at the author's direction (2026-09-28). No other changes besides converting private-note links to plain text.


> **BlackSwanLabz SOP set** — SOP index  ·  **this doc:** frozen single-source-of-truth for the client lifecycle loop (every module, data flow, integration point)
>
> Active: Master-SOP · Operator-SOP · Hardened-Blueprint-v2.1 · Day-to-Day-Operating-Manual · Complete-Client-Loop · Propulsion-Engine-SOP  ·  Superseded: Operating-Blueprint-v1 · Loop-v0.1

# BlackSwan Complete Client Loop

**Status:** frozen  
**Created:** 2026-08-08  
**Author:** Lord Wilson / BlackSwanLabz  
**Purpose:** Complete end-to-end client operating loop. Every module, data flow, output, and integration point. Single source-of-truth for client lifecycle. Precedes any automation or outreach.

---

# The loop

```text
                         PROSPECT
                            │
                            ▼
                    PRE-RESEARCH ENGINE
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
     COMPANY           CUSTOMERS          COMPETITORS
        │                   │                   │
        ▼                   ▼                   ▼
   LEADERSHIP           REVIEWS              MARKET
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                     SIGNAL FUSION
                            │
                            ▼
                      AIL / MoIE
                            │
                            ▼
                    OPPORTUNITY MAP
                            │
                            ▼
                         OUTREACH
                            │
                            ▼
                       CUSTOMER
                            │
                            ▼
                    $999 FIRST BUILD
                            │
                            ▼
                       AUTOMATION
                            │
                            ▼
                       DEPLOYMENT
                            │
                            ▼
                 CUSTOMER-JOURNEY LOG
                            │
          ┌─────────────────┼──────────────────┐
          ▼                 ▼                  ▼
       TIME SAVED       MISTAKES          EXCEPTIONS
          │                 │                  │
          └─────────────────┼──────────────────┘
                            ▼
                       MONITORING
                            │
          ┌─────────────────┼──────────────────┐
          ▼                 ▼                  ▼
     COMPETITORS       CUSTOMER VOICE      AUTOMATION
     MONTHLY              MONTHLY           HEALTH
          │                 │                  │
          └─────────────────┼──────────────────┘
                            ▼
                    MONTHLY REPORT
                            │
                            ▼
                      FOLLOW-UP CALL
                            │
                            ▼
                 WHAT CHANGED / WHY?
                            │
                            ▼
                    NEXT OPPORTUNITY
                            │
                            ↺
```

That is the business. Each section below is a **module** inside the loop.

---

# 1. PRE-RESEARCH ENGINE

**Module:** Sensor + Thinker (Loop v0.1)  
**Input:** Company name, public web  
**Output:** Opportunity Map  
**Rule:** 14-layer public-signal collection with competitor-as-control-group framing.  
**Spec:** `BlackSwanLabz-Pre-Research-Engine.md`

Every prospect runs through this before any human contact.

---

# 2. OPPORTUNITY MAP

**Module:** Thinker → Planner transition  
**Output format:**

```text
SIGNAL
↓
SOURCE
↓
OBSERVATION
↓
CROSS-CHECK
↓
HYPOTHESIS
↓
CONFIDENCE
↓
POTENTIAL IMPACT
↓
AUTOMATION POTENTIAL
↓
RECOMMENDED NEXT QUESTION
```

**Rule:** One row per significant finding. Not a research dump.  
**Consume by:** Human reviewer before outreach.

---

# 3. OUTREACH

**Module:** Planner → Operator transition  
**Input:** Opportunity Map  
**Output:** First contact  
**Rules:** 8 non-negotiable CX rules apply from first touch.

1. Plain language, no jargon
2. PDF / Word only, no markdown
3. Client chooses delivery channel
4. Cover note always included
5. Warm intro before sending; no unsolicited surprise attachments
6. Soft follow-up: 5 days = one short nudge, 10 days = archive
7. Phone / SMS option available
8. Beginner-friendly report structure: 1-page summary → key findings → competitor snapshot → "what you might do next" → supporting detail

**Pitch frame:** Team-member relationship, not vendor. References 6000+ hours and custom Intelligence Strategist Architect Engineer system. Permission-based. No pressure.

---

# 4. $999 FIRST BUILD

**Module:** Operator  
**Scope:** 7-phase fixed-scope engagement.

1. Discovery
2. Automation design
3. Build (up to 3 integrations)
4. Testing (normal, missing, invalid, failure, handoff, duplicate)
5. Deployment
6. Documentation
7. 30-day stabilization

**Rule:** Does not promise pre-determined savings before measuring. ROI calculated post-automation.  
**ROI formula:**  
- `(Annual Labor Value of Hours Saved) / Implementation Cost`
- `Payback Period = Implementation Cost / Monthly Savings`

**Example:**  
- 5 hrs/week × $20 × 52 = $5,200/year
- 15 hrs/week × $20 × 52 = $15,600/year

**Positioning:** Eliminating wasted human effort, not "AI consulting."

---

# 5. CUSTOMER-JOURNEY MEMORY

**Module:** Memory (Loop v0.1)  
**Type:** Core system, not side feature.  
**Record type:** Longitudinal per client.

```text
CLIENT
│
├── Initial Research
├── Initial Opportunity
├── Proposal
├── Approval
├── Build
├── Deployment
├── Automation Events
├── Human Interventions
├── Customer Events
├── Problems
├── Fixes
├── Time Saved
├── Mistakes
├── Outcomes
├── Competitor Changes
├── Monthly Reports
└── Follow-Up Calls
```

**Rule:** Six months later you can answer: "What actually happened?"

---

# 6. TIME-SAVED LEDGER

**Module:** Verifier + Memory  
**Track:**

```text
Task
Before automation
After automation
Frequency
Estimated time avoided
Actual measured time where possible
Human interventions
```

**Example table:**

| Workflow | Before | After | Frequency | Estimated monthly time avoided |
|---|---:|---:|---:|---:|
| Lead routing | 8 min | 1 min | 240 | 28 hrs |
| Follow-up | 6 min | 30 sec | 180 | 16.5 hrs |
| Report creation | 2 hrs | 15 min | 4 | 7 hrs |

**Rule:** Call it **capacity released**, not "money saved," unless the business actually reduces payroll or can verify financial impact.  
**Example:** 51.5 hrs/month @ $20/hr = $1,030/month capacity released.

---

# 7. RECURRING ERROR REGISTER

**Module:** Verifier + Memory  
**Schema:**

```text
ERROR
↓
WHEN
↓
WHERE
↓
FREQUENCY
↓
CAUSE
↓
HUMAN / SYSTEM / PROCESS
↓
FIX
↓
DID FIX WORK?
```

**Goal:** After several months, surface process-level patterns, not just error counts.  
**Example insight:** "37% of workflow exceptions originate from incomplete customer information."

---

# 8. HUMAN INTERVENTION TRACKING

**Module:** Verifier + Operator feedback  
**Track:**

```text
Automation
   ↓
Exception
   ↓
Human intervention
   ↓
Reason
   ↓
Resolution
```

**Rule:** If the same human intervention happens 40 times, that is the **next automation candidate.**  
**Output:** System can generate `NEXT AUTOMATION CANDIDATE` proposals.

---

# 9. FOLLOW-UP CALL ENGINE

**Module:** Memory + Operator (human)  
**Structured cadence:**

- First follow-up: "What stood out?"
- Second: "Did we identify something that was actually happening?"
- Third: "Did the automation change the process?"
- Monthly: "What changed since last month?"
- Quarterly: "What should we automate next?"

**Rule:** Record all answers. You are continuously learning the customer's business.

---

# 10. OUTCOME TRACKING

**Module:** Verifier + Memory  
**Schema:**

```text
HYPOTHESIS
     ↓
ACTION
     ↓
EXPECTED RESULT
     ↓
ACTUAL RESULT
     ↓
DELTA
```

**Rule:** Build evidence, not impressive reports.

---

# 11. COMPETITOR CHANGE DETECTION

**Module:** Sensor + Memory  
**Method:** Store previous state. Diff against current state.

```text
MONTH 1
Competitor A: 12 jobs

MONTH 2
Competitor A: 19 jobs

CHANGE: +7

SIGNAL: Possible expansion

MONTH 3
New facility announcement

CONFIRMATION: Expansion hypothesis strengthened
```

**Output:** Competitor intelligence becomes **temporal intelligence**.

---

# 12. CUSTOMER VOICE TREND

**Module:** Sensor + Memory  
**Method:** Track review themes over time.

```text
January
Delivery complaints: 7%

March
Delivery complaints: 11%

June
Delivery complaints: 19%
```

**Rule:** Compare against competitors.  
**Output:** Customer sentiment trajectory, not static reviews.

---

# 13. AUTOMATION HEALTH

**Module:** Verifier + Operator  
**Per deployed automation:**

```text
Executions
Success rate
Failures
Latency
Exceptions
Human interventions
API failures
Credential failures
Downtime
Last successful execution
```

**Kill switch rule:**

```text
ANOMALY
   ↓
THRESHOLD
   ↓
PAUSE AUTOMATION
   ↓
NOTIFY HUMAN
   ↓
INVESTIGATE
   ↓
RESUME
```

---

# 14. SECURITY / ACCESS

**Module:** Operator + Verifier  
**Scope:** Touches customer information, credentials, APIs, business systems, employee data.

**Rules:**

- Least privilege
- Credential separation
- Audit logs
- Access expiration
- Backups
- Recovery procedures
- Human approval for sensitive actions
- Explicit definition of what information will NOT be collected

**Rule:** Not sexy. Essential.

---

# 15. EXIT / PORTABILITY

**Module:** Operator + Memory  
**Contract answers:** "What happens if we stop working together?"

**Client receives:**

- Workflow documentation
- Configuration documentation
- Customer-journey records belonging to them
- Relevant reports
- Exportable data
- Instructions for disabling automation

**Rule:** Makes the offer more trustworthy. Never trap a client.

---

# 16. MONTHLY REPORT

**Module:** Memory → Human  
**Format:** BlackSwan Monthly Intelligence

### BUSINESS
What changed?

### CUSTOMER JOURNEY
Where are customers moving / stalling?

### AUTOMATION
What did the system accomplish?

### TIME
How much capacity was released?

### ERRORS
What mistakes happened most frequently?

### HUMAN INTERVENTIONS
Where did people have to step in?

### CUSTOMER VOICE
What are customers saying?

### COMPETITORS
What changed externally?

### ANOMALIES
What looks unusual?

### OPPORTUNITIES
What should we investigate next?

### RECOMMENDATION
What should the client do?

### NEXT AUTOMATION
What should BlackSwanLabz consider building?

---

# 17. FOLLOW-UP CALL ENGINE (CLOSED LOOP)

**Module:** Memory → Human → Operator  
**Input:** Monthly Report  
**Output:** Recorded answers → new Opportunity Map rows

```text
CUSTOMER
   ↓
AUTOMATION
   ↓
MONITORING
   ↓
REPEATED HUMAN INTERVENTION
   ↓
PATTERN
   ↓
NEXT AUTOMATION OPPORTUNITY
   ↓
PROPOSAL
   ↓
APPROVAL
   ↓
BUILD
   ↓
NEW AUTOMATION
```

The system generates its own sales pipeline.

---

# 18. PRICE PROMISE

**Module:** Business rule  
**Framing:**

> **BlackSwanLabz Price Promise: Once you become a BlackSwanLabz client, we don't raise the agreed recurring service price on you. Your established monthly rate stays your monthly rate.**

**Boundary:** New automations, major expansions, new services, or third-party costs are scoped separately.

**Good-relationship gesture:**

> "You may occasionally see a discount simply because you've been good to work with. We believe good relationships deserve to be rewarded."

---

# 19. RETainer PRICING

**Module:** Business rule  
**Model:** Option A (founding rate)

```text
Months 1–6: $99/month (Founding Care)
Month 7+: $199/month (Standard Care)
```

**Promise:** Once the client reaches $199, that rate never increases.

**What the retainer includes:**

- Continuous intelligence + automation care
- Tracked customer-journey metrics (workflow performance, hours saved, intervention history)
- Monthly reporting
- Competitor intelligence
- Automation health monitoring

---

# 20. HARDENED POSITIONING

> **We don't just automate a process and disappear.**
>
> **We build it, monitor it, maintain it, track the customer journey, measure operational capacity released, identify recurring mistakes, watch competitors, listen to customer feedback, and give you a monthly picture of what changed and what deserves attention next.**
>
> **And once your ongoing rate is established, BlackSwanLabz doesn't raise it. If you've been good to work with, you might even see a discount.**

**Product:** Continuously maintained business intelligence + automation relationship.  
**Not:** "AI consulting."  
**Not:** Standalone automation service.

---

# Integration with Loop v0.1

| Client Loop Module | Loop Machine | Function |
|---|---|---|
| Pre-Research Engine | Sensor | Detects changes across public web, competitor activity, customer voice |
| Signal Fusion / AIL | Thinker | Interprets evidence, identifies anomalies, generates hypotheses |
| Opportunity Map | Thinker → Planner | Designs approved workflows, defines outcomes/risks |
| Outreach | Planner → Operator | Obtains human authorization, executes outreach |
| $999 First Build | Operator | Executes workflows via automation / human handoff |
| Automation Health | Verifier | Validates execution results, logs errors, kill switch |
| Customer-Journey Memory | Memory | Records all events, customer journeys, lessons learned |
| Time-Saved Ledger | Verifier → Memory | Validates outcomes, feeds capacity-released data back |
| Recurring Error Register | Verifier → Thinker | Feeds pattern detection back into hypothesis generation |
| Competitor / Customer Voice Trends | Sensor → Memory | Feeds temporal intelligence back to Sensor |
| Follow-Up Call → Next Opportunity | Memory → Sensor | Closes the loop: new signals from existing relationship |
| Monthly Report | Memory → Human | Communicates state to customer |
| Exit / Portability | Memory → Operator | Enables clean handoff without lock-in |

**Loop direction:** All Memory outputs feed back to Sensor, closing the loop continuously.

---

# First 3 customers: laboratory roadmap

**Customer 1:** Manual-assisted loop execution. Identify breakages.  
**Customer 2:** Automate repeated workflows. Identify generalizable patterns.  
**Customer 3:** Automate additional workflows. Extract common abstraction.  
**Customer 4+:** Deploy standardized known operating pattern.

**Rule:** No expansion of the core 6-machine loop until validation with the first 3 customers is complete.  
**This document** governs what happens inside the loop during validation.

---

# Customer-facing origin story

Past individual project work ([company], [company], prior automation builds) was foundational concept-building for the core BlackSwanLabz system. 6000+ hours across AI, agents, and orchestration formed the custom Intelligence Strategist Architect Engineer system. The arc of work builds a cohesive end-to-end intelligence and automation system.

The generalized operating loop (observe → reason → generate → execute → verify → remember → improve) is the underlying architecture. Every past project was a module inside this loop, not a disconnected offering.

**Customer-facing language:**

> "We gone break it down simply. Nothing is set in stone. I would like to be your team member. This landscape is vast. I have 6000+ hours. The technology is still developing and needs to stay updated. I have created an Intelligence Strategist Architect Engineer system agent. This agent gives strategic intelligence for any part of your organization. With these systems I can help save you time and help red-team issues."
