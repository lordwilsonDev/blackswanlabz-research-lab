---
source: two blind scorers (Sonnet, Haiku) scoring the 15 candidate domains, run by the assistant, 2026-10-05
captured: 2026-10-05
status: pending
---

# Domain benchmark, part 1 of IA-1: result

**Registered decision ([IA-1](../../../../06-proofs/integrated-assessment-ia-1.md)): INCONCLUSIVE.** The rule required the two scorers to agree within one level on at least 12 of 15 domains. They agreed on **4 of 15**.

Evidence: this repo and the lab's repos cloned read-only for the session. Neither scorer ran code. The ledgers are [scorerA.json](scorerA.json) (Sonnet), [scorerB.json](scorerB.json) (Haiku), both validated by `benchmark.py`. "Lower of two" below is the lower level per domain, computed from them.

| Domain | A | B | Within 1 |
|---|---|---|---|
| ai_agent_systems | 9 | 6 | no |
| software_engineering | 8 | 6 | no |
| formal_mathematics_verification | 9 | 7 | no |
| aerospace_orbital_mechanics | 7 | 7 | yes |
| antitrust_industrial_organization | 7 | 0 | no |
| logistics_freight | 3 | 1 | no |
| voice_speech_systems | 3 | 0 | no |
| cybersecurity_security_engineering | 9 | 6 | no |
| ai_economics_infrastructure_economics | 6 | 4 | no |
| astronomy_exoplanet_analysis | 0 | 0 | yes |
| ecology | 1 | 2 | yes |
| epidemiology_network_science | 3 | 6 | no |
| linguistics | 0 | 1 | yes |
| communication_theory | 3 | 1 | no |
| cybernetics | 3 | 1 | no |

| Metric | Scorer A | Scorer B | Lower of two |
|---|---|---|---|
| L2+ domains | 12 | 8 | 7 |
| L7+ | 6 | 2 | 2 |
| L8+ | 4 | 0 | 0 |
| L9+ | 3 | 0 | 0 |
| L10 | 0 | 0 | 0 |
| Total depth points | 70 | 44 | 39 |
| Domain-depth equivalents | 7.00 | 4.40 | 3.90 |

Neither ledger reproduces the remembered "104 of 150, 10 domains at L7+, 5 at L8+, 1 at L9+". Scorer A's total is 70 with 6 at L7+, 4 at L8+ and 3 at L9+. Both agree on L10: zero domains, and on astronomy: no evidence in what they could see.

## Why they disagree (read from the two ledgers)

- A awards L8 and L9 to AI agents, formal verification and cybersecurity on the strength of this session's own re-runs of the author's pinned harnesses. B treats pending claim rows as not executed and stops at L6 or L7. Whether a re-run by the assistant counts as "reconstruction without hidden conversational state" is the open judgment, and it drives most of the gap.
- A gives antitrust L7 from a document it read, not ran. B gives 0. The ladder says execution requires an execution record (Rule F), so A's L7 for antitrust is the weakest score in either ledger.
- A and B overlap on D-001 and D-008 for A: the same MSB v3 re-run evidence is counted in two domains.

## What this means

The instrument is not reliable enough, as scored by two Claude models reading the same corpus, to quote a single depth number. The floor (lower of two) is a defensible lower bound; the ceiling (A) depends on contested level-9 and level-7 awards. The scorers are not independent of each other or of the assistant, so agreement would not have validated the levels either. A person scoring the same rubric would be the check.
