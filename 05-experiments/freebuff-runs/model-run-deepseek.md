---
source: Freebuff local logs under ~/.config/manicode/projects (log.jsonl, run-state.json, chat-meta.json), read directly on 2026-10-06; hashes in model-runs-manifest.json
captured: 2026-10-06
status: pending
---

# FreeBuff worker run record: DeepSeek

**OBSERVED** from Freebuff's local logs, not independently verified; `pending` (AGENTS.md rule 2), no claim row. Unrecovered fields are `UNRESOLVED`. Method and limits: [recovery record](model-runs-recovery-2026-10-06.md).

## Identity and window

- Agent templates: `base3-free-deepseek-flash` (6902 steps), `base3-free-deepseek` (610 steps), `base2-free-deepseek-flash` (32 steps). Models logged: `deepseek/deepseek-v4-flash` (6934), `deepseek/deepseek-v4-pro` (610). `free` cost mode, 200 steps per run.
- First and last logged step: 2026-08-08 01:27Z and 2026-09-30 01:23Z (none on October 4). 27 days, 28 chats, 429 runs, 7544 steps, 429 prompts sent to this agent.

## Work performed

**8561** tool calls (attributed by the logged `model`): `run_terminal_command` 4761, `str_replace` 1111, `read_files` 865, `write_file` 422, `code_search` 415, `suggest_followups` 272. Edit calls (`str_replace`, `write_file`) by tree named in the path (call counts, not files): msb-v3 844, other 386, Vault 256, FREEBUFF_PZS 45, fcve 2.
Verifier-like commands: 1971; exit-0 over total by category: make-test 7/7; mypy 35/35; npm-test 4/4; pytest 404/411; ruff 59/60; tsc 8/8; verify-or-gate 1345/1409. The `verify-or-gate` match is broad and overcounts, an exit code does not show a check was meaningful, and whether each verifier could fail is `UNRESOLVED`.

## Failures and interventions

Error events: `Precondition Required` 5; `The operation timed out.` 4; `ENOSPC: no space left on device, write` 2; `user-interrupt` 1; `Upstream provider error: DeepSeek provider network` 1; `Upstream provider error (502): (html)` 1. Tool errors passed to the model: 28 (approximate). Last-run output per chat: 21x lastMessage; 7x error: The session ended before this response; 1x error: Agent run error: Failed after 4; 1x error: Your free session has ended. Send. Prompts sent 429; follow-ups clicked 228; `ask_user` calls 90; interrupts 1.

## Not recovered

Prompt text (private archive, withheld here), work quality, human acceptance of results, and whether this worker "fixed the persistent memory" (the logs show edits, not what they repaired; the documented stale-RAG repair of 2026-10-03/04 falls after its last step). Tool calls under an opaque model key are unattributed, so these totals may omit some work.
