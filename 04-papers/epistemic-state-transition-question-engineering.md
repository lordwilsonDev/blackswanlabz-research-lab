---
source: vault:30_Architecture/Epistemic-State-Transition-Question-Engineering-Research-White-Paper-v1.0.md
vault-date: 2026-09-20
captured: 2026-09-28
status: active
---

# EPISTEMIC STATE TRANSITION

## Question Engineering, Knowledge Acquisition, and Verified Inquiry

**Black Swan Labs — Research White Paper**

**Author:** Lord Wilson, Black Swan Labs
**Research Program:** Black Swan Labs Research Lab
**Version:** 1.0 — September 2026
**Status:** Working Research Hypothesis / Experimental Framework
**Research Principle:** *The model can propose. The experiment decides.*

---

## Abstract

Current AI systems are commonly evaluated according to the quality of the answers they produce. This framing assumes that the problem presented to the system is already sufficiently specified, that the relevant information is known, that the appropriate question has been asked, and that the available evidence is sufficient to support an answer.

Many real problems violate these assumptions.

The central proposition of this paper is that competent inquiry can instead be represented as a sequence of **epistemic state transitions**. A system begins in a state containing some combination of known information, unknown information, assumptions, competing explanations, evidence, constraints, available actions, and unresolved uncertainty. It then selects questions, information-acquisition actions, measurements, experiments, simulations, expert consultations, or reframings intended to change that state. The system evaluates whether the resulting evidence actually resolved the relevant uncertainty, updates its state, and determines what should be investigated next or whether inquiry should stop.

Within this framework, **Question Engineering** is not merely the generation of questions. It is the construction and selection of questions because their answers are expected to produce useful changes in epistemic state.

The resulting research hypothesis is:

> **A domain-agnostic architecture for constructing, evaluating, and executing epistemic state transitions may transfer across substantially different domains more reliably than domain-specific reasoning patterns alone, provided that domain knowledge supplies the mechanisms, constraints, evidence standards, and operating envelope required to instantiate those operations.**

The framework emerged through iterative cross-domain experimentation involving technical diagnosis, software incidents, scientific and archaeological reasoning, safety-sensitive decisions, knowledge acquisition, and mathematical problem analysis. The experiments repeatedly exposed weaknesses in earlier formulations, leading from answer generation to question engineering, from question quality to epistemic state, and finally to epistemic state transition as the proposed underlying unit.

The paper does **not** claim that this framework has been proven superior to frontier models, that it constitutes a new theory of intelligence, that it reduces required model parameters, or that it establishes a minimal invariant of intelligence. Those propositions remain empirical research questions.

---

# 1. The Problem

A conventional AI interaction can be represented as:

$$
\text{Question} \rightarrow \text{Answer}
$$

This model works well when:

* the question is correctly framed;
* the relevant variables are known;
* the required information is available;
* the evidence is trustworthy;
* competing explanations are understood;
* the decision criterion is clear; and
* the requested answer is actually the appropriate endpoint.

Real-world inquiry frequently fails one or more of these conditions.

A production failure may have an incorrect initial diagnosis.

A scientific investigation may not know which variable is decisive.

A medical decision may depend on information absent from the initial case.

An engineering problem may contain unreliable instrumentation.

A mathematical problem may have a representation that obscures the most tractable route.

An organization may ask for a decision when the real need is to determine whether the decision itself is correctly framed.

Therefore:

$$
\text{Question} \neq \text{Problem}
$$

and:

$$
\text{Information} \neq \text{Evidence}
$$

and:

$$
\text{Evidence} \neq \text{Resolution}
$$

and:

$$
\text{Resolution} \neq \text{Decision}
$$

This motivates a different computational objective.

---

# 2. From Answer Generation to Epistemic Navigation

The proposed architecture begins with a state rather than an answer.

Let the epistemic state at time \(t\) be represented abstractly as:

$$
E_t =
(K_t,U_t,C_t,H_t,V_t,D_t,A_t,S_t)
$$

where:

* \(K_t\): currently established knowledge;
* \(U_t\): unresolved unknowns;
* \(C_t\): decision- or claim-critical unknowns;
* \(H_t\): competing hypotheses, models, or explanations;
* \(V_t\): evidence and evidence-reliability state;
* \(D_t\): decision or research space;
* \(A_t\): available epistemic actions;
* \(S_t\): current sufficiency, stopping, and resolution state.

