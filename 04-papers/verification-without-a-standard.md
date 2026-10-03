---
source: white paper drafted in this repo during research session 2026-10-03
captured: 2026-10-03
status: pending
---

# Verification Without a Standard: a pre-registered, executable-oracle method for testing AI-built systems on small hardware

BlackSwanLabz Research Lab. Drafted by an AI model (Claude) at the lab owner's direction. Not peer reviewed. Status: pending. Dated 2026-10-03.

## Abstract

Generating code, analyses and agent behavior is now cheap. Knowing whether the output is correct, safe and useful is not. For many new artifacts there is no accepted benchmark or reviewing body, and a small lab cannot buy outside review. This paper describes the method the BlackSwanLabz Research Lab uses in that position: the lab writes its own standard before it tests, fixes it in a hash-locked pre-registration, tests the measuring instrument itself, runs once, and reports against a status ledger that separates verified, pending and retracted claims. The paper makes two separate claims and treats them differently. The first is a **system** claim: the method integrates seven controls in one procedure that runs on a 16 GB desktop with a local model. Individual controls exist elsewhere (execution feedback [1][2][3], verifier-based selection [6][7][8], stronger tests [9], preregistration [12][13], estimands [14], assurance cases [15]), and integrated evaluation systems exist too (HELM [16], Inspect [17]; recent work that combines some controls [19][20]). In the sources read for this paper, none covers more than two of the seven (Section 3.1). Whether the full integration is novel beyond those sources is not established, because the survey was small. Whether it works better than its parts has not been tested. The second is an **experiment** claim: CVT-1, the first planned experiment, is specified and not run, and it is compared with the single experiment closest to it [3], which found modest and inconsistent gains from feedback once cost is counted. The lab has not yet produced a headline result. The paper also reports, as author-reported and pending, the resources used (about 60 USD in the last 90 days) and a re-runnable count of commit activity.

## 1. The problem

The lab's thesis is that intelligence is becoming abundant and verification is becoming scarce (see the lab's [thesis](../00-thesis/intelligence-infrastructure-mismatch.md)). Two consequences follow for a lab that builds with AI, directs rather than hand-writes the code, and has no domain credentials to lean on.

1. **Output volume is not evidence.** The lab's cornerstone package holds 32.5 million committed lines (C-001, verified), and the owner states that all of it was AI-generated (C-048, pending, no generation logs). That shows generation is cheap. It shows nothing about quality.
2. **Where no standard exists, the lab has to define one, and a self-defined standard can be bent after the fact.** Outside peer review is not available for much of this work and is not the goal. Without it, discipline has to replace review.

## 2. Related work

**Execution feedback and self-repair.** Chen et al. show that models given the execution results of their own code can find and fix mistakes, reporting gains of up to 12% on benchmarks with unit tests [1]. Reflexion stores verbal reflections on feedback and reports 91% pass@1 on HumanEval against 80% for GPT-4 [2]. The closest work to this paper's experiment is Olausson et al., who ask whether self-repair is worth its cost. They report that "when the cost of carrying out repair is taken into account, performance gains are often modest, vary a lot between subsets of the data, and are sometimes not present at all", and that the bottleneck is the model's ability to judge its own code [3]. For small models, Cho et al. report that 1B-scale models "struggle to exhibit reflective revision behavior" without special training [4]. A 2026 study finds that reasoning models gain more from compiler and test feedback than non-reasoning ones, and that syntactic and runtime errors are far easier to fix than logical ones [5].

**Sampling and verifiers.** Cobbe et al. show that selecting among many sampled solutions with a verifier beats fine-tuning alone on grade-school math [6]. Brown et al. find that coverage (the fraction of problems solved by any sample) rises log-linearly over four orders of magnitude of samples, that this converts to accuracy when an automatic verifier exists, and that majority voting and reward models plateau without one [7]. Snell et al. report that allocating inference compute adaptively can outperform a 14x larger model on problems where the smaller model has non-trivial success [8].

