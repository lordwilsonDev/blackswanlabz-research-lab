---
source: recovery of the GLM, DeepSeek and Alpha Space Bunny worker runs from Freebuff's local logs, 2026-10-06
captured: 2026-10-06
status: pending
---

# Recovery record: the three FreeBuff worker runs

Wilson names three models as workers in one persistent environment: GLM, DeepSeek and Alpha Space Bunny. This repository had no record of them. This page records their recovery from raw evidence. **Nothing here is VERIFIED.** Recovered facts are `OBSERVED` (read by Claude from Freebuff's own logs, not independently checked); the rest is `UNRESOLVED`. Nothing was reconstructed from memory.

Records: [GLM](model-run-glm.md), [DeepSeek](model-run-deepseek.md), [Alpha Space Bunny](model-run-space-bunny-alpha.md). Source hashes: [model-runs-manifest.json](model-runs-manifest.json).

## The gap, and its scope

| Where searched | How | Result |
|---|---|---|
| This repository, 31 branches and remote refs (252 commits) | `git grep -i` for `glm`, `space bunny`, `deepseek`; `git log --grep` | No `glm`, no `space bunny` anywhere; `deepseek` only in `03-systems/msb-v3-governance-sop.md` on master; no commit message names any of them. The gap was real. |
| FreeBuff PZS notebook (`~/FREEBUFF_PZS`) | ripgrep for the same names | No file or changelog line names GLM or Space Bunny. `deepseek` appears only in project notes about other work, not as run records. |
| Freebuff's local chat logs (`~/.config/manicode/projects/*/chats/*`) | Read directly (below) | **Found.** 96 chat folders, 58 with a recorded run state, 2026-08-07 to 2026-10-06. This is the only primary source. |
| The 2026-10-04 forensic review session | Four captured turns | The claim originates here: Wilson's brief (turn 1), the assistant report (turn 2) and Wilson's follow-up (turn 7). Secondary evidence, not a run record. |

This is a statement about the places listed, not about the whole machine.

## What was recovered

Freebuff logs a line per agent step with the template and model, and a separate line per step with the tool calls and results. The two carry no shared identifier, so tool calls are attributed by their `model` field; run-start lines name the agent for each prompt.

| Worker | First step | Last step | Steps | Runs | Chats |
|---|---|---|---|---|---|
| GLM | 2026-08-14 11:03Z | 2026-09-12 22:55Z | 713 | 30 | 8 |
| DeepSeek | 2026-08-08 01:27Z | 2026-09-30 01:23Z | 7544 | 429 | 28 |
| Alpha Space Bunny | 2026-09-24 20:33Z | 2026-10-01 15:31Z | 705 | 53 | 6 |

Templates and models are in each record. Name mapping, so a later search finds them: "Alpha Space Bunny" is Freebuff's `stealth/space-bunny-alpha` model (agent display name "Buffy on Space Bunny Alpha"). The brief said "GLM-5"; the logs show `glm-5.2` and `glm-5.3-flash`, and no exact "GLM-5" identifier.

DeepSeek starts first (August 8), GLM runs inside its window (August 14 to September 12), and Alpha Space Bunny follows from September 24. Whether any task moved between models is `UNRESOLVED`.

## The October 4 date and the earlier summary

No step by any of the three is dated October 4; that is when the forensic review session listed them. Last steps: September 12 (GLM), September 30 (DeepSeek), October 1 (Alpha Space Bunny). The review's windows agree for GLM and Alpha Space Bunny; DeepSeek differs (Aug 13 to Sep 18 there, Aug 8 to Sep 30 here). Its edit counts (msb-v3 / Vault / PZS) also differ: DeepSeek 804 / 203 / 46 against 844 / 256 / 45; GLM 141 against 176; Alpha Space Bunny 60 / 16 / 11 against 85 / 24 / 11. Counts here are `str_replace` plus `write_file` calls by path; the earlier method is not recorded, so the cause is `UNRESOLVED`.

## Limits and exclusions

- 5,172 tool calls carry an opaque Freebuff model key and cannot be assigned to any worker (probably other agents, not established), so per-worker totals may omit some work. Other agents in the logs (mimo, muse-spark, catalog, luna, solar-pro4) are outside this request.
- Logs are mutable local files, hashed on 2026-10-06. Run-state keeps only the last run of a chat, so counts come from the logs and last-run outputs from run-state. Per-chat step counts are in the private archive.
- Excluded on purpose: prompt text, command text, the account email, the user identifier and every Freebuff model key.
- No quality comparison was recovered: "continued operating in the same environment" is observed, "equally well" is `UNRESOLVED`.

## Provenance

The 42 attributed `log.jsonl` files (a 23 MB archive), a full per-file manifest and the aggregation script are held privately, because the logs contain the account email and key strings, and kept out of this repository to stay under its size budget. [model-runs-manifest.json](model-runs-manifest.json) publishes the archive hash, the full-manifest hash and per-worker rollup hashes. Recovered by Claude on 2026-10-06 at Wilson's request; same-author, no independent check.
