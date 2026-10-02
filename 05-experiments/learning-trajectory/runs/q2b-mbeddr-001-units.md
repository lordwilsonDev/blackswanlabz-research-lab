# Q2B-MBEDDR-001 — Physical-Units Capability Tranche

## Starting question

Build a small extensible C-like language capability that expresses typed physical quantities, computes dimensions through arithmetic, rejects dimensionally invalid operations, and generates runtime code without unit metadata.

## Source-derived requirements

mbeddr documentation describes physical units as annotations on types/literals, SI base and derived units, unit-aware type checking, dimensional computation for multiplication/division, rejection of incompatible addition, and erasure of unit metadata from generated runtime code.

## First artifact

A custom-parser Python prototype was constructed from the capability question rather than copied from mbeddr.

Mechanisms:
- dimensional-vector unit representation,
- scaled units,
- derived-unit expressions,
- typed values,
- compatibility checking,
- dimensional arithmetic,
- generated C-like runtime statements.

## Hidden semantic validation

8 cases:
1. same-unit addition
2. derived-unit division
3. derived-unit multiplication
4. incompatible-unit addition rejection
5. minute/second scale normalization
6. unitless arithmetic
7. dimension mismatch rejection
8. nested derived expression

Result: 8/8 PASS.

## Artifact verification

Generated C was compiled with gcc -std=c11 -Wall -Wextra -Werror.

Compiler result: exit 0.
Runtime result: 10.

Result: COMPILE + RUNTIME PASS.

## Capability state

L1/L2/L3-style evidence: demonstrated in this bounded slice.
L4 transfer: not yet run for this tranche.
L5: not claimed; no independent reconstruction yet.
Retention: pending.
Cross-model reconstruction: pending.
TCR: intentionally not calculated because the 10 person-year mbeddr reference covers the whole project, not this isolated feature.

## Next tranche

Expand from one feature to an actual language-extension workflow with a fresh extension, static checking, test construction, and independent reconstruction.