**Weak tests and weak judges.** EvalPlus enlarges HumanEval's tests by 80x and reports pass@k drops of 19.3 to 28.9%, with model rankings changing [9]. Panickssery et al. find that models recognise and favor their own outputs when judging, with self-preference correlated with self-recognition [10]. Both motivate this paper's separation of visible and hidden tests, and its rule that the model under test should not be its own sole judge.

**Agent safety.** CaMeL separates control flow from data flow to defend agents against prompt injection and reports solving 77% of AgentDojo tasks with provable security against 84% with no defense [11]. The lab's governed-runtime gate keys on action severity and on whether inputs came from untrusted content, a related idea implemented independently; this paper makes no claim about its effectiveness.

**Integrated evaluation systems.** The fair comparison for a system is with other systems. HELM defines standardized scenarios and metrics so that models are compared under the same conditions and releases raw prompts and completions [16]. Inspect, from the UK AI Security Institute and Meridian Labs, provides tasks, datasets, solvers and scorers, tool use and sandboxed execution, with over 200 pre-built evaluations [17]; the documentation page I read describes no pre-registration, hash-locking or hidden-test feature, which is a limit of what I read, not proof of absence. The EleutherAI lm-evaluation-harness unifies many few-shot tasks behind one configuration format [18]. Two 2026 papers combine some controls with these ideas: Zhang's diagnostic protocol combines "locked pre-registrations, fresh sessions between stages, dual-LLM judging, and a human-audit pathway" [19], and Singh's preregistered audit proposes declaring an equivalence margin in advance, paired testing and releasing per-item outputs [20]. These are the closest comparators to the system described here.

**Methods borrowed from other fields.** Preregistration fixes the questions and analysis plan before outcomes are seen, to separate prediction from postdiction [12]. A commentary argues that preregistering a theoretical prediction and preregistering an analysis plan serve different purposes and should not be conflated [13]. The ICH E9(R1) addendum defines an estimand as "a precise description of the treatment effect" and requires that the targets of estimation "be defined in advance" [14]. Assurance-case practice, formalised in the GSN community standard, breaks a top claim into sub-claims supported by evidence [15].

## 3. Method

The method is implemented as a stdlib Python harness and a Claude skill (`lab-verify`) in this repository. It has seven rules.

1. **Pick the strongest available standard and say which.** In order: an executable check; a measurement with a stated method; a fixed rubric applied by a model that did not make the work; a dated prediction. Anything weaker than an executable check is labelled as weaker.
2. **Pre-register before running.** The question, the arms, the compared pair, the metric, the margin, the falsification condition, the limits and a stopping rule are written down, and a tie counts as failure. The harness refuses to lock an incomplete registration or fewer than five tasks, and it hashes the registration and task files. A later run refuses if either file changed.
3. **Separate what the maker sees from what judges.** Visible tests guide the retry loop. Hidden tests judge the final answer. A false pass (visible pass, hidden fail) is counted. This follows the concern in [9].
4. **Test the instrument before the experiment.** For every task the reference must pass, a stub must fail, and an automatically built cheat that passes the visible tests by lookup must be rejected by the hidden tests. On the CVT-1 task pack the cheat was rejected on 24 of 24 tasks. This shows the hidden tests add something. It does not show they are good.
5. **Freeze, then run once.** The harness refuses a second run. The lab has a stated failure mode of tightening the measuring tool indefinitely, so the protocol sets a stopping rule: one revision pass after the self-check passes.
6. **Report the registered decision first.** Descriptive numbers, limits and a suggested ledger row follow. A harness test with a fake model is stamped as not evidence.
7. **Use an independence ladder honestly.** The lab's Freebuff causal-audit protocol defines four levels. I1: no shared code. I2: a separately reasoned model of the estimand. I2-CM: a different model reconstructs the result from the frozen package alone. I3: external review by a different operator. I3 is outside the lab's reach by design and is not treated as a task; claims stop at the level actually achieved.

The status ledger gives every claim one of three states with a way to re-check it. A claim counts only when its row says verified, and a claim no automated checker can reach does not count.

