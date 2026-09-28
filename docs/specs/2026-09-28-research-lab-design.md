# BlackSwanLabz Research Lab — Design Spec (v1)

- **Date:** 2026-09-28
- **Author:** Lord Wilson (lordwilsonDev)
- **Status:** approved design, awaiting spec review
- **Repo:** `lordwilsonDev/blackswanlabz-research-lab` (built locally first; publishing is Wilson's decision)

## 1. Purpose

One place where all of Wilson's work can be found, understood, and checked.

Two readers, one repo:

1. **People** — land on the README and are guided, stop by stop, from the problem to the proof.
2. **A single AI model** — pointed at this one repo, it can understand the whole body of work without cloning any other repo.

Core rule: **every claim links to its evidence.** Anything unverified is labeled pending, never stated as fact.

## 2. Approach

**Hub + curated snapshots.** The lab holds explanations and evidence (thesis, papers, specs, results, receipts, timeline). Source code stays in its own repos, pinned by commit hash. Rejected: full monorepo (too large for a model context; duplicates repos with their own CI) and README-only hub (fails the single-model goal).

## 3. Scope (v1)

In: the pillars Wilson named — the thesis, GitHub AI Projects (cornerstone), North Star, Axiom Inversion Logic (AIL), MoIE, ACTS, Adaptive Infrastructure, MSB v3, FCVE, white papers, tests run, proofs.

Out of v1: older 2025 projects/repos and an archive timeline (candidate for v2).

## 4. README tour (problem-first)

| Stop | Title | Links to |
|---|---|---|
| 0 | Hook — "Intelligence is becoming abundant. Verification isn't. This lab is the evidence." | — |
| 1 | The Problem — Intelligence Infrastructure Mismatch in ~5 sentences | `00-thesis/` |
| 2 | The Prediction — Dec 2025: 32.5M lines committed, 35 categories, 208+ projects; prediction table | `01-cornerstone/` |
| 3 | The Principles — North Star, AIL, MoIE, ACTS, Adaptive Infrastructure | `02-frameworks/` |
| 4 | The Proof — MSB v3 (active), FCVE (archived) | `03-systems/`, `06-proofs/` |
| 5 | The Papers & Tests — including pre-registered, not-yet-run benchmarks | `04-papers/`, `05-experiments/` |
| 6 | Check Everything | `CLAIMS.md`, `scripts/verify.sh` |
| 7 | For AI readers | `llms.txt`, `AGENTS.md` |

Every number in the README links to a `CLAIMS.md` row.

## 5. Repository layout

```
blackswanlabz-research-lab/
├── README.md
├── llms.txt
├── AGENTS.md
├── CLAIMS.md
├── CITATION.cff
├── LICENSE            (CC BY 4.0 — writing/papers)
├── LICENSE-CODE       (MIT — scripts)
├── 00-thesis/
├── 01-cornerstone/
├── 02-frameworks/
├── 03-systems/
├── 04-papers/
├── 05-experiments/
├── 06-proofs/
├── scripts/verify.sh
├── .github/workflows/verify.yml
└── docs/specs/
```

## 6. Folder contents and sources

| Folder | Contents | Source |
|---|---|---|
| `00-thesis/` | Intelligence Infrastructure Mismatch (verbatim) | Vault `10_Projects/BlackSwanLabz/BlackSwanLabz-Thesis-Intelligence-Infrastructure-Mismatch.md` |
| `01-cornerstone/` | Package summary; 35 categories; code-frequency evidence (screenshot + API JSON); `prediction-timeline.md`; cloc/tokei breakdown (pending) | `github.com/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE` |
| `02-frameworks/` | `north-star.md`, `axiom-inversion-logic.md`, `moie.md`, `acts-5-act-research.md` (+ worked example AIL-AI-SMB-001), `adaptive-infrastructure.md` | Vault `10_Projects/BlackSwanLabz/BlackSwanLabz-North-Star-Architecture.md`, `30_Architecture/North-Star-FDE-Cybernetic-Loop.md`, `30_Architecture/Scientific-Research-Apparatus/`, MoIE wiki (`30_Architecture/diagrams/Sovereign-Stack-Tooling/wiki/MoIE-Framework-2.0-revised.md`), msb-v3 `docs/blueprints/` (adaptive build environment, Meta-System), `~/acts_mixture_of_inversion_experts` |
| `03-systems/` | `msb-v3.md` (what it is, audit results, MVP closure evidence, pinned commit); `fcve.md` (archived 2026-09-19, what it proved) | `~/projects/AI-Agents/msb-v3`, Vault `10_Projects/msb-v3/MSB-v3.md`; `github.com/lordwilsonDev/fcve` |
| `04-papers/` | AIL-WP-2026-08-005 (AIL + MoIE); Epistemic State Transition Question Engineering paper; others selected during build | ACTS repo; Vault `30_Architecture/` |
| `05-experiments/` | Tests run and results: MSB v3 suite + CI gates; Meta-System small-model scoreboard (8/9 delegated functions correct); Hermes12 AIL+MoIE benchmark (pre-registered, **not run**) | msb-v3; ACTS `98_HERMES12_BENCHMARK/` |
| `06-proofs/` | FCVE VCE-001/002 runs + receipts; Lean/Collatz verification; upstream PRs leanprover/lean4export#52, ammkrn/nanoda_lib#36 | `lordwilsonDev/fcve`, `lordwilsonDev/ico-collatz-verification` |

## 7. Snapshot rules

1. Each snapshot file has a header: `source`, `commit` or `vault-date`, `captured`, `status` (active / archived / pending).
2. Copy explanations; link code at a pinned commit.
3. **Nothing private.** No client material, legal/family matters, secrets, tokens, or personal notes. Every copied file is secrets-scanned before commit.
4. Faithful, not rewritten. Corrections are shown, not silently applied.

## 8. Prediction timeline

`01-cornerstone/prediction-timeline.md` maps each cornerstone category to a later industry event. A row is included only if **both sides are dated and sourced** and the cornerstone date comes first. Cornerstone date anchor: GitHub code frequency, week of 2025-12-14. Rows that can't be dated stay out (or are listed as pending).

## 9. CLAIMS.md

One table: `ID | claim | evidence | how to check | status (verified / pending / retracted) | date checked`.

Seed rows:

| ID | Claim | Evidence | Status |
|---|---|---|---|
| C-001 | 32,543,981 lines added to GITHUB_AI_PROJECTS_PACKAGE in week of 2025-12-14 (net 32,543,027 to date) | GitHub Code Frequency; API `/repos/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE/stats/code_frequency` | verified (2026-09-28, from Wilson's export) |
| C-002 | Breakdown of C-001 into own source / vendored / data | `cloc` or `tokei` at pinned commit | pending (needs disk or VM) |
| C-003 | Package contains 208+ projects, 35 categories, 19,864 Python files, 649 dependencies | package README | pending (README self-report; recount) |
| C-004 | AIL+MoIE outperforms compute-matched baselines (H1c) | Hermes12 benchmark | pending — not run |

"Lines committed" is never restated as "lines of code" until C-002 is verified.

## 10. AI entry point

- `llms.txt` (llmstxt.org format): summary, reading order (thesis → cornerstone → frameworks → systems → papers → experiments → proofs → CLAIMS), one line per file.
- `AGENTS.md`: `CLAIMS.md` is authoritative; pending ≠ verified; code lives in linked repos at pinned commits.
- **Size budget:** repo text (excluding images) stays under ~150k tokens so one model can hold it.

## 11. Verification

`scripts/verify.sh` checks:

1. Cornerstone code frequency still matches C-001.
2. Every pinned commit exists in its repo.
3. Internal links resolve.
4. Every number in README has a `CLAIMS.md` row.
5. Text size stays under budget.

The GitHub Action runs it on push and weekly; the README badge reflects the result.

## 12. Licensing and citation

CC BY 4.0 (writing, papers), MIT (scripts). `CITATION.cff` with Wilson's name; ORCID left blank until a real one is registered (see Vault `30_Architecture/Research-Output-System.md` correction of 2026-09-14).

## 13. Build order

1. Spec (this document)
2. Implementation plan
3. Scaffold
4. Fill pillar by pillar, adding CLAIMS rows as each goes in
5. `verify.sh` green
6. Wilson reviews
7. Wilson decides on publishing

## 14. Known limitations

- Commit dates prove existence **by** 2025-12-14, not origin dates of individual projects.
- FCVE is archived; the lab presents it as completed work, not ongoing.
- The AIL+MoIE benchmark has no results; the lab presents its pre-registration and falsification condition only.
- Snapshots can drift from sources; headers and `verify.sh` make drift visible, not impossible.
