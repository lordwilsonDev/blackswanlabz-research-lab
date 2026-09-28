---
source: vault:10_Projects/BlackSwanLabz/SOPs/Day-to-Day-Operating-Manual.md
vault-date: 2026-09-15
captured: 2026-09-28
status: active
---

> Redacted for publication: 5 mentions of 5 company names replaced with [prospect] at the author's direction (2026-09-28). No other changes besides converting private-note links to plain text.


> **BlackSwanLabz SOP set** — SOP index  ·  **this doc:** daily operations — the control-center queues and the day-to-day loop
>
> Active: Master-SOP · Operator-SOP · Hardened-Blueprint-v2.1 · Day-to-Day-Operating-Manual · Complete-Client-Loop · Propulsion-Engine-SOP  ·  Superseded: Operating-Blueprint-v1 · Loop-v0.1

# BlackSwanLabz — Day-to-Day Operating Manual

> **CURRENT STATE, 2026-09-15 — read this before anything below.** Everything in this manual describes the *finished machine* — a discovery engine, auto-classified responses, monitoring dashboards, an "ask what happened overnight" command. As verified in BlackSwanLabz-Position-Dossier-2026-09-14, **none of that automation exists or is running yet.** Real current state: zero dials made on Batch 1, zero active clients, the GHL account has never had a funnel built in it. There is no orchestration layer to operate — there's a phone, a list of 5 companies, and scripts already written in BlackSwanLabz-Batch1-Dial-Sheet.
>
> **If you are a new hire or helper reading this to figure out what to do today:** skip to §26 below. Everything from §2–25 is the target state this business is built toward, not a queue that exists right now. Don't look for a dashboard — there isn't one yet. The manual stays as-is below because it's the right design to grow into; it's just not where the business is today.

## 1. The core operating principle

BlackSwanLabz runs on one continuous loop:

> **Find → Research → Validate → Contact → Diagnose → Improve/Automate → Measure → Monitor → Report → Discover the next opportunity.**

You are **not supposed to manually perform every step**.

Your job is increasingly to operate the orchestration layer.

---

# 2. Daily Control Center

Every morning, BlackSwanLabz should produce a single dashboard:

### TODAY

| Queue            | What you're looking for               |
| ---------------- | ------------------------------------- |
| 🔎 Research      | Companies requiring research          |
| 📬 Outreach      | Prospects requiring contact           |
| 💬 Responses     | Prospects who replied                 |
| 📞 Calls         | Today's client/prospect conversations |
| 🛠️ Builds       | Automations awaiting work             |
| ⚠️ Exceptions    | Failures requiring human judgment     |
| 📊 Measurement   | Metrics needing verification          |
| 👁️ Monitoring   | Client systems showing changes        |
| 🧠 Opportunities | New opportunities discovered          |
| 📄 Reports       | Reports due                           |

You should be able to open one screen and ask:

> **"What needs me today?"**

Everything else should be handled by the infrastructure.

---

# 3. Morning Operating Cycle

## 8:00–8:30 — Intelligence Sweep

The system checks:

### Client changes

* website changes
* job postings
* leadership changes
* competitor activity
* customer reviews
* news
* public announcements
* operational signals

### Internal changes

* automation failures
* API changes
* pending approvals
* unusual customer activity
* unresolved errors

Output:

```text
BLACKSWAN MORNING BRIEF

3 client changes
2 competitor changes
1 automation warning
4 new opportunities
1 human decision required
```

You don't read everything.

**You read what changed.**

---

# 4. Prospecting Block

## 8:30–10:00 — Find the Next Businesses

The discovery engine evaluates the regional/company pipeline.

Example:

```text
TOP 50
 ↓
TOP 20
 ↓
TOP 10
 ↓
TOP 3
```

For each candidate:

### Research

* company
* industry
* employees
* leadership
* hiring
* customer voice
* competitors
* operational signals
* technology
* logistics
* employee friction