An inquiry operation \(a_t\) produces evidence \(e_{t+1}\), which may produce:

$$
E_t
\xrightarrow{a_t,e_{t+1}}
E_{t+1}
$$

The objective is therefore not simply to maximize information.

It is to produce **useful, justified state transitions**.

---

# 3. Question Engineering

Question Engineering is defined here as:

> **The systematic construction, evaluation, selection, and sequencing of questions intended to produce useful epistemic state transitions.**

This differs from ordinary question generation.

### Question Generation

"What questions could I ask?"

### Question Answering

"What is the answer?"

### Question Engineering

"Which question should be asked now because its answer could materially improve the current epistemic state?"

This distinction is supported by existing research showing that LLMs can struggle to identify necessary clarification questions even when they can solve the corresponding fully specified problem. QuestBench, for example, formalized underspecified reasoning tasks in which missing information must be acquired through a question; its reported results showed substantial difficulty on some logic and planning settings.

The present framework extends the problem from selecting a missing variable to managing an evolving inquiry state.

---

# 4. The Epistemic State Transition

The central research object is:

$$
\boxed{E_t \rightarrow E_{t+1}}
$$

A transition can be useful even when it does not increase the amount of information possessed.

For example:

* discovering that a sensor is unreliable;
* proving that two hypotheses are observationally equivalent under current measurements;
* eliminating an entire class of explanations;
* discovering that the original problem boundary is incorrect;
* demonstrating that a proposed action is unauthorized;
* proving that a decision cannot responsibly be made with available evidence;
* reducing an infinite mathematical uncertainty to a finite residual problem.

Thus:

$$
\text{Knowledge Gain}
\neq
\text{Epistemic Progress}
$$

A negative result can represent substantial progress.

---

# 5. The Question-Transition Loop

The proposed core loop is:

$$
\boxed{
\text{CURRENT STATE}
\rightarrow
\text{UNKNOWN SPACE}
\rightarrow
\text{CRITICALITY}
\rightarrow
\text{QUESTION}
\rightarrow
\text{EPISTEMIC ACTION}
\rightarrow
\text{EVIDENCE}
\rightarrow
\text{STATE UPDATE}
\rightarrow
\text{NEXT QUESTION}
}
$$

The loop terminates when the system reaches a justified terminal state such as:

* VERIFIED;
* SUPPORTED;
* DECISION-READY;
* CAUSALLY UNRESOLVED;
* INSUFFICIENT EVIDENCE;
* UNRESOLVABLE WITH CURRENT METHODS;
* DECISION NOT RESPONSIBLY AVAILABLE;
* BLOCKED;
* OUT OF SCOPE.

Stopping is therefore part of epistemic competence.

A system that continually asks questions without recognizing sufficiency has not solved the problem.

---

# 6. What Makes a Question Valuable?

The experiments revealed that there is no defensible universal scalar called "best question."

A question may be:

* informative but irrelevant;
* technically sophisticated but causally downstream;
* highly specific but based on a false premise;
* actionable but unsupported;
* highly discriminating but currently unresolvable;
* low-information but decision-critical.

Question quality therefore requires multiple dimensions.

Candidate dimensions include:

1. **Validity** — Is the question well-formed under the current state?
2. **Criticality** — Could its answer materially affect the claim or decision?
3. **Discrimination** — Does it distinguish competing hypotheses?
4. **Dependency** — How much downstream reasoning depends upon it?
5. **Resolvability** — Can the available methods answer it?
6. **State-transition value** — Would its resolution materially improve the epistemic state?
7. **Adaptation value** — Does it enable better subsequent questions?
8. **Efficiency** — What state improvement is obtained relative to cost?
9. **Path equivalence** — Can different questions lead to equivalent justified states?
10. **Stopping value** — Could the result legitimately establish sufficiency or justify stopping?

This leads to a critical methodological conclusion:

> **Question Engineering should evaluate inquiry trajectories, not isolated questions alone.**

---

# 7. The Role of Information Gain

Information gain and uncertainty reduction are established concepts in information theory and active learning. Active-learning systems commonly select queries according to informativeness, uncertainty, disagreement, or related criteria, and research also explicitly studies stopping criteria.

The present framework does not claim to replace these methods.

Instead, it proposes that information gain is insufficient as the sole objective for consequential inquiry.

