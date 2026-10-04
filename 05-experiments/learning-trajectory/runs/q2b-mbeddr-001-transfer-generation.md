---
source: BlackSwanLabz Research Lab record - Q2B-MBEDDR-001 — Transfer and Generation Update
captured: 2026-10-02
status: pending
---

# Q2B-MBEDDR-001 — Transfer and Generation Update

## Trajectory

Initial physical-units tranche: 8/8 semantic validation.

Transfer perturbation:
- changed unit definitions to support scaled and compound derived units,
- mixed-scale addition,
- speed/time composition,
- incompatible-dimension rejection,
- nested derived expressions.

First pass: 4/6. Investigation showed both misses were oracle mistakes:
1. 36 km/h × 1 h = 36 km = 36,000 m, not 1,000 m.
2. (36 km/h × 1 h) / 1000 = 36 m, not unitless.

Corrected transfer suite: **6/6 PASS**.

## Generation extension

Added integer unit exponents and compound-unit support:
- m^2
- s^-1
- m/s^2
- kg*m/s^2
- dimensional rejection for incompatible addition
- runtime unit erasure

First pass: 6/7. The single miss was a verifier type mismatch: Fraction(196,5) was compared to Python float 196/5.

Corrected generation suite: **7/7 PASS**.

## Artifact verification

The generated C output was compiled with gcc -std=c11 -Wall -Wextra -Werror and executed successfully, returning 10 on the reference program.

## Important methodological finding

Across the mbeddr tranche, benchmark failures have included both learner/implementation failures and oracle failures. The protocol therefore requires an explicit **verifier audit** before assigning failure to the learner.

The correction trail is preserved. Oracle corrections do not count as learner repairs.

## Current state

Initial semantics: PASS 8/8
Transfer: PASS 6/6 after oracle correction
Generation extension: PASS 7/7 after oracle correction
Compilation/runtime: PASS
Retention: pending
Independent learner reconstruction: pending
Cross-model reconstruction: pending
Full-project trajectory compression: not yet valid
