# Meta Skill: Why the Trainer Asks the Question

## Purpose

This meta-skill teaches a trainer, instructor, researcher, or AI training agent to understand **why each workforce-readiness question exists before asking it**.

It sits above `workforce-grant-readiness`.

The workforce skill answers:

> **What evidence must we collect and what must we decide?**

This meta-skill answers:

> **Why does this question exist, what decision does it unlock, what failure does it prevent, and what would change if the answer were different?**

The trainer must never become a form-filling operator. Every question is an instrument for resolving a dependency in the evidence chain.

## Core Invariant

**Question → Purpose → Dependency → Evidence → Decision → Consequence**

For every question, the trainer must be able to state:

1. **What are we trying to learn?**
2. **Why does it matter?**
3. **What decision depends on it?**
4. **What evidence can legitimately answer it?**
5. **What happens if the answer is unknown, contradicted, or negative?**
6. **What is the next question or action?**

If the trainer cannot explain the purpose of a question, the question should not be asked yet.

## The Workforce Causal Chain

The trainer uses this chain to understand the architecture:

**Employer Need**
→ **Occupational Need**
→ **Skills Gap**
→ **Training Intervention**
→ **Demonstrated Competency**
→ **Employment / Retention / Advancement**
→ **Wage / Productivity Outcome**
→ **Employer Economic Impact**
→ **Persistent Workforce Capacity**

A question belongs to this chain because it resolves one or more dependencies.

## Question Classes

### 1. Eligibility Questions

Examples:
- Is the applicant eligible?
- Has the applicant operated long enough?
- Is there an eligible Wisconsin employer?
- Are the trainees eligible?
- Is the required match available?

**Why ask:** These are gates, not scoring opportunities.

**Failure meaning:** If a mandatory eligibility condition is false, better curriculum or stronger narrative cannot repair the application.

**Trainer behavior:** Resolve early. Do not spend hours optimizing a proposal that is structurally ineligible.

---

### 2. Employer-Need Questions

Examples:
- What job problem exists today?
- Which workers cannot currently perform the required function?
- What skill is missing?
- What evidence demonstrates the gap?
- What does the employer lose because the gap exists?

**Why ask:** Workforce training must solve an actual employer/workforce problem rather than merely teach an interesting technology.

**Failure prevented:** Training-first design, technology theater, and curriculum looking for a justification after the fact.

**Trainer test:**

> If the training disappeared, what operational problem would remain?

If the answer is unclear, employer need is not yet established.

---

### 3. Occupational Questions

Examples:
- What occupation actually performs the work?
- What recognized occupational classification best describes it?
- Which tasks belong to that occupation?
- What competencies are required for entry, advancement, or increased functionality?

**Why ask:** A workforce grant funds occupational capability, not an abstract list of AI concepts.

**Failure prevented:** Inventing an internal title and treating it as an occupation.

**Trainer rule:** BlackSwanLabz L1–L10 describes capability progression. It does **not** replace an external occupational classification.

---

### 4. Skills-Gap Questions

Examples:
- What can the worker do now?
- What must the worker be able to do after training?
- What observable behavior separates the two states?
- Which skills are missing versus merely unfamiliar?

**Why ask:** The gap defines the training intervention.

**Failure prevented:** Training content being mistaken for competency.

**Key distinction:**

> Knowing a concept is not the same as demonstrating the occupational behavior.

---

### 5. Training-Design Questions

Examples:
- What will workers actually practice?
- What sequence produces the required competency?
- What is taught, rehearsed, assessed, and transferred?
- What evidence demonstrates successful learning?

**Why ask:** The grant reviewer must be able to see a credible path from training activity to worker capability.

**Failure prevented:** A curriculum that is intellectually impressive but operationally untestable.

---

### 6. Competency Questions

Examples:
- What counts as passing?
- Can the worker perform the task independently?
- Can they perform it under constraints?
- Can they reproduce the result?
- Can they handle a holdout or novel case?

**Why ask:** Completion is not competency.

**Failure prevented:** Counting attendance, course completion, or certificates as proof of job capability.

**Preferred evidence progression:**

**Taught → Practiced → Tested → Passed → Held-out → Transferred → Verified**

---

### 7. Outcome Questions

