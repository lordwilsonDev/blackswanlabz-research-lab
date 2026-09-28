---
source: ~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/index.md
vault-date: 2026-08-25
captured: 2026-09-28
status: active
---

# ACTS — the 5-Act research method

AIL ACT (also called ACTS in this repo, for its five Acts) is the outer operating shell for running a research investigation as a continuous, stateful process rather than a sequence of disconnected answers: five sequential acts, each producing a structured handoff to the next, never silently resetting between acts.

| Act | Title | What it does |
|---|---|---|
| I | Knowledge Acquisition Planning / Research Mission | Decides what knowledge must be acquired, from where, at what depth. Produces a Research Acquisition Blueprint. |
| II | Intelligence Collection & Evidence Characterization | Gates evidence before it reaches the hypothesis generator. Forces Evidence Objects, separates observation/finding/claim/hypothesis, assigns per-claim evidence states. |
| III | Research Memory & Forward Progress | Persistent state across research cycles: ledgers, hypothesis versioning, redundancy detection, next-run continuity. |
| IV | Research Ontology, Integrity, Error Handling & Recovery | Validates the whole object graph for integrity — identity, provenance, duplication, contradictions, errors, recovery, whether the state is safe to advance. |
| V | Research Decision & Human Intent Gate | Reconstructs the cycle for a human, separates "evidence supports X" from "therefore do Y," and stops to ask what happens next. Never auto-launches another cycle. |

## Worked example: AIL-AI-SMB-001

The apparatus has one complete, evidence-cited run, on the question: **"Under what conditions does generative AI adoption create measurable net value for small businesses, and does workflow redesign outperform tool access alone?"**

- **Act I** produced the research mission: the question, an initial consensus model ("AI tools improve productivity, so access should create value"), five candidate inversions, and four competing hypotheses — from H1 ("access sufficiency": tool access is enough) through H4 ("adoption lag": local gains can coexist with flat firm-level productivity during implementation).
- **Act II** collected and characterized four evidence objects — including a randomized task-level experiment, a survey-based analysis, a field study, and transaction-based adoption research — each tagged with what it does and does not support, and its limitations.
- **Act III** converted Acts I–II into persistent state: an evidence ledger, hypothesis-version history, and a ranked research frontier.
- **Act IV** validated the resulting object graph, recorded integrity warnings, and defined the cycle's discriminating falsification test, **FT-001**.
- **Act V** reconstructed the cycle, classified what was learned (established / plausible / contested / rejected), and stopped at the human decision gate rather than continuing on its own.

**FT-001 — defined, not completed.** The test compares comparable small-business workflow units under three conditions: (1) control / normal workflow; (2) AI tool access without formal workflow redesign; (3) AI tool access plus explicit workflow redesign, human review, KPI measurement, and task boundaries. Its stated falsifying or weakening result: "Condition 2 performs as well as or better than Condition 3 across multiple workflows, or workflow redesign adds cost without improving net outcomes." As of the worked example, this test is specified but was not run.

The run's own conclusion at Act V: the leading hypothesis moved from H1 to H2 ("integration condition" — durable value depends on task fit, workflow integration, human review, incentives, and measurement, not tool access alone), but the evidence for the exact integration mechanism is explicitly labeled indirect, and the source's own self-assessment notes the run "demonstrates the method's shape and discipline; it does not demonstrate that the method produced a true result rather than an interesting, well-supported hypothesis."

## Human decision gate

Act V is a hard stop, not a summary. It presents established/plausible/contested/rejected findings, what changed since the last cycle, the active hypothesis's vulnerabilities and falsification condition, the current research frontier, and a list of available next paths (continue research, challenge the conclusion, explore a competing hypothesis, design a test, apply the knowledge, archive, or a user-defined direction) — then ends by asking the user directly:

> **"Now that we have these findings, what would you like to do with the information?"**

The operating skill is explicit that the system may recommend a path but "the final selection belongs to the user," and that it must "not automatically perform the selected next action until the user chooses it."

## Sources

- `~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/index.md`
- `~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/raw-source/ail-act-research-SKILL.md`
- `~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/raw-source/worked-example-Act-I.md`
- `~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/raw-source/worked-example-Act-II.md`
- `~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/raw-source/worked-example-Act-III.md`
- `~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/raw-source/worked-example-Act-IV.md`
- `~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/raw-source/worked-example-Act-V.md`