Then MoIE attacks the conclusions.

The output becomes:

```text
COMPANY
     ↓
SIGNALS
     ↓
CONTRADICTIONS
     ↓
OPPORTUNITIES
     ↓
CONFIDENCE
     ↓
RECOMMENDATION
```

---

# 5. Outreach

## 10:00–11:00

You contact the strongest prospects.

But you're not sending:

> "We do AI automation."

You're sending:

> **"We found something worth looking at."**

The outreach should be based on actual research.

### Prospect package

```text
Company snapshot
+
2–3 evidence-backed observations
+
potential opportunity
+
competitor context
+
offer to provide deeper analysis
```

The goal isn't to sell the whole system.

### Goal #1:

**Get the conversation.**

---

# 6. Response Management

When somebody responds:

The system classifies the response.

```text
INTERESTED
QUESTIONS
WANTS CALL
WANTS REPORT
NOT INTERESTED
LATER
REFERRAL
```

Then generates the appropriate response for your approval.

You remain the human relationship layer.

---

# 7. Client Call

## 11:00–12:00

The call is primarily **discovery**.

You are trying to determine:

### What actually happens?

Not:

> "What AI do you want?"

Instead:

> "Walk me through what happens from the moment X occurs until it's finished."

Capture:

```text
PERSON
 ↓
ACTION
 ↓
SYSTEM
 ↓
DECISION
 ↓
HANDOFF
 ↓
WAIT
 ↓
ERROR
 ↓
RESULT
```

---

# 8. The Five Questions

For almost every workflow:

### 1.

**What triggers this?**

### 2.

**Who does it?**

### 3.

**What systems do they use?**

### 4.

**Where does it slow down or break?**

### 5.

**What happens when someone makes a mistake?**

Those five questions expose a surprising amount of operational friction.

---

# 9. Afternoon Build Block

## 1:00–3:00

Now the system moves from intelligence to intervention.

For every opportunity:

```text
Evidence
 ↓
Baseline
 ↓
Economic value
 ↓
Readiness
 ↓
Risk
 ↓
Decision
```

Then:

### DO NOTHING

If the economics don't work.

### IMPROVE

If process redesign is better.

### AUTOMATE

If automation is justified.

---

# 10. Automation Construction

When automation is approved:

Don't automatically build another giant system.

First ask:

> **What does the client already have?**

Potentially:

```text
ChatGPT
Claude
Microsoft
Google
CRM
ERP
Email
Calendar
Slack/Teams
Existing APIs
Existing automation
```

Then orchestrate those systems.

Your role is:

# **Make the existing ecosystem work together.**

---

# 11. Automation Build Checklist

Every automation passes:

### DESIGN

What exactly happens?

### INPUT

Where does the information come from?

### PROCESS

What does AI do?

### DECISION

Where does a human approve?

### OUTPUT

What happens afterward?

### FAILURE

What happens if something breaks?

### LOGGING

How do we know it ran?

### ROLLBACK

How do we stop it?

---

# 12. Measurement

Before deployment:

**BASELINE IT.**

For example:

```text
Current:
47 orders/week
18 min/order
7 errors/week
3 follow-ups/order
```

After automation:

```text
52 orders/week
9 min/order
2 errors/week
1 follow-up/order
```

Now you have evidence.

---

# 13. Daily Monitoring

The system watches deployed workflows.

You don't.

Unless something goes wrong.

### Normal

```text
Automation healthy
247 executions
0 failures
```

No action.

### Abnormal

```text
Automation failure rate ↑
API changed
Customer response time ↑
Repeated employee intervention
```

That becomes your queue.

---

# 14. Exception-First Operations

This is one of the most important principles.

Your day should **not** look like:

> manually checking 100 automations.

It should look like:

```text
SYSTEM
   ↓
MONITOR
   ↓
NORMAL?
   │
 ┌─┴─┐
YES  NO
 │    │
 ↓    ↓
LOG  YOU
      ↓
   INVESTIGATE
```

