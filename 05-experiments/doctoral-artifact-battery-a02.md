---
source: Doctoral Artifact Battery records and the A02 ledger repository (local; repository not yet public)
captured: 2026-10-06
status: active
---

# Doctoral Artifact Battery, artifact A02: a tamper-evident run ledger

The battery asks how fast one builder, directing AI systems, can produce an advanced artifact that holds up when checked. The unit of measurement is the artifact and its evidence trail, not the builder and not any model. This page records the first artifact that was completed, what was built, what was checked and what was not.

## What was built

A zero-dependency Python library and command-line tool that records events, such as an AI agent's tool calls, in an append-only, hash-chained file with separately authenticated checkpoints. A standalone verifier tells an outsider whether the record has been altered. The requirements (R1 to R10), the adversarial test list and 45 acceptance tests were written and frozen before any implementation existed.

## How it was done

Three parties, one loop. Wilson set direction, froze each decision and caught drift. Claude wrote the specification and the tests first, then verified every build in a clean export, independently of the builder. FreeBuff built the implementation and the production file set and reported its own failures. Each cycle ended with a check by someone other than the author of the change.

## Results

All rows are recorded in the local project records and the repository, which is not yet public. They are therefore **pending** here until the repository can be re-run by a reader.

| Result | Claim |
|---|---|
| Closed with limits stated at tag `a02-final` (commit `6c7a301`), 10 h 09 m of a 120 h box, cost $0, battery level 3 (verification) on the author side; level 5 (independent) not claimed | [C-049](../CLAIMS.md), pending |
| 68 tests pass; the 45 frozen acceptance tests are byte-identical to the commit that predates the implementation; 14 of 15 source mutants are killed, the survivor being the skipped-fsync case | [C-050](../CLAIMS.md), pending |
| The verification pack hashes to the same sha256 on every rebuild; its leak gate caught 11 of 11 planted leaks | [C-051](../CLAIMS.md), pending |
| The operator pass matched 15 of 15 steps; it was directed by Wilson and executed by Claude, so it is delegated and not independent | [C-052](../CLAIMS.md), pending |

## What the failures showed

Twenty-two failures were logged, each with the assumption it rested on inverted, a test or control, and a status ([C-053](../CLAIMS.md), pending). Most were handoff failures, not code failures: measuring the wrong thing, an instruction read as "save" instead of "build", a stale hold, a clipboard that was overwritten, a prompt with no done-criterion, a claim of absence made after a partial search.

The result that repeats: a passing test run did not catch the weaknesses that mattered. The frozen suite passed with the chain-link check deleted; a pack leak gate passed three planted phrases; a mutation script reported success on a red baseline. Each was found by running a check against a deliberate fault. The practice that came out of it is to mutate the checker before trusting the checks, and it is now packaged as a skill, `failure-to-control`, with a handoff lint, a record lint, a repository progress report and a generic mutation runner.

## What this does not show

- No outside party has verified anything. A verification pack exists (a clean export of the artifact, the requirements, the rubric and a prompt that names no builder), and no outside responses have been collected.
- No cryptographic security, no expert review, no power-loss durability test, no hosted CI run.
- Nothing about the other artifacts. The battery ended after one completed artifact: A01 was stopped before any result existed (215 of about 450 model calls collected and never analysed), A03 and A07 were proposed and never started, and the remaining six were never begun ([C-054](../CLAIMS.md), pending).
- Nothing about the builder's ability. The records show a working pattern.

## To check it

When the repository is public: check out tag `a02-final`, run `python3 -m unittest discover -s tests`, `python3 scripts/mutation_check.py`, `./scripts/operator_run.sh` and `bash verification-pack/make_pack.sh`. Expected: all tests pass, 14 of 15 mutants killed, 15 of 15 operator steps matching, and the pack hash above.
