---
source: owner-supplied package (The_BAD_IDEA1.zip, uploaded 2026-10-05); body unchanged, front matter added
captured: 2026-10-05
status: pending
---

# Intent–Reality Fidelity: Domain-Crossing & Domain-Depth Benchmark

This package measures how many domains the research program substantively entered, how deeply it progressed in each domain, and how quickly those transitions occurred.

## Files

- `DOMAIN_BENCHMARK.md` — benchmark specification and Level 1–10 rubric.
- `domain_ledger.yaml` — candidate domain registry. It intentionally starts with `max_level: 0` so the benchmark cannot pre-credit the work.
- `example_ledger.json` — small example of a scored ledger.
- `benchmark.py` — standard-library-only validator/scorer.
- `test_benchmark.py` — self-tests for anti-inflation rules and metric math.

## Run self-tests

```bash
python3 test_benchmark.py
```

## Score a ledger

The scorer accepts JSON because the local Mac Mini can validate it without adding YAML dependencies:

```bash
python3 benchmark.py example_ledger.json --start 2026-07-14 --cutoff 2026-10-03
```

## Intended production workflow

1. Audit the full research corpus.
2. Normalize candidate domains.
3. Freeze evidence IDs.
4. Assign the highest defensible level for each domain.
5. Run the validator.
6. Calculate breadth/depth/velocity.
7. Generate scientific and layperson summaries from the same ledger.
8. Run the human-comprehension test on the lay summary.

## Important

The candidate list in `domain_ledger.yaml` is not the benchmark result. It is a starting inventory that must be evidence-scored.

The benchmark measures **documented depth of engagement and evidence production**, not professional credentialing or universal expertise.