A question can reduce uncertainty about a variable while leaving decision-critical uncertainty unchanged.

Therefore:

$$
\text{Information Gain}
\not\Rightarrow
\text{Decision-Relevant Progress}
$$

A useful future quantity would therefore measure something closer to:

$$
\text{State Transition Value}
=
f(
\Delta C,
\Delta H,
\Delta V,
\Delta D,
\Delta S
)
$$

where the deltas represent changes in critical unknowns, hypothesis space, evidence quality, decision space, and stopping state.

This is proposed as a research construct, not an established mathematical law.

---

# 8. Epistemic Action Selection

A question is only useful if the system can determine how to investigate it.

Possible epistemic actions include:

* retrieve a document;
* query a database;
* inspect source code;
* run a computation;
* simulate a system;
* measure an instrument;
* consult an expert;
* inspect a physical artifact;
* run an experiment;
* reproduce a result;
* change an operating condition;
* seek an independent measurement;
* reframe the problem;
* defer the decision.

Thus the architecture becomes:

$$
\text{Question}
\rightarrow
\text{Evidence Method}
$$

rather than:

$$
\text{Question}
\rightarrow
\text{Web Search}
$$

This distinction is fundamental.

Sometimes the correct response to uncertainty is retrieval.

Sometimes it is measurement.

Sometimes it is experimentation.

Sometimes it is recognizing that the current methods cannot resolve the uncertainty.

---

# 9. AIL Integration

Axiom Inversion Logic (AIL) is used as an adversarial mechanism within the epistemic transition process.

AIL asks:

> **What assumptions are structuring the current reasoning space?**

and then deliberately challenges them.

Relevant inversion classes include:

* technical;
* causal;
* boundary;
* measurement;
* temporal;
* organizational;
* epistemic;
* statistical;
* dependency;
* institutional;
* meta-axiomatic.

The purpose is not to generate contrarian answers.

The purpose is to determine whether changing an assumption changes the **search space itself**.

This produces a distinction:

$$
\text{Hypothesis}
=
\text{candidate explanation within a search space}
$$

whereas:

$$
\text{Reframing}
=
\text{change to the search space}
$$

Question Engineering therefore operates downstream of framing but can also challenge the framing itself.

---

# 10. MoIE Integration

The Mixture of Inversion Experts (MoIE) architecture provides structured diversity.

Instead of asking multiple agents to independently produce the same answer, different reasoning roles can be assigned:

* causal analyst;
* measurement analyst;
* boundary analyst;
* domain specialist;
* falsification specialist;
* decision analyst;
* evidence critic;
* experimental designer.

Disagreement is not treated as a vote.

It becomes an input into Question Engineering:

$$
\text{Disagreement}
\rightarrow
\text{Unresolved Difference}
\rightarrow
\text{New Question}
$$

This preserves competing explanations rather than prematurely collapsing them into consensus.

---

# 11. Evidence Authority

The framework distinguishes:

$$
\text{Question Answered}
$$

from:

$$
\text{Question Resolved}
$$

Evidence must therefore be evaluated for:

* provenance;
* reliability;
* independence;
* completeness;
* timing;
* calibration;
* comparability;
* regime change;
* analytical validity;
* chain of custody where applicable;
* admissibility where applicable;
* testability;
* decay.

The system must be able to say:

> "The question was investigated, but the evidence did not resolve it."

This is a central anti-hallucination mechanism.

---

# 12. The Erdős–Faber–Lovász Case

The Erdős–Faber–Lovász conjecture provides a useful historical mathematical case study.

The conjecture, posed in 1972, states in one equivalent formulation that the chromatic index of every linear hypergraph on \(n\) vertices is at most \(n\).

The problem has a long history of partial progress. The current Erdős Problems database classifies it as **DECIDABLE — resolved up to a finite check**, noting that Kang, Kelly, Kühn, Methuku, and Osthus proved the conjecture for all sufficiently large \(n\).

Their paper, published in *Annals of Mathematics* in 2023, proves the conjecture for every sufficiently large \(n\) and gives stability versions of the result.

The important point for this framework is not to claim that the mathematical problem itself constitutes evidence for Question Engineering.

Rather, it illustrates a specific kind of epistemic transition.

Initially:

$$
E_0:
\text{truth of an infinite family unresolved}
$$

