#!/usr/bin/env python3
"""Adapter for a local Ollama server. Reads the prompt on stdin, prints the reply, reports tokens on stderr.

Env: OLLAMA_MODEL (default qwen3:8b), OLLAMA_HOST (default http://localhost:11434), HARNESS_SEED (set by the harness),
OLLAMA_TEMPERATURE (default 0.7), OLLAMA_NUM_PREDICT (default 512), OLLAMA_NUM_CTX (default 8192),
OLLAMA_SYSTEM (default: a code-writing system prompt; set it for non-code experiments).

Fails closed: if the prompt fills the context window the model would silently drop the start of it, so the adapter exits
with an error instead of returning a corrupted answer.
"""
import json, os, re, sys, urllib.request

SYSTEM = os.environ.get("OLLAMA_SYSTEM") or "You are a careful Python programmer. Reply with exactly one ```python code block and nothing else."
host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
num_ctx = int(os.environ.get("OLLAMA_NUM_CTX", "8192"))
body = {"model": os.environ.get("OLLAMA_MODEL", "qwen3:8b"), "stream": False, "think": False,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": sys.stdin.read()}],
        "options": {"temperature": float(os.environ.get("OLLAMA_TEMPERATURE", "0.7")),
                    "seed": int(os.environ.get("HARNESS_SEED", "0")),
                    "num_predict": int(os.environ.get("OLLAMA_NUM_PREDICT", "512")),
                    "num_ctx": num_ctx}}
req = urllib.request.Request(host + "/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=900) as r:
    data = json.load(r)
tin = data.get("prompt_eval_count")
if tin is not None and tin >= num_ctx - 8:
    sys.exit(f"context overflow: prompt used {tin} of {num_ctx} tokens; raise OLLAMA_NUM_CTX instead of accepting a truncated prompt")
text = re.sub(r"<think>.*?</think>", "", data["message"]["content"], flags=re.S).strip()
print(text)
print(f"TOKENS_IN={tin if tin is not None else 0} TOKENS_OUT={data.get('eval_count', len(text) // 4)}", file=sys.stderr)
