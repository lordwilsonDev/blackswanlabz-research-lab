---
source: FreeBuff (Buffy) run record from the PZS notebook, 06_ARCHITECTURE/v7-0-question-engineering-application.md; body copied unchanged except that links to other notebook files are written as plain references
captured: 2026-10-03
status: pending
---

# v7.0 Question Engineering — First Application, Applied to Itself

Date: 2026-10-03
Status: in-progress

Protocol: *Adversarial Question Engineering & Governed Inquiry, Question
Engineering Blueprint v7.0*. Question set:
`state/questions/QE-2026-10-03-question-set.md` (FreeBuff notebook file `../state/questions/QE-2026-10-03-question-set.md`).

> v7.0 is the **methodology layer** every earlier blueprint assumed and none
> applied. Its §1 mission — *"what question would most efficiently reveal whether
> our current understanding is wrong?"* — has an obvious first use: run it on the
> eight-document blueprint series itself.

## What the series actually produced

| Blueprint | Terminal state |
|---|---|
| v1.2 | a question list |
| v2 / v2.0 | reconciliation + build order |
| v3.0 | `HOLD` at the §8 boundary |
| v4.0 | `BLOCKED` 7/14 |
| v4.1 | `BLOCKED`, `NOT_CERTIFIED` |
| v4.2 | `BLOCKED` 9/14, two self-corrections |
| v5.0 | `PRODUCTION_TESTING_PARTIAL` 11/40 |
| **v7.0** | four governed questions, one answered |

**Every terminal state is a non-state** — `BLOCKED`, `PARTIAL`, `UNCALIBRATED`,
`UNKNOWN`. Across eight documents: **no memory promoted, no policy changed, no
transition authorized, zero.** A system whose only outputs are non-states is not
yet a control system.

What *was* real: six instruments with controls, 12 real-git parser cases, two
standing lessons, ~11 defects found — **four of them in my own verification
machinery** — and one file deleted by a test that then caught its predecessor.

## Q-001 — answered, and it changes the critical path

The question nobody had asked across eight documents: **is the v2.0 artifact
actually the bottleneck, or just *a* bottleneck?**

```text
v2.0-dependent gates (1-3):  0 / 3
remaining gates (4-14):       6 / 11
```

**The artifact clears 3 of 14 gates.** Even with it in hand, five still block:
T0 (no validator commits), the mutation matrix, META-003, and the provenance
ledger — plus gate 5, which resolves as the tree settles.

Four are engineering. **One is a decision only Wilson can make.**

Treating one blocker as *the* blocker without measuring the others is
`WRONG_QUESTION` (v7.0 §61) — and that is the classification the prior eight
documents earn.

## Q-002 — the threat class has zero observed incidence

§19 forces observed/reasoned separation. Every defect recorded tonight, by class:

| Class | Count |
|---|---:|
| Parser / measurement | 6 |
| Interface / propagation | 2 |
| Verifier coverage | 2 |
| Destructive test bug | 1 |
| Predicate drift | 1 |
| **Authority / semantic / staleness / memory-poisoning** | **0** |

Not one observed defect was an authority leak, a semantic collapse, or a
stale-memory-consumed-as-current. Every single one was in the class §§113–§119
target — which was *already instrumented* before tonight.

The competing explanation (v7.0 §44) is that the governance class is
**unobservable** rather than absent. The discriminating test is cheap: find one
place a model output was consumed as authority. Three candidates exist and each
was corrected by a later document in this same series — **the documents are the
control, and they are working.** That is the honest reading, and it is a weaker
claim than "governance is necessary here."

## §18 paranoid rubric, applied to the series

> *If I assumed this system was misleading me while appearing correct, how could
> it do so?*

**It could have looked like progress while changing nothing.** Eight documents
of escalating formality, each referencing the last, all terminating in a
non-state, none converging on the one required input. And it would have read as
rigorous throughout, because every document was internally consistent and
honestly reported.

The three genuine outputs — the porcelain suite, the two lessons, the four
self-found defects — are all **verification** work, and all would survive
without the governance blueprint series.

## Q-004 — one action dominates

| Action | Cost | Unblocks |
|---|---|---:|
| **Save v2.0 to a file** | ~1 min | gates 1, 2, 3 |
| Rule META-003 | 1 sentence | gate 12 |
| Run the §25 mutation matrix | ~20 min | gate 11 |
| Version-control `~/.agents` | ~5 min | gate 4 |
| Build the provenance ledger | ~30 min | gate 14 |
| **Author blueprint v7.1** | hours | **nothing** |

v7.0 §45: the first wins on every dimension including cost. The last is the
highest cost with the lowest demonstrated return. **v7.1 would be
architecture-theatre's seventh consecutive appearance** — v1.2 §60 asks *"what
would make us remove the component?"* and the answer for the series is: a single
recorded instance where a governance control prevented a failure.

## Q-005 — `CLOSED_BY_INDEPENDENCE_LIMIT`

> *Is the series the smallest mechanism that closes the observed gap, or a
> response to a gap whose incidence is zero?*

**I cannot falsify this myself.** Establishing it requires an instance where a
governance control prevented a failure a non-governed system would have shipped
— which needs a counterfactual that did not happen. That is
`CLOSED_BY_INDEPENDENCE_LIMIT` (v7.0 §68), `HUMAN_DECISION_REQUIRED` (§69). It
is a real limit, not an evasion.

## §72

```text
This record is NOT the answer. Not evidence. Not a decision.
It authorizes nothing. Q-001..004 are PROPOSED and carry no authority.
Q-005 is HUMAN_DECISION_REQUIRED.
```

## Related

- Question set (FreeBuff notebook file `../state/questions/QE-2026-10-03-question-set.md`)
- [v5.0 production series record](v5-0-production-series-record.md)
- Reconciliation and inversion (FreeBuff notebook file `../05_DECISIONS/epistemic-blueprint-reconciliation-and-inversion.md`)