You spend human time where the system cannot safely decide.

---

# 15. Customer Journey Monitoring

Every client has a journey model.

For example:

```text
Lead
 ↓
Contact
 ↓
Quote
 ↓
Order
 ↓
Production
 ↓
Delivery
 ↓
Support
 ↓
Repeat
```

The system looks for:

* delays
* abandonment
* complaints
* repeated questions
* unusual behavior
* communication gaps

---

# 16. Employee Friction Monitoring

Look for repeated operational complaints.

Examples:

> "I have to enter this twice."

> "Nobody knows who handles that."

> "I have to email three people."

> "We keep missing these."

Those aren't just complaints.

They're **workflow signals**.

---

# 17. Error Intelligence

Every repeated error gets classified.

```text
ERROR
 ↓
FREQUENCY
 ↓
ROOT CAUSE
 ↓
COST
 ↓
PREVENTABILITY
```

Then:

> Can training solve it?

> Can process redesign solve it?

> Can automation prevent it?

---

# 18. End-of-Day Intelligence Review

## 4:00–4:30

The system produces:

### TODAY'S RESULTS

```text
Prospects researched: 7
Outreach sent: 4
Replies: 2
Calls: 1
Automations built: 1
Automations monitored: 12
New opportunities: 5
Critical issues: 0
```

Then:

### HUMAN DECISIONS

Only the things requiring you.

---

# 19. Weekly Operating Cycle

Every Friday, review:

### Pipeline

* prospects
* conversations
* proposals
* clients

### Delivery

* builds
* deployments
* failures
* maintenance

### Value

* hours saved
* errors reduced
* capacity released
* measurable business outcomes

### Intelligence

* new patterns
* competitor movements
* customer trends

### Business

* revenue
* recurring revenue
* acquisition cost
* delivery time

---

# 20. Weekly Question

The most important question:

> **"What did we learn this week that makes the next client easier?"**

Put the answer into the Pattern Library.

---

# 21. Monthly Client Cycle

Every month:

```text
RESEARCH
 ↓
CUSTOMER VOICE
 ↓
EMPLOYEE SIGNALS
 ↓
COMPETITOR ANALYSIS
 ↓
AUTOMATION HEALTH
 ↓
VALUE MEASUREMENT
 ↓
ERROR ANALYSIS
 ↓
NEW OPPORTUNITIES
 ↓
REPORT
 ↓
CLIENT CALL
```

The client gets:

### 1-page executive summary

**What changed?**

### Performance

**What improved?**

### Customer

**What are customers saying?**

### Operations

**What's happening internally?**

### Competitors

**What's changing externally?**

### Automation

**What's working?**

### Opportunities

**What's next?**

---

# 22. Six-Month Cycle

Because your founding offer is:

**$99/month × 6 months**

the six-month period should deliberately prove the model.

### Month 1

Baseline + first intervention.

### Month 2

Measurement + maintenance.

### Month 3

Customer + employee intelligence.

### Month 4

Competitor evolution.

### Month 5

Pattern discovery.

### Month 6

Full value review.

Then:

**$199/month continuous intelligence + maintenance.**

---

# 23. What You Do vs. What the System Does

This is critical.

## SYSTEM

```text
Research collection
Data organization
Signal detection
Competitor monitoring
Review monitoring
Change detection
Report drafting
Metric calculations
Automation monitoring
Error classification
Opportunity generation
Follow-up reminders
Documentation
```

## YOU

```text
Client relationships
Strategic judgment
Final recommendations
High-risk decisions
Approvals
Complex troubleshooting
Sales conversations
Trust
Negotiation
Architecture decisions
```

Your goal is:

> **The system handles volume. You handle judgment.**

---

# 24. The BlackSwanLabz Daily Command

Eventually you should be able to ask:

> **"What happened overnight?"**

And get:

