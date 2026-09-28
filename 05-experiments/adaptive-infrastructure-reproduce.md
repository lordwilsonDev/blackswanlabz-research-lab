---
source: https://github.com/lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE/blob/765979bda8b7fb5be123261578fdd4cf0d943c53/reproduce.py
repo: lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE
commit: 765979bda8b7fb5be123261578fdd4cf0d943c53
captured: 2026-09-28
status: active
---

# Adaptive Infrastructure — `reproduce.py` reproduction

## What it computes

`reproduce.py` is a single self-contained script (stdlib `math` + `numpy`) covering five unrelated toy calculations bundled as a preliminary artifact:

- **Orbit / SSO** — solves for the sun-synchronous inclination at 550 km altitude via J2 nodal-precession balance, then derives orbital period, eclipse fraction/duration, a Hohmann-style end-of-life deorbit delta-v, and a 10-degree plane-change delta-v.
- **Power** — a first-order orbital power budget (eclipse/sunlit energy, nominal array power, minimum battery capacity) plus an end-of-life array power and radiator sizing from a fixed heat-rejection load.
- **Thermal** — the radiator area needed to reject 150 W (125 W × 1.2 margin) via a black-body-style Stefan-Boltzmann radiator at 293 K, ε = 0.9.
- **Revisit simulation** — a simplified spherical (no-perturbation) propagation of a 3-plane, 2-satellite-per-plane Walker-like constellation over 8 days at 1-minute sampling, computing point coverage and the maximum revisit gap over a mid-latitude grid.
- **HHI** — a synthetic market-concentration (Herfindahl-Hirschman Index) calculation before/after a hypothetical consolidation, unrelated to the orbital mechanics above.

## Command and result

```bash
PY=/opt/homebrew/Caskroom/miniforge/base/bin/python
cd ~/projects/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE
$PY reproduce.py > out.txt
diff out.txt reproduce_results.txt && echo IDENTICAL
```

Re-run 2026-09-28 at commit `765979bda8b7fb5be123261578fdd4cf0d943c53`: **IDENTICAL** (byte-for-byte `diff`, zero output).

Python 3.12.9, numpy 2.2.6 (`$PY -c "import sys,numpy;print(sys.version.split()[0],numpy.__version__)"`).

Note: numpy on Apple Silicon can print spurious BLAS/matmul performance warnings to stderr on some builds; `reproduce.py`'s stdout (the file diffed above) is unaffected, and the simulation output contains zero NaN/Inf values (checked directly against `reproduce_results.txt`).

## Hand-checked values

Independent hand recomputation of the published numbers (SSO inclination 97.59° at 550 km, period 95.65 min, 10° plane-change delta-v 1,322 m/s, HHI 1864 → 3106) is recorded as [C-006](../CLAIMS.md). The outbreak figures in the same artifact (RR 7.39, OR 18.42) come from a separate run record, not `reproduce.py`; they recompute from its counts of 38/60 exposed ill versus 12/140 unexposed ill ([C-046](../CLAIMS.md)). This byte-identical reproduction is [C-005](../CLAIMS.md).
