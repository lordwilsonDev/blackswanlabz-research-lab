# Workforce Grant Harness

## Purpose

Run the internal BlackSwanLabz workforce-grant preflight before writing or submitting an application.

## Command

```bash
python3 scripts/workforce_grant_harness.py scripts/fixtures/workforce_grant_case.example.json
```

## Input contract

The case JSON contains:

- `gates`: boolean mandatory eligibility/evidence gates
- `scores`: 0-to-category-maximum internal rubric scores
- `unknowns`: unresolved evidence
- `contradictions`: conflicting evidence

## Decision semantics

- **BLOCKED**: one or more mandatory gates fail, or evidence is contradictory.
- **NOT_READY**: gates pass but internal score is below 70.
- **GRANT_READY_PARTNER_REQUIRED**: score is at least 70 but unresolved evidence remains.
- **GRANT_READY**: all gates pass, score is at least 70, and no unresolved evidence remains.

The harness is deliberately conservative. It does not infer eligibility, employer demand, wages, placement, or match from macro evidence.
