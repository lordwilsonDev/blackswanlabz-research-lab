# Business functions and SOPs

## Tier first, then functions

| Tier | Who | Formalize now | Leave informal |
|---|---|---|---|
| 0 | One person, or a side business | Sell, deliver, get paid, keep records, legal basics | Everything else |
| 1 | 2 to 15 people | Plus: simple roles, customer follow-up, recurring SOPs | Committees, heavy reporting |
| 2 | 15 to 150 | Plus: managers, hiring, finance routine, department OKRs, risk register | Enterprise governance |
| 3 | Mid-size | Plus: controls, change management, compliance, vendor management, internal audit | |
| 4 | Fortune 500 scale | Plus: portfolio governance, formal RACI, enterprise risk, regulatory reporting | |

Ask which tier the person is in. Do not hand a Tier 0 person Tier 3 structure.

## Functions: the question each answers and the first artifact

| Function | Question | First artifact |
|---|---|---|
| Strategy and leadership | Where are we going and why? | One-page intent and North Star |
| Product or service delivery | How do we make what we promise? | Delivery SOP |
| Marketing | How do people learn we exist? | Who it's for, one channel, one message |
| Sales | How does interest become a paying customer? | Simple pipeline list and follow-up rule |
| Customer success and support | How do we keep and help customers? | Complaint and follow-up log |
| Operations | How does work move without dropping? | Weekly operating checklist |
| Finance and accounting | Are we paid, solvent, and compliant? | Cash view and bookkeeping routine (professional for tax) |
| Legal, risk, compliance | What can hurt us, and who must review? | Contract template and risk list (professional review) |
| People | Who does the work, and are they sustained? | Role list and coverage plan |
| Technology and data | What systems hold our work, and are they safe? | Tool list, access rules, backups |
| Procurement and suppliers | What do we depend on others for? | Supplier list with fallback |
| Research and development | What do we need to learn before we commit? | Research question and evidence ledger |

For each function ask: do we need it in the next 90 days? If no, write "not yet" and a revisit date.

## Gates borrowed from the lab (use as a spine for any business)

Finding an opportunity is not proving it. Proving it is not delivering improvement. Before building: evidence, a baseline, a decision (do nothing, improve, or automate), human approval, then measure against the baseline. The lab's own docs state these as rules; whether they work in a live business is not shown in the repo (its operating manual says no clients were active as of 2026-09-15; re-check with `repo_state.py`).

## SOP template

```
Name / ID / version / status (DRAFT | TESTED | ACTIVE) / owner / review date
Purpose (one sentence)
Trigger (what starts it)
Inputs (what you need in hand)
Steps (numbered, one action each)
Decision points (if X then Y)
Outputs (what exists at the end)
Quality check (how you know it was done right)
Exceptions and escalation (when to stop and who to ask)
Metrics it affects
Records kept
```

Write an SOP only for work done repeatedly or work that is costly to get wrong. Status stays DRAFT until someone other than the author follows it and it works; then TESTED. ACTIVE needs an owner and a review date.

## Which lab documents map to what (read only what the person needs)

| Need | Repo document (`08-operations/` unless noted) |
|---|---|
| End-to-end service-business lifecycle | master-sop.md, complete-client-loop.md |
| Step-by-step runbook | operator-sop.md |
| Deciding do nothing / improve / automate | hardened-blueprint-v2.1.md |
| Researching a company | research-manual-v1.md |
| Intake of a new customer | fde-customer-intake-sop-v1.3.md |
| Daily rhythm | day-to-day-operating-manual.md (its banner says the automation is a target, not running; section 26 is the live part) |
| People coverage and quality | black-swan-labs-research-group.md (sections 27 to 30), plus Vault `People-Relief-and-Flexible-Coverage-System.md` (unverified, legal review needed) |
| Compiling a new domain into skill + SOP + harness | workforce-grant-os-v1.md and `skills/workforce-grant-readiness` (one worked domain) |

## Research-lab variant

Functions in the lab's design: research director, research operator, methods engineer, verification lead, systems engineer, domain specialist, people lead; one person can hold several. Core artifacts: claims ledger with a status per claim, experiment record with a stated falsifier, decision record, capability record. A claim is not verified because a model said it or because several models agree; it is verified by a check the author could not have faked. These are designs in the repo; check `repo_state.py` for what has actually been run.
