---
source: Freebuff local logs under ~/.config/manicode/projects (log.jsonl, run-state.json, chat-meta.json), read directly on 2026-10-06; hashes in model-runs-manifest.json
captured: 2026-10-06
status: pending
---

# FreeBuff worker run record: Alpha Space Bunny (Space Bunny Alpha)

**OBSERVED** from Freebuff's local logs, not independently verified; `pending` (AGENTS.md rule 2), no claim row. Unrecovered fields are `UNRESOLVED`. Method and limits: [recovery record](model-runs-recovery-2026-10-06.md).

## Identity and window

- Agent templates: `base3-free-space-bunny-alpha` (705 steps).
- Models logged: `stealth/space-bunny-alpha` (705 steps).
- Run configuration: `free` cost mode, 200 steps per run (vendor-built Freebuff loop; internals not seen).
- First and last logged step: 2026-09-24 20:33Z and 2026-10-01 15:31Z. None is dated October 4.
- 6 days with steps, 6 chats, 53 runs, 705 logged steps, 53 prompts sent to this agent.

## Task and question

`UNRESOLVED` by choice: prompt text is in the private archive, withheld from this public repository.

## Chats (start UTC, steps)

`09-24T01-18` (172), `09-24T22-58` (155), `09-26T23-43` (43), `09-27T23-40` (86), `09-29T00-42` (47), `09-30T20-24` (202).

## Work performed

**859** tool calls, attributed to this worker by the `model` field on each logged line. Top tools: `run_terminal_command` 390, `str_replace` 148, `code_search` 94, `write_todos` 61, `write_file` 54, `skill` 32.

## Artifacts touched

`str_replace` plus `write_file` calls by the tree named in the path (call counts, not distinct files; `other` means no listed tree was named): msb-v3 85, other 82, Vault 24, FREEBUFF_PZS 11.

## Verifier-like commands and exit codes

192 verifier-like terminal commands, exit codes from the logged results. `verify-or-gate` is a broad match and overcounts. An exit code does not show a check was meaningful; whether each could fail is `UNRESOLVED`.

| Category | Exit 0 | Non-zero |
|---|---|---|
| mypy | 11 | 2 |
| pytest | 30 | 10 |
| ruff | 8 | 6 |
| unittest | 35 | 0 |
| verify-or-gate | 80 | 9 |

## Failures preserved

Error events: `Provider returned an empty response` 4; `ERROR` 1; `Precondition Required` 1. Tool errors passed through to the model: 48 (attributed to the agent last seen in the file; approximate). Last-run output per chat: 3x lastMessage; 1x error: ERROR; 1x error: Your free session has ended. Send.

## Human interventions

Prompts sent 53; suggested follow-ups clicked 5 (attributed to the agent last seen in the file); `ask_user` calls 8; user interrupts 0. Human review or acceptance of the resulting work is `UNRESOLVED`.

## Not recovered

- Quality of the work and whether any result was accepted or reverted: `UNRESOLVED`.
- Whether this worker "fixed the persistent memory": `UNRESOLVED`. The logs show edits, not what they repaired; the documented stale-RAG repair (2026-10-03/04, per the forensic session report, not re-checked) falls after this worker's last step.
- Tool calls under an opaque model key are unattributed (recovery record); this worker's totals may omit some work.
