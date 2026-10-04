---
source: FreeBuff (Buffy) run record from the PZS notebook, 06_ARCHITECTURE/v4-0-repair-rebaseline-record.md; body copied unchanged except that links to other notebook files are written as plain references
captured: 2026-10-03
status: pending
---

# v4.0 Repair & Rebaseline — Record and Terminal State

Date: 2026-10-03
Status: in-progress

Protocol: Wilson's *Rebaseline & Artifact Integrity Repair Blueprint v4.0*
(Status: PROPOSED — REPAIR/REBASELINE ONLY).
Machine artifacts: `state/repair/repair-gate.mjs`, `state/repair/REPAIR_GATE_v4_0.txt`,
`state/repair/test-link-containment.mjs`.

> **§37 terminal state: `BLOCKED`.** 7 of 14 gates pass.
> **`REBASELINE_READY` is not reached, so PT-2026-10-03-002 is not permitted.**
> Per §36 every failed gate is recorded with evidence. Nothing was silently
> bypassed and nothing was repaired to make the gate green.

## §6 — v2.0 Recovery Gate: `V2_ARTIFACT_NOT_FOUND`

> **WITHDRAWN by [v4.1](v4-1-instrumentation-integrity-record.md).** The finding
> below was an **absence claim produced by a detector that had never passed a
> positive control**, on a `timeout`-bounded scope — which v4.1 §14/§16 prohibit
> reading as ABSENT. The corrected, calibrated result is
> **`NOT_FOUND_IN_SEARCH_SCOPE`**, and no absence claim is made anywhere.
> Kept verbatim below because the error is the record.

Searched every source v4.0 §6 authorizes:

```bash
$ grep -rl -e "Immediate Execution Boundary" -e "ASSERTION_SUBSTITUTION_RATE" \
         -e "Rebaseline & Artifact Integrity Repair" -e "Non-Intervention Rule" ~
# zero matches, whole home directory
```

Also checked: git history (270 objects, latest commit `973c823` — adds only a
*pointer note*), `git stash` (empty), `git fsck --lost-found` (nothing),
`~/.freebuff` (holds `mcp.json` + `project-id`, **no transcript**),
`~/.claude/projects` (present, no matching content).

**The v2.0 bytes exist only in the live conversation buffer.** Per §6,
`BLOCKED`. Per §5, `CHAT_TEXT` is explicitly not a `VERBATIM_ARTIFACT`, and
retyping is prohibited. Gates 1, 2 and 3 fail as a direct consequence.

## §10/§11 — T0 Evaluation

| Half | Verdict | Evidence |
|---|---|---|
| **Vault** | `T0_VALID` | commit `cb997e40f5879fb169902d1ef8d40820519a6c87`, tree `0d73ed93ad9aff1893135f32de0b0c78c2f1fd21`, 2026-10-01T13:27:09-05:00. Contains **zero** epistemic/v2/v3 pointer notes and **no `state/` tree**. The session's edit to `existence-is-not-freshness.md` is absent from it. |
| **Validators** | `T0_UNPROVABLE` | `~/.agents` **is** a git repo but has **zero commits** on its branch (`does not have any commits yet`). No version-control evidence of pre-treatment state. |
| **Overall** | **`T0_PARTIAL`** | partial is not pass |

Supporting-but-insufficient for the validator half: all 7
`freebuff-pzs-memory` script mtimes are 2026-09-21 / 09-22 / 10-02 — **none
modified today**. That is a witness, not a snapshot. Per the vault's own
`existence-is-not-freshness` (FreeBuff notebook file `../39_LESSONS/existence-is-not-freshness.md`), an
mtime is not freshness.

Per §12: **history was not rewritten, T0 was not backdated, no mutation was
deleted.** The partial verdict is recorded as partial.

## §13 — Session-Mutation Ledger (9 entries, 9 classified)

| ID | Op | Relevance | Path |
|---|---|---|---|
| MUT-001 | GENERATE | UNRELATED | `00_SYSTEM/CHANGELOG.md` |
| MUT-002 | GENERATE | UNRELATED | `00_SYSTEM/INDEX.md` |
| MUT-003 | EDIT | UNRELATED | `39_LESSONS/existence-is-not-freshness.md` |
| MUT-004 | CREATE | BEFORE | `05_DECISIONS/epistemic-blueprint-reconciliation-and-inversion.md` |
| MUT-005 | CREATE | BEFORE | `06_ARCHITECTURE/governed-memory-blueprint-v2.md` |
| MUT-006 | CREATE | BEFORE | `06_ARCHITECTURE/governed-memory-blueprint-v3-production-test.md` |
| MUT-007 | CREATE | BEFORE | `06_ARCHITECTURE/production-test-pt-2026-10-03-001.md` |
| MUT-008 | CREATE | BEFORE | `40_OPEN_LOOPS/epistemic-blueprint-v1-v1-1-unaccounted.md` |
| MUT-009 | CREATE | BEFORE | `state/` |

All nine carry a stated rationale. **Zero** are classified `TREATMENT` — which is
the correct outcome: the v3.0 §2 intervention was never performed, so nothing in
this session is the treatment.

## §14 — PT-2026-10-03-001 disposition

Permanently classified **`HOLD — NO TREATMENT OCCURRED`**. Not
`EXPERIMENT_INVALIDATED_BY_PRE-INTERVENTION_MUTATION`: that class would imply a
run that began. This one never began its treatment. It must never be represented
as a successful treatment run.

## §29 — Link Integrity Repair: implemented and green

`state/repair/test-link-containment.mjs` — **6/6 controls pass**, exits non-zero
on violation. The two caught `../../state/` escapes are now permanent regression
cases, alongside `../../../etc/passwd` and a symlink-containment sweep.

