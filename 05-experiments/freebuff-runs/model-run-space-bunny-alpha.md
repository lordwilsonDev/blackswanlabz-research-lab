---
source: Freebuff local logs under ~/.config/manicode/projects (log.jsonl, run-state.json, chat-meta.json), read directly on 2026-10-06; hashes in model-runs-manifest.json
captured: 2026-10-06
status: pending
---

# FreeBuff worker run record: Alpha Space Bunny (Space Bunny Alpha)

**OBSERVED** from Freebuff's local logs, not independently verified; `pending` (AGENTS.md rule 2), no claim row. Unrecovered fields are `UNRESOLVED`. Method and limits: [recovery record](model-runs-recovery-2026-10-06.md).

## Identity and window

- Agent templates: `base3-free-space-bunny-alpha` (705 steps). Models logged: `stealth/space-bunny-alpha` (705). `free` cost mode, 200 steps per run.
- First and last logged step: 2026-09-24 20:33Z and 2026-10-01 15:31Z (none on October 4). 6 days, 6 chats, 53 runs, 705 steps, 53 prompts sent to this agent.

## Work performed

**859** tool calls (attributed by the logged `model`): `run_terminal_command` 390, `str_replace` 148, `code_search` 94, `write_todos` 61, `write_file` 54, `skill` 32. Edit calls (`str_replace`, `write_file`) by tree named in the path (call counts, not files): msb-v3 85, other 82, Vault 24, FREEBUFF_PZS 11.
Verifier-like commands: 192; exit-0 over total by category: mypy 11/13; pytest 30/40; ruff 8/14; unittest 35/35; verify-or-gate 80/89. The `verify-or-gate` match is broad and overcounts, an exit code does not show a check was meaningful, and whether each verifier could fail is `UNRESOLVED`.

## Failures and interventions

Error events: `Provider returned an empty response` 4; `ERROR` 1; `Precondition Required` 1. Tool errors passed to the model: 48 (approximate). Last-run output per chat: 3x lastMessage; 1x error: ERROR; 1x error: Your free session has ended. Send. Prompts sent 53; follow-ups clicked 5; `ask_user` calls 8; interrupts 0.

## Not recovered

Prompt text (private archive, withheld here), work quality, human acceptance of results, and whether this worker "fixed the persistent memory" (the logs show edits, not what they repaired; the documented stale-RAG repair of 2026-10-03/04 falls after its last step). Tool calls under an opaque model key are unattributed, so these totals may omit some work.
