---
source: provenance of the domain-benchmark package, recorded by the assistant
captured: 2026-10-05
status: pending
---

# Provenance and what was checked

Supplied by the owner as `The_BAD_IDEA1.zip` on 2026-10-05 (the owner's account of the original: `intent_reality_domain_benchmark.zip`, saved 2026-10-03). Contents: the specification (Level 1-10 ladder, anti-inflation rules A-J, metrics), a 15-domain candidate registry, an example ledger, a standard-library validator and six self-tests.

SHA-256 of the files as received: `DOMAIN_BENCHMARK.md` aeabc5fb..., `README.md` 485403e1..., `benchmark.py` 4d560d1d..., `domain_ledger.yaml` 13c134a9..., `example_ledger.json` 1fbdeb4e..., `test_benchmark.py` 817ad45d.... The two `.md` files here have a front-matter header added; their bodies are unchanged.

## Checked by the assistant on 2026-10-05

- `python3 test_benchmark.py`: 6 of 6 tests pass (clean domain, no skipped levels, missing evidence, L10 public-record guard, rejected domain excluded, metric math).

## Not established

- The registry is a draft: status DRAFT, 15 candidate domains, every `max_level` 0, no dates. It is not a result.
- No scored ledger is in this package. A reported "104 of 150 points, mean 6.9, DDE 10.4" is arithmetically consistent with 15 domains (104/15 = 6.93, 104/10 = 10.4), and many score distributions give it. It is not reproduced from evidence and is not quoted as a result.
- The example ledger's domains are invented examples. Its numbers are not results.
- Levels are meant to be derived from evidence. Scoring them needs a reviewer other than the author for the claimed levels, since Level 9 itself says a second assertion by the same author is not enough.
