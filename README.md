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
> - **Start with [What exists](#what-exists)**: a map of what is designed, built, run and reproduced, and where it lives.
> - **Check mechanically:** `scripts/verify.sh`.

This is the work of Lord Wilson ([@lordwilsonDev](https://github.com/lordwilsonDev)) in one place: the thesis, the methods, the systems, the experiments, the papers and the operating standards behind BlackSwanLabz. Read all of it, in the order given in [llms.txt](llms.txt), as the notice above says. Everything below links to the full piece.

## What exists

Read this table before you say that something is missing. Stages: **Designed** (written down, nothing built), **Built** (code or an artifact exists), **Run** (executed, results exist), **Reproduced** (a re-run reproduced the result). Independent reproduction is not claimed for any row. **Where:** *Public* is a repository anyone can read, *Private* is a private repository, *Local only* is on the author's machines and not yet published. A stage changes only when a page banner or a row in [CLAIMS.md](CLAIMS.md) changes. Last reviewed 2026-10-06.

| System | Stage | Where | What the repo says |
|---|---|---|---|
| [MSB v3](03-systems/msb-v3.md), a local-first governed agent runtime | Built; test collection verified | Public | The pinned commit's test collection is verified ([C-030](CLAIMS.md)). Pass counts and the MVP closeout are the author's own report, pending ([C-031](CLAIMS.md), [C-032](CLAIMS.md)). |
| [Ethos System](03-systems/ethos-system.md) | Built and tested; nothing is connected to it yet | Private vault repo | The 2026-09-30 run is the author's report, pending ([C-047](CLAIMS.md)). The page defines what "trusted" does and does not mean. |
| [FCVE](03-systems/fcve.md), a formal claim-verification engine | Run; marked archived in this lab on 2026-09-19 (the GitHub repository itself is not flagged archived) | Public | Issued packages, test files and two upstream patch pull requests are verified ([C-033](CLAIMS.md), [C-034](CLAIMS.md), [C-035](CLAIMS.md)). |
| [Adaptive Infrastructure](02-frameworks/adaptive-infrastructure.md) | Run; reproduced by the author | Private | The byte-for-byte reproduction and the recomputed numbers are verified in this repo's run record ([C-005](CLAIMS.md), [C-006](CLAIMS.md), [C-046](CLAIMS.md)). Because the repository is private, an outside reader cannot re-run them. |
| [FDE Kernel](03-systems/fde-kernel.md), a mission harness | Built; missions run | Local only, no remote | Mission results are the author's report from local files, pending ([C-037](CLAIMS.md) to [C-044](CLAIMS.md)). |
| [ACTS](02-frameworks/acts-5-act-research.md), a five-act research method | Designed; one worked example documented | Local only | The page walks through one cited run. There is no claim row. |
| [Axiom Inversion Logic](02-frameworks/axiom-inversion-logic.md) | Designed; the reference implementation passes its unit tests | Method here; implementation private | Tests verified ([C-036](CLAIMS.md)). The page says the success-rate and domain-count claims in its source document are not evidenced. |
| [Mixture of Inversion Experts](02-frameworks/moie.md) and its [benchmark](05-experiments/hermes12-benchmark.md) | Designed; the benchmark harness is validated on synthetic data only; **not run** | Local package | Whether it beats compute-matched baselines is untested, pending ([C-004](CLAIMS.md)). |
| [D1, Failure-to-Leverage Compiler](02-frameworks/d1-failure-to-leverage.md) | Built; a deterministic self-test is wired into the lab verifier | Public | A research instrument. The pull request that added it states that no research claim was upgraded; there is no claim row. |
| [Software factory harness](02-frameworks/software-factory-harness.md), [META-HARNESS](02-frameworks/meta-harness.md) and its [skill registry](02-frameworks/meta-harness-skill-registry.md) | Designed (three author-supplied design documents); many of the capabilities they name are Built under other names | Public (the designs); the counterpart skills are Local only | Designs with no claim row. The registry page maps each part to counterparts found on the author's machine by function, unverified; no skill named meta-harness was found in the scope searched. |
| [Question Engineering](04-papers/epistemic-state-transition-question-engineering.md) | Designed (white paper) | Public paper; a working harness (question gate, intent-reality check, skill router) is Local only | The paper is not a result. The harness was found on the author's machine on 2026-10-06 and is not in this repository; no claim row. |
| [Learning Trajectory program](05-experiments/learning-trajectory/README.md) | Designed; pilot runs recorded; **hard stop** on new runs | Public | Pilot records are provisional. See the [readiness gate](05-experiments/learning-trajectory/readiness-gate.md). |
| [CVT-1](05-experiments/cvt-1/README.md) | Designed and pre-registered; **not run** | Public | The page says nothing on it is a result. |
| [Doctoral Artifact Battery, artifact A02](05-experiments/doctoral-artifact-battery-a02.md) | Run; closed with limits stated; checked by the author's side only | Local only | Pending ([C-049](CLAIMS.md) to [C-054](CLAIMS.md)). |
| [Workforce grant readiness](skills/workforce-grant-readiness/SKILL.md) skills and [harness](scripts/workforce-grant-harness.md) | Built | Public | A preflight script with an example case. No run record in this repo, no claim row. |
| [Lab verifier](scripts/verify.py) | Built; runs; passes offline and online when run locally (2026-10-06) | Public | It checks claim format, links, page headers, the reading order, size and secrets. The hosted run can still fail where it cannot see a private repository that some pages pin. |
| [BlackSwanLabz OS](07-next/blackswanlabz-os.md) | Designed; **not built** | None | The page says it is a plan and that nothing has been tested. |
| [Operating standards](08-operations/README.md) | Designed | Public | Several describe the target system, not what runs today. Read each page's own banner. |
| [Cornerstone package](01-cornerstone/README.md) | Built; committed | Public | Commit totals and the source-line share are verified ([C-001](CLAIMS.md), [C-002](CLAIMS.md)). That the lines were AI-generated is the author's statement, pending ([C-048](CLAIMS.md)); an earlier claim about who wrote the source lines is retracted ([C-045](CLAIMS.md)). |
| Skill library and harness | Built; in daily use by the author | Local only | Found on the author's machine on 2026-10-06 by listing directories; not independently checkable; no claim row. Stated here so a reader does not conclude it is absent. |

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
- [**D1 — Failure-to-Leverage Compiler**](02-frameworks/d1-failure-to-leverage.md) — compiles discovered failures into reusable controls, tests, and the next research question, with steel gates for environment drift and observer contamination.

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