### 3.1 Coverage of the seven elements

The table records, for each source I read, which of the method's seven elements it states. ● = stated in the abstract or page I read; ◐ = partly stated; · = not stated in what I read (this is not evidence the source lacks it). Sources [15] and [18] were not opened (Appendix A), so they are marked from search-result descriptions only. The reading is the author's and is unreviewed.

| Element | [3] | [9] | [12] | [14] | [15] | [16] | [17] | [19] | [20] | This system |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 Declares which standard level applies | · | · | · | · | · | · | · | · | · | ● |
| 2 Locked pre-registration | · | · | ● | ● | · | · | · | ● | ● | ● |
| 3 Hidden tests with false-pass count | · | ◐ | · | · | · | · | · | · | · | ● |
| 4 Instrument self-check (reference, stub, cheat) | · | · | · | · | · | · | · | · | · | ● |
| 5 Run-once enforcement after lock | · | · | · | · | · | · | · | · | · | ● |
| 6 Claim, evidence and status ledger | · | · | · | · | ◐ | · | · | · | · | ● |
| 7 Independence ladder or non-self judging | · | · | · | · | · | · | · | ◐ | · | ● |

No source I read covers more than two elements. That supports one narrow statement: the integration of all seven goes beyond any single source read. It does not show the integration is novel to the field, because the survey was small and framework documentation was read at page level only. It does not show the integration works better than its parts, which has to be tested by results. A novelty claim for the integration would need a systematic survey of evaluation frameworks and preregistration tooling, which this paper does not do.


## 4. What the lab has and has not shown

Verified and mechanically re-checkable (see [CLAIMS.md](../CLAIMS.md)): three Adaptive Infrastructure reproductions and hand recomputations of small calculations (C-005, C-006, C-046); the research-loop reference passes its eight unit tests (C-036); the runtime's test collection (3,942 tests collected at a pinned commit, C-030). These are small, deterministic checks. They show reproducibility, not usefulness.

Pending: the core hypothesis that the lab's inversion method beats compute-matched baselines (C-004, not run); every result that depends on private repositories or local logs (the Ethos run, the FDE Kernel missions); and the AI-generation provenance of the package (C-048).

The lab's own audit of a small synthetic experiment, run in a Freebuff session and reported by the owner (not independently re-run, so pending), produced one finding worth recording: the frozen estimand left the inclusion rule for one target unspecified, and excluding that target moved the primary estimate beyond the agreed tolerance. This is the problem the estimand framework [14] exists to prevent, and it appeared here for the same reason: the quantity was not pinned down before the data was seen.

### 4.1 Resources and 90-day trajectory

The owner states that the work in the 90 days to 2026-10-03 cost about 60 USD (a 20 USD per month Claude subscription) plus electricity, using free tools (Freebuff, Hermes, Ollama), with no funding, no formal technical credentials and about 20 months of experience. These statements are author-reported and cannot be checked from the repositories ([C-050](../CLAIMS.md), [C-051](../CLAIMS.md), pending). What can be checked is activity: in the same window 20 public repositories had 1,753 unique commits, 1,470 of them under the owner's two git author names, on 62 of 91 days with no gap longer than five days ([C-049](../CLAIMS.md), verified, re-runnable with `scripts/activity_window.py`; see [the activity page](../05-experiments/activity-window-90d.md)).

A descriptive reading of the repositories' first-commit dates, which is the author's and not a measurement, shows a sequence: a governed agent runtime in July, assurance tooling and satellite services in August, formal-verification and research-lab repositories in September, and protocol and independence-ladder work in October. Throughput was bursty (169 owner commits on one day, 2026-08-10), and some bursts coincide with an automated adapter also committing, so commits measure directed throughput, not hand-written work and not effort. Five private repositories were also active and could not be read.

**What this supports.** A resource-normalised statement: the controls in Section 3 were assembled and operated on a very small budget by one person. This is the claim the lab's own thesis predicts, that the scarce thing is verification discipline and not spend.

