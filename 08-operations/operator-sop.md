---
source: vault:10_Projects/BlackSwanLabz/SOPs/Operator-SOP.md
vault-date: 2026-09-01
captured: 2026-09-28
status: active
---


> **BlackSwanLabz SOP set** — SOP index  ·  **this doc:** execution runbook — exactly what an operator or agent does, in order, per phase
>
> Active: Master-SOP · Operator-SOP · Hardened-Blueprint-v2.1 · Day-to-Day-Operating-Manual · Complete-Client-Loop · Propulsion-Engine-SOP  ·  Superseded: Operating-Blueprint-v1 · Loop-v0.1

# BlackSwanLabz Operator SOP v1.0

## Purpose

This document is the operational spine. It tells an operator or agent **exactly what to do, in what order, with what inputs, and what acceptable outputs look like** for each phase of a BlackSwanLabz client engagement.

Every exception, handoff, and quality gate is explicit.

---

## 0. Hard rules before anything else

### Evidence

* Public evidence only generates research hypotheses.
* Firsthand/experience evidence is a validation lead, not a published fact.
* Inference is never presented as fact. Label every claim: **Fact / Observation / Inference / Hypothesis / Unknown**.
* All findings require at least one source.

### HIPAA / PHI

* BlackSwanLabz does not accept, process, store, transmit, or automate PHI/ePHI.
* If a workflow touches health information: **decline or escalate immediately**.

### Intervention rules

* Only three valid interventions: **DO NOTHING**, **IMPROVE**, **AUTOMATE**.
* Finding a problem ≠ proving a problem.
* Proving a problem ≠ delivering improvement.
* Never claim value unsupported by evidence.
* No guaranteed savings, 100% success rates, or autonomous optimization claims until the ledger proves them.

### Scope

* $999 founding engagement is one defined business-improvement intervention.
* Out-of-scope work requires a separate SOW.
* Implementation-boundary language only: never say "production-ready."

---

## 1. Phase map

```text
Phase 0 — Discovery & Qualification
Phase 1 — Research & Intelligence
Phase 2 — Opportunity Mapping & Decision
Phase 3 — Baseline & Validation
Phase 4 — Intervention Design
Phase 5 — Implementation
Phase 6 — Measurement & ROI
Phase 7 — Monitoring & Maintenance
Phase 8 — Monthly Intelligence & Next Opportunity
```

Each phase has:
* objective
* inputs
* steps
* outputs
* quality gates
* handoff criteria
* who/what executes it
* estimated duration

---

## 2. Phase 0 — Discovery & Qualification

### Objective

Find companies worth approaching and qualify them before spending research budget.

### Inputs

* Geography filter: Fox Valley / Wisconsin / region
* Industry filter: manufacturing / logistics / distribution / similar
* Size filter: 20–250 employees preferred
* Sources: public filings, job boards, review sites, news, LinkedIn, competitor maps

### Steps

1. Run Market Discovery Engine ranking.
2. Apply scorecard: operational friction, automation potential, evidence strength, accessibility, economic potential, urgency, competitive pressure, risk.
3. Produce ranked list: TOP 50 → TOP 20 → TOP 10 → TOP 3.
4. For TOP 3, run lightweight pre-screen.
5. Check HIPAA boundary; decline immediately if engaged activity involves PHI.
6. Store candidate record with score and pre-screen notes.

### Outputs

* Ranked prospect list
* TOP 3 candidate cards

### Quality gates

* Every score has a cited reason.
* HIPAA boundary checked.
* No unsolicited outreach before warm intro or client approval.

### Handoff

Pass TOP 3 to Phase 1 research.

---

## 3. Phase 1 — Research & Intelligence

### Objective

Build a defensible operational intelligence package for one company.

### Inputs

* Company name
* Authorized research scope
* Pre-screen notes

### Steps

#### 3.1 Data collection

Collect across all 12 research lanes:

