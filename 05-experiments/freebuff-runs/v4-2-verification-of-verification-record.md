---
source: FreeBuff (Buffy) run record from the PZS notebook, 06_ARCHITECTURE/v4-2-verification-of-verification-record.md; body copied unchanged except that links to other notebook files are written as plain references
captured: 2026-10-03
status: pending
---

# v4.2 Verification of Verification — Record and Terminal State

Date: 2026-10-03
Status: in-progress

Protocol: *Recursive Instrument Verification & Rebaseline Control Blueprint
v4.2*. Built: `test-git-porcelain.mjs`.

> **§50 terminal state: `BLOCKED`.** Instrumentation ceiling `NOT_CERTIFIED`.
> `REBASELINE_READY` not reached; PT-2026-10-03-002 **not permitted**.

## The headline: v4.2 §12 and §14 correct two of my own v4.1 claims

Both corrections came from reading the protocol against what I actually ran, not
from re-reading my work. That is the discipline v4.2 exists to impose.

### §12 — I extrapolated a `VERIFIER_GAP` from a static scan

v4.1 reported *"6 hardcoded `pass: true`"* and treated all six as
`VERIFIER_GAP`. The evidence for that was a **regex scan of the runner's source
text**. Only **one** gate has execution evidence: gate 5 reported `PASS` while
printing an `UNCLASSIFIED` row — I watched that happen.

§12 is explicit:

> *Do not extrapolate this observation to the other gates without execution
> evidence.*

Correct classification:

| Gates | Status |
|---|---|
| **5** | `VERIFIER_GAP_OBSERVED` — executed evidence |
| 1–4, 6–14 | `UNKNOWN_UNTIL_MUTATION_TESTED` |

A static pattern match shows what the source *says*, not what the gate *does*.
The v4.1 phrasing claimed more than the run established.

### §14 — the mutation matrix never executed the runner

This is worse. `state/repair/gate-mutation.mjs` references `repair-gate.mjs`
exactly twice, both to `readFileSync` it as text for the §21 pattern scan:

```
grep -c 'repair-gate|execFile|spawn|execSync' gate-mutation.mjs  ->  1
line 23: const RUNNER = join(HERE, 'repair-gate.mjs')
line 24: const src = existsSync(RUNNER) ? readFileSync(RUNNER, 'utf8') : ''
```

**It never runs it.** The 14/14 matrix exercised the harness's *own
re-implementation* of each gate verdict. That is non-circular in the obvious way
— the logic is independently written — but it means:

- **14/14 says nothing about whether `repair-gate.mjs`'s gates can fail.**
- **`gate_mutation_harness: VERIFIED` was overstated.** It demonstrated its own
  reasoning, not the runner's behaviour. Downgraded to `PARTIAL`.

§14's failure modes — duplicate guard, upstream failure, shared fixture
contamination, cached result — are all about attributing a detection to a gate
that did not evaluate the mutation. Here the detected mutation never reached the
runner at all.

**Honest position: the runner's 14 gates remain entirely unvalidated by
execution.**

## §32 — the git porcelain regression suite (built, verified)

The v4.1 record flagged the porcelain parser as
`FAILED_THEN_FIXED_UNCALIBRATED`: three bugs fixed, no suite. v4.2 §32 names the
required cases, so they are now executable.

`state/repair/test-git-porcelain.mjs` builds **real temporary git repositories**
and drives the real `git status --porcelain -z` binary. Nothing is mocked.

```
ok C1_modified_leading_space          ok C7_multiple_records
ok C2_added_staged                    ok C8_empty_output
ok C3_untracked                       ok C9_path_with_spaces
ok C4_deleted                         ok C10_first_vs_later_status_not_confused
ok C5_renamed                         ok C10b_one_record_per_file
ok C6_copied                          ok C11_malformed_rejected

12/12 cases passed — VERIFIED      (direct exit 0)
```

### The suite found a second real defect in the technique I had certified

C5 failed on first run. `--porcelain -z` emits a rename as **two NUL-separated
fields** — new path, then the original path — so the parser I had just certified
as the fix produced:

```json
[{"status":"R ","path":"renamed.txt"},{"status":"??","path":"seed.txt"}]
```

The original path was being consumed as a phantom untracked record. The suite
existed for exactly this, caught it immediately, and the fix consumes the extra
field for `R`/`C` statuses.

**A repair certified by inspection had a defect the repair's own regression suite
found on its first run.** That is the argument for §31 in one line.

One further correction, to my own test rather than the parser: C10b initially
asserted no record may have status `??`, which is wrong — an untracked file
*should* be `??`. The assertion, not the code, was wrong. Fixed to check
one-record-per-file.

## §35 — artifact hash stability

