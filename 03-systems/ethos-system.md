---
source: vault:30_Architecture/Ethos-System-Map.md and vault:80_Tools/verify/ (private vault repo, commit bf1d6a3)
vault-date: 2026-09-29
captured: 2026-09-29
status: active
---

# The Ethos System

**A conscience you can ask, and an immune system that keeps it honest.**

Most "AI ethics" lives in a policy document. The Ethos System turns the seven principles this whole body of work is built on — love, safety, abundance, growth, transparency, never harm, and the Golden Rule — into software that can be asked about any action and answers *allow*, *pause* or *refuse*, with a reason for every principle.

## The three parts

| Part | What it does |
|---|---|
| **The Conscience** | Judges an action against the seven principles. A concern must cite evidence, and **missing evidence is a concern, never "ok".** It runs a loop: understand → question → check → act → verify → explain → learn. |
| **The Front Door** | One plain form anyone can fill in — a person, a script, or an agent in any language. It answers with a decision, a reason per principle, and exactly what's missing. **Blank means pause.** |
| **The Immune System** | Proves the conscience hasn't been altered, fooled or made to overclaim: sealed files, a live watcher, a signed decision ledger, deliberate sabotage tests, and a review gate that won't close while a defect is open. |

## How the immune system works

- **The seal.** 51 important files — including the tests themselves — are fingerprinted and signed with a key kept outside the folder. If any one changes by a single character, the system refuses to run rather than report a result you might act on.
- **The watcher.** Records changes to those files as they happen.
- **Earned trust.** It starts at *"I don't know"* and has to earn *"trusted — detection only"* by producing evidence during the run. If a piece is missing, it refuses and names what's missing.
- **The ledger.** A signed, tamper-evident diary of every consequential act.
- **Sabotage tests.** The system is deliberately broken 143 different ways — including quiet breaks like silencing an alarm while the code still looks right — to prove its own alarms go off.

## Latest results

From the generated [executive summary](ethos-executive-summary.md) of the run on 2026-09-30 (UTC):

- **485 automated checks, 0 failures**, across 17 suites.
- **143 of 143 deliberate sabotage attempts caught.**
- **The seal is valid across all 51 protected files.**
- **78 of 78** checks on the front door judging actions by the seven principles.

It rates itself **"trusted — detection only"**, and it says exactly what that means: this Mac can *detect* tampering, not *prevent* it. Six ways of preventing changes were actually tried and measured; the one that can't be undone by the same user needs administrator rights. The summary lists every gap the system can't yet prove, instead of hiding them.

## Where it stands

The door is built and tested. Nothing is connected to it yet — the next steps are hooking up an agent (such as Hermes), a client automation, or a web form, and adding an AI reviewer that may only *add* concerns, never remove them. The code lives in a private repository for now.

## Read more

- [Executive summary](ethos-executive-summary.md) — the full plain-language report, generated from the test run.
- The seven principles come from the workspace constitution that governs all of this work.