1. Customer
2. Employee
3. Leadership
4. Operations
5. Quality
6. Logistics
7. Sales
8. Customer journey
9. Technology
10. Competitors
11. Reputation
12. Strategic / external signals

For each lane:
* Collect public evidence only.
* Classify every item: Fact / Observation / Inference / Hypothesis / Unknown.
* Record source and timestamp.
* Note firsthand experience separately as validation lead.

#### 3.2 Company DNA

Map:

* WHO: customers, employees, leadership, suppliers
* WHAT: products, services, revenue drivers
* HOW: processes, systems, decisions, handoffs, bottlenecks
* CUSTOMERS: journey stages, pain signals, repeat behavior
* PEOPLE: roles, workflows, complaints, hiring patterns
* SYSTEMS: tools, integrations, data flows
* PROCESSES: inputs, steps, approvals, exceptions
* COMPETITORS: positioning, strengths, gaps
* RISKS: regulatory, operational, market
* OPPORTUNITIES: preliminary hypotheses

#### 3.3 MoIE / adversarial analysis

For every major finding:

* Ask: "What if we're wrong?"
* Identify contradicting evidence.
* Generate competing hypotheses.
* Falsify weak conclusions.

Output must include **contradictions** alongside **supporting signals**.

#### 3.4 Intelligence file assembly

Produce a 20-section intelligence file:

1. Company overview
2. Leadership
3. Employees / workforce
4. Customers
5. Products / services
6. Operations
7. Quality
8. Logistics
9. Sales
10. Customer journey
11. Technology / systems
12. Competitors
13. Reputation / reviews
14. Strategic signals
15. Hiring signals
16. Employee friction signals
17. Evidence classification summary
18. MoIE contradictions
19. Opportunity hypotheses
20. Research metadata / sources

### Outputs

* 20-section intelligence file
* MoIE contradiction report
* Opportunity hypothesis list

### Quality gates

* Every hypothesis is falsifiable.
* Every signal has a source.
* Inference is never labeled fact.
* HIPAA boundary remains clear.

### Handoff

Pass intelligence file to Phase 2.

---

## 4. Phase 2 — Opportunity Mapping & Decision

### Objective

Convert research into prioritized, scored, decision-ready opportunities.

### Inputs

* 20-section intelligence file
* MoIE contradiction report
* Opportunity hypothesis list

### Steps

#### 4.1 Opportunity scoring

Score each opportunity on 5 dimensions:

1. **Evidence** — how strong is the supporting evidence?
2. **Impact** — how much operational/financial effect?
3. **Readiness** — how ready is the client to act?
4. **Economics** — does ROI justify intervention?
5. **Risk** — what could go wrong?

Apply veto gates where required.

#### 4.2 Economic analysis

For each candidate:

* Estimate annual labor value of hours saved.
* Estimate implementation cost.
* Compute ROI = (annual labor value) / (implementation cost).
* Compute payback period = implementation cost / monthly savings.
* If ROI does not clear threshold, mark **DO NOTHING**.

#### 4.3 Decision Card

Every opportunity receives a formal Decision Card YAML with required fields:

```yaml
opportunity: ""
evidence: ""
contradicting_evidence: ""
impact: ""
confidence: ""
readiness: ""
economic_case: ""
risk: ""
alternatives: ""
recommended_action: ""  # DO_NOTHING | IMPROVE | AUTOMATE
why: ""
why_not_other_options: ""
revisit_condition: ""
measurement_plan: ""
owner: ""
```

#### 4.4 Review

Founder reviews all Decision Cards.
AI drafts; human approves.

### Outputs

* Scored opportunity list
* Decision Card YAML for each candidate
* Recommendation list with veto rationale

### Quality gates

* No opportunity proceeds without a completed Decision Card.
* Economic threshold must be explicit.
* All five dimensions must be present.

### Handoff

Pass approved opportunity to Phase 3.

---

## 5. Phase 3 — Baseline & Validation

### Objective

Establish pre-intervention measurement and validate the opportunity with the client.