**What it does not support.** It does not show the method is better than the methods in Section 2, and it does not separate the owner's contribution from the models'. The framework in the lab's human-AI idea-realization page says that separation needs interventions, not observation. The tools used are also products of well-funded teams, so "no funding" is not "no resources". The relevant peer group for this system is other practitioners with the same access to the same tools, and this paper does not survey them.

## 5. The first planned experiment (CVT-1), and its prior work

**Question.** On 24 small Python tasks, does a small local model that sees the failure message of a failed attempt (arm C) solve more hidden tests than the same model re-sampled from scratch with the same attempt limit (arm B-n)?

**Registered decision.** Supported only if the mean per-task difference is at least 0.10 and the 95% bootstrap interval over tasks has a lower bound above 0. Otherwise not supported.

**Prior work.** CVT-1 is a single experiment, so the right comparison is with the single experiment closest to it. That is [3], which compared repair with sampling and found modest, inconsistent gains once cost is counted. In the limited search done for this paper (a handful of queries on 2026-10-03), I did not find a pre-registered test of this comparison with a small locally run model, but the search was shallow and this is not a claim of novelty. Related small-model work [4][5] suggests the effect may be weak for small non-reasoning models, so a "not supported" result is plausible and would be informative.

**Differences from [3] that bound what CVT-1 can show.** CVT-1 matches the attempt limit, not total tokens, and feedback prompts are longer than resampling prompts. It records tokens and seconds but does not decide on them. It uses 24 author-written tasks and one model.

## 6. Limits

- The lab has produced no headline result. This paper describes a procedure and its checks, not a finding.
- Integration is a different kind of claim from effectiveness. Combining controls shows the pieces fit together and that the mechanisms work (for example, the cheat is rejected on 24 of 24 tasks); it does not show that results produced this way are more trustworthy than results produced another way.
- The same author writes visible and hidden tests, so false passes are caught only for cases the author thought of.
- Passing tests demonstrate that artifacts match their specifications (verification). They do not show the specification is right or useful (validation). Most of the lab's current evidence is of the first kind.
- AI wrote most of the code and the tests, so they can share blind spots [10].
- Several sources were checked from abstract pages only. See Appendix A.
- Cost, background and the owner's experience are author-reported and pending; only the commit counts are mechanically checkable.
- Nothing here is externally validated.

## 7. Next steps

Run CVT-1 once and publish the registered decision whichever way it falls. Re-run it with a second local model in a new experiment directory to test whether the result holds beyond one model. Add a shell-command oracle to the harness so the same process can test the agent gate. Move the pending claims that depend on private logs either into public form or leave them pending.

## References

