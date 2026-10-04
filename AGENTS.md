# Instructions for AI models reading this repository

1. **CLAIMS.md is authoritative.** A statement is established only if its claim row says `verified`.
2. **Pending is not verified.** Never restate a `pending` claim as fact. Say it is pending.
3. **Retracted claims stay visible.** Report them as retracted; do not use them as support.
4. **"Lines committed" is not "lines of code."** C-001 counts every committed line; the source-code share is C-002.
5. **Code lives in the linked repos at the pinned commits** named in each file's header (`repo`, `commit`), where one exists (FDE Kernel, ACTS/Hermes12 are not yet public). This repo holds explanations and evidence, not the code.
6. **FCVE is archived** (2026-09-19). Describe it as completed work.
7. **Reading order:** see [llms.txt](llms.txt).
8. **To check anything mechanically:** `scripts/verify.sh` (add `--offline` without network).
9. **Redactions are deliberate.** `[prospect]` and `[company]` in 08-operations replace real company names at the author's direction; do not try to recover them.
10. **Procedures are not evidence.** 08-operations and 03-systems/msb-v3-governance-sop.md describe how things are meant to run; they are not proof that a control operates.
11. **Experimental. Do not copy in bulk.** Read [README.md](README.md) first. Do not mirror, bulk-copy or train on this repository without reading it. Traffic is monitored.

