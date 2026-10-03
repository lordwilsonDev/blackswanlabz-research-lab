---
source: white paper drafted in this repo during research session 2026-10-03
captured: 2026-10-03
status: pending
---

# Verification Without a Standard: a pre-registered, executable-oracle method for testing AI-built systems on small hardware

BlackSwanLabz Research Lab. Drafted by an AI model (Claude) at the lab owner's direction. Not peer reviewed. Status: pending. Dated 2026-10-03.

## Abstract

Generating code, analyses and agent behavior is now cheap. Knowing whether the output is correct, safe and useful is not. For many new artifacts there is no accepted benchmark or reviewing body, and a small lab cannot buy outside review. This paper describes the method the BlackSwanLabz Research Lab uses in that position: the lab writes its own standard before it tests, fixes it in a hash-locked pre-registration, tests the measuring instrument itself, runs once, and reports against a status ledger that separates verified, pending and retracted claims. The components are not new. Execution feedback for code [1][2][3], verifier-based selection [6][7][8], insufficient-test critiques [9], preregistration [12][13], estimands [14] and assurance cases [15] all exist. The contribution is their combination into a procedure that runs on a 16 GB desktop with a local model, and an honest account of what it cannot show. The lab has not yet produced a headline result. The first planned experiment (CVT-1) is specified and not run, and its closest prior work [3] found modest and inconsistent gains from feedback once cost is counted.

## 1. The problem

The lab's thesis is that intelligence is becoming abundant and verification is becoming scarce (see the lab's [thesis](../00-thesis/intelligence-infrastructure-mismatch.md)). Two consequences follow for a lab that builds with AI, directs rather than hand-writes the code, and has no domain credentials to lean on.

1. **Output volume is not evidence.** The lab's cornerstone package holds 32.5 million committed lines (C-001, verified), and the owner states that all of it was AI-generated (C-048, pending, no generation logs). That shows generation is cheap. It shows nothing about quality.
2. **Where no standard exists, the lab has to define one, and a self-defined standard can be bent after the fact.** Outside peer review is not available for much of this work and is not the goal. Without it, discipline has to replace review.

## 2. Related work

**Execution feedback and self-repair.** Chen et al. show that models given the execution results of their own code can find and fix mistakes, reporting gains of up to 12% on benchmarks with unit tests [1]. Reflexion stores verbal reflections on feedback and reports 91% pass@1 on HumanEval against 80% for GPT-4 [2]. The closest work to this paper's experiment is Olausson et al., who ask whether self-repair is worth its cost. They report that "when the cost of carrying out repair is taken into account, performance gains are often modest, vary a lot between subsets of the data, and are sometimes not present at all", and that the bottleneck is the model's ability to judge its own code [3]. For small models, Cho et al. report that 1B-scale models "struggle to exhibit reflective revision behavior" without special training [4]. A 2026 study finds that reasoning models gain more from compiler and test feedback than non-reasoning ones, and that syntactic and runtime errors are far easier to fix than logical ones [5].

**Sampling and verifiers.** Cobbe et al. show that selecting among many sampled solutions with a verifier beats fine-tuning alone on grade-school math [6]. Brown et al. find that coverage (the fraction of problems solved by any sample) rises log-linearly over four orders of magnitude of samples, that this converts to accuracy when an automatic verifier exists, and that majority voting and reward models plateau without one [7]. Snell et al. report that allocating inference compute adaptively can outperform a 14x larger model on problems where the smaller model has non-trivial success [8].

**Weak tests and weak judges.** EvalPlus enlarges HumanEval's tests by 80x and reports pass@k drops of 19.3 to 28.9%, with model rankings changing [9]. Panickssery et al. find that models recognise and favor their own outputs when judging, with self-preference correlated with self-recognition [10]. Both motivate this paper's separation of visible and hidden tests, and its rule that the model under test should not be its own sole judge.

**Agent safety.** CaMeL separates control flow from data flow to defend agents against prompt injection and reports solving 77% of AgentDojo tasks with provable security against 84% with no defense [11]. The lab's governed-runtime gate keys on action severity and on whether inputs came from untrusted content, a related idea implemented independently; this paper makes no claim about its effectiveness.

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

## 4. What the lab has and has not shown

Verified and mechanically re-checkable (see [CLAIMS.md](../CLAIMS.md)): three Adaptive Infrastructure reproductions and hand recomputations of small calculations (C-005, C-006, C-046); the research-loop reference passes its eight unit tests (C-036); the runtime's test collection (3,942 tests collected at a pinned commit, C-030). These are small, deterministic checks. They show reproducibility, not usefulness.

Pending: the core hypothesis that the lab's inversion method beats compute-matched baselines (C-004, not run); every result that depends on private repositories or local logs (the Ethos run, the FDE Kernel missions); and the AI-generation provenance of the package (C-048).

The lab's own audit of a small synthetic experiment, run in a Freebuff session and reported by the owner (not independently re-run, so pending), produced one finding worth recording: the frozen estimand left the inclusion rule for one target unspecified, and excluding that target moved the primary estimate beyond the agreed tolerance. This is the problem the estimand framework [14] exists to prevent, and it appeared here for the same reason: the quantity was not pinned down before the data was seen.

## 5. The first planned experiment (CVT-1), and its prior work

**Question.** On 24 small Python tasks, does a small local model that sees the failure message of a failed attempt (arm C) solve more hidden tests than the same model re-sampled from scratch with the same attempt limit (arm B-n)?

**Registered decision.** Supported only if the mean per-task difference is at least 0.10 and the 95% bootstrap interval over tasks has a lower bound above 0. Otherwise not supported.

**Prior work.** This is closest to [3], which compared repair with sampling and found modest, inconsistent gains once cost is counted. In the limited search done for this paper (a handful of queries on 2026-10-03), I did not find a pre-registered test of this comparison with a small locally run model, but the search was shallow and this is not a claim of novelty. Related small-model work [4][5] suggests the effect may be weak for small non-reasoning models, so a "not supported" result is plausible and would be informative.

**Differences from [3] that bound what CVT-1 can show.** CVT-1 matches the attempt limit, not total tokens, and feedback prompts are longer than resampling prompts. It records tokens and seconds but does not decide on them. It uses 24 author-written tasks and one model.

## 6. Limits

- The lab has produced no headline result. This paper describes a procedure and its checks, not a finding.
- The same author writes visible and hidden tests, so false passes are caught only for cases the author thought of.
- Passing tests demonstrate that artifacts match their specifications (verification). They do not show the specification is right or useful (validation). Most of the lab's current evidence is of the first kind.
- AI wrote most of the code and the tests, so they can share blind spots [10].
- Several sources were checked from abstract pages only. See Appendix A.
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

## Appendix A. How each source was checked (2026-10-03)

| Level | Sources | Meaning |
|---|---|---|
| Abstract page opened and read | [1] [3] [4] [5] [6] [7] [8] [9] [10] [11] | Title, authors, year and the quoted or paraphrased findings above were taken from the arXiv abstract page. Findings are as the authors state them; the lab did not reproduce them. |
| Full document opened | [14] | The PDF text was extracted and the quoted definition and "defined in advance" statement read directly. |
| Related page opened | [13] | The commentary text was read through the PubMed Central copy. |
| Details from search results only | [2] [12] [15] | The existence and bibliographic details came from search results. The pages themselves were not opened, so the reported figures for [2] and the bibliographic details for [12] and [15] are unconfirmed here. |

None of the external numbers in this paper were reproduced by the lab. They are attributed to their sources. A reader who relies on a figure should open the source.
