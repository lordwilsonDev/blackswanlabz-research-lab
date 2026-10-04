---
source: FreeBuff (Buffy) run record from the PZS notebook, 06_ARCHITECTURE/v5-0-production-series-record.md; body copied unchanged except that links to other notebook files are written as plain references
captured: 2026-10-03
status: pending
---

# v5.0 Production Series PTS-2026-10-03-001 — Record

Date: 2026-10-03
Status: in-progress

Protocol: *Full-Stack Production Test Series, Production Testing Blueprint
v5.0*. Runner: `state/repair/series-runner.mjs`. Raw output:
`state/repair/SERIES_v5_0.txt`.

> **`PRODUCTION_TESTING_PARTIAL`. Capability ceiling `NOT_CERTIFIED`.**
> **11 of 40 tests executed. No repair was performed on any component under test.**
> Improvement claim: **`NO_TREATMENT_EFFECT_MEASURED`** (§47) — which is *not*
> `NO_EFFECT`.

## §48 summary

| | |
|---|---:|
| tests executed | 11 |
| passed | 8 |
| failed | 3 |
| not run | 26 |
| verifier gaps | 0 |
| measurement limits | 3 |
| interface defects | 1 |

## Results

| Test | Result | Instrument | Note |
|---|---|---|---|
| PT-003 runner execution truth | `RUNNER_EXECUTION_UNPROVABLE` | VERIFIED | see below |
| PT-006 exit propagation | `FAIL` (test defect) | VERIFIED | my PIPESTATUS probe was malformed |
| PT-007 downstream consumer | **`INTERFACE_STATE_COLLAPSE`** | VERIFIED | exit-code consumer → `PASS` on a `BLOCKED` system |
| PT-008 parser production test | `PARSER_CORRECT` | VERIFIED | 12/12, real git, rename NUL field handled |
| PT-010 hash stability | `HASH_STABLE` ×4 | VERIFIED | after restoring a file my own PT-011 deleted |
| PT-011 reconstruction | `NOT_TESTED` | VERIFIED | my test deleted an artifact and never restored it |
| PT-012 timestamp determinism | **`NONDETERMINISTIC`** | VERIFIED | exactly 1 differing line |
| PT-017 predicate repeatability | `PASS` | PARTIAL | counts + snapshot hash stable across runs |
| PT-018 predicate/prose drift | **`PREDICATE_DRIFT`** | PARTIAL | CHANGELOG says 20%, generated says 20.5% |
| PT-033 unknown propagation | `PASS` | VERIFIED | 4 unknowns injected, 0 collapsed |
| PT-019 META completeness | `PASS` | VERIFIED | all four META items present |

## The three findings that matter

### PT-012 — one line of non-determinism, exactly located

Two runs of `baseline.mjs` differ on **a single line**:

```
L1  "PT-2026-10-03-001  T0 BASELINE  2026-10-03T22:14:12.928Z"
    "PT-2026-10-03-001  T0 BASELINE  2026-10-03T22:14:16.745Z"
```

That is the whole cost of `generated_at`. Everything else is byte-identical —
including every measurement. Useful and precise: the derived artefacts are
deterministic *except* for the stamp, so a reconstruction test must mask that one
field or it will report failure forever.

### PT-018 — the drift is mine

The generated value is **20.5%**. `00_SYSTEM/CHANGELOG.md` says **20%** — my own
prose from earlier tonight, written before §72/§37 forbade it. The drift detector
found it by comparing generated against narrative, which is exactly its job.

The 20.0% was never *wrong* — 9/44 is 4.5% × 2 for staleness only by
coincidence of rounding. It was an under-precision that let a hand-written
number drift from its source. **Not corrected here**: §18/§50 forbid mid-series
repair, and the drift record *is* the finding.

### PT-003 — the instrument refused to conclude

The process-level probe is `NODE_DEBUG=child_process`, which makes Node log
every `spawn()`. Standalone, it works:

```
$ NODE_DEBUG=child_process node -e "execFileSync('echo',['x'])"
CHILD_PROCESS 8658: spawnSync ...
$ NODE_DEBUG=child_process node state/repair/gate-mutation.mjs 2>&1 >/dev/null | grep spawn
(nothing)
```

So the answer to "does the harness execute the runner?" is **`RUNNER_NOT_EXECUTED`**,
established outside the series.

**Inside** the series runner, the same probe returned **zero events for the
positive control as well** — the control script spawns nothing under those stdio
settings. With its own control failing, the instrument correctly refused to
conclude and returned **`RUNNER_EXECUTION_UNPROVABLE`**.

That is the v5.0 system behaving correctly. §10 permits three answers, and
`UNPROVABLE` is one of them. The instrument degraded rather than guessing.

## The defect I caused, and the one that caught it

**PT-011 deleted `state/repair/REPAIR_GATE_v4_0.txt` and never restored it.**

The reconstruction test is *supposed* to remove a derived artefact and rebuild
it. My implementation did `rmSync(target)`, then ran `repair-gate.mjs` with
`execFileSync(..., {encoding:'utf8'})` — which captures stdout into a **string**.
The rebuild never reached disk. The first series run died at PT-012 with a path
error, leaving the file deleted and the backup removed.

**PT-010 caught it on the next run** by reporting `REPAIR_GATE_v4_0.txt=MISSING`.
That is the hash-stability instrument detecting a destructive regression in its
own predecessor one run earlier — no one told it to look.

Restored from commit `5374c89`; hash `67089e68…` matches the value recorded
before the deletion.

Two lessons, both §49 classifications:

- The PT-011 implementation is a **`TEST_DEFECT`**. It is recorded, not repaired.
- The first series run also had a second `TEST_DEFECT` (PT-012 passed a
  vault-relative path with a subdirectory `cwd`).

Neither became a system defect, because neither was a system defect.

## §51 capability ceiling

| Instrument | Status |
|---|---|
| SEARCH | `VERIFIED` |
| PARSER | `VERIFIED` |
| **GATE_RUNNER** | **`UNKNOWN`** — the runner is still never executed |
| **RESULT_INTERFACE** | **`FAILED`** — `INTERFACE_STATE_COLLAPSE` confirmed |
| RECONSTRUCTION | `NOT_TESTED` |
| **Overall** | **`NOT_CERTIFIED`** |

The ceiling is the weakest critical instrument, not an average. Two of five are
not acceptable, so the total is not acceptable regardless of the rest.

## §51 tally, honestly

Of the seven instruments v4.2 §51 named:

| Instrument | Status |
|---|---|
| SEARCH | tested — `VERIFIED` |
| PARSER | tested — `VERIFIED` |
| **GATES** | **still untested. Still never executed.** |
| METRICS | repeatability tested; accuracy still `UNCALIBRATED`, no reference set |
| BASELINES | Vault `VALID`, Validators `UNPROVABLE` |
| **RESULTS** | **still failing — interface collapse confirmed again** |
| AUTHORIZATION | not exercised this series |

Two of seven tested, both green. The two that were reported as problems last
cycle are the two that remain unfixed, and one of them now has a *fresh*
process-level proof against it.

## §59

The series ends. It did not authorise PT-002, and it produced no causal claim.
The governing sequence was honoured: **run, observe, classify, trace, compare,
report** — no repair-and-rerun, and no result treated as progress.

## Related

- [v4.2 verification-of-verification record](v4-2-verification-of-verification-record.md)
- [v4.1 instrumentation record](v4-1-instrumentation-integrity-record.md)
- Series runner (FreeBuff notebook file `../state/repair/series-runner.mjs`) ·
  Raw series output (FreeBuff notebook file `../state/repair/SERIES_v5_0.txt`)