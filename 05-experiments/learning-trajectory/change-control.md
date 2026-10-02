---
source: BlackSwanLabz Research Lab protocol (authored in this repo)
captured: 2026-10-02
status: pending
---

# Benchmark Change Control

## Principle

The benchmark is designed to evolve. Evolution must be observable.

No measurement-relevant definition is silently overwritten after it has been used in a registered run.

## Versioning

Use research-instrument semantic versioning.

PATCH changes wording or format without changing measurement meaning.

MINOR adds metrics, optional arms, or evidence channels without changing the construct.

MAJOR changes a construct definition, level boundary, primary metric, or experimental comparison.

## Required change record

Every measurement-relevant change records version, date, author, old definition, new definition, reason, evidence prompting the change, affected runs, and comparability of prior results.

## Frozen runs

A registered or preregistered run references the exact benchmark version and commit SHA.

Later changes do not retroactively alter its interpretation.

## Amendments

A preregistered experiment may be amended only with a dated amendment, reason, exact changed fields, effect on analysis, and preservation of the original plan.

## Retractions

Incorrect claims are retained as historical records and marked RETRACTED rather than deleted.

## Adjustment loop

run → observe failure → record issue → propose change → adversarial review → version → rerun

The benchmark itself is therefore auditable.
