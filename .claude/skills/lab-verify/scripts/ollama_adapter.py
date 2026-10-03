#!/usr/bin/env python3
"""Adapter for a local Ollama server. Reads the prompt on stdin, prints the reply, reports TOKENS_OUT on stderr.

Env: OLLAMA_MODEL (default qwen3:8b), OLLAMA_HOST (default http://localhost:11434), HARNESS_SEED (set by the harness),
OLLAMA_TEMPERATURE (default 0.7), OLLAMA_NUM_PREDICT (default 512).
"""
import json, os, re, sys, urllib.request

SYSTEM = "You are a careful Python programmer. Reply with exactly one ```python code block and nothing else."
host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
body = {"model": os.environ.get("OLLAMA_MODEL", "qwen3:8b"), "stream": False, "think": False,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": sys.stdin.read()}],
        "options": {"temperature": float(os.environ.get("OLLAMA_TEMPERATURE", "0.7")),
                    "seed": int(os.environ.get("HARNESS_SEED", "0")),
                    "num_predict": int(os.environ.get("OLLAMA_NUM_PREDICT", "512"))}}
req = urllib.request.Request(host + "/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=600) as r:
    data = json.load(r)
text = re.sub(r"<think>.*?</think>", "", data["message"]["content"], flags=re.S).strip()
print(text)
print(f"TOKENS_OUT={data.get('eval_count', len(text) // 4)}", file=sys.stderr)
