---
source: authored in this lab (first committed 52de004)
captured: 2026-10-02
status: active
---

# Q2B-MBEDDR-001 — Flagship Project Selection

## Selection

Project: mbeddr
Repository: https://github.com/mbeddr/mbeddr.core
Pinned repository commit: d67b690593ddf98804faaf139d93a88e850edaad

## Why selected

The published mbeddr case study reports that approximately 10 person-years were spent on mbeddr itself, excluding the platform, after allocating 8.8 person-years by LOC and accounting for rework. The same study describes mbeddr as an extensible C language environment with approximately 88,000 LOC of implementation and 45,000 LOC of implementation/test code in the reported accounting.

The public repository exposes 3,317 tracked files at the pinned commit, including 690 paths matched by the preflight test/verification path filter used in this selection audit. This is a repository-path measure, not a test-function count.

## Public capability surface

mbeddr documentation describes:
- extensible C,
- physical units,
- state machines,
- components/interfaces,
- unit testing,
- requirements/tracing,
- product-line variability,
- model checking/formal verification,
- code generation and debugging.

## First capability tranche

Target physical-units type-system capability:
- SI and derived units,
- unit annotations on numeric quantities,
- dimensional arithmetic,
- rejection of incompatible addition,
- compatible scaled-unit normalization,
- runtime code generation without unit metadata.

## Reference-effort boundary

The 10 person-year figure is reported effort for mbeddr itself. It is not the effort of the physical-units feature alone.

Therefore no trajectory-compression ratio is reported for this tranche.

## Status

FLAGSHIP SELECTED
FIRST TRANCHE EXECUTED
FULL-PROJECT TCR: NOT YET VALID
