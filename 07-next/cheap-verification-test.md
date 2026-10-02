---
source: proposal written in this repo during research session 2026-10-02
captured: 2026-10-02
status: pending
---

# CVT-1: does cheap verification beat expensive generation? (proposal)

**Not run.** The runnable version is in [05-experiments/cvt-1](../05-experiments/cvt-1/README.md). This is a proposed experiment. No result exists, and nothing here is evidence.

## Why this test

The thesis says generation is getting cheap and verification is scarce. The lab's own constraint is budget: no large GPU spend. That points to one question the lab is placed to answer, and the existing evidence only half-answers it:

- A small local model passed 8 of 9 delegated functions (C-028, pending) but failed a real, well-specified job under the harness in 3 of 3 attempts (C-029, pending).
- In FDE Kernel M008 the kernel arm cut claim violations (1 against 7 and 18) but got the right root cause less often than the rules-only arm (C-042, C-043, pending). Verifying the process did not make the answer correct.

Both point at the same design rule: verify the **outcome** with an executable check, not the model's reasoning.

## Question

On tasks whose answers can be checked by running code, does a small local model inside a retry-until-the-oracle-passes loop reach the pass rate of a large cloud model's single attempt at equal or lower cost?

## Arms

| Arm | Description |
|---|---|
| A | Large cloud model, one attempt |
| B | Small local model, one attempt |
| C | Small local model, retry loop with the oracle's failure output fed back, capped at a token budget |
| D | Large cloud model with the same oracle loop (ceiling) |

Arm C is the hypothesis. Arms A and D bound it from above.

## Tasks

Reuse tasks that already have executable oracles: the Q2B-LTB pilot tasks and the mbeddr tasks under [learning-trajectory](../05-experiments/learning-trajectory/README.md). Add no task that lacks an automatic pass/fail check. Hold out a set the author has not seen.

## Metrics

- **Primary:** passes per dollar, with local cost estimated from measured wall-clock time and device power draw.
- Secondary: pass rate, tokens used, attempts to pass, and false passes (oracle passed, hand review failed).

## Falsification, to be fixed before any run

Register the margin and the sample size first. The hypothesis fails if arm C's passes per dollar do not exceed arm A's by the registered margin on the held-out set. A tie counts as a failure. Report arm D regardless, so the effect of the loop is separated from the effect of the model.

## Known risks

- A weak oracle makes arm C look better by passing wrong code; the false-pass metric exists to catch this.
- Small samples, as in M008 (3 to 8 runs per arm), support a direction, not a claim.
- Local cost depends on hardware; publish the hardware and the power measurement method.

## Status of claims

None. This page adds no row to [CLAIMS.md](../CLAIMS.md) until a pre-registration is committed and a run exists.