After the large-\(n\) theorem:

$$
E_1:
\text{large-}n\text{ regime established; finite residual domain remains}
$$

The theorem therefore changes the **shape of the remaining uncertainty**.

This illustrates:

$$
\boxed{
\text{Epistemic Progress}
\neq
\text{Information Accumulation}
}
$$

A mathematical result can be valuable because it transforms the remaining search space.

---

# 13. What the EFL Case Reveals

The EFL example produced a useful sequence of questions:

### Q0

Is the conjecture true?

### Q1

What precisely remains unresolved after the large-\(n\) theorem?

### Q2

Can the remaining finite region be explicitly characterized?

### Q3

Can those cases be reduced structurally?

### Q4

Can they be computationally verified?

### Q5

Can computational results be independently certified?

### Q6

Can a stronger theorem eliminate the residual cases?

### Q7

What structural mechanism explains the general result?

These are not merely additional questions.

Each question corresponds to a different possible transition through the research state.

The experiment therefore supports the working hypothesis that **research progress can be represented as controlled traversal through a changing question space**.

It does not establish that this is universally true.

---

# 14. Cross-Domain Structural Invariance

Prior experiments applied the architecture to substantially different problem types, including:

* industrial rotating-equipment diagnosis;
* PostgreSQL production-failure investigation;
* archaeological causal inference;
* battery thermal-risk analysis;
* anticoagulation decision analysis;
* structural fatigue investigation;
* mathematical problem analysis.

Across these cases, the domain-specific content changed substantially.

The recurring structure was:

$$
\text{Observation}
\rightarrow
\text{Unknowns}
\rightarrow
\text{Critical Unknowns}
\rightarrow
\text{Competing Explanations}
\rightarrow
\text{Evidence}
\rightarrow
\text{Discrimination}
\rightarrow
\text{State Update}
\rightarrow
\text{Next Inquiry}
$$

This motivates the following hypothesis.

---

# 15. Structural Epistemic Transfer Hypothesis

> **A domain-agnostic set of epistemic operations — including problem representation, assumption identification, unknown-space construction, criticality assessment, competing-hypothesis generation, discriminating inquiry, evidence evaluation, state updating, and stopping — may transfer across domains more reliably than domain-specific knowledge or surface-level reasoning patterns, provided appropriate domain knowledge is supplied to instantiate those operations.**

This hypothesis is intentionally bounded.

The experiments do not establish:

* that these operations are sufficient;
* that they are minimal;
* that they are unique;
* that they outperform frontier systems;
* that they constitute a theory of intelligence.

Those are future experimental questions.

---

# 16. Why Domain Knowledge Still Matters

The architecture is not intended to eliminate domain expertise.

The opposite is true.

The system requires domain knowledge to instantiate:

* mechanisms;
* constraints;
* operating envelopes;
* failure modes;
* evidence standards;
* measurement interpretation;
* causal relationships;
* safety requirements;
* domain-specific stopping conditions.

Therefore the proposed division is:

$$
\boxed{
\text{General Epistemic Architecture}
+
\text{Domain Knowledge}
=
\text{Domain-Applicable Inquiry}
}
$$

The hypothesis is that the **architecture of inquiry may transfer**, while the **contents of expertise remain domain-specific**.

---

# 17. Relation to Existing Research

The proposed framework sits near several established research areas.

### Active Learning

Active learning studies how systems select informative observations or labels, including uncertainty-based, disagreement-based, and other query strategies.

### Information-Seeking Questioning

Recent work such as QuestBench directly evaluates whether LLMs can identify necessary questions when information is missing.

### Uncertainty-Aware Planning

Research has also investigated selecting questions according to expected uncertainty reduction and planning over possible future answers.

### Tool-Using Agents

Other research evaluates systems that combine reasoning with actions such as database querying and information retrieval.

The contribution proposed here is therefore not:

> "No one has studied questions, uncertainty, or information acquisition."

Rather, the research direction is to investigate whether these components can be unified around a more general computational object:

$$
\boxed{\text{Epistemic State Transition}}
$$

and evaluated as a persistent architecture rather than as isolated question-answering behavior.

---

# 18. Experimental Framework

A serious test of the hypothesis should compare systems that receive the same task, evidence environment, tools, time, and budget.

Candidate conditions include:

### C0 — Closed Book

No external acquisition.

### C1 — Standard RAG

