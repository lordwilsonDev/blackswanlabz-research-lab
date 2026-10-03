# FreeBuff Governed Memory & Epistemic Control — Question Blueprint v1.1

> **Status: pending.** This is a design prompt, not a verified system. Nothing here is a
> claim about what exists. It extends *FreeBuff Governed Memory & Epistemic Control
> Blueprint v1.0* (pasted into the session 2026-10-03, not stored in this repo) and the
> PZS Memory Promotion Validator spec v1.0 (`scripts/memory_validator.py` implements part of it).

**What this is.** v1.0 states a design as assertions. v1.1 restates it as questions, because
a question can be answered, falsified, and re-asked after a version change. An assertion can
only be believed. It also adds what v1.0 left out (gap register at the end) and closes with a
meta-question (Part Ω) that loops on the blueprint's own axioms and version logic.

---

## 0. How to run this prompt

Run Parts A → Ω in order. Rules that bind every answer:

1. **Tag every answer** `OBSERVED` (you saw it in a file, log, or test), `INFERRED`,
   `PROPOSED`, or `UNKNOWN`. An unanswerable question is answered `UNKNOWN`. It is never skipped.
2. **Cite evidence** by path/commit/hash, or write `NO_EVIDENCE`. A model's own statement is
   never evidence for itself (`MODEL_PROPOSAL`, not `OBSERVED`).
3. **Name the state it could change.** If an answer cannot change any decision, scope, authority,
   architecture, resource, risk, or memory disposition, mark the question `NO_MATERIAL_IMPACT`
   and stop recursing on that branch.
4. **Fail closed.** Any gate question answered `UNKNOWN` blocks the consequential action it
   guards. Result is `BLOCKED` or `NEEDS_REVIEW`, never `PASS`.
5. **Do not act from this prompt.** It produces decisions and records. Execution needs the
   authority chain of Part F and the transition contract of Part G.
6. **Stamp the run** (see the header below) so any answer can be tied to the exact blueprint
   and axiom-registry versions it was produced under.

```yaml
run:
  id: RUN-YYYY-MM-DD-NNN
  blueprint_version: 1.1.0
  axiom_registry_version: AXR-1
  meta_loop_iteration: 0          # incremented by Part Ω
  root_question: Q-YYYY-MM-DD-NNN
  budget: {max_depth: ..., max_questions: ..., max_cost: ..., max_wall_time: ...}
  actor: {id: ..., role: ..., is_model: true|false}
```

---

## Part A — Objective and necessity (the "why" gate)

- A1. Why are we doing this? State the objective in one sentence. Who selected it, and on what evidence?
- A2. What underlying need does the objective serve? Is the requested *mechanism* the need, or one way to meet it?
- A3. What happens if we do nothing? Is that outcome measurably worse, and by what measure?
- A4. What is the cheapest, safest alternative that meets the same need? Why is it rejected?
- A5. What existing mechanism already covers most of this? (Check the validator, `CLAIMS.md`, the existing FreeBUF causal-audit blueprint, and permanent memory before inventing.)
- A6. What assumption makes this objective necessary? What would make it unnecessary?
- A7. **Anti-performative-work:** would we still do this if we had not already invested in the current approach? If not, raise `SUNK_COST_RISK`. Are we doing it because the framework exists, a model suggested it, the task is interesting, or a previous plan said so?
- A8. **Anti-architecture-theater:** what problem does each proposed component solve, what evidence says that problem exists, and what is the smallest mechanism that could solve it? How will we know it worked?
- A9. What is the success definition, the failure definition, and the decision this work is meant to change?
- A10. Outcome: `CONTINUE`, `REDIRECT`, `DEFER`, `STOP`, or `ESCALATE`? A rejected goal ends execution; a modified goal creates a new question version.
- A11. **Kill criteria:** what observation, by what date, would tell us the memory system does not deliver value, and what do we build instead? (Without this the architecture is self-justifying.)

## Part B — The question object

For the request under analysis, fill all eight slots, tagging each `OBSERVED/INFERRED/PROPOSED/UNKNOWN`:

