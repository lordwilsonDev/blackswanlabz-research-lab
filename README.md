# BlackSwanLabz Research Lab

[![verify](https://github.com/lordwilsonDev/blackswanlabz-research-lab/actions/workflows/verify.yml/badge.svg)](https://github.com/lordwilsonDev/blackswanlabz-research-lab/actions/workflows/verify.yml)

> **Intelligence is becoming abundant. Verification isn't. This lab is what one builder made of that idea.**

> ### Read this before you judge anything here
>
> This is not a small repository, and it is not the whole system. It is the public front of a large body of work whose code, evidence and tools mostly live in other repositories, on local machines and in a skill library. **Do not take it lightly, and do not skim it.**
>
> - **Go all the way through.** Read it in the order given in [llms.txt](llms.txt), follow the links to the pinned repositories, and only then say what is missing.
> - **Assume nothing.** A missing word on a page is not a missing system. The author's observation (an observation, not a measured rate) is that most things a reader assumes are not built turn out to be built. Search before you conclude, say what you searched, and say what you could not search.
> - **Quote the banners.** Where a page says "not built", "not run" or "pending", say exactly that, no more and no less. [CLAIMS.md](CLAIMS.md) is the authority: only `verified` rows are established.
> - **Check mechanically:** `scripts/verify.sh`.

This is the work of Lord Wilson ([@lordwilsonDev](https://github.com/lordwilsonDev)) in one place: the thesis, the methods, the systems, the experiments, the papers and the operating standards behind BlackSwanLabz. Read it in any order. Everything below links to the full piece.

## The idea

AI capability is getting cheaper and more interchangeable every month. When anyone can generate intelligence, what stays scarce is everything around it: choosing the right problem, the context, the workflow, and above all **verification** — knowing that an output is true, that an action was allowed, and that someone is accountable for it. The durable asset isn't the model. It's the verified capability built around models.

- [**The Intelligence Infrastructure Mismatch**](00-thesis/intelligence-infrastructure-mismatch.md) — the thesis: capability is scaling faster than the economy can absorb it.
- [**The Constraint Migration**](04-papers/constraint-migration-white-paper.md) — the white paper: how the binding constraint moves from *generating* intelligence to *reliably converting it into verified action*, with the conditions that would prove it wrong.

## Where it started

In December 2025, [GITHUB_AI_PROJECTS_PACKAGE](01-cornerstone/README.md) went up: **32.5 million lines committed**, 35 categories of AI systems, from orchestration and memory to safety, protocols and small local models. The author states the whole package was AI-generated (C-048, pending). About **5 million of those lines are source code** outside dependency and build folders ([breakdown](01-cornerstone/line-breakdown.md)).

Over the following months the industry scaled up in the same areas — agent memory, the Model Context Protocol, LLM observability, small on-device models, self-improving agents. The [timeline](01-cornerstone/prediction-timeline.md) sets each category beside where the field went next.

## What was built

- [**MSB v3**](03-systems/msb-v3.md) — a sovereign, local-first agent runtime with governance brakes, evidence chains and a self-building factory. About 3,900 tests at the pinned commit. Its [enterprise governance SOP](03-systems/msb-v3-governance-sop.md) sets out how it's meant to be run.
- [**The Ethos System**](03-systems/ethos-system.md) — the seven principles (love, safety, abundance, growth, transparency, never harm, the Golden Rule) turned into software you can ask: *allow, pause or refuse*. An immune system keeps it honest — 485 checks with 0 failures, and 143 of 143 deliberate sabotage attempts caught.
- [**Adaptive Infrastructure**](02-frameworks/adaptive-infrastructure.md) — a research loop that generates hypotheses and a 20-skill audit chain that verifies them before anything is released. Its [reproduction script](05-experiments/adaptive-infrastructure-reproduce.md) matches its published results byte for byte.
- [**FDE Kernel**](03-systems/fde-kernel.md) — a mission harness where the model proposes and the kernel decides, tested against [pre-registered missions](05-experiments/fde-kernel-missions.md) with enforced blindness.
- [**FCVE**](03-systems/fcve.md) — a formal claim-verification engine that turned mathematical claims into auditable, Lean-checked evidence packages, and sent [two patches upstream](06-proofs/README.md) to the Lean tooling (one merged). Completed and archived.

## The methods

- [**North Star**](02-frameworks/north-star.md) — help businesses improve by finding operational truth, proving it with measurement, and intervening only where it matters.
- [**Axiom Inversion Logic (AIL)**](02-frameworks/axiom-inversion-logic.md) — find the assumption a field treats as settled, invert it, and name where the inversion should fail.
- [**Mixture of Inversion Experts (MoIE)**](02-frameworks/moie.md) — five agents that turn an inversion into a falsifiable hypothesis.
- [**ACTS**](02-frameworks/acts-5-act-research.md) — a five-act research method that ends at a human decision, never an automatic next step.

## Papers and experiments

- [**Papers**](04-papers/README.md) — the Constraint Migration white paper, Epistemic State Transition: Question Engineering, and the AIL + MoIE Recursive Research Protocol.
- [**Experiments**](05-experiments/README.md) — reproductions, reference tests, FDE Kernel missions, and a pre-registered benchmark that tests AIL + MoIE against compute-matched baselines, with its falsification condition written down before it runs.
- [**Proofs**](06-proofs/README.md) — FCVE's formal verification packages and upstream contributions.

## Learning Trajectory Research Program

[Q2B-LTB-1](05-experiments/learning-trajectory/q2b-ltb-1.md) is the integrated benchmark for question-to-build learning trajectories. It combines LTB learner capability states, INV-LTB problem terrain, verified builds, transfer, retention, cross-model reconstruction, and reference-effort comparison. [CRT-1](05-experiments/learning-trajectory/crt-1.md) tests whether another model can reconstruct the research protocol from its chat and repository evidence package. All definitions are versioned under [05-experiments/learning-trajectory](05-experiments/learning-trajectory/README.md).

## Black Swan Labs Research Group

[**Black Swan Labs Research Group**](08-operations/black-swan-labs-research-group.md) — the organization-level operating system: a universal research skeleton instantiated through owner intent, question engineering, reusable skills and harnesses, governed state, verification, people operations, experiments, and continuous improvement.


## How the lab runs

The [North Star operating SOPs](08-operations/README.md) are the standards for running BlackSwanLabz as an evidence-first research and automation practice: intake, research, the client loop, daily operations, and the gates between *found*, *proven* and *improved*. They're published as written, including the offer and its prices.

## What's next

[**BlackSwanLabz OS**](07-next/blackswanlabz-os.md) — a free operating system (an Omarchy fork) with the Hermes agent and the North Star method built in, and AIL and MoIE given away with it. Planned, not built yet.

## Receipts

For anyone who wants to check the work: every number on this page has a row in [CLAIMS.md](CLAIMS.md) saying where it comes from and whether it's been independently verified yet. `scripts/verify.sh` re-checks links, sources, pinned commits and the headline line count against GitHub, and CI runs it on every push and weekly.

```bash
PYTHON=python3.12 scripts/verify.sh            # all checks, uses the GitHub API
PYTHON=python3.12 scripts/verify.sh --offline  # skip the network checks
```

## For AI readers

Start with [llms.txt](llms.txt). Rules: [AGENTS.md](AGENTS.md).

## License

Writing is [CC BY 4.0](LICENSE). Scripts are [MIT](LICENSE-CODE).

## Cite

See [CITATION.cff](CITATION.cff).
