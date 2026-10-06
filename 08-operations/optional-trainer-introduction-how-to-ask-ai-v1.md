---
source: authored in this repository (commit 1016347, 2026-10-05): optional trainer introduction; original working location not recorded
captured: 2026-10-05
status: pending
---

# Optional Trainer Introduction: How to Ask AI the Right Questions v1

## Status
OPTIONAL TRAINER MATERIAL

## Purpose
A one-hour orientation for trainers and facilitators teaching people to use Claude, Codex, or another capable AI environment as a governed question-and-capability engine rather than an answer oracle.

The learner does not need to understand the underlying architecture before starting. The system should load the appropriate skills and harnesses as the problem is classified.

## Core promise
You do not need to know the answer before you start. You need to learn how to ask questions that make the answer discoverable, testable, and reusable.

## One-hour curriculum

### 0-5 min — What you are actually learning
Problem -> Questions -> Evidence -> Independent Verification -> Test -> Verified Answer -> SOP -> Skill -> Reusable Capability.

The learner's job is to ask good questions and refuse to treat an unverified answer as truth.

### 5-12 min — The first question
Use:

"I have a problem I need to solve:
[DESCRIBE THE PROBLEM]

Don't jump straight to the answer.
First:
1. Restate what you think I'm trying to accomplish.
2. Identify what you know versus what you're assuming.
3. Tell me what information is missing.
4. Generate the most important questions we need to answer.
5. Explain which questions should be answered first and why.
6. Tell me what evidence would change your conclusion.
If you are uncertain, say so."

### 12-20 min — Question engineering
Teach:
1. What exactly are we talking about?
2. What exactly are we claiming?
3. What is inside and outside the scope?
4. Who or what has authority to establish this?
5. What are we required to do?
6. Does time change the answer?
7. What will this answer be used for?

Boundary question:
"What question should I have asked that I haven't asked?"

### 20-28 min — Evidence separation
Teach the distinctions:
- fact
- source claim
- model interpretation
- assumption
- hypothesis
- inference
- verified result
- human decision

Prompt:
"Separate your response into known facts, evidence/source claims, assumptions, hypotheses, inferences, unknowns, contradictions, and what would verify or falsify the conclusion. Do not present an inference as a fact. Do not fill an unknown with a guess."

### 28-36 min — Multi-model verification
Core rule: agreement is not proof.

Have at least two models analyze independently. Ask for agreement, disagreement, unsupported assumptions, missing evidence, failure modes, and the smallest discriminating test.

Prompt:
"Here is a problem that another model analyzed. Do NOT assume its conclusion is correct. Independently analyze the problem. Identify points of agreement, points of disagreement, unsupported assumptions, missing evidence, possible failure modes, and what test would discriminate between competing explanations. If both analyses could be wrong for the same reason, identify that shared failure mode."

### 36-44 min — When the models are both wrong
Teach correlated failure:
- shared training data
- shared hidden assumptions
- misleading sources
- ambiguous questions
- incorrect premises
- corrupted inputs
- tool failures
- outdated information
- shared multimodal interpretation errors

Multimodal breakdown prompt:
"We may have a correlated multimodal failure. Analyze the problem again without assuming that the text, image, audio, or other modalities are correct. For each modality: what information does it actually establish; what could it be misinterpreting; what assumptions does it introduce; could the modalities share the same underlying error; and what independent evidence could break the correlation? Then identify the smallest test that could distinguish the competing explanations."

### 44-50 min — Compile the answer into an SOP
Once verified, use:
"Turn the verified solution into an SOP. Include purpose, when to use it, inputs, prerequisites, step-by-step procedure, decision points, failure conditions, verification checks, expected outputs, evidence to preserve, escalation conditions, and how to test the SOP on a new case. Do not invent missing requirements. Mark unknowns explicitly."

Transformation:
Conversation -> Procedure -> Skill -> Harness -> Capability.

### 50-55 min — Errors, confusion, and recovery
If confused: "Stop. Explain what I am misunderstanding."
If suspicious: "Attack your own conclusion."
If models disagree: "Find the smallest piece of evidence that would resolve the disagreement."
If both agree: "Find the assumption that could make both of you wrong."
If the question is bad: "Rewrite my question so that it is actually testable."
If information is missing: "Do not guess. Tell me exactly what you need."
If evidence is insufficient: "What would we have to observe or test before this could become a verified claim?"
If something breaks: "Do not silently repair the failure. Record what failed, why it matters, and what should happen next."

### 55-60 min — Final learner exercise
Give the learner an unfamiliar problem. Require:
1. State the problem.
2. Generate questions.
3. Identify assumptions.
4. Establish evidence.
5. Ask another model.
6. Find disagreement.
7. Attack agreement.
8. Resolve uncertainty.
9. Produce the answer.
10. Compile an SOP.
11. Test the SOP.
12. Preserve the capability.

Passing means the learner can operate the loop rather than merely repeat instructions.

## Trainer operating rule
Do not teach the underlying architecture as a prerequisite unless needed.

Don't know what to ask? Ask the AI what you should ask.
Don't trust the answer? Ask another model.
They agree? Try to prove them both wrong.
Still uncertain? Find the evidence that would settle it.
Solved? Turn it into an SOP.
Worked again? Turn the SOP into a skill.
Failed? Learn from the failure and compile the next version.

## Relationship to the Learner OS
This is optional trainer orientation to the general Learner OS / SOP Compiler. The underlying system is domain-independent. The workforce-grant implementation is one compiler target, not the definition of the architecture.

The learner starts with a problem. The system classifies it, loads relevant skills and harnesses, guides question formation, verifies evidence, and compiles successful solutions into reusable procedures and capabilities.

## Safety and governance
- AI output is not automatically evidence.
- Model agreement is not proof.
- Unknown is not false and is not true.
- NOT_READY is not FAIL.
- A failed test is information.
- Human decisions remain explicit.
- Sensitive or high-impact matters require appropriate human oversight and authoritative evidence.
- Do not conceal model or tool failures.

## Success criterion
The learner can take an unfamiliar problem and, without being handed the answer, use the question -> evidence -> verification -> test -> SOP loop to produce a defensible, reusable capability.