### Inputs

* Approved Decision Card
* Opportunity recommendation

### Steps

#### 5.1 Baseline design

For each metric:

```text
Task:
Current state:
Measurement method:
Frequency:
Owner:
```

Examples:

```text
Task: Order status inquiry
Current state: 18 minutes per inquiry, 47 inquiries/week
Measurement method: Time logs / system logs
Frequency: Weekly for 2 weeks
Owner: Office manager
```

#### 5.2 Client validation

Present findings to client:

* Company snapshot
* 2–3 evidence-backed observations
* Opportunity hypothesis
* Contradictions / competing explanations
* Preliminary recommendation
* Potential impact

Ask: **"Walk me through what actually happens."**

#### 5.3 Workflow interview

Use five questions for every workflow:

1. What triggers this?
2. Who does it?
3. What systems do they use?
4. Where does it slow down or break?
5. What happens when someone makes a mistake?

#### 5.4 Authorization

Client must authorize:

* research scope
* system access
* workflow observation
* intervention approach
* measurement approach

#### 5.5 Time-saved ledger setup

Initialize ledger fields for every tracked task:

```text
Task | Before automation | After automation | Frequency | Estimated time avoided | Actual measured time | Human interventions
```

### Outputs

* Baseline measurement plan
* Client authorization record
* Time-saved ledger template
* Updated intelligence file

### Quality gates

* Baseline is measurable before intervention.
* Client has explicitly authorized scope.
* No intervention begins before baseline is recorded.

### Handoff

Pass authorized opportunity to Phase 4.

---

## 6. Phase 4 — Intervention Design

### Objective

Design the smallest reliable intervention for the approved opportunity.

### Inputs

* Decision Card
* Baseline plan
* Client authorization
* Time-saved ledger

### Steps

#### 6.1 Intervention selection

Apply the three-option rule:

* **DO NOTHING** — if economics, readiness, or risk veto.
* **IMPROVE** — if process redesign is simpler, cheaper, or safer than automation.
* **AUTOMATE** — only if automation passes all checks.

#### 6.2 Ecosystem audit

Before designing automation, list what the client already uses:

* Email
* Calendar
* CRM / ERP
* Spreadsheets
* Chat / Teams / Slack
* Existing APIs
* Existing automation
* Cloud services

#### 6.3 Automation design checklist

Every automation must pass:

* **DESIGN** — what exactly happens?
* **INPUT** — where does information come from?
* **PROCESS** — what does AI do?
* **DECISION** — where does human approve?
* **OUTPUT** — what happens after?
* **FAILURE** — what if something breaks?
* **LOGGING** — how do we know it ran?
* **ROLLBACK** — how do we stop it?

#### 6.4 Implementation plan

* Step-by-step build sequence
* Testing plan
* Deployment plan
* Rollback plan
* Communication plan for client team

### Outputs

* Intervention design document
* Implementation plan
* Test plan
* Rollback plan

### Quality gates

* Smallest reliable intervention chosen.
* No "fancy AI" for its own sake.
* All checklist items answered.
* Client approved design before build.

### Handoff

Pass to Phase 5.

---

## 7. Phase 5 — Implementation

### Objective

Build, test, and deploy the approved intervention.

### Inputs

* Intervention design document
* Implementation plan
* Client authorization

### Steps

#### 7.1 Build

* Configure integrations using client's existing ecosystem.
* Write scripts only when necessary.
* Implement human approval gates where required.
* Add logging at every step.

#### 7.2 Test

Test suite:

* Happy path
* Edge cases
* Failure scenarios
* Bad data handling
* Security boundaries
* Recovery / rollback

#### 7.3 Client approval

Client reviews test results.
Client approves deployment.

#### 7.4 Deploy

* Graduated rollout preferred.
* Monitor first 24 hours closely.
* Provide client team with rollback instructions.

### Outputs

* Built intervention
* Test results
* Deployment record
* Rollback record

### Quality gates

* All tests pass.
* Client approved.
* Rollback plan exists and is communicated.

### Handoff

Pass to Phase 6.

---

## 8. Phase 6 — Measurement & ROI

### Objective

Prove whether the intervention worked.

### Inputs

* Baseline measurement plan
* Time-saved ledger template
* Deployed intervention

### Steps

#### 8.1 Measurement period

Run for minimum 2–4 weeks.

Collect:

* Task times before and after
* Error rates before and after
* Human interventions count
* Frequency of task
* Actual measured outcomes

#### 8.2 ROI calculation

```text
ROI = (annual labor value of hours saved) / implementation cost
Payback period = implementation cost / monthly savings
```

#### 8.3 Ledger update

Populate time-saved ledger with actuals.

#### 8.4 Client report

Present:

* What was done
* What was measured
* What changed
* Economic value
* What to watch going forward

### Outputs

* Measurement report
* Time-saved ledger
* ROI calculation
* Client-facing report

### Quality gates

* Measurement compares against baseline, not impression.
* ROI formula applied consistently.
* Client receives report before ongoing billing transitions.

### Handoff

Pass to Phase 7.

---

## 9. Phase 7 — Monitoring & Maintenance

### Objective

Keep the intervention working and detect drift.

### Inputs

* Deployed intervention
* Measurement baseline
* Alert thresholds

### Steps

#### 9.1 Monitoring setup

* Monitor execution success/failure.
* Monitor client workflow changes.
* Monitor API / system changes.
* Monitor repeated human interventions (signal: friction returned).

#### 9.2 Exception-first response

Do not manually review every execution.

Act only when:

* failure rate increases
* API changes
* customer response time changes
* repeated employee interventions detected

#### 9.3 Maintenance

* Fix failures promptly.
* Update integrations when APIs change.
* Retire automation if it no longer provides value.

### Outputs

* Monitoring dashboard / alerts
* Maintenance log
* Exception queue

### Quality gates

* System runs unattended when healthy.
* Human acts only on exceptions.

### Handoff

Pass to Phase 8.

---

## 10. Phase 8 — Monthly Intelligence & Next Opportunity

### Objective

Keep the client relationship fresh and continuously discover the next intervention.

### Inputs

* Monitoring data
* Client business changes
* Competitor intelligence
* Customer signals
* Employee signals
* Pattern library

### Steps

#### 10.1 Monthly intelligence cycle

Every month:

1. Refresh company DNA with public signals.
2. Review competitor changes.
3. Review customer reviews / complaints.
4. Review employee signals.
5. Review automation health.
6. Review error patterns.
7. Identify new opportunity hypotheses.

#### 10.2 Pattern check

Query pattern library for recurring patterns:

* Same pain in another company
* Same root cause
* Same automation candidate

If pattern repeats 3+ times, consider packaging as a regional offering.

#### 10.3 Client report

Deliver monthly report with sections:

1. What changed?
2. What improved?
3. What are customers saying?
4. What's happening internally?
5. What competitors are doing?
6. What's working in automation?
7. What's next?

#### 10.4 Next opportunity

From monthly intelligence, surface 1–2 new opportunity candidates.

Present to client for decision.

### Outputs

* Monthly intelligence report
* Updated company DNA
* Pattern library entry
* Next opportunity brief

### Quality gates

* Report is plain language, no jargon.
* PDF or Word only; no markdown to client.
* Report is diagnostic interface into the system, not the product itself.

### Handoff

Loop back to Phase 2 for new opportunity, or Phase 4 for approved intervention.

---

## 11. Role assignments

### Founder / Systems Orchestrator

* Phases 0, 2, 4, 6 strategic decisions
* Client relationships
* High-risk approvals
* System design

### Research Intelligence Analyst (AI-assisted)

* Phase 1 execution
* MoIE adversarial analysis
* Quality control

### Automation Engineer

* Phase 5 build and test
* Phase 7 maintenance

### Customer Success / Relationship Manager