- B1. **Referent:** what exact object (ID, path, commit) is the question about? Is it resolved or ambiguous?
- B2. **Proposition:** what is being asked, in one falsifiable sentence?
- B3. **Scope:** which system, domain, and boundaries? What is explicitly out of scope?
- B4. **Authority:** who may decide this, from what source, until when?
- B5. **Obligation:** what state transition, if any, is being requested?
- B6. **Time:** when is the question valid (from/until)? Which policy/rubric/schema version applies?
- B7. **Dependencies:** which claims, evidence, decisions, memories, or questions must hold first?
- B8. **Consumption:** what outputs may be produced, and which are forbidden?
- B9. What inferred field did normalization add? Is any silently assumed? Remove or tag it.
- B10. **Speech act:** is each sentence in the input a question, observation, claim, hypothesis, request, decision, authorization, instruction, prohibition, retraction, review, summary, or historical record? Does "use MEM-0007" differ from "MEM-0007 may be relevant" and "MEM-0007 is authorized here"? Preserve the difference.
- B11. **Ambiguity gate:** which words (*current, latest, official, safe, approved, relevant, trusted, production…*) are doing consequential work? For each: what is its operational referent, who defines it, what threshold, valid when? Unresolved → `BLOCKED` / `NEEDS_REVIEW`.
- B12. Which of the 10 integrity properties could normalization have broken: referent, negation, modality, quantifier, scope, time, conditional, exception, source, speech act?

## Part C — Axioms and inversion (AIL)

