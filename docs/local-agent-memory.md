# Local agent memory and wake-up pings

Status: pending. The code is tested against a fake Ollama endpoint, not a real model.

`scripts/local_agent_memory.py` gives Ollama models persistent, governed memory without
running them continuously. Same workspace layout as `scripts/memory_validator.py`.

```bash
export PZS_ROOT=~/pzs-workspace     # git repo with 03_COMPLETED, 42_PERMANENT_MEMORY, state/
echo wilson > $PZS_ROOT/state/approvers.txt          # humans allowed to approve

scripts/local_agent_memory.py ping --task "Summarize today's open loops"   # queue a wake-up
scripts/local_agent_memory.py wake --model llama3.1                         # drain once, exit
scripts/local_agent_memory.py approve CAND-2026-10-03-001 --by wilson \
    --title "Short title" --text "The durable knowledge, written by you, not the transcript."
scripts/local_agent_memory.py show-memory                                  # what the next wake injects
```

## Wake on a schedule (the "ping")

```cron
*/15 * * * * PZS_ROOT=$HOME/pzs-workspace /path/to/scripts/local_agent_memory.py wake --model llama3.1
```

Anything that can run `ping` (cron, a webhook handler, a file watcher, another script) can
trigger a model. `wake` takes a lock, so overlapping runs are safe.

## What the governance does

- Model output is stored as a `NEEDS_REVIEW` candidate (14-day deadline). It is **not** memory.
- `approve` needs an identity in `state/approvers.txt` and rejects `model:*`. You write the memory text.
- Only ACTIVE, non-stale memory is injected, wrapped as data, within a 6000-character budget.
- Integrity failures (IDs, provenance, references, supersession, merges) stop injection and
  the model runs stateless; the degradation is logged. An expired-review backlog does not.
- Events are append-only in `state/pings.jsonl`, `state/usage.jsonl`, `state/decisions.jsonl`.

## Not built

Reject/demote/supersede commands, the review-expiry resolver, and automatic summarization of
candidates into memory text. Until you approve candidates, models have only the memory you
have already approved.