Examples:
- Will the worker be hired?
- Retained?
- Promoted?
- Receive increased wages?
- Receive increased hours/functionality?
- What measurable employer result follows?

**Why ask:** Training is valuable because capability changes economic/workforce outcomes.

**Failure prevented:** Claiming impact without an outcome mechanism.

**Trainer rule:** Distinguish:
- projected outcome,
- employer-committed outcome,
- observed outcome,
- verified outcome.

Never collapse them.

---

### 8. Wage Questions

Examples:
- What is the worker's baseline wage?
- What is the expected post-training wage?
- Is the increase committed or merely projected?
- What evidence will verify it?

**Why ask:** Wage movement can demonstrate economic opportunity and workforce value.

**Failure prevented:** Fabricated or ambiguous wage claims.

**Rule:** Never invent a wage. Label the evidence state.

---

### 9. Employer-Commitment Questions

Examples:
- Who will hire?
- Who will retain?
- Who will raise wages?
- What exactly has the employer committed to?
- Is the commitment documented?

**Why ask:** A training program without an employer pathway is not the same thing as employer-led workforce development.

**Failure prevented:** Treating hypothetical placement as committed placement.

---

### 10. Equity and Economic-Opportunity Questions

Examples:
- Who gains access?
- Who is economically disadvantaged or underrepresented?
- Does the training create a meaningful advancement pathway?
- Is the credential or competency stackable?
- Does the intervention increase mobility?

**Why ask:** Opportunity must be designed and evidenced, not asserted.

**Failure prevented:** Generic equity language disconnected from program mechanics.

---

### 11. Capacity-Building Questions

Examples:
- What remains after the grant?
- Can the employer continue training workers?
- Is the curriculum reusable?
- Are trainers being developed?
- Are assessments and evidence systems persistent?
- Can successful procedures become organizational capability?

**Why ask:** Capacity building turns a grant-funded project into durable workforce infrastructure.

**Failure prevented:** One-time training with no institutional residue.

---

### 12. Evidence-Provenance Questions

Examples:
- Who says this?
- What document supports it?
- Is the source authoritative?
- Is the evidence current?
- Is it employer-signed?
- Is it reproducible?
- Is it observation, claim, inference, hypothesis, or verified result?

**Why ask:** A plausible statement is not automatically evidence.

**Failure prevented:** Evidence laundering, unsupported claims, stale data, and model inference masquerading as fact.

Evidence states:

**VERIFIED → SUPPORTED → PROVISIONAL → INFERRED → UNKNOWN → CONTRADICTED**

---

## The Trainer's Meta-Question

Before asking any question, ask internally:

> **What uncertainty are we trying to collapse?**

Then classify the uncertainty:

- **Eligibility uncertainty**
- **Need uncertainty**
- **Occupation uncertainty**
- **Skills-gap uncertainty**
- **Training-design uncertainty**
- **Competency uncertainty**
- **Outcome uncertainty**
- **Wage uncertainty**
- **Employer-commitment uncertainty**
- **Equity uncertainty**
- **Capacity uncertainty**
- **Evidence/provenance uncertainty**

The trainer should ask the smallest question capable of resolving the uncertainty.

## Minimum-Sufficient-Question Rule

Do not ask questions merely because a form contains them.

Prefer:

**one question → one decision dependency**

Avoid:

**one giant question → ambiguous answer → multiple unresolved dependencies**

When a response contains multiple claims, decompose them.

## Question Provenance Record

Every important question should be representable as:

```
question_id
question
question_class
purpose
dependency
decision_unlocked
required_evidence
acceptable_evidence_state
negative_answer_consequence
next_action
```

Example:

```
question_id: EMP-NEED-001
question: What operational problem requires this training?
question_class: employer_need
purpose: establish that training responds to a real workforce gap
dependency: documented_employer_need
decision_unlocked: proceed to occupational mapping
required_evidence: employer documentation or signed statement
acceptable_evidence_state: VERIFIED | SUPPORTED
negative_answer_consequence: NOT_READY
next_action: obtain employer evidence or stop
```

## Trainer Decision Logic

The trainer should not merely collect answers.

Use:

**Ask → Classify → Verify → Resolve → Branch**

### If verified