Retrieve relevant information and answer.

### C2 — RAG + Question Generation

Generate questions before retrieval.

### C3 — RAG + Expert Checklist

Provide an explicit checklist of information categories.

### C4 — Active Retrieval

Allow adaptive retrieval based on uncertainty.

### T1 — Full Epistemic State Architecture

Maintain:

* problem frame;
* known information;
* unknown information;
* critical unknowns;
* competing hypotheses;
* evidence reliability;
* candidate questions;
* candidate epistemic actions;
* state transitions;
* stopping conditions.

### Ablations

Remove individually:

* persistent state;
* AIL;
* criticality ranking;
* question adaptation;
* evidence-resolution testing;
* stopping engine;
* domain competence model.

The purpose is to determine whether the architecture itself contributes causal value.

---

# 19. Proposed Metrics

No single metric is assumed to capture epistemic competence.

Candidate measures include:

### Critical Question Recall

$$
CQR =
\frac{
\text{critical questions discovered}
}{
\text{gold critical questions}
}
$$

### Criticality Ranking Accuracy

Does the system correctly prioritize which unknowns matter most?

### False Closure Rate

How often does the system declare sufficient evidence when critical uncertainty remains?

### Evidence Resolution Rate

How often does acquired evidence actually resolve the question for which it was obtained?

### Question Adaptation Score

Does the next question appropriately depend on the updated state?

### Frame Correction Rate

How often does the system detect that the original framing is inadequate?

### Stopping Accuracy

Does the system stop when further inquiry is unnecessary, and continue when critical uncertainty remains?

### Acquisition Efficiency

$$
AE =
\frac{
\text{verified epistemic improvement}
}{
\text{acquisition cost}
}
$$

### State Transition Quality

A multidimensional evaluation of whether:

$$
E_{t+1} > E_t
$$

along relevant dimensions of:

* critical uncertainty;
* hypothesis discrimination;
* evidence quality;
* decision clarity;
* operating-envelope knowledge;
* falsifiability;
* justified stopping.

The ordering relation \(>\) must itself be operationalized empirically; it should not be assumed.

---

# 20. The Hardest Experimental Problem

The framework encountered a major methodological obstacle:

> **How do we objectively determine that one epistemic state is better than another?**

This is more difficult than evaluating answer correctness.

Two systems may reach different but equally valid investigative paths.

Two experts may propose different questions that lead to the same justified conclusion.

One question may produce more information but less decision value.

Therefore the benchmark must not assume that there is always one correct question.

Instead it should evaluate **equivalence classes of valid inquiry trajectories**.

This is a critical design requirement.

---

# 21. Gold Standards

A proposed gold-standard process is:

1. recruit multiple qualified domain experts;
2. independently identify necessary information;
3. identify decision-critical unknowns;
4. identify acceptable evidence;
5. identify discriminating questions;
6. identify valid stopping conditions;
7. independently construct counterfactuals;
8. reconcile disagreements;
9. preserve legitimate alternative paths;
10. blind evaluators to system identity.

A question should be considered decision-critical when changing its answer could change the permissible or justified decision, claim, or required action.

This avoids reducing expert knowledge to one arbitrary list of "correct questions."

---

# 22. Falsification Conditions

The hypothesis should be considered weakened or falsified if strong controls demonstrate that:

1. ordinary RAG performs equivalently;
2. explicit checklists eliminate the advantage;
3. generic self-questioning matches the full architecture;
4. persistent state provides no measurable benefit;
5. AIL contributes no measurable benefit;
6. criticality ranking contributes no measurable benefit;
7. the architecture produces more questions but not better transitions;
8. state-transition metrics cannot reliably distinguish progress;
9. experts cannot reliably evaluate state transitions above chance or baseline agreement;
10. the apparent advantage disappears under unseen domains;
11. the architecture requires extensive domain-specific hand engineering to function;
12. improvements result primarily from additional retrieval budget rather than the architecture.

These are features, not threats, of the research program.

A framework that cannot be broken experimentally is not yet a sufficiently specified research hypothesis.

---

# 23. The Breaking Point

The current strongest unresolved problem is:

> **Can epistemic state transition quality be defined and measured reliably enough to support causal experimental claims?**

We have demonstrated that the concept is useful for describing the behavior of the systems we tested.

We have not yet demonstrated that an independent evaluator can reliably quantify:

