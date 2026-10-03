#!/usr/bin/env python3
"""Adapter for the `claude` CLI in print mode. Reads the prompt on stdin, prints the reply, reports tokens on stderr.

Env: CLAUDE_MODEL (default haiku; any alias or id the CLI accepts), CLAUDE_SYSTEM (system prompt),
CLAUDE_ADAPTER_LOG (optional path: appends one JSON line per call with the resolved model, tokens, cost and seconds).

Choices that matter for an experiment, all recorded here so they can be registered:
- Runs in an empty temporary directory so no project instructions are loaded, with all tools disabled.
- Extended thinking is disabled (MAX_THINKING_TOKENS=0) so the prompted procedure is the only reasoning scaffold.
- TOKENS_IN is estimated as characters/4 of the experiment prompt; it excludes the CLI's fixed per-call scaffolding
  (about 850 tokens measured). TOKENS_OUT is the output token count the API reports.
- The CLI exposes no seed and no temperature, so HARNESS_SEED is ignored and runs are not exactly reproducible.
Retries transient failures; exits non-zero (and so aborts the run) if the CLI keeps failing.
"""
import json, os, subprocess, sys, tempfile, time

model = os.environ.get("CLAUDE_MODEL", "haiku")
system = os.environ.get("CLAUDE_SYSTEM", "You are a careful research assistant.")
prompt = sys.stdin.read()
env = {**os.environ, "MAX_THINKING_TOKENS": "0"}
cmd = ["claude", "-p", "--model", model, "--tools", "", "--system-prompt", system, "--output-format", "json", "--no-session-persistence"]
cwd = tempfile.mkdtemp(prefix="claude-adapter-")
last = ""
t0 = time.time()
for attempt in range(6):
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=cwd, env=env, timeout=600)
    last = (r.stderr or r.stdout)[-300:]
    if r.returncode == 0:
        try:
            d = json.loads(r.stdout)
        except ValueError:
            d = None
        if d and not d.get("is_error") and d.get("result"):
            break
    time.sleep(2 * (attempt + 1))
else:
    sys.exit(f"claude CLI failed after retries: {last}")
used = sorted(d.get("modelUsage", {}))
out_tokens = int(d.get("usage", {}).get("output_tokens", len(d["result"]) // 4))
if os.environ.get("CLAUDE_ADAPTER_LOG"):
    with open(os.environ["CLAUDE_ADAPTER_LOG"], "a") as f:
        f.write(json.dumps({"models": used, "output_tokens": out_tokens, "thinking_tokens": d.get("usage", {}).get("output_tokens_details", {}).get("thinking_tokens", 0),
                            "cost_usd": d.get("total_cost_usd"), "seconds": round(time.time() - t0, 2)}) + "\n")
print(d["result"])
print(f"MODEL={','.join(used)}", file=sys.stderr)
print(f"TOKENS_IN={max(1, len(prompt) // 4)} TOKENS_OUT={out_tokens}", file=sys.stderr)
