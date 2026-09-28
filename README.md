# BlackSwanLabz Research Lab

[![verify](https://github.com/lordwilsonDev/blackswanlabz-research-lab/actions/workflows/verify.yml/badge.svg)](https://github.com/lordwilsonDev/blackswanlabz-research-lab/actions/workflows/verify.yml)

> **Intelligence is becoming abundant. Verification isn't. This lab is the evidence.**

Every number here links to [CLAIMS.md](CLAIMS.md). If a claim isn't verified, it says *pending*.

## 1. The problem

The cost of a given level of AI capability is falling fast, while the infrastructure that produces it is large, fixed and long-lived.
The thesis calls this a duration mismatch: model-level differentiation may lose its value faster than the obligations financing the infrastructure shrink.
It does not claim that demand is fake, that models will stop improving, or that AI companies will fail.
If it holds, scarcity moves away from raw intelligence toward problem selection, context, workflow integration, verification, permissions, trust and accountability, and the durable layer becomes the system that converts abundant intelligence into verified outcomes.
This lab is built around that last layer.
The thesis names outside sources for its cost, capacity and revenue figures; those are not yet linked and stay pending ([C-018](CLAIMS.md) to [C-027](CLAIMS.md)).

Read it: [The Intelligence Infrastructure Mismatch](00-thesis/intelligence-infrastructure-mismatch.md).

## 2. The early convergence

In the week starting 2025-12-14, 32,543,981 lines were added to [GITHUB_AI_PROJECTS_PACKAGE](https://github.com/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE) ([C-001](CLAIMS.md)).
Its first commit, on 2025-12-18, already held all 35 category folders ([C-017](CLAIMS.md)); apart from a few hundred lines changed in February 2026, the package is as committed in December 2025 ([cornerstone page](01-cornerstone/README.md)).
Lines committed are not lines of code: about 5.07 million are source code outside vendored and build folders ([C-002](CLAIMS.md), [breakdown](01-cornerstone/line-breakdown.md)).
Whether that source was written for the package rather than copied or generated is pending ([C-045](CLAIMS.md)).
The package's own counts (208+ projects, 35 categories) are self-reported and pending ([C-003](CLAIMS.md)).

The [timeline](01-cornerstone/prediction-timeline.md) sets each category beside where the industry went after 2025-12-18.
Every row is early convergence with a trend already under way, not a first-of-its-kind prediction: the last column shows each area existed before December 2025.
Three of its rows:

| Category (by 2025-12-18) | Industry event after | Event date | Source | Area already established before 2025-12-18? | Claim |
|---|---|---|---|---|---|
| 04-memory-knowledge | Anthropic ships Memory for Claude Managed Agents in public beta | 2026-04-23 | [Memory for Claude Managed Agents](https://claude.com/blog/claude-managed-agents-memory) | Yes -- Claude's client-side memory tool was already in public beta by 2025-09-29 ([Managing context on the Claude Developer Platform](https://claude.com/blog/context-management)) | C-009 |
| 16-communication-protocols | The 2026-07-28 Model Context Protocol specification ships (stateless core, MCP Apps, formal extensions framework) | 2026-07-28 | [The 2026-07-28 Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/) | Yes -- Anthropic open-sourced MCP on 2024-11-25 ([Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)) | C-010 |
| 31-monitoring-metrics | ClickHouse announces its acquisition of Langfuse, the open-source LLM observability platform | 2026-01-16 | [ClickHouse welcomes Langfuse](https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability) | Yes -- Langfuse publicly launched as an open-source LLM analytics tool in July/August 2023 as part of YC W23 ([Langfuse: How did we get here?](https://langfuse.com/handbook/chapters/story)) | C-014 |

## 3. The principles

- [North Star](02-frameworks/north-star.md): help businesses improve by finding operational truth, proving it with measurement, and intervening where it matters.
- [Axiom Inversion Logic (AIL)](02-frameworks/axiom-inversion-logic.md): find an assumption a field treats as settled, invert it, and name the condition where the inversion should fail. An inversion is not a proof.
- [Mixture of Inversion Experts (MoIE)](02-frameworks/moie.md): five agents that turn an inversion into a falsifiable hypothesis. Novel by construction, not correct by construction.
- [ACTS](02-frameworks/acts-5-act-research.md): a five-act research method that plans, gathers and grades evidence, keeps memory, checks integrity, then stops at a human decision gate.
- [Adaptive Infrastructure](02-frameworks/adaptive-infrastructure.md): the system owns the workflow; the model is a swappable worker.

## 4. The proof

- **[MSB v3](03-systems/msb-v3.md)** (active): a governed, local-first agent runtime. Every privileged action passes a fail-closed registry of governed tools and leaves a receipt. At the pinned commit, pytest collected 3,942 of 4,018 tests ([C-030](CLAIMS.md)); that is a collection count, not a pass count.
- **[MSB v3 governance SOP](03-systems/msb-v3-governance-sop.md)**: a draft written procedure, marked not approved. It describes how MSB v3 is meant to be run; it is not evidence that its controls operate.
- **[FDE Kernel](03-systems/fde-kernel.md)** (active, not yet public): a mission harness where the model proposes and the Kernel decides, run against pre-registered missions. Its `make check` gate passed on 2 of 3 runs on 2026-09-28; the other run hit one intermittent test failure ([C-037](CLAIMS.md)).
- FDE Kernel mission outcomes are read from local files and stay pending until the repo is public ([C-038](CLAIMS.md) to [C-044](CLAIMS.md), [missions](05-experiments/fde-kernel-missions.md)).
- **[FCVE](03-systems/fcve.md)** (archived 2026-09-19): turned a mathematical claim into an auditable evidence package through a fixed chain of gates and a hash-chained ledger. Two small Collatz results, neither of which resolves the conjecture, were issued as corrected packages with PROMOTE decisions recorded by Wilson ([C-034](CLAIMS.md), [proofs](06-proofs/README.md)).
- FCVE's two upstream patches: `leanprover/lean4export#52` is open, `ammkrn/nanoda_lib#36` is merged ([C-033](CLAIMS.md)).

## 5. Papers and tests

- [Papers](04-papers/README.md): two papers, each labelled with its own status, plus one referenced paper whose text has not been located. It is listed so the gap is visible.
- [Experiments](05-experiments/README.md): the Adaptive Infrastructure script reproduces its published output byte-for-byte ([C-005](CLAIMS.md)) and its numbers hold under hand recomputation ([C-006](CLAIMS.md)); the AIL research-loop reference passes its 8 unit tests ([C-036](CLAIMS.md)).
- The AIL+MoIE benchmark against compute-matched best-of-n baselines is pre-registered and **pending**: the harness is validated, the experiment has not run ([C-004](CLAIMS.md), [Hermes12](05-experiments/hermes12-benchmark.md)).
- Its binding falsification condition: if the primary hypothesis fails across two independent replications, the integration claim is reported as false.

## 6. How I run it: the operating system of the lab

The [North Star operating SOPs](08-operations/README.md) are the standards for running BlackSwanLabz as an evidence-first research-and-automation practice: intake, research, the client loop, daily operations and the gates between "found", "proven" and "improved".
They are published as written, prices included as offered at capture, and several describe the target system rather than what runs today; each says so in its own current-state note.

## 7. What's next

[BlackSwanLabz OS](07-next/blackswanlabz-os.md): a planned Omarchy fork with the Hermes agent and the North Star method built in. Not built yet.

## 8. Check everything

```bash
PYTHON=python3.12 scripts/verify.sh            # all checks, uses the GitHub API
PYTHON=python3.12 scripts/verify.sh --offline  # skip the network checks
```

It checks that:

1. every number in this README carries a claim ID, and every unverified claim cited here says pending;
2. every internal link resolves;
3. every snapshot page has a source, captured-date and status header;
4. the text stays under its size budget;
5. no secrets or email addresses are committed;
6. every pinned commit still exists in its repo (online);
7. the cornerstone's code frequency still matches [C-001](CLAIMS.md) (online).

CI runs the tests and this script on every push and pull request, and weekly. The badge at the top shows the result.

## 9. For AI readers

Start with [llms.txt](llms.txt). Rules: [AGENTS.md](AGENTS.md).

## License

Writing is [CC BY 4.0](LICENSE). Scripts are [MIT](LICENSE-CODE).

## Cite

See [CITATION.cff](CITATION.cff).