On its first run it found one real escape and one false positive:

- **Real:** `39_LESSONS/verify-symlink-before-calling-it-a-copy.md →
  ../../.agents/skills/freebuff-pzs-memory/SKILL.md`. This genuinely escapes the
  vault root. Per §29 escapes are rejected *unless explicitly authorized*, so it
  was added to an `AUTHORIZED_EXTERNAL` map **with a written reason** — recorded,
  not silenced, and still reported on every run.
- **False positive:** `<video_url>&t=<seconds>s` — markdown template syntax in
  documentation, not a link. Now filtered.

`89 relative links OK (2 placeholders skipped, 1 authorized external)`.

## §23 — Validator Target Contract: 4 declared

| Validator | Source of declaration | Exercised |
|---|---|---|
| `check-closeout.mjs` | source read | **yes** |
| `check-constitution.mjs` | source read | **yes** |
| `state-machine.mjs` (s10) | **vault note, not source** | no |
| `claim_states.py` | source read | **no** |

Two honesty flags ride with this table and are not decoration:

- `state-machine.mjs` targets are declared **from a prose note**, not from its
  source. §23 forbids inferring targets from filenames; it does not license
  inferring them from documentation either.
- `claim_states.py` was **never executed** this session. §45 forbids treating
  "module exists" as coverage.

That is why **gate 11 fails**: §25 requires an *executed* mutation matrix, and
no per-validator mutation runs were performed.

## Four bugs found in the repair tooling itself

Recorded in the gate's `self_bugs_found` and promoted to a standing lesson:
`git-porcelain-is-whitespace-significant` (FreeBuff notebook file `../39_LESSONS/git-porcelain-is-whitespace-significant.md`).

`.trim()` on `git status --porcelain` deleted the leading **status character** of
the first line only, because porcelain is whitespace-significant. That produced a
plausible, specific, wrong claim about a file that was in the table the whole time.
Two earlier parse bugs (`slice(3)`, then a `\S{2}` regex that cannot match a
leading space) produced the same wrong verdict in opposite directions. And gate 5
was hardcoded `pass: true`, so it reported success while its own input contained
an unclassified row — **a gate that cannot fail**.

All four were found by **running** the gate, three times. None would have been
found by reading the final version.

## §31 gate board — 7/14

> **RELABELLED by [v4.1](v4-1-instrumentation-integrity-record.md):**
> **`7/14 [diagnostic, gate-runner-uncalibrated]`.**
> Six of the fourteen gates are hardcoded `pass: true`; only one is computed. The
> ratio is an assertion about the world written before running anything, not a
> measurement. `0 of 14` are certified measurements.

| # | Gate | | Evidence |
|---:|---|:---:|---|
| 1 | exact v2.0 artifact recovered | **FAIL** | `V2_ARTIFACT_NOT_FOUND` |
| 2 | v2.0 byte hash recorded | **FAIL** | no artifact → no hash |
| 3 | treatment identity frozen | **FAIL** | depends on 1–2 |
| 4 | valid pre-treatment T0 | **FAIL** | `T0_PARTIAL` — vault valid, validators unprovable |
| 5 | prior mutations classified | **PASS** | 9/9, each with rationale |
| 6 | slice-one path corrected | **PASS** | `39_LESSONS/existence-is-not-freshness.md` |
| 7 | slice-one semantics recorded | **PASS** | PRIMARY=FRESHNESS/STALENESS; PROVENANCE and VERIFICATION = NOT_ESTABLISHED |
| 8 | why-durable predicate frozen | **PASS** | `2/44`, accuracy `NONE` |
| 9 | staleness predicate frozen | **PASS** | `staleness-mention-v1`, `9/44 = 20.5%`, accuracy `NONE` |
| 10 | checker targets declared | **PASS** | 4 declared, 2 carrying honesty flags |
| 11 | mutation matrix executable | **FAIL** | no executed mutation runs |
| 12 | META-003 disposition resolved | **FAIL** | Wilson's call — §27 |
| 13 | link controls green | **PASS** | 6/6 controls |
| 14 | artifact provenance complete | **FAIL** | no provenance ledger exists |

## What unblocks `REBASELINE_READY`

Four things, three of them yours:

1. **Save v2.0 to a file.** Clears gates 1, 2, 3. Nothing else can substitute.
2. **Commit or version the validator subtree** so pre-treatment state is
   provable. Clears gate 4's validator half.
3. **META-003** — `NEWLY_AUTHORED` or `EXPLICITLY_DROPPED`. Clears gate 12.
4. **Run the §25 mutation matrix** against the two unexercised validators.
   Clears gate 11. Plus an artifact provenance ledger for gate 14.

## §35, applied

Repair success would mean *the experiment can be run without violating its own
protocol*. It does not mean the memory system is better. That question is still
unanswered, and §38 is the right governing principle for the whole phase:

> `EXACT ARTIFACT > RECONSTRUCTION` · `VALID BASELINE > CONVENIENT BASELINE` ·
> `UNKNOWN > FALSE CERTAINTY`

## Related

- [PT-2026-10-03-001 — T0 Baseline and HOLD](production-test-pt-2026-10-03-001.md)
- Production Testing Blueprint v3.0 (FreeBuff notebook file `governed-memory-blueprint-v3-production-test.md`)
- Git porcelain output is whitespace-significant (FreeBuff notebook file `../39_LESSONS/git-porcelain-is-whitespace-significant.md`)
- Slice-one readiness against v2.0 §76 (FreeBuff notebook file `../state/slice-one/SLICE_ONE_READINESS_v2_0.md`)