Proceed to the next dependency.

### If supported but not verified

Mark the claim supported and identify what would verify it.

### If provisional

Do not build downstream certainty on it.

### If unknown

Ask the smallest next question that can resolve it.

### If contradicted

Stop propagation of the claim. Investigate the conflict.

### If false

Branch to the appropriate failure state.

**NOT_READY is not FAIL.**

A case can be incomplete without being disqualified.

## Why the Questions Are Ordered

The order is causal, not bureaucratic.

1. **Eligibility** — Can this project legally/structurally proceed?
2. **Employer need** — Is there a real problem to solve?
3. **Occupation** — What work is actually being changed?
4. **Skills gap** — What capability is missing?
5. **Training design** — How will capability be developed?
6. **Competency** — How will capability be demonstrated?
7. **Employer commitment** — Where does the capability go?
8. **Outcomes** — What changes economically?
9. **Equity** — Who benefits and how?
10. **Capacity** — What persists?
11. **Evidence** — Can every important claim survive scrutiny?
12. **Rubric** — How does the complete case score?

Do not optimize the rubric before resolving the causal chain.

## Anti-Optimization Rule

A high score cannot repair a broken causal dependency.

Examples:

- Strong curriculum + no employer need = blocked.
- Strong employer need + no occupational mapping = not ready.
- Strong training + no competency assessment = weak outcome evidence.
- Strong projected outcomes + no employer commitment = unsupported.
- Strong narrative + contradictory evidence = investigate, do not average away.
- Strong score + mandatory eligibility failure = blocked.

The rubric is a measurement instrument, not a substitute for reality.

## Trainer Teaching Mode

When teaching another trainer, explain questions using this format:

**Question:** What problem are you solving?

**Why it exists:** What dependency does it resolve?

**Why it comes now:** What downstream work depends on it?

**What counts as evidence:** What source can answer it?

**What bad answer looks like:** What failure mode does it expose?

**What happens next:** What branch does the answer trigger?

This is the core pedagogical behavior of the meta-skill.

## Connection to BlackSwanLabz

The architecture is:

**Human Intent**
→ **Meta-Skill: Why**
→ **Workforce Grant Skill: What**
→ **Evidence Collection**
→ **Occupational Mapping**
→ **Training / Capability Design**
→ **Assessment**
→ **Employer Outcome**
→ **Rubric**
→ **Adversarial Review**
→ **Decision**

The meta-skill protects the system from becoming a checklist.

The workforce skill operationalizes the checklist.

The harness mechanically tests the case.

The Research OS preserves the reasoning, evidence, artifacts, and learned capability.

## Connection to AIL + MoIE

This meta-skill uses the same underlying invariant as BlackSwanLabz research:

1. Identify the assumed axiom.
2. Invert it.
3. Ask what would make the assumption false.
4. Generate competing explanations.
5. Seek discriminating evidence.
6. Verify before propagating the claim.

For workforce training, the hidden axiom is often:

> "This training will produce valuable workforce capability."

Invert it:

> **What evidence would show that this training will NOT produce the claimed workforce capability?**

That inversion drives better trainer questions.

## Adversarial Trainer Tests

A trainer passes the meta-skill when they can detect:

- a training program with no demonstrated employer need;
- an internal job title masquerading as an occupation;
- a curriculum with no observable competency;
- completion being mistaken for capability;
- projected wages being reported as actual wages;
- a placement claim without employer commitment;
- a model-generated claim presented as evidence;
- stale labor-market evidence;
- a mandatory gate hidden inside a scoring category;
- a high rubric score masking a broken causal chain.

## Success Criterion

The trainer is successful when they can answer, for every material question:

> **Why are we asking this, what uncertainty does it resolve, what evidence can answer it, what decision does it unlock, and what happens if the answer is wrong?**

That is the difference between **administering a grant questionnaire** and **operating a governed workforce-development system**.

## Relationship to the Existing Skill

This file is the meta-layer for:

`skills/workforce-grant-readiness/SKILL.md`

It does not replace that skill.

It teaches the reasoning behind it.

**Meta-Skill = Why**

**Workforce Grant Skill = What / How**

**Harness = Mechanical Check**

**Research OS = Persistent System of Record**
