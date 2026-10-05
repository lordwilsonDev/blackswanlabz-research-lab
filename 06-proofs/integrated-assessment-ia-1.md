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
| 2 | Rebuild | Does a fresh agent reconstruct FCVE from the repo, using its skill and harness? | [clean-room test](clean-room-agent-test-2026-10-03.md), stage C rerun, with a wider but explicit tool allowlist | C1 to C4 as registered there. The allowlist is a test-setup limit, recorded as such. |
| 3 | Operator pipeline | With an operator, do forge, lock, self-check, run, analyze and report fit together? | [operator smoke test](operator-smoke-test-2026-10-03.md) | Already run: every stage completed and each guard fired. The result says nothing about any method. Registered after the fact. |
| 4 | Method comparison | Does AIL+MoIE produce more novel hypotheses than compute-matched baselines, blind-judged? | `ail-moie-h1c-002`, its registered decision | Its own registered rule. Baseline sample counts are capped; the cap is declared as an outcome-independent deviation before the baseline phase runs (see its README). |

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

## Results

Not yet run.
