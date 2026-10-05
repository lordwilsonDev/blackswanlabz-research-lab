---
source: pre-registration of an integrated assessment, written by the assistant at the owner's direction, 2026-10-05
captured: 2026-10-05
status: pending
---

# Integrated assessment IA-1 (pre-registered before three of its four parts have results)

**Registered 2026-10-05, before the domain ledger is reconciled, before clean-room stage C is rerun and before the AIL+MoIE baseline phase has run. Part 3 already has a result (2026-10-03) and is disclosed as such.**

The owner asked for the four existing tests to be done, combined, and the combination turned into one more test. This page fixes how, so the combination cannot be shaped by the results.

## The four parts

| # | Part | Question | Instrument | Pass rule (fixed here) |
|---|---|---|---|---|
| 1 | Domain breadth and depth (result: INCONCLUSIVE, 4 of 15 agree; [details](../05-experiments/domain-benchmark/runs/2026-10-05/RESULT.md)) | How many domains does the repo's evidence support, how deep? | [domain benchmark](../05-experiments/domain-benchmark/DOMAIN_BENCHMARK.md), two blind scorers (Sonnet, Haiku), reconciled by the assistant | Validator passes on the reconciled ledger **and** the two scorers agree within one level on at least 12 of 15 domains. Otherwise the part is INCONCLUSIVE (the instrument is not reliable enough to quote). |
| 2 | Rebuild (result: PASS on C1 to C4, operator-assisted; [details](clean-room-agent-test-2026-10-03.md)) | Does a fresh agent reconstruct FCVE from the repo, using its skill and harness? | [clean-room test](clean-room-agent-test-2026-10-03.md), stage C rerun, with a wider but explicit tool allowlist | C1 to C4 as registered there. The allowlist is a test-setup limit, recorded as such. |
| 3 | Operator pipeline | With an operator, do forge, lock, self-check, run, analyze and report fit together? | [operator smoke test](operator-smoke-test-2026-10-03.md) | Already run: every stage completed and each guard fired. The result says nothing about any method. Registered after the fact. |
| 4 | Method comparison (result: SUPPORTED with caveats; [details](../05-experiments/ail-moie-h1c-002/README.md)) | Does AIL+MoIE produce more novel hypotheses than compute-matched baselines, blind-judged? | `ail-moie-h1c-002`, its registered decision | Its own registered rule. Baseline sample counts are capped; the cap is declared as an outcome-independent deviation before the baseline phase runs (see its README). |

## Combination rule

No weighted score and no single "rating" number. The report is a table of four statuses (PASS, FAIL, INCONCLUSIVE, NOT RUN) with one line each. The overall label follows the weakest part:

- **Established on these tests**: all four parts have a result and none is FAIL or INCONCLUSIVE.
- **Partial (n of 4)**: otherwise, naming which parts are missing or failed.

A FAIL is reported as prominently as a PASS. Parts 1 and 3 test the instrument and the process; only parts 2 and 4 test a thing, and the page says so.

## The fifth test: consistency between parts

Using only the four results, check whether the depth claims in Part 1 are corroborated by Parts 2 to 4 where they overlap:

- For every domain Part 1 scores at L7 or higher, is there an execution record from Parts 2 to 4, or another recorded run, that supports the executed-validation claim? Domains whose L7+ rests only on a file nobody ran in this assessment are listed as not corroborated here.
- Report the corroborated and not-corroborated counts. No pass threshold: it is descriptive, and it feeds the next version of the ledger.

## Limits, fixed in advance

- The scorers and the assistant are all Claude models; they are not independent of each other in the way two people are. Agreement between them is a reliability check on the rubric, not an independent validation of the levels.
- The evidence is limited to this repo and the lab's repos cloned for this session. Domains evidenced elsewhere will score low here.
- The date window for velocity is not fixed by the benchmark package (its README says 2026-07-14 to 2026-10-03; the repo's first commit is 2025-12-18). Velocity is not reported until the owner fixes it.
- Nothing here is peer review, external validation or independent confirmation.

## Results (2026-10-05)

| # | Part | Status | One line |
|---|---|---|---|
| 1 | Domain breadth and depth | **INCONCLUSIVE** | Two blind scorers agreed on 4 of 15 domains (needed 12); depth ranges from 39 (lower of two) to 70 (Sonnet) points. |
| 2 | Rebuild | **PASS, operator-assisted** | C1 to C4 met; the operator ran the long install because the agent ended its session twice. |
| 3 | Operator pipeline | **PASS (plumbing only)** | Every stage completed and every guard fired; the tasks were too easy to separate the arms. |
| 4 | Method comparison | **SUPPORTED (registered rule), with caveats** | C4 beats all three compute-matched baselines on novelty (g 0.79, 1.74, 1.07; Holm p 0.0117, 0.0007, 0.0024), but the sample cap favours C4, C4's answers are longer, the judges are Claude models, and C4 is not coherence non-inferior to C3-bon. |

**Overall label under the weakest-part rule: Partial (3 of 4 parts have a usable result; part 1 is inconclusive).** It is not "Established on these tests". Part 4's SUPPORTED does not establish its claim; the experiment's own registration requires replication with judges from another family or human raters.

Only parts 2 and 4 test a thing. Parts 1 and 3 test the instrument and the process.

## The fifth test: consistency between parts

Scorer A's L7-and-above domains (the generous ledger), checked against recorded runs from this assessment or from verified `CLAIMS.md` rows:

| Domain (A's level) | Corroborated by a recorded run? |
|---|---|
| formal_mathematics_verification (9) | Yes: C-060 audit, and Part 2 ran the FCVE doctor and smoke test. The smoke test checks the machinery, not a theorem. |
| ai_agent_systems (9) | Yes: C-052 and C-057 re-runs of MSB v3 at the pinned commit. |
| cybersecurity_security_engineering (9) | Yes, by the same MSB v3 re-runs as above. One run is counted for two domains (the double counting the adjudication draft addresses). |
| aerospace_orbital_mechanics (7) | Yes: C-005 byte-for-byte reproduction. |
| software_engineering (8) | No: the L8 rests on a mutation report in another repo that was not re-run here. |
| antitrust_industrial_organization (7) | No: read, not run (Rule F). |

Four of six are corroborated, and two of those four share one run. The two not corroborated are the ones to treat as weakest. The ones above L6 that Scorer B also gave (aerospace, formal verification at L7) are corroborated. This is descriptive: it feeds the next version of the ledger, not a score.

## Limits that apply to the whole assessment

The scorers, generator and judges are Claude models, so agreement is not independent confirmation. Evidence was limited to this repo and the clones available to the session, so domains evidenced elsewhere score low. The date window for velocity is not fixed, so velocity is not reported. Nothing here is peer review.