- C1. Which axiom does the default framing assume? Write it as a sentence a skeptic could deny. Register it as `AX-NNN` (see the seed registry in Part Ω).
- C2. Invert it. What would be true if the opposite held?
- C3. What observable anomaly would exist if the inverse were true? Have we looked?
- C4. What competing explanations fit the same evidence?
- C5. What falsifiable prediction separates the original from each competitor? What is the cheapest test?
- C6. Run the test (or state precisely why it cannot be run now). What was observed?
- C7. Synthesize: which axiom survived, which narrowed, which failed? What did the original question look like before and after?
- C8. Does the inversion replace the original question? (It must not. It exposes the original's failure conditions.)
- C9. Which implicit axioms hide in the words *must, never, always, only, safe, durable, authoritative*?

## Part D — Independent critics (MoIE) and their honest limits

- D1. Which attack surfaces apply: epistemic, linguistic, cybernetic, communication, security, implementation, provenance, **human-factors**, **cost/operations**, **legal/privacy**?
- D2. For each, what does its critic assume, find, cite, and leave unresolved?
- D3. **How independent are these critics really?** Same model, same prompt lineage, same context, same author? Record independence per defect class (code, data, semantic, reasoning, authority, external validity). Same-model critics are contaminated for semantic and reasoning defects; say so rather than counting them as separate votes.
- D4. Did the critics agree, disagree, contradict, or leave open? (No majority vote, no averaging.)
- D5. For each disagreement: same referent? same proposition? different assumption? different evidence? What is the smallest discriminating test?
- D6. Is there a critic who was *not* asked, because no one has the relevant expertise or access? What does that gap imply for authority?
- D7. Has any critic seen the conclusion before critiquing? If yes, downgrade independence.
- D8. What evidence from outside the model family (a human, a test, an external source) is required, and is it available?

## Part E — Evidence, claims, and the firewall

- E1. What is raw evidence, what is observation, what is interpretation, what is claim, and what is decision? Are they stored separately?
- E2. Classify each evidence item: `OBSERVED, DERIVED, INFERRED, REPORTED, EXTERNAL, REPRODUCED, UNVERIFIED, CONTESTED`. Is any model output sitting in a log as if it were observation?
- E3. For each claim: id, proposition, scope, sources, evidence, authority, validity window, status (`PROPOSED, SUPPORTED, QUALIFIED, CONFLICTED, STALE, RETRACTED, INVALIDATED`). Was the status *recorded*, or inferred from file presence?
- E4. What would change a `SUPPORTED` claim to `STALE`? Who watches for that, and how?
- E5. Is the evidence reproducible (command, commit, hash)? Has anyone reproduced it independently?
- E6. Which conclusion rests on a single source? On a source that depends on another source already counted?
- E7. What evidence is missing, and is the decision blocked without it?
- E8. Compression: for any summary used as evidence, what information, modality, scope, or time-meaning was lost? Can the source be reconstructed?

## Part F — Authority, roles, and human decision boundary

- F1. For each action: who **said** it, **verified** it, may **decide** it, may **execute** it, may **consume** it? Roles: asker, proposer, evaluator, verifier, approver, executor, consumer. Which overlap, and is the overlap declared?
- F2. **Approver registry:** who is on the list of identities allowed to approve each state transition? Who maintains it, and who approves changes to it?
- F3. Is any approver a model or model-only process? (Not permitted for `PROMOTE, DELETE, AUTHORIZE, EXECUTE, PUBLISH, GRANT_ACCESS`.)
- F4. **Separation of duties:** may the proposer approve their own proposal? Under what recorded exception?
- F5. **Delegation and expiry:** can authority be delegated? For how long? What revokes it? What happens to decisions made under revoked authority?
- F6. **Authority conflict:** two authorities disagree. Which wins, who decided that rule, and where is it recorded? If nowhere → `AUTHORITY_UNRESOLVED`.
- F7. **Human decision boundary:** is the case an ambiguous objective, authority dispute, policy change, material semantic conflict, high-risk action, or uncertain scope? Then `HUMAN_DECISION_REQUIRED`, with no hidden confidence score standing in.
- F8. When uncertainty rises, does authority fall? Show where in the process that happens.
- F9. **Review fatigue:** how many decisions per reviewer per cycle? What is the error rate vs. load? Is a decision being rubber-stamped?
- F10. How is a reviewer's disagreement with the rubric captured without silently overriding it?

## Part G — State transitions, atomicity, and recovery

- G1. For each action: from-state, to-state, actor, authority source, question id, evidence refs, preconditions, postconditions, rollback, consumption policy. Is any missing? Then there is no transition.
- G2. Is `CREATED` distinguished from `VALIDATED`, `AUTHORIZED`, `CONSUMABLE`? Can an `ACTIVE` memory be `STALE`, `VALID` yet `OUT_OF_SCOPE`, `PROMOTED` yet `CONFLICTED`?
- G3. **Atomicity:** if the process dies between "write MEM" and "update disposition", what state is left? Is it detectable and repairable? What is the transaction boundary?
- G4. **Idempotency:** what happens if the same transition is submitted twice? Is the second a no-op, an error, or a duplicate?
- G5. **Concurrency:** two actors transition the same item at once. What locks, versions, or compare-and-set rules decide? What does the loser see?
- G6. **Source of truth:** is the append-only event log authoritative, with notes/INDEX/STATS derived? Can all derived state be rebuilt from events? What is `RECONSTRUCTION_FAILURE` and who is asked why?
- G7. **Rollback:** for each transition, what undoes it, who may undo it, and what cannot be undone?
- G8. **Degraded mode:** when the validator, retrieval, or a tool is unavailable, what may proceed (read-only?) and what must halt? Is there a kill switch, and who holds it?
- G9. **Backup and disaster recovery:** what is backed up, how often, where, and when was a restore last *tested*?
- G10. **Clock trust:** which timestamps are trusted, from which clock? What happens with skew, backdating, or a clock set forward to expire a review?

## Part H — PZS integration and vocabulary reconciliation

- H1. FreeBuff owns the decision process, PZS the memory lifecycle. Show where a FreeBuff decision becomes a PZS disposition. Can FreeBuff write permanent memory any other way? (It must not.)
- H2. **Vocabulary:** v1.0 says `SUPERSEDE`/`KEEP`/`M-*`/`D-*`(decision) and `D-NNN`(defect). PZS says `SUPERSEDED`/`KEEP_COMPLETED`/`MEM-*`. Which vocabulary is authoritative, and where is the mapping recorded? Rename the defect class prefix (proposed `DEF-NNN`).
- H3. Should every non-trivial disposition (`PROMOTE, MERGE, SUPERSEDED, REJECT`) carry a `decision_id` that resolves to a decision with question id, authority, evidence, proposer, approver, `model_generated` flag? How does the validator enforce it?
- H4. Is there a status mapping between FreeBuff states (`VALIDATED, AUTHORIZED, CONSUMABLE`) and PZS states (`ACTIVE, SUPERSEDED, DEMOTED`)? Where does `STALE` live?
- H5. **Policy governance:** who may change the promotion rubric, thresholds (80% mix alert, 14-day review, verify intervals), or the disposition enum? How is that change versioned, and what happens to decisions made under the old rubric?
- H6. **Schema evolution:** when frontmatter or event schemas change, how are old records migrated, and how is a consumer told its schema is stale?
- H7. Where does this blueprint's content overlap the existing FreeBUF causal-audit blueprint? Which is authoritative where they differ?

## Part I — Promotion, minimality, retrieval, and feedback

- I1. Why might this completed item deserve permanence? What durable knowledge exists? What is merely historical? What evidence supports each knowledge unit?
- I2. Are we preserving **knowledge** or preserving **narrative**? What is the smallest durable representation? What would be lost if it were not preserved, and could it be reconstructed instead?
- I3. Decompose the candidate: core knowledge, provenance, context, limitations, history. Which part belongs in permanent memory?
- I4. If the memory is stale, what breaks? If it is wrong? If it conflicts with another?
- I5. Which future decision would this memory influence, and how will we know it did? (A memory that never changes a future action is trivia.)
- I6. **Projection loss:** record source size, memory size, knowledge units before/after, semantic deltas, explicit exclusions. Did any negation, modality, quantifier, scope, or time meaning change?
- I7. **Retrieval:** why retrieve this memory now? Is it relevant to this scope, current enough, from an authoritative source, and is *this consumer* allowed to use it? What evidence would make us stop using it?
- I8. Does retrieval resolve supersession chains to the active head, exclude superseded/demoted by default, expose provenance and verification status, and flag staleness?
- I9. **Feedback:** after use, was it not used / used successfully / unsuccessfully / irrelevant / stale / conflicting? Recorded where, tied to which question?
- I10. Negative feedback: was the source wrong, memory stale, scope too broad, projection lossy, retrieval wrong, consumer unauthorized, or the original decision wrong? Investigate the class; do not just edit the memory.
- I11. **Conflict:** two active memories disagree. Compare referent, scope, time, source authority, evidence, proposition. Outcome: A supersedes B / both valid in different scopes / one invalid / unresolved. No majority vote.
- I12. **Demotion:** what evidence triggers it, who decides, where does the record go, and what learning event does it create?
- I13. **Cold start:** how are the first memories judged with no usage history? What replaces retrieval-utility data until it exists?
- I14. **Forgetting and retention:** when may memory be deleted for privacy, legal, or hygiene reasons? How does that coexist with "no silent deletion" and with redactions (AGENTS.md)?

## Part J — Messages, transport, and versions

- J1. For each consequential message: sender, receiver, channel, encoding, version, scope, timestamp, sequence number, payload hash, authority, evidence refs, consumption policy. Which fields are missing?
- J2. Which failures can occur here: loss, duplication, replay, reordering, truncation, mutation, ambiguity, context loss, version mismatch, authority loss, scope loss, semantic drift? What detects each? Show a mutation test per class.
- J3. If "may promote after verification" arrives as "may promote", does anything detect it?
- J4. **Version semantics:** is Q-001 v7 ever silently consumed as v8? What marks v7 `INVALIDATED`, and what must a consumer do on seeing it?
- J5. At each cross-tool boundary (PZS → Claude / Hermes / MCP): which system is authoritative, which are replicas, what may diverge, who wins on conflict, who authorized that rule? If unanswered → `SOURCE_OF_TRUTH_UNRESOLVED`.
- J6. How are delivery, integrity, version, semantic fidelity, authority fidelity, and retrieval behavior monitored?

## Part K — Security and adversarial conditions

- K1. **Prompt injection through memory:** can stored text instruct a consuming model? Is memory content treated as data, never instruction? What proves it?
- K2. **Memory poisoning:** how could an adversary or a plain mistake insert a false memory that passes the gates? Which gate stops it?
- K3. **Authority leakage:** can a memory, summary, or model output carry authority it was never granted?
- K4. **Access control:** who may read, write, promote, demote, and retrieve, per sensitivity level? Are redacted `[prospect]`/`[company]` items protected from recovery?
- K5. **Secrets and personal data:** can any note, log, or event contain credentials or personal data? How is that detected and removed without violating append-only rules?
- K6. **Replay and rollback attacks:** can an old valid event, approval, or version be re-submitted to reverse a later decision?
- K7. **Insider and compromised-reviewer cases:** what limits the damage of one bad approver? Is there a second signature for the highest-impact transitions?
- K8. **Supply chain:** which tools, models, and dependencies can alter state, and what verifies their outputs (tool-result contract: tool, version, request id, input/output hash, status, errors)?
- K9. **Model output contract:** is each model output classified `MODEL_PROPOSAL/INTERPRETATION/SUMMARY/CLASSIFICATION/CODE` and never promoted to fact, authorization, truth, or policy without a separate verification step?

## Part L — Observability, health, and cost

- L1. What does each run record: root question, questions generated, inversions, experts, disagreements, tests, evidence, transitions, memory updates, feedback, depth, closure reason?
- L2. Which metrics are tracked **separately** (never one score): resolution rate, decision reversal, defect discovery, novel defect rate, evidence coverage, semantic preservation, authority leakage, memory utility, staleness detection, projection loss, retrieval failure, reviewer disagreement, recursion depth, recursive yield, question cost, decision impact?
- L3. **Question debt:** how many questions are open, blocked, expired, ownerless, or no longer able to change state? Is the backlog growing?
- L4. **Goal drift:** original vs. current vs. final objective — unchanged, refined, narrowed, broadened, replaced, abandoned? Was each change recorded?
- L5. **Architecture drift:** do question contract, approved design, implementation, tests, and docs still agree?
- L6. **Cost and capacity:** what does a governed run cost in time, tokens, and reviewer hours? What is the budget, and what happens when it is exceeded (`RECURSION_LIMIT_REACHED`, not `PASS`)?
- L7. Service levels: what latency and availability are required of retrieval vs. promotion, and who is paged when they fail?
- L8. What alerts are *alerts*, and which are *failures*? Who owns each, and by when must it be acted on?

## Part M — Verifying the verifier

- M1. What does each detector assume, which defect classes can it catch, which can it not, and could it share the blind spot of the thing it checks?
- M2. Does each critical test actually **exercise** its target (imported, executed, observed, mutation reached)? If not: `TEST_NOT_EVIDENCE`.
- M3. For every feature: positive test, negative control, mutation test, integration test, reconstruction test. For governance checks additionally: authority attack, stale-state attack, replay attack, semantic mutation, scope mutation, version mutation.
- M4. Are all mutation classes covered and detected: remove check, bypass authority, drop provenance, alter negation/modality/scope/time/version/source, replay/drop/duplicate/reorder event, drop knowledge unit, bypass retrieval or consumption gate?
- M5. Who verifies the verifier? What independent challenge exists (Level-5 question), and what is its independence class?
- M6. **Blind-spot inventory:** what is open, tested, closed in `state/BLIND_SPOTS.yaml`? Does "no new defect found" get reported as such, and never as "all defects exhausted"?
- M7. Could the validator return a false `PASS`? Which negative control would expose it?
- M8. **Closure of the validator:** implementation passes AND negative controls pass AND required mutations detected AND self-tests pass AND reconstruction works AND blind spots documented AND independence limits documented?

## Part N — Tool and model selection

- N1. What capability, evidence source, and authority boundary does the task need, before naming any tool?
- N2. Which tool has that access, what failure modes does it add, what can observe it?
- N3. Is the model a replaceable component here? What breaks if it is swapped, and how is that detected (version-pinned behavior tests)?
- N4. What is the cost/benefit of using a model vs. a deterministic check for this step? Prefer the deterministic check wherever one exists.

## Part O — Build sequencing, acceptance, and the human system

- O1. What is the smallest slice that tests the central claim (a question-driven loop can convert completed work to durable, useful memory without laundering uncertainty into authority)? Build only that first.
- O2. What are the acceptance criteria for each slice, written as checks a machine can run?
- O3. What does the bootstrap migration (batches of ~10) measure, and what result would stop the program?
- O4. Which modules from v1.0's tree are justified by evidence today, and which are speculative? Defer the speculative ones with a written reason.
- O5. Who maintains this, who is on call, and what is the handover procedure if the author is unavailable?
- O6. Who is the user of the memory (person, agent, both)? What did they ask for, and have they confirmed this solves their problem?
- O7. What training or documentation does a reviewer need to apply the rubric consistently? How is judgment drift measured against a fixed sample?
- O8. What is deliberately *not* governed (exploratory thinking is open-ended; actions are not)? Where is that line written?

## Part P — Closure, recursion limits, and outcomes

- P1. Is `RECURSIVE_CLOSURE` met: no unresolved contradiction, no material unanswered why, no blocking dependency, no authority ambiguity, no unbounded semantic ambiguity, and the next question would not change decision or state?
- P2. If not, what is the next question? Score it on novelty, discrimination, decision impact, testability, cost (dimensions kept separate).
- P3. What is the information gain: which uncertainty, decision, or transition would the answer change? If none → `DEFER`, `MERGE`, or `DROP`.
- P4. Was a budget bound hit? Then the result is `RECURSION_LIMIT_REACHED` → `BLOCKED` or `NEEDS_REVIEW`. Never convert unfinished recursion into approval.
- P5. Closure reason: `CLOSED_BY_EVIDENCE / DECISION / AUTHORITY / SCOPE / RESOURCE / INDEPENDENCE_LIMIT / POLICY / NO_MATERIAL_NEXT_QUESTION`. (Never just "done".)
- P6. Outcome class: `CONFIRMED, PARTIALLY_CONFIRMED, FAILED, BLOCKED, REVERSED, SUPERSEDED, UNRESOLVED, NO_EFFECT, UNEXPECTED_EFFECT`. Which diagnostic question does a non-success outcome generate?
- P7. Error class this loop: `NO_ERROR, SCOPE, MODEL, EVIDENCE, AUTHORITY, IMPLEMENTATION, COMMUNICATION, TEMPORAL, MEMORY, OBJECTIVE`. Did we execute the wrong task correctly (`OBJECTIVE_ERROR`)?

---

## Part Ω — The meta-question (recursive loop on axioms and version logic)

Everything above rests on assumptions and exists in a version. Part Ω asks whether
those assumptions still hold and what a change to them invalidates. It feeds its result
back to Part A under a new version. It is the only part allowed to modify this prompt.

### Ω0. Seed axiom registry (AXR-1)

Each axiom is a sentence a skeptic can deny. Register more as C9 and Ω1 surface them.

| ID | Axiom assumed by this blueprint | Inversion to test |
|---|---|---|
| AX-001 | Asking structured questions before acting improves decisions. | Structured questions add cost and delay without changing decisions. |
| AX-002 | Completed work and durable memory are different states. | A single archive with good retrieval beats a promotion pipeline. |
| AX-003 | Permanent memory improves future work. | Permanent memory degrades future work (stale, duplicate, bias-amplifying). |
| AX-004 | When uncertainty rises, authority should fall. | Uncertain situations call for *more* delegated authority (faster correction). |
| AX-005 | Multiple independent critics find defects one path misses. | Critics from one model family share blind spots and add false assurance. |
| AX-006 | Feedback from use is a valid signal of memory value. | Usage reflects availability or habit, not value. |
| AX-007 | Derived state should be reconstructible from events. | Reconstruction cost exceeds its value; snapshots suffice. |
| AX-008 | Recursion should stop when no next question can change a decision. | Material questions exist that no one knows to ask. |
| AX-009 | Failing closed is better than failing open. | Fail-closed gates stall work until people bypass them. |
| AX-010 | Provenance and meaning survive summarization and transport. | They do not, and detection is weaker than assumed. |
| AX-011 | A version number identifies a unique, stable meaning. | The same version is read differently by different consumers (`SEMANTIC_DRIFT`). |
| AX-012 | Re-asking this meta-question improves the blueprint. | The loop optimizes for self-consistency, not for truth or usefulness. |

### Ω1. Enumerate

- Ω1.1. Which axioms does *this version* of the blueprint actually rely on? List the registry entries **plus** every implicit one found by scanning for *must, never, always, only, safe, durable, authoritative, independent*. Which have no `AX-` ID yet?
- Ω1.2. Which part (A–P) depends on each axiom? Build the dependency map axiom → parts → decisions → memories → claims.

### Ω2. Invert and test (AIL, applied to the blueprint itself)

For each axiom:

- Ω2.1. State the inverse. What would we observe if the inverse were true?
- Ω2.2. What evidence do we already hold for and against? Tag `OBSERVED/INFERRED/UNKNOWN`. (Evidence for AX-003, AX-006, and AX-010 is `UNKNOWN` until the bootstrap migration produces data.)
- Ω2.3. What is the cheapest falsifying test, and who other than the author can run it?
- Ω2.4. Result: `SURVIVED`, `NARROWED`, `FAILED`, or `UNTESTED`. Is `UNTESTED` allowed to carry weight in any gate? (Default: no.)

### Ω3. Version logic

- Ω3.1. **What is a version here?** Which artifacts carry versions (blueprint, axiom registry, rubric, schemas, questions, decisions, memories), and what is the rule that bumps each?
- Ω3.2. **Classify the change set** from Ω2:
  - *Patch* — wording only; no axiom, gate, or schema changed.
  - *Minor* — added question/axiom/check; no existing decision's validity depends on it.
  - *Major* — an axiom `FAILED` or `NARROWED`, or a gate/schema/vocabulary changed.
- Ω3.3. **Invalidation set.** For a Major change, which decisions, memories, claims, and questions depended on the changed axiom? Mark each `INVALIDATED` (not deleted) and queue a re-review question. Who is notified, and what must a consumer do on seeing `INVALIDATED` (J4)?
- Ω3.4. **Compatibility.** Can a consumer on v_n safely read v_(n+1) output? If not, is it refused explicitly rather than silently misread?
- Ω3.5. **Provenance of the change.** Which axiom, which test, which evidence, and which authority (F2) produced v_(n+1)? Could the author alone have approved it? (If yes and the change is Major → `HUMAN_DECISION_REQUIRED`.)
- Ω3.6. **Replay and rollback.** Can v_(n+1) be reverted to v_n by replaying an old approval? What prevents it, and what record shows the revert?

### Ω4. Produce the next version

- Ω4.1. Write v_(n+1): the diff, the new axiom registry (`AXR-(k+1)`), and the invalidation set.
- Ω4.2. **Self-reference check.** Does the Ω loop itself (this very section) rest on any axiom that changed? If so, v_(n+1) must change Ω too, and the new Ω has not been run yet. Say so and run it.
- Ω4.3. Increment `meta_loop_iteration` and re-stamp the run header.

### Ω5. Recurse (the loop)

> **Ω★ — Given the axioms that this version of the blueprint rests on, and the version
> logic that decides what each change invalidates: which axiom, if inverted, would change
> the most decisions — and does recording that answer require a new version whose own
> axioms must be put through this same question?**

Apply Ω★ to v_(n+1), then v_(n+2), and so on. At each pass answer:

- Ω5.1. Is the change set from Ω2 empty across **all** required attack surfaces, and for a second pass by a critic that did not see the first pass's conclusion?
- Ω5.2. **Oscillation / ABA check.** Does v_(n+2) equal v_n (an axiom flipped and flipped back)? Is any axiom changing status repeatedly? Then the loop is unstable, so stop and escalate. Do not accept it as convergence.
- Ω5.3. **Fixed point is not truth.** If v_(n+1) = v_n, the system is *self-consistent under its own tests*. Does that tell us the axioms are correct, or only that this loop cannot find the defect? Record `NO_NEW_DEFECT_FOUND`. Never record `ALL_DEFECTS_EXHAUSTED` without evidence from an authority outside the loop.
- Ω5.4. Which axiom can this loop **not** test from the inside (it supplies its own criteria for testing itself: AX-005, AX-008, AX-012 in particular)? Which independent authority or external observation must test it? Name it. If none exists → `CLOSED_BY_INDEPENDENCE_LIMIT` and `HUMAN_DECISION_REQUIRED`.
- Ω5.5. **Budget.** Depth, cost, question count, wall time used? If any bound is hit with a nonempty change set → `RECURSION_LIMIT_REACHED` → `BLOCKED`/`NEEDS_REVIEW`. The bound is a safety stop and never a verdict.
- Ω5.6. **Yield.** Did this pass produce a changed decision, scope, objective, new evidence, or new defect class? A pass that only restates is low-yield; if two consecutive passes are low-yield, close with `CLOSED_BY_NO_MATERIAL_NEXT_QUESTION` and the caveat in Ω5.3.

### Ω6. Return to the start

- Ω6.1. Closure reason (P5): which one, and who (authority) accepted the closure?
- Ω6.2. Go back to **A1** under the new version stamp: *Why are we doing this?* If the answer, or the evidence behind it, is different from the last pass, a new root question `Q-…` is opened at version +1. If it is the same, record why it is still the same.
- Ω6.3. **Ω-final.** Why are we building this memory system at all? What capability does it make possible? Does that capability justify its complexity, risk, and upkeep? What evidence would show that it does not? What do we build instead if it fails? Answer from the latest evidence, never from the previous pass's answer.

> The loop ends only by a recorded closure reason and an authority that accepted it. It
> does not end because a pass felt complete or because the budget ran out.

---

## Gap register (what v1.1 adds to v1.0)

Each gap is the question v1.0 could not answer.

| Gap | Question v1.0 left open | Where |
|---|---|---|
| Necessity evidence | What evidence says the problem exists; what are the kill criteria? | A5, A8, A11 |
| Critic independence | Are same-model critics independent? | D3, D7, D8, M5 |
| Approver identity | Who exactly may approve, and who edits that list? | F2–F5 |
| Review fatigue and bias | What happens to decision quality under load? | F9, F10, O7 |
| Atomicity, idempotency, concurrency | What state is left after a crash, a double-submit, or a race? | G3–G5 |
| Source of truth and rebuild | Is the event log authoritative; can state be rebuilt? | G6, J5 |
| Degraded mode, kill switch, DR | What halts, what continues, was restore tested? | G8, G9 |
| Clock trust | Can time be spoofed to expire or backdate a decision? | G10 |
| Vocabulary and ID collisions | `SUPERSEDE` vs `SUPERSEDED`, `D-*` twice, `M-*` vs `MEM-*` | H2–H4 |
| Decision-to-disposition link | Does a `decision_id` bind every disposition? | H3 |
| Policy and schema governance | Who changes the rubric/thresholds/schema, and what happens to old decisions? | H5, H6 |
| Overlap with existing blueprint | What does FreeBUF causal-audit v3 already cover? | H7 |
| Cold start | How are early memories judged with no usage data? | I13 |
| Retention, deletion, privacy | How does forgetting coexist with append-only and redactions? | I14, K5 |
| Prompt injection and poisoning | Can memory instruct or corrupt a consumer? | K1, K2 |
| Access control and insiders | Who can read/write/promote; what limits one bad approver? | K4, K7 |
| Replay/rollback of approvals | Can an old approval reverse a newer decision? | K6, Ω3.6 |
| Cost, capacity, SLOs, ownership | What does it cost, who is paged, who maintains it? | L6–L8, O5 |
| Smallest slice and acceptance | What is built first, and how is "done" checked? | O1–O4 |
| Axiom registry | Which assumptions does the blueprint rest on, and are they tested? | Ω0–Ω2 |
| Version logic | What does a change invalidate, and can a consumer detect it? | Ω3 |
| Self-reference and loop stability | Can the loop fool itself, oscillate, or call a fixed point truth? | Ω4.2, Ω5.2–Ω5.4 |

*Not verified: no claim in this file is established until it appears as a `verified` row in `CLAIMS.md`.*
