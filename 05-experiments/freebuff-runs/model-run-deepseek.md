---
source: Freebuff local logs under ~/.config/manicode/projects (log.jsonl, run-state.json, chat-meta.json), read directly on 2026-10-06; hashes in model-runs-manifest.json
captured: 2026-10-06
status: pending
---

# FreeBuff worker run record: DeepSeek

**Evidence level: OBSERVED**, read from Freebuff's local logs and not independently verified; `pending` under [AGENTS.md](../../AGENTS.md) rule 2, no claim row added. Fields that could not be recovered are `UNRESOLVED`. Method, limits and differences from the earlier summary: [recovery record](model-runs-recovery-2026-10-06.md).

## Identity and window

- Agent templates: `base3-free-deepseek-flash` (6902 steps), `base3-free-deepseek` (610 steps), `base2-free-deepseek-flash` (32 steps).
- Models logged: `deepseek/deepseek-v4-flash` (6934 steps), `deepseek/deepseek-v4-pro` (610 steps).
- Run configuration: `free` cost mode, `maxAgentSteps` 200 per run. Runtime: Freebuff, a vendor-built loop; the logs show behavior, not its internals.
- First and last logged step: 2026-08-08 01:27Z and 2026-09-30 01:23Z. None is dated October 4.
- 27 days with steps, 28 chats, 429 runs, 7544 logged steps, 429 prompts sent to this agent.

## Task and question

`UNRESOLVED` here by choice, not loss: prompt text is in the private archive and withheld from this public repository (recovery record, "Limits and exclusions").

## Chats

Chat start (UTC, minute) and logged steps by this worker; full times are in the private archive.

`08-07T21-24` (32), `08-13T17-45` (116), `08-13T19-14` (18), `08-14T12-04` (716), `08-14T20-15` (996), `08-17T23-30` (576), `08-19T02-23` (619), `08-20T09-48` (542), `08-21T12-35` (92), `08-22T13-09` (10), `08-28T17-05` (118), `08-29T09-44` (716), `09-02T12-40` (91), `09-08T22-15` (25), `09-09T20-39` (140), `09-09T23-53` (272), `09-16T00-42` (362), `09-17T23-25` (43), `09-18T16-25` (80), `09-19T09-44` (72), `09-21T20-12` (102), `09-22T00-08` (389), `09-23T14-56` (92), `09-23T18-20` (45), `09-25T00-02` (93), `09-25T00-48` (312), `09-29T00-42` (808), `09-30T00-52` (67).

## Work performed

**8561** tool calls, attributed to this worker by the `model` field on each logged line. Top tools: `run_terminal_command` 4761, `str_replace` 1111, `read_files` 865, `write_file` 422, `code_search` 415, `suggest_followups` 272, `write_todos` 257, `list_directory` 198.

## Artifacts touched

`str_replace` plus `write_file` calls by the tree named in the path (call counts, not distinct files; `other` means no listed tree was named): msb-v3 844, other 386, Vault 256, FREEBUFF_PZS 45, fcve 2.

## Verifier-like commands and exit codes

1971 terminal commands matched a verifier-like pattern; exit codes come from the logged tool results. `verify-or-gate` is a broad match (any command containing `verify`, `gate`, `validate` or `check`) and overcounts. An exit code does not show that a check was meaningful, and whether each verifier could fail is `UNRESOLVED`.

| Category | Exit 0 | Non-zero |
|---|---|---|
| make-test | 7 | 0 |
| mypy | 35 | 0 |
| npm-test | 4 | 0 |
| pytest | 404 | 7 |
| ruff | 59 | 1 |
| tsc | 8 | 0 |
| verify-or-gate | 1345 | 64 |

## Failures preserved

Error events: `Precondition Required` 5; `The operation timed out.` 4; `ENOSPC: no space left on device, write` 2; `user-interrupt` 1; `Upstream provider error: DeepSeek provider network` 1; `Upstream provider error (502): (html)` 1. Tool errors passed through to the model: 28 (attributed to the agent last seen in the file; approximate). Last-run output per chat: 21x lastMessage; 7x error: The session ended before this response; 1x error: Agent run error: Failed after 4; 1x error: Your free session has ended. Send.

## Human interventions

Prompts sent 429; suggested follow-ups clicked 228 (attributed to the agent last seen in the file); `ask_user` calls 90; user interrupts 1. Human review or acceptance of the resulting work is `UNRESOLVED`.

## Not recovered

- Quality of the work and whether any result was accepted or reverted: `UNRESOLVED`.
- Whether this worker "fixed the persistent memory": `UNRESOLVED`. The logs show tool calls and edits, not which edits repaired memory. The repair documented in detail (the stale-RAG repair of 2026-10-03/04, msb-v3 PR #10, per the 2026-10-04 forensic session report and not re-checked here) falls after this worker's last logged step.
- Tool calls logged under an opaque model key cannot be attributed (recovery record); this worker's totals may exclude some of its work.
