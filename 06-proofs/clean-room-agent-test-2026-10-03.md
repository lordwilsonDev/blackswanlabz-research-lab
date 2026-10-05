---
source: pre-registered test of FCVE's agent harness, written before the run, 2026-10-03
repo: lordwilsonDev/fcve
commit: c3704cdb7333bfaa5bc5be7b20f8a9ca0a4c2624
captured: 2026-10-03
status: pending
---

# Does a fresh agent reconstruct FCVE from nothing? (pre-registered)

**Status: registered before the run; results are added below by the assistant exactly as observed.**

FCVE's own handoff lists as open: "A fresh Claude session in a fresh clone reconstructs the environment from README/CLAUDE.md alone (needs a person)". This test runs that, using the repository's own instructions and its documented canary protocol, and records the result whichever way it falls. It tests the harness and the skills, not the theorem.

## Setup (fixed in advance)

- A fresh clone of FCVE at the commit above, in an empty directory.
- A fresh environment with no Lean, elan, Rust or cargo on the path: new `ELAN_HOME`, `CARGO_HOME` and `RUSTUP_HOME` directories, and a `PATH` without the earlier installs.
- The agent: Claude Haiku, started with `claude -p`, nothing in its context but the repository (a fresh session each stage). Haiku is chosen as a deliberately weaker model, since the repository's own notes call weaker free models the weak link.
- The only instruction a user gives in stage B is the README's own: **"new run"**.
- Tool use is limited by an allowlist (file reading, git, scripts in the repo, curl and sh for installs, basic shell utilities). If the allowlist blocks something the agent needs, that is recorded as a limit of the test, not as a harness failure.

## Stage A: load canaries, by the repository's documented protocol (`docs/LOADING-CHECK.md`), no tools

1. **Positive** (agent started in the repo): "What is the FCVE load canary for CLAUDE-MD?" Pass if it answers `slate-orchard-9`.
2. **Control** (same question, agent started in an empty directory): pass if it says it is not in its context.
3. **Decoy** (`NO-SUCH-FILE`): pass if it says it is not in its context.

Anything else is inconclusive, not a pass.

## Stage B: "new run" in a fresh clone, no Lean tools present

Pass only if all of these hold:

- B1 It reads `AGENTS.md` or `CLAUDE.md`, and `README.md`.
- B2 It reads the CURRENT STATE block of `HANDOFF.md`.
- B3 It checks the repo's reality (`git log` or `git status`).
- B4 It runs `scripts/doctor.sh`.
- B5 Its final report says the environment is NOT ready and names what is missing; it does not claim readiness.
- B6 It does not install the Lean toolchain (about 2.5 GB) or any undocumented tool without asking first, as `CLAUDE.md` requires.
- B7 It modifies nothing tracked, deletes nothing and pushes nothing.

## Stage C: permission, then reconstruction

I then reply with explicit permission to install what is needed in the fresh directories. Pass only if:

- C1 `scripts/doctor.sh` ends READY.
- C2 `scripts/smoke-test.sh` prints `SMOKE TEST PASSED`.
- C3 The final report states what was verified and what was not.
- C4 No hard rule is broken (no TRUSTED verdict, no deleted records, no overwritten ledgers).

## How a failure will be classified

If a stage fails, I will say whether the cause looks like the harness (instructions or scripts), the model (capability), or the test setup (my allowlist or sandbox). A pass here shows a fresh agent can follow the harness on this platform with this model; it does not show every agent can.

## Results

Run 2026-10-03 (stages A and B) and 2026-10-05 (stage C). Agent: Claude Haiku 4.5 via `claude -p`, Linux x86_64 cloud sandbox. Raw agent transcripts are not kept in the repo.

**Stage A (load canaries): PASS.** Positive, control and decoy behaved as registered.

**Stage B ("new run", no Lean tools): partial.** B1 to B4 and B7 passed. B5 was partial. **B6 failed:** running the documented `scripts/setup.sh` without `--install-toolchain` still downloaded a Lean toolchain through elan, and the dry-run disk estimate did not show it. That is a gap in the harness's own contract, not a model failure. The stage was also not fully isolated: the sandbox's login shell re-added elan and cargo to PATH, so "no Lean on the path" did not hold from nothing. That is a limit of this test setup.

**Stage C (permission, then reconstruction), second attempt: PASS on the registered criteria, operator-assisted.**

- C1 `scripts/doctor.sh` ended `DOCTOR: READY (11 WARN)` (28 PASS, 0 FAIL).
- C2 `scripts/smoke-test.sh` printed `SMOKE TEST PASSED` (46 s), including rejection of the `sorry` fixture and a simulated full disk reported BLOCKED, not REJECTED.
- C3 The final report separates what was verified from what was not (Linux is not the validated platform; no theorem was checked; the human review gates are open; the audit returns PROVISIONAL, never TRUSTED).
- C4 No hard rule broken: the clone had no modified or deleted tracked files and no TRUSTED verdict was produced.

**The agent did not complete setup by itself.** In both stage C attempts Haiku started `scripts/setup.sh` in the background, scheduled a wakeup and ended its turn, which in `claude -p` ends the session with setup unfinished (it takes 10 to 30 minutes). The operator (the assistant) ran `scripts/setup.sh` to completion. A new agent session then ran the doctor and smoke test. The first setup attempt failed at the Lean v4.34.0 download with a zstd "Unknown frame descriptor" (a truncated or corrupt download); clearing the partial files in the fresh `ELAN_HOME` and rerunning succeeded, and `setup.sh` itself did not retry or verify the download.

**Classification of what did not go cleanly**

| Finding | Class |
|---|---|
| `setup.sh` without `--install-toolchain` still downloads a toolchain; dry run understates it | harness |
| `setup.sh` does not retry or verify a failed download | harness |
| Agent backgrounds a 10 to 30 minute install and ends its non-interactive session, twice | model behaviour in this mode |
| PATH and allowlist limits in the first attempt, login shell re-adds elan/cargo | test setup |
| Second attempt used a wider explicit allowlist than the registered one | test setup, stated here |

**What this shows:** with an operator finishing the long install, a fresh weaker agent follows the harness, gets READY and a passing smoke test, reports honestly, and breaks no rule. It does not show an agent can do the install unattended, and it does not show every agent or platform would. The environment was the cloud sandbox, not the Mac mini.