$$
E_t \rightarrow E_{t+1}
$$

across domains.

That is the next major methodological barrier.

If this cannot be solved, the framework may remain a useful conceptual architecture without becoming a rigorous quantitative theory.

If it can be solved, the research program becomes substantially stronger.

---

# 24. Research Program

The proposed research sequence is:

### Phase I — Construct Validity

Determine whether independent evaluators can reliably identify:

* known;
* unknown;
* critical unknown;
* evidence sufficiency;
* hypothesis discrimination;
* useful state transition;
* justified stopping.

### Phase II — Comparative Validation

Compare Question Engineering against:

* RAG;
* Self-Ask;
* active retrieval;
* expert checklists;
* strong reasoning baselines.

### Phase III — Ablation

Remove architectural components individually.

### Phase IV — Cross-Domain Transfer

Test previously unseen domains.

### Phase V — Adversarial Evaluation

Introduce:

* misleading true facts;
* contradictory evidence;
* unreliable measurements;
* changing problem frames;
* hidden variables;
* insufficient evidence;
* contaminated sources;
* irreversible actions.

### Phase VI — Longitudinal Adaptation

Test whether experience produces improved future epistemic transitions.

### Phase VII — Real-World Validation

Compare the architecture against expert teams performing actual investigations.

---

# 25. Broader Architectural Implication

The work suggests a possible decomposition of capable AI into:

$$
\boxed{
\text{Representation}
+
\text{Reasoning}
+
\text{Acquisition}
+
\text{Verification}
+
\text{Adaptation}
}
$$

Traditional scaling has concentrated heavily on increasing model capability through larger parameter counts, training data, and computation.

The hypothesis here is complementary:

> Intelligence may also scale through the architecture that determines how a system converts available information into verified capability.

This does not imply that model scale is unimportant.

It proposes another possible scaling dimension:

$$
\text{Intelligence}
\not\equiv
\text{Stored Knowledge}
$$

and potentially:

$$
\text{Capability}
\approx
f(
\text{Model},
\text{Acquisition Architecture},
\text{Evidence},
\text{Tools},
\text{Verification},
\text{Environment}
)
$$

This remains a hypothesis requiring controlled testing.

---

# 26. Relationship to the Broader Black Swan Labs Architecture

Epistemic State Transition does not replace the existing architecture.

It provides a deeper abstraction that connects several existing components.

### Capability Architecture

Determines what capabilities are required.

### Domain Expertise

Constructs the domain model required to instantiate those capabilities.

### Acquisition

Obtains missing knowledge and evidence.

### AIL

Challenges assumptions and frames.

### MoIE

Maintains structured competing reasoning paths.

### Question Engineering

Constructs and selects the next inquiry.

### Epistemic Action Selection

Chooses how to resolve the relevant uncertainty.

### Evidence Authority

Determines whether evidence establishes the claim.

### MSB

Controls authorized action and operational execution.

### L5

Learns from failure, gaps, and broken assumptions.

The resulting loop is:

$$
\boxed{
MISSION
\rightarrow
CAPABILITY
\rightarrow
EXPERTISE
\rightarrow
UNKNOWN
\rightarrow
QUESTION
\rightarrow
ACTION
\rightarrow
EVIDENCE
\rightarrow
STATE
\rightarrow
VERIFY
\rightarrow
UPDATE
}
$$

---

# 27. Central Hypothesis

The current research program therefore freezes the following hypothesis:

> **Epistemic State Transition Hypothesis**
>
> Complex problem solving may be understood as the controlled transformation of epistemic states. A capable system identifies what is known, unknown, uncertain, contested, and decision-critical; selects questions or actions capable of resolving consequential uncertainty; evaluates the resulting evidence; updates its representation; and determines whether to continue, reframe, decide, or stop. A domain-agnostic architecture implementing these operations may transfer across substantially different domains when domain-specific knowledge supplies the mechanisms, constraints, evidence standards, and operating envelope required to instantiate them.

---

# 28. What Has Been Established Versus What Remains Hypothetical

## Observed / Established Within This Research Program