1. Chen, X., Lin, M., Schärli, N., Zhou, D. *Teaching Large Language Models to Self-Debug.* arXiv:2304.05128 (2023). https://arxiv.org/abs/2304.05128
2. Shinn, N., Cassano, F., Berman, E., Gopinath, A., Narasimhan, K., Yao, S. *Reflexion: Language Agents with Verbal Reinforcement Learning.* NeurIPS 2023. arXiv:2303.11366. https://arxiv.org/abs/2303.11366
3. Olausson, T. X., Inala, J. P., Wang, C., Gao, J., Solar-Lezama, A. *Is Self-Repair a Silver Bullet for Code Generation?* ICLR 2024. arXiv:2306.09896. https://arxiv.org/abs/2306.09896
4. Cho, J., Kang, D., Kim, H., Lee, G. G. *Self-Correcting Code Generation Using Small Language Models.* Findings of EMNLP 2025. arXiv:2505.23060. https://arxiv.org/abs/2505.23060
5. Zhang, L., Kothari, S. *Unlocking LLM Code Correction with Iterative Feedback Loops.* arXiv:2606.17514 (2026). https://arxiv.org/abs/2606.17514
6. Cobbe, K., Kosaraju, V., Bavarian, M., et al. *Training Verifiers to Solve Math Word Problems.* arXiv:2110.14168 (2021). https://arxiv.org/abs/2110.14168
7. Brown, B., Juravsky, J., Ehrlich, R., Clark, R., Le, Q. V., Ré, C., Mirhoseini, A. *Large Language Monkeys: Scaling Inference Compute with Repeated Sampling.* arXiv:2407.21787 (2024). https://arxiv.org/abs/2407.21787
8. Snell, C., Lee, J., Xu, K., Kumar, A. *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters.* arXiv:2408.03314 (2024). https://arxiv.org/abs/2408.03314
9. Liu, J., Xia, C. S., Wang, Y., Zhang, L. *Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation.* arXiv:2305.01210 (2023). https://arxiv.org/abs/2305.01210
10. Panickssery, A., Bowman, S. R., Feng, S. *LLM Evaluators Recognize and Favor Their Own Generations.* arXiv:2404.13076 (2024). https://arxiv.org/abs/2404.13076
11. Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N., Fabian, D., Kern, C., Shi, C., Terzis, A., Tramèr, F. *Defeating Prompt Injections by Design.* arXiv:2503.18813 (2025). https://arxiv.org/abs/2503.18813
12. Nosek, B. A., Ebersole, C. R., DeHaven, A. C., Mellor, D. T. *The preregistration revolution.* Proceedings of the National Academy of Sciences 115(11):2600-2606 (2018). https://doi.org/10.1073/pnas.1708274114
13. Ledgerwood, A. *The preregistration revolution needs to distinguish between predictions and analyses.* Proceedings of the National Academy of Sciences (2018). https://www.pnas.org/doi/10.1073/pnas.1812592115
14. International Council for Harmonisation. *ICH Harmonised Guideline E9(R1): Addendum on Estimands and Sensitivity Analysis in Clinical Trials to the Guideline on Statistical Principles for Clinical Trials.* Final version, adopted 20 November 2019. https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf
15. GSN Community. *GSN Community Standard Version 1.* https://www.faa.gov/about/office_org/headquarters_offices/ang/redac/redac-sas-201503-gsn-community-standard-v1.pdf
16. Liang, P., Bommasani, R., Lee, T., Tsipras, D., et al. *Holistic Evaluation of Language Models.* Transactions on Machine Learning Research (2023). arXiv:2211.09110. https://arxiv.org/abs/2211.09110
17. UK AI Security Institute and Meridian Labs. *Inspect: an open-source framework for large language model evaluations.* https://inspect.aisi.org.uk/
18. EleutherAI. *lm-evaluation-harness: a framework for few-shot evaluation of language models.* https://github.com/EleutherAI/lm-evaluation-harness
19. Zhang, D. *Testing Frontier Large Language Models' Physics Literacy in Parallel Physical Worlds.* arXiv:2607.00276 (2026). https://arxiv.org/abs/2607.00276
20. Singh, A. *Certifying Compressed Language Models: An Audit and a Statistical Toolkit.* arXiv:2608.15046 (2026). https://arxiv.org/abs/2608.15046

## Appendix A. How each source was checked (2026-10-03)

| Level | Sources | Meaning |
|---|---|---|
| Abstract page opened and read | [1] [3] [4] [5] [6] [7] [8] [9] [10] [11] [16] [19] [20] | Title, authors, year and the quoted or paraphrased findings above were taken from the arXiv abstract page. Findings are as the authors state them; the lab did not reproduce them. |
| Full document opened | [14] | The PDF text was extracted and the quoted definition and "defined in advance" statement read directly. |
| Related page opened | [13] | The commentary text was read through the PubMed Central copy. |
| Project page opened | [17] | The Inspect home page was read at page level; statements about features it does not mention are limits of that page. |
| Details from search results only | [2] [12] [15] [18] | The existence and bibliographic details came from search results. The pages themselves were not opened, so the reported figures for [2] and the bibliographic details for [12], [15] and [18] are unconfirmed here. |

None of the external numbers in this paper were reproduced by the lab. They are attributed to their sources. A reader who relies on a figure should open the source.
