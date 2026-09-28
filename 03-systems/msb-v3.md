---
source: github.com/lordwilsonDev/msb-v3
repo: lordwilsonDev/msb-v3
commit: 5cbe03ef43d924c3c3a3cd1d2dbe730ad5f2c370
captured: 2026-09-28
status: active
---

# MSB v3 — governed, local-first agent runtime

## What it is

MSB v3 is a sovereign, local-first, governed agent runtime — FastAPI + SQLite + Qwen3/Ollama + Prometheus. Its own README states it plainly: not a chatbot, not a multi-user SaaS, not a dashboard product. It is a governed loop: a request enters, the system decides whether to run it, executes it under a fail-closed permission boundary, and produces proof of what happened. The canonical path is `/agent/handle → intent → task DAG → ActionGate → governed tools → verification → evidence spine → audit chain → replay`.

Every action passes through a scanner (Guardian), an auditor (Argus), and a memory (Hippocampus) — the "Triumvirate." The ActionGate returns one of `SAFE` / `REVIEW` / `BLOCK` (plus `FAIL`), and a keyword-based pre-filter (MoIE) sits in front of it as a first gate, not the security boundary — the repo is explicit that the ActionGate, a closed fail-closed registry of governed tools, is the actual boundary. `msb_ledger` is an append-only hash chain with Merkle proof-of-inclusion, a signed anchor, and a notary. Every run leaves one evidence receipt — request → intent → MoIE verdict → authorization decision → capability → result → verification → timestamps → model calls → audit hash — and the receipt distinguishes what was directly rerun (`basis: "rerun"`) from what was inferred from logs (`inferred-from-logs`), or `decision-only` for a denial where nothing ran.

Above the agent harness sits PLEI (Project Lifecycle Engineering Intelligence): seven phases (Project Twin → Capability Graph → Dependency/Risk → Monte Carlo → Decision Engine → Harness Integration → Calibration) that model where a project stands and recommend the next-best engineering action. A cron scheduler makes the system proactive (nine built-in governed actions, a wake loop that lets a resident agent answer messages left from any session), and a Vesta trust/evidence perimeter wraps a subset of surfaces (`model.inference`, `memory.read`, a signed-device FILE_READ/FILE_WRITE/SHELL_EXEC approval path) for a companion phone/device protocol.

## Why it matters to the thesis

This lab's thesis is that governance brakes and evidence chains — not raw capability — are what make autonomous systems trustworthy enough to act on. MSB v3 is the verification layer built to test that claim directly: every privileged action must pass an explicit governed-tool registry before it runs, every run (allowed or denied) leaves a receipt that says exactly how it was verified, and the project ships its own claims-checking discipline — a `verify-claims.py`-style gate that blocks a numeric or factual claim from shipping without an evidence link, the same discipline this research lab itself runs (`scripts/verify.py`). MSB v3 is where "show your work, and prove the record wasn't rewritten" gets built as running code rather than stated as a principle.

## Evidence

The project's draft enterprise governance procedure (MSB-ENT-SOP-001) is snapshotted verbatim at [msb-v3-governance-sop.md](msb-v3-governance-sop.md). It is a written procedure, not evidence that its controls operate.

At the pinned commit above, `pytest --collect-only -q` collected **3,942 of 4,018 tests** (76 deselected) — see [C-030](../CLAIMS.md), status verified, checked by re-running the collection command below.

The author's vault project note records the project's own MVP closeout audit on 2026-09-24 as **CLOSED** (MVP scope: system runs, agents run, Gemini works), with each criterion marked VERIFIED against live evidence collected that day (server restart + health check, full test suite 3,799 passed / 0 failed, governance status endpoint, agent registry, a local governed chat reply, a real Gemini Live tool-calling turn, and a Telegram round trip through the Hermes gateway) — see [C-031](../CLAIMS.md), status pending (author-reported in the vault, not independently re-run in this lab).

The author's 2026-08-16 audit (an AI-assisted audit, described in the same vault note as "run-verified, not surface-read") reported 1,272 tests passed / 5 skipped, `mypy src` clean over all 195 files, a CI gate enforcing `--cov-fail-under=70` and `pip-audit --strict`, and zero silent `except: pass` across 188 `except Exception` blocks (87 return, 70 log, 26 re-raise, 9 documented) — see [C-032](../CLAIMS.md), status pending (pending; author-reported, predates this lab and this commit pin, not independently re-run).

## Honest limits

The same 2026-08-16 audit, whose numbers above remain pending ([C-032](../CLAIMS.md)), also named a recurring pattern in the project's own history: it "builds like a senior/staff engineer" (fail-closed defaults, brakes-before-engine, verifiability as a system property) but "finishes like a mid-level one" — new subsystems tend to get opened before the previous one is fully wired, tested under its real gate, and declared done. The vault note tracks this by name as the "build-vs-converge pattern" and records repeated audit cycles closing specific instances of it (governance wiring, stub interfaces, gateway integration) rather than treating it as solved once.

One concrete instance: as of 2026-08-27, the project's `gateway/` package already provided the intended capability-check → auth-check → backend-select → audit mechanism, but had no canonical-path caller — the only caller was `harnesses/base.py`, itself an optional (non-default) harness. That meant the registry and its adapters could exist in the codebase without the runtime being forced to route through them, which the note's own acceptance criterion states directly: a production-path capability invocation should be impossible without passing through the gateway/contract resolution boundary, and at that date it was not. Subsequent vault entries record this as substantially closed later (`ActionGate` established as the enforcement boundary, with the gateway becoming a best-effort audit entry point on `agent/handle.py`) — a self-reported resolution not independently re-checked here.

## Sources

- `README.md` and `README-OUTSIDERS.md`, github.com/lordwilsonDev/msb-v3 @ `5cbe03ef43d924c3c3a3cd1d2dbe730ad5f2c370`
- Vault: `10_Projects/msb-v3/MSB-v3.md` (author's own project log; not reproduced verbatim, summarized for the claims used above)