* The architecture can be instantiated across substantially different domains.
* The same broad epistemic operations recur across those domains.
* Adversarial testing repeatedly exposed and improved weaknesses in earlier formulations.
* Question quality cannot safely be reduced to information gain alone.
* Different valid inquiry paths can exist.
* Evidence acquisition and evidence resolution are distinct.
* Knowledge gain and epistemic progress are distinct concepts.
* A problem can become substantially more tractable when its uncertainty structure changes.
* The Erdős–Faber–Lovász case provides a concrete mathematical example of a theorem transforming the residual uncertainty space.

## Hypotheses

* Epistemic state transition is a useful general unit of intelligent inquiry.
* Structural epistemic operations transfer across domains.
* Persistent epistemic state improves inquiry relative to strong retrieval baselines.
* Question Engineering improves critical-information discovery.
* Epistemic Action Selection improves inquiry efficiency.
* These mechanisms may provide a scalable complement to model-size scaling.

## Not Established

* A new general theory of intelligence.
* A minimal set of epistemic invariants.
* Superiority over frontier models.
* Parameter-efficiency gains.
* Economic superiority.
* Autonomous scientific discovery at expert level.
* Universal objective measurement of epistemic state quality.

---

# 29. Conclusion

The central insight of this research is a shift in the object being optimized.

The conventional question is:

> **Can the system produce the correct answer?**

Question Engineering asks:

> **What should the system ask before attempting the answer?**

Epistemic Control asks:

> **What action should the system take to resolve the uncertainty?**

Epistemic State Engineering asks:

> **What state must the system reach before the claim or decision is justified?**

Epistemic State Transition unifies these questions:

> **How does the system move from its current epistemic state to a better justified one?**

The proposed architecture does not assume that every uncertainty can be resolved.

It does not assume that more information is always better.

It does not assume that the first question is the correct question.

It does not assume that an answer constitutes evidence.

It does not assume that evidence constitutes resolution.

It does not assume that resolution requires certainty.

And it does not assume that continuing to ask questions is always progress.

Instead, it treats inquiry as a controlled process:

$$
\boxed{
\text{Represent}
\rightarrow
\text{Identify Unknowns}
\rightarrow
\text{Prioritize}
\rightarrow
\text{Question}
\rightarrow
\text{Act}
\rightarrow
\text{Observe}
\rightarrow
\text{Verify}
\rightarrow
\text{Update}
\rightarrow
\text{Stop / Decide / Reframe}
}
$$

The deepest research question is therefore no longer:

> "How can an AI answer more questions?"

It is:

> **Can an AI system learn to determine what must become known, select how that knowledge can be obtained, verify whether the resulting evidence actually changes what can be justified, and autonomously navigate toward an epistemically sufficient state?**

That is the hypothesis this paper proposes to test.

**The model can propose.
The question can direct.
The action can investigate.
The evidence can constrain.
The experiment can discriminate.
The state can update.
The system can stop.
And reality gets the final vote.**

---

## Selected References

1. Kang, D. Y., Kelly, T., Kühn, D., Methuku, A., & Osthus, D. *A proof of the Erdős–Faber–Lovász conjecture.* Annals of Mathematics 198(2), 537–618 (2023).

2. Kang, D. Y., Kelly, T., Kühn, D., Methuku, A., & Osthus, D. *Solution to a problem of Erdős on the chromatic index of hypergraphs with bounded codegree.* arXiv:2110.06181.

3. Bloom, T. F. *Erdős Problem #19.* Erdős Problems database. Current database status: "DECIDABLE — Resolved up to a finite check."

4. Li, B. Z., Kim, B., & Wang, Z. *QuestBench: Can LLMs ask the right question to acquire information in reasoning tasks?* arXiv:2503.22674 (2025).

5. Shannon, C. E. *A Mathematical Theory of Communication.* Bell System Technical Journal 27 (1948). [Foundational information-theoretic reference underlying information gain and entropy-based inquiry.]

6. Ren, P. et al. *A Survey of Active Learning for Natural Language Processing.* arXiv:2210.10109.

---

## Research Status

**Framework:** Proposed
**Cross-domain stress testing:** Preliminary / internal
**Construct validity:** Unresolved
**Causal superiority:** Untested
**Generalization:** Hypothesis
**Mathematical case study:** Illustrative
**Publication claim:** No claim of established theory
**Next decisive experiment:** Epistemic State Transition Benchmark (EST-Bench)

**Governing principle:**

> **Do not optimize for answers. Optimize for justified transitions in what the system knows, does not know, can establish, and is therefore entitled to conclude or do.**
