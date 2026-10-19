# North Star, OKRs, KPIs

| Term | Plain meaning | Rule |
|---|---|---|
| North Star | The one number that best shows customers are getting the value you exist to give | One per stage. Change it only when the stage changes, and record why |
| OKR | Objective (a short, qualitative aim for a period, usually a quarter) plus 3 to 5 Key Results (measurable outcomes with a start value and a target) | Key Results are outcomes, not tasks. "Launch the website" is a task |
| KPI | An ongoing health measure with a normal range | Watched continuously; act only when out of range |

How they fit: North Star = direction. OKRs = what to change this period. KPIs = whether everything else stays healthy.

## Metric card (one per metric)

```
Name:
Definition (exact, in writing):
Why it matters:
Type: leading | lagging
Baseline: <value and date>  or  "measure first"
Target: <value and date>    or  "set after baseline"
Source of truth (where the number comes from):
Owner:
Cadence (how often it is read):
Paired guardrail (what must not get worse):
Decision it changes:
```

## Rules

- **Baseline before target.** No baseline, no target. Write "measure first" and schedule the measurement.
- **Pair every metric.** Speed with quality, volume with error rate, sales with refunds. A single metric gets gamed.
- **Outcomes over activity.** Calls made is activity; booked appointments is an outcome.
- **Fix the definition.** Changing how a number is counted is a new metric; record the change and the date.
- **Capacity released is not money.** Hours saved become value only when converted: overtime cut, a hire avoided, more paid work done, faster response that keeps customers. Say which.
- **Read from records the actor can't edit** (invoices, system logs), not from self-report.
- **Fewer is better.** Solo: 1 North Star, 1 OKR set, at most 5 KPIs. Small team: OKRs per function. Large organization: OKRs cascade from the top, KPIs live on dashboards with named owners, and a metric owner approves definition changes.

## Worked shape (placeholders on purpose; do not copy numbers)

Solo mobile pet groomer.
- North Star: repeat bookings per week.
- Objective (this quarter): build a reliable base of repeat customers.
  - KR1: rebook rate within 30 days, baseline [measure first] to [set after baseline].
  - KR2: average days from request to appointment, baseline [measure first] to [set after baseline].
  - KR3: share of customers with a recorded next appointment, baseline [measure first] to [set after baseline].
- KPIs: no-show rate (guardrail: don't overbook), review score, hours worked per week (guardrail: stay sustainable), cash collected versus invoiced.

## Research-lab variant

The BlackSwanLabz research-lab repo uses "verified knowledge or capability produced per unit research time" as a method metric, with verification yield, reproduction rate, transfer rate, failure-to-capability rate, quality-escape rate, and evidence completeness as supporting measures (`08-operations/black-swan-labs-research-group.md`, §41 to 45). The repo itself says these are method metrics, not laws, and that more output with falling verification yield is unhealthy. They are a design; the repo records no values for them.
