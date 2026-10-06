---
source: index of FreeBuff run records held in this lab
captured: 2026-10-04
status: pending
---

# FreeBuff run records, 2026-10-03

Records of runs made by the FreeBuff agent on 2026-10-03, copied from its PZS notebook. Each file's body is as written there, including its own `Status:` line. Two changes were made: a header was added to place it in this repository, and links to other notebook files, which are not in this repository, were rewritten as plain references (`FreeBuff notebook file ...`) so that no link is broken.

**These are run records, not verified results.** Status here is `pending` under [AGENTS.md](../../AGENTS.md) rule 2: nothing on these pages becomes a claim until a row in [CLAIMS.md](../../CLAIMS.md) says `verified`. No claim rows were added. Most records describe themselves as in-progress; one is a method definition that was not run.

| Record | What it is | Date |
|---|---|---|
| [v5-0-production-series-record](v5-0-production-series-record.md) | v5.0 production series PTS-2026-10-03-001 | 2026-10-03 |
| [v7-0-question-engineering-application](v7-0-question-engineering-application.md) | v7.0 question engineering applied to itself | 2026-10-03 |
| [v8-0-pbr-cycle-001-record](v8-0-pbr-cycle-001-record.md) | PBR-2026-10-03-001 cycle 001 record | 2026-10-03 |
| [production-test-pt-2026-10-03-001](production-test-pt-2026-10-03-001.md) | PT-2026-10-03-001: T0 baseline and hold | 2026-10-03 |
| [skill-validator-adversarial-audit-2026-10-03](skill-validator-adversarial-audit-2026-10-03.md) | skill validator adversarial audit; findings open | 2026-10-03 |

Not included: the three earlier v4.x records (v4.0, v4.1, v4.2), held back to keep this repository under its 250,000-token size budget (they remain in the FreeBuff notebook), and one 8-line completion note (rag-stale-memory-publication-2026-10-04) that contains an SSH key fingerprint, and the benchmark definition `domain-crossing-depth-benchmark-v1-0` (a method, not yet run).

## FreeBuff worker runs recovered from logs, 2026-10-06

Recovered by Claude from Freebuff's local logs on 2026-10-06 (not from the notebook). Evidence level `OBSERVED`, not independently verified; unrecoverable fields are marked `UNRESOLVED`.

| Record | What it is |
|---|---|
| [model-runs-recovery-2026-10-06](model-runs-recovery-2026-10-06.md) | How the three worker runs were found, what was searched, limits, and where this differs from the earlier summary |
| [model-run-glm](model-run-glm.md) | GLM worker, 2026-08-14 to 2026-09-12 |
| [model-run-deepseek](model-run-deepseek.md) | DeepSeek worker, 2026-08-08 to 2026-09-30 |
| [model-run-space-bunny-alpha](model-run-space-bunny-alpha.md) | Alpha Space Bunny worker, 2026-09-24 to 2026-10-01 |
| [model-runs-manifest.json](model-runs-manifest.json) | rollup hashes of the source logs and of the private archive |