* Phase 3 client validation
* Phase 6 report delivery
* Phase 8 monthly client report

### AI / Software systems

* Phase 1 data collection and classification
* Phase 7 monitoring and alerting
* Phase 8 pattern detection

---

## 12. Daily operating rhythm

### 8:00–8:30 — Intelligence Sweep

* Review overnight changes across clients, competitors, prospects.
* Produce morning brief: counts + human actions required.

### 8:30–10:00 — Prospecting / Research

* Advance research for TOP candidates.
* Update intelligence files.
* Run MoIE on new findings.

### 10:00–11:00 — Outreach

* Contact strongest prospects.
* Respond to inbound replies.
* Classify responses and generate reply drafts for approval.

### 11:00–12:00 — Client / Prospect Calls

* Discovery calls for new prospects.
* Validation calls for qualified opportunities.
* Follow-up calls for active clients.

### 1:00–3:00 — Build Block

* Build approved automations.
* Test and deploy.
* Resolve exceptions from monitoring.

### 3:00–4:00 — Measurement & Reporting

* Update time-saved ledgers.
* Draft client reports.
* Review ROI calculations.

### 4:00–4:30 — End-of-Day Review

* Today's results.
* Tomorrow's queue.
* Human decisions required.

---

## 13. Weekly operating rhythm

### Monday

* Weekly plan from overnight brief.
* Prospect pipeline review.
* Prioritize builds and client work.

### Wednesday

* Midweek research check.
* MoIE review of new findings.
* Update TOP prospects.

### Friday

* Pipeline review: prospects, conversations, proposals, clients.
* Delivery review: builds, failures, maintenance.
* Value review: hours saved, errors reduced, capacity released.
* Intelligence review: new patterns, competitor moves.
* Business review: revenue, CAC, delivery time.
* Weekly question: **"What did we learn this week that makes the next client easier?"**
* Write pattern library entry if warranted.

---

## 14. Monthly operating rhythm

### Week 1

* Client intelligence refresh for active clients.
* Competitor movement review.
* Customer signal review.
* Error pattern review.

### Week 2

* Automation health review.
* Time-saved ledger audit.
* ROI verification.
* Draft monthly reports.

### Week 3

* Client report delivery.
* Client call / review meeting.
* Next-opportunity brief.

### Week 4

* Pattern library update.
* Business metrics review.
* Pipeline refresh for new prospects.
* System improvements / automation of internal workflows.

---

## 15. Communication standards

### Internal

* All research labeled: Fact / Observation / Inference / Hypothesis / Unknown.
* Decision Cards are authoritative; no intervention without one.
* Every exception creates a ticket.

### External (client-facing)

* Plain language; no jargon.
* PDF or Word only.
* Client chooses delivery channel.
* Cover note always included.
* Warm intro before sending; no unsolicited attachments.
* Soft follow-up: day 5 = short nudge; day 10 = archive.
* Phone/SMS option available.
* Beginner-friendly structure:
  1. One-page summary
  2. Key findings
  3. Competitor snapshot
  4. "What you might do next"
  5. Supporting detail

---

## 16. Non-negotiable rules summary

1. Evidence before claim.
2. Inference never presented as fact.
3. HIPAA/PHI absolute exclusion.
4. Three interventions only: DO NOTHING / IMPROVE / AUTOMATE.
5. Finding ≠ proving ≠ improving.
6. Measurement before and after.
7. Baseline before deployment.
8. Client approval before intervention.
9. Rollback plan before deployment.
10. Pattern library updated after every engagement.
11. Warm intro before outreach.
12. Plain language to client.
13. Implementation-boundary language only.
14. No guaranteed savings or success-rate claims.
15. The system searches for where attention is warranted; BlackSwanLabz does not manufacture work.

---

## 17. Document control

* Version: 1.0
* Status: Active
* Supersedes: prior fragmented phase specs
* Maintained by: Founder / Systems Orchestrator
* Review cycle: quarterly or after 3rd client loop