| Artifact | Result |
|---|---|
| `REPAIR_GATE_v4_0.txt` | `HASH_STABLE` `67089e68…` |
| `GATE_MUTATION_v4_1.txt` | `HASH_STABLE` `83ec5a8f…` |
| `INSTRUMENTATION_CERT_v4_1.txt` | `HASH_STABLE` `221d0566…` |

Read → hash → read → hash → compare. No `ARTIFACT_INSTABILITY`.

## §36 — reconstruction

Not run this cycle. Recorded as `NOT_TESTED` rather than assumed. The derived
artefacts here embed a `generated_at` timestamp, so byte-exact reconstruction
requires normalising that field first — which is itself a defect in the artefact
design, since it makes derived state non-deterministic. Noted, not fixed (§45).

## §17 / §44 — result envelope

This record's own results carry the four-field separation:

```json
{ "execution_status": "COMPLETED_EXIT_0",
  "system_state": "BLOCKED",
  "measurement_status": "UNCALIBRATED",
  "certified": false }
```

Observed twice tonight, and worth repeating because it keeps happening: the
porcelain suite **failed on first run and still exited 0** when piped through
`tee`. Exit code from a pipeline is not the script's exit code. The suite's own
verdict said `FAILED`; only the direct run said `1`. v4.2 §17 is about exactly
this.

## §41/§42 — certification ceiling, corrected

| Instrument | v4.1 said | v4.2 correction |
|---|---|---|
| `search_detector` | `VERIFIED` | `VERIFIED` — controls pass |
| `git_porcelain_parser` | `FAILED_THEN_FIXED_UNCALIBRATED` | **`VERIFIED`** — 12/12 against real git |
| `gate_mutation_harness` | `VERIFIED` | **`PARTIAL`** — never executed the runner (§14) |
| `gate_runner` | `FAILED` | **`UNKNOWN_UNTIL_MUTATION_TESTED`** — 1 gate observed, 13 untested (§12) |
| `link_containment_test` | `VERIFIED` | `VERIFIED` |
| `metric_generators` | `UNCALIBRATED` | `UNCALIBRATED` |
| `authorization_controls` | `BLOCKED` | `BLOCKED` — self-granted, no approver |
| `interface_consumers` | `DEFECT_CONFIRMED` | `DEFECT_CONFIRMED` |

Two statuses moved *toward* green (parser verified) and two moved *away*
(harness overstated, runner over-claimed). Net effect on the ceiling: unchanged.
`NOT_CERTIFIED`.

## §48 — rebaseline gate

| Item | |
|---|:---:|
| search detector positive control | PASS |
| search detector negative control | PASS |
| search universe declared | PASS |
| v2.0 status correctly scoped | PASS |
| all 14 gate mutations executed | **FAIL** — the runner was never executed |
| no undetected critical gate mutation | **FAIL** — undeterminable, not zero |
| exit/state interface tested | **FAIL** — defect confirmed, not fixed |
| authorization evidence valid | **FAIL** — self-granted |
| complete META set represented | **FAIL** — META-001/003 unresolved |
| metric scope attached | PASS |
| parser mutation suite passed | PASS |
| provenance generator tested | **FAIL** — no generator exists |
| baseline dimensions classified | PASS |
| critical instrumentation certified | **FAIL** |

**9/14.** `REBASELINE_READY` not reached.

## §49 — v2.0 remains an explicit blocker

`V2_ARTIFACT_NOT_FOUND` stands. Per §49 the system may separately preserve a
`RECONSTRUCTED_REFERENCE_ARTIFACT` for research, but it is a **different
artifact** with its own id, hash, and provenance, and it cannot satisfy the
exact-artifact requirement. No substitute was manufactured.

## §51

```text
SEARCH   must be tested as a search      -> done, 12/12 + 3 controls
GATES    must be tested as gates         -> NOT DONE. The runner is untested.
PARSERS  must be tested as parsers       -> done, 12/12, and it found a bug
METRICS  must be tested as measurements  -> NOT DONE. No reference set exists.
BASELINES must be tested as baselines    -> Vault VALID, Validators UNPROVABLE
RESULTS  must be tested as results       -> FAIL. Exit 0 masked a failing suite.
```

Two of seven done. One of them was previously reported as done and was not.

## Related

- [v4.1 instrumentation record](v4-1-instrumentation-integrity-record.md)
- [v4.0 repair record](v4-0-repair-rebaseline-record.md)
- Git porcelain regression suite (FreeBuff notebook file `../state/repair/test-git-porcelain.mjs`)
- Git porcelain output is whitespace-significant (FreeBuff notebook file `../39_LESSONS/git-porcelain-is-whitespace-significant.md`)