```text
BLACKSWAN MORNING BRIEF

CLIENTS
3 changes detected.

AUTOMATIONS
14 healthy.
1 requires attention.

CUSTOMERS
2 recurring complaints detected.

EMPLOYEES
1 repeated workflow friction detected.

COMPETITORS
Competitor X changed positioning.

PROSPECTS
Company Y moved into TOP 3.

OPPORTUNITIES
4 generated.
2 high confidence.

HUMAN ACTIONS
1 approval.
1 client call.
1 investigation.
```

That is what **systems orchestration** looks like in practice.

---

# 25. The Business Becomes a Machine

Eventually the operating model becomes:

```text
                    BLACKSWANLABZ
                          │
             ┌────────────┴────────────┐
             │                         │
       MARKET INTELLIGENCE       CLIENT INTELLIGENCE
             │                         │
       FIND COMPANIES             UNDERSTAND BUSINESS
             │                         │
             └────────────┬────────────┘
                          ↓
                    MOIE ANALYSIS
                          ↓
                  OPPORTUNITY ENGINE
                          ↓
               ┌──────────┼──────────┐
               ↓          ↓          ↓
           NOTHING      IMPROVE    AUTOMATE
                                     ↓
                                  DEPLOY
                                     ↓
                                  MEASURE
                                     ↓
                                  MONITOR
                                     ↓
                                  MAINTAIN
                                     ↓
                              MONTHLY REPORT
                                     ↓
                             NEW OPPORTUNITY
                                     ↓
                              PATTERN LIBRARY
                                     ↓
                            REGIONAL INTELLIGENCE
                                     ↓
                              MARKET DISCOVERY
```

### That's your day-to-day business.

And the most important operational rule I'd put at the very top of the SOP is:

> **BlackSwanLabz does not manufacture work to keep itself busy. The system continuously searches for evidence of where attention is actually warranted.**

That keeps the company from becoming another consulting shop that produces reports because reports are what it sells.

---

# 26. WHAT TO ACTUALLY DO TODAY (current state, 2026-09-15)

This section is the real, current job — the only part of this manual that's live right now. No automation exists yet. Everything here can be done by one person with a phone, a spreadsheet, and the scripts already written. If someone new is helping, this is their entire job until told otherwise.

### The daily loop, as it actually exists today

1. **Open BlackSwanLabz-Deal-Pipeline.** Find the next un-dialed company in Batch 1 ([prospect], [prospect], [prospect], [prospect], [prospect]).
2. **Open BlackSwanLabz-Batch1-Dial-Sheet.** Find that company's script — angle, opener, the full line, the close. Read it before calling. Don't improvise the opener.
3. **Make the call.**
4. **Log it immediately**, in the Deal-Pipeline's Batch Outreach Log and per-call table: dialed (yes/no), connected (yes/no), outcome, next step. Every call, every time, even a no-answer.
5. **If they want a call/demo:** schedule it, note the date in the tracker, tell Wilson.
6. **If not interested:** mark it, move to the next company. Don't argue, don't oversell.
7. **Repeat for the rest of Batch 1.**

### When Batch 1 is done (all 5 dialed and logged)

Apply the decision rule already written in BlackSwanLabz-Funnel: **≥1 demo booked → next batch expands to 10 dials. 0 demos → stop dialing, tell Wilson to rework the opener/angle before continuing.** Don't keep dialing into a script that isn't working.

### What this is NOT yet

Not a queue system. Not a dashboard. Not auto-research, auto-classification, or auto-monitoring — those are the target state described in §2–25 above, and they get built once there's real call volume and at least one paying client to justify them. Right now, "the system" is a spreadsheet and a person on the phone. That's correct for this stage, not a shortfall.

### Where to send referrals or new leads

If someone offers a referral (an accountant, insurance agent, or banker who knows a business owner — see BlackSwanLabz-Position-Dossier-2026-09-14 §Missing Pieces), add them to the Deal-Pipeline the same way as any researched prospect, then follow the same loop above.
