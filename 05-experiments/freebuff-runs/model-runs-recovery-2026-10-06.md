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
| The 2026-10-04 forensic review session | Four captured turns | The claim originates here: Wilson's brief (turn 1) lists the three as claimed worker substitutions, the assistant report (turn 2) tabulates them, and Wilson's follow-up (turn 7) states they are the three models he uses. This is secondary evidence (a brief and an assistant summary), not a run record. |

This is a statement about the places listed, not about the whole machine.

## What was recovered

Freebuff logs a line per agent step with the template and model, and a separate line per step with the tool calls and results. The two carry no shared identifier, so tool calls are attributed by their `model` field; run-start lines name the agent for each prompt.

| Worker | Agent templates | Models logged | First step | Last step | Steps | Runs | Chats |
|---|---|---|---|---|---|---|---|
| GLM | `base3-free-glm`, `base3-free-glm-5-3-flash` | `z-ai/glm-5.2`, `z-ai/glm-5.3-flash` | 2026-08-14 11:03Z | 2026-09-12 22:55Z | 713 | 30 | 8 |
| DeepSeek | `base3-free-deepseek-flash`, `base3-free-deepseek`, `base2-free-deepseek-flash` | `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro` | 2026-08-08 01:27Z | 2026-09-30 01:23Z | 7544 | 429 | 28 |
| Alpha Space Bunny | `base3-free-space-bunny-alpha` | `stealth/space-bunny-alpha` | 2026-09-24 20:33Z | 2026-10-01 15:31Z | 705 | 53 | 6 |

Name mapping, so a later search finds them: "Alpha Space Bunny" is Freebuff's `stealth/space-bunny-alpha` model (agent display name "Buffy on Space Bunny Alpha"). The brief said "GLM-5"; the logs show `glm-5.2` and `glm-5.3-flash`, and no exact "GLM-5" identifier.

DeepSeek starts first (August 8), GLM runs inside its window (August 14 to September 12), and Alpha Space Bunny follows from September 24. Whether any task moved between models is `UNRESOLVED`.

## The October 4 date

No step by any of the three workers is dated October 4: that is the date of the forensic review session that listed them (first turn captured 2026-10-04 13:51 UTC). Last steps: September 12 (GLM), September 30 (DeepSeek), October 1 (Alpha Space Bunny).

## Difference from the earlier summary

The forensic session report gave approximate windows and edit counts "log-attributed", without stating its method. The values recomputed here differ; neither set has been independently verified, and the recomputed one states its method.

Windows agree for GLM (Aug 14 to Sep 12) and Alpha Space Bunny (Sep 24 to Oct 1). DeepSeek differs: Aug 13 to Sep 18 in the summary, Aug 8 to Sep 30 here. Edit counts (msb-v3 / Vault / PZS) differ: DeepSeek 804 / 203 / 46 against 844 / 256 / 45; GLM 141 against 176 (msb-v3); Alpha Space Bunny 60 / 16 / 11 against 85 / 24 / 11.

Recomputed counts are `str_replace` plus `write_file` tool calls whose path text names the tree. The cause of the differences is `UNRESOLVED` (the earlier method is not recorded).

## Limits and exclusions

- **Unattributed tool calls.** 5172 logged tool calls carry an opaque Freebuff model key instead of a model name and cannot be assigned to any worker (about 1190 of them are verifier-like commands). The agent step lines for all three workers carry readable model names, so these probably belong to other agents, but that is not established. The per-worker numbers may therefore exclude some real work.
- **Other agents are not recorded here.** The logs also show runs by other Freebuff agents (last run per chat: mimo 6, muse-spark 4, catalog 3, luna 1, solar-pro4 1, luna-6 1). They were outside the request.
- **Logs are mutable local files**, not signed or chained; hashed on 2026-10-06, so later changes are detectable and earlier ones are not. Run-state files keep only the last run of a chat, so counts come from the logs and last-run outputs from the run-state files.
- **Excluded on purpose:** prompt text, command text, the account email, the user identifier and every Freebuff model key. They are in the raw logs and in the private archive, not in this repository.
- **No quality comparison** between the workers was recovered; "continued operating in the same environment" is observed, "equally well" is `UNRESOLVED`.

## Provenance and reproduction

- Raw copies of the 42 attributed `log.jsonl` files are held outside any repository (a 23 MB archive), with the sha256 of all source files in a full manifest. Both are private because the logs contain the account email and key strings. [model-runs-manifest.json](model-runs-manifest.json) publishes the archive hash, the full-manifest hash and a per-worker rollup hash of the source files.
- The aggregation script (it reads the Freebuff folders and writes aggregates only, never prompts or commands) is held privately too, hash in the manifest. Script, archive and manifest were kept out of this repository to stay under its 250,000-token size budget, as was done for the earlier v4.x run records; they can be added if wanted.
- Recovered by Claude on 2026-10-06 at Wilson's request. Same-author: no independent party has checked these numbers.
