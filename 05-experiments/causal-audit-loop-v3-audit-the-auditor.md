---
source: authored in this repository (commit 2fcb5f3, 2026-10-03): FreeBuff causal-audit loop v3 blueprint; original working location not recorded
captured: 2026-10-03
status: pending
---

# FREEBUF CAUSAL-AUDIT LOOP v3
## Audit the Auditor — Independence, Retraction, Weighting, and Stop/Freeze

### Status

**Purpose:** close the current causal-audit cycle without inventing another experiment.

**Current scientific state:** the prior matched-strata claim is narrow and pending final closure. The next action is an I2-CM reconstruction from the frozen package, after the target-2 inclusion-rule amendment is frozen and the claim ledger is written.

**I3 is the lab ceiling. Do not treat it as an open task.**

---

# 0. WHY THIS VERSION EXISTS

The previous cycle established a load-bearing matched-strata accuracy difference in a small synthetic referential world, but the inverse audit found that the pipeline had not demonstrated independence between the original analyst and the recomputation.

The lab has now defined a four-level independence ladder:

| Level | Definition |
|---|---|
| **I1** | Code separation — no shared imports |
| **I2** | Reasoning separation — different author's model of the estimand |
| **I2-CM** | Cross-model reconstruction — a different model receives only the frozen package and reconstructs the estimand/results |
| **I3** | External review — different operator with independent priors |

**I3 is the lab ceiling and is unreachable by design. It is not a missing task.**

This blueprint therefore treats the current work as a closure problem:

> **Can the narrow claim survive cross-model reconstruction, while the inclusion rule, weighting interpretation, retractions, provenance, and stopping boundary remain explicit?**

---

# 1. CORE QUESTION

> **Does the claim C-B8-001 deserve to move from PENDING to an appropriate evidence status after the target-2 inclusion rule is frozen, the existing frozen rows are recomputed under that rule, and a cross-model I2-CM analyst independently reconstructs the claim from the frozen package without receiving the prior report or estimand?**

Do not broaden the claim.

Do not reopen the experimental substrate unless an existing artifact fails.

Do not add new strata, new weighting schemes, or new instrumentation merely to reduce residual uncertainty in the estimate.

---

# 2. CURRENT CLAIM

Record exactly:

```
CLAIM_ID:        C-B8-001
CLAIM:           Relevant message produces higher referential accuracy than a
                 matched irrelevant message in a 3-object synthetic referential
                 world, at rho=1.0 and T=1.0.
ESTIMATE:        +0.578333 before final target-2 inclusion-rule amendment
WORLD:           synthetic, 3 objects, 2-3 attributes,
                 fingerprint 882027e856db
PARAMETERS:      rho_channel=1.0, temperature=1.0
SCOPE:           This world. These parameters. No claim about real settings.
STATUS:          PENDING
EVIDENCE:        06_RAW_ROWS.jsonl, per-target strata
INDEPENDENCE:    I1 present, I2 absent, I2-CM pending, I3 ceiling
RETRACTIONS:     +0.6021, +0.3756, prior Level-3 label,
                 preservation claim, harness-null interpretation
BOUNDARY:        null world collapses to +0.0042; one-attribute messages
                 contract from +0.774 to +0.376; target-2 inclusion rule pending
NEXT STEP:       Freeze amendment → recompute → I2-CM → close
```

The estimate must NOT be treated as final until the target-2 inclusion rule amendment is frozen and applied to the already-collected data.

---

# 3. IMMEDIATE NEXT MOVE

Execute exactly this sequence:

```
existing frozen raw rows
        ↓
freeze target-2 inclusion rule amendment
        ↓
apply amendment to existing data
        ↓
independent recomputation of C-B8-001
        ↓
update claim ledger
        ↓
I2-CM blind reconstruction
        ↓
close cycle
```

This is closure of the existing experiment.

It is NOT a new scientific experiment.

---

# 4. TARGET-2 INCLUSION RULE AMENDMENT

Target 2 is the known edge case where `red square` can partially match multiple objects.

Before claim closure:

1. write the inclusion/exclusion rule explicitly;
2. state why the rule is required;
3. record that the rule is an amendment to the preregistration;
4. preserve the original preregistration;
5. apply the amended rule to the existing frozen rows;
6. recompute the affected estimate.

Do not collect new observations.

Do not select the rule based on which result is preferred.

The rule must be justified from the construct definition, not from the resulting estimate.

---

# 5. RETRACTION PRESERVATION

Every earlier interpretation remains visible.

At minimum preserve:

- original headline result;
- corrected result;
- defect ID;
- date/version;
- affected analysis;
- reason for retraction;
- what remains valid.

Required states:

```
ORIGINAL
→ CORRECTED
→ RETRACTED or QUALIFIED
→ CURRENT
```

Never overwrite a retracted claim.

A corrected result is not a reason to delete the incorrect one.

---

# 6. THE INDEPENDENCE LADDER

## I1 — Code separation

A separate code path exists with no shared imports.

This establishes implementation separation only.

## I2 — Reasoning separation

A different author independently constructs the estimand, grouping, conditioning, weighting, and interpretation.

This is not currently established.

## I2-CM — Cross-model reconstruction

A different model receives only the frozen package:

- raw rows;
- construct;
- model;
- world fingerprint;
- required evidence metadata.

It does NOT receive:

- the prior report;
- the prior estimate;
- the original estimand wording;
- the original interpretation;
- expected numerical output;
- post-hoc explanations.

The cross-model analyst independently determines:

1. what claim is being tested;
2. what estimand is appropriate;
3. which rows belong;
4. how strata should be formed;
5. how the gap should be computed;
6. what conclusion is justified.

**I2-CM is second-analyst evidence, not external validation.**

## I3 — External review

Different operator with independent priors.

I3 is the lab ceiling.

Do not create work whose purpose is to reach I3.

A completed I2-CM result is a valid stopping point.

---

# 7. BLIND I2-CM PACKAGE

The I2-CM package must contain only what is necessary to reconstruct the claim.

Required:

```
06_RAW_ROWS.jsonl
02_CONSTRUCT.md
03_MODEL.md
world fingerprint
data/schema description
question under audit
scope constraints
```

Not included:

```
09_FINDINGS.md
prior report
expected +0.578333
previous interpretation
previous p-values
previous retractions
original recomputation script
```

The purpose is to test whether a second model can independently recover the estimand rather than reproduce the first model's framing.

---

# 8. I2-CM OUTPUT CONTRACT

The cross-model analyst must return:

### A. Reconstructed question

What it believes the data can establish.

### B. Reconstructed estimand

Exact formula.

### C. Included rows

How rows were selected.

### D. Strata

How matched strata were identified.

### E. Weighting rule

Exactly how the aggregate estimate was formed.

### F. Estimate

Independent numerical result.

### G. Uncertainty

Appropriate uncertainty measure.

### H. Interpretation

What the estimate means within scope.

### I. Alternative explanation

At least one plausible competing mechanism.

### J. Falsifier

What observation would overturn the interpretation.

### K. Independence statement

What information was unavailable to the cross-model analyst.

---

# 9. ESTIMAND RECONSTRUCTION

Do not assume the previously named `+0.6021` or `+0.578333` is automatically the correct estimand.

Ask:

> **What population is this estimate intended to represent?**

Possible estimands include:

- equal weight across matched strata;
- observed-sample-weighted effect;
- fixed target-population effect;
- per-target paired effect.

Only use an estimand that can be justified from the preregistered design or the explicit amendment.

If multiple defensible estimands exist:

> **freeze one for the claim and label the others as sensitivity descriptions, not competing hidden primary answers.**

Do not keep generating weighting schemes.

---

# 10. NO MORE TIGHTENING RULE

After the amended inclusion rule is applied:

- do not add new strata;
- do not add new weighting schemes;
- do not add new matched controls;
- do not add new instrumentation;
- do not search for a more favorable aggregation.

The current cycle's purpose is:

> **claim closure, not estimate optimization.**

If the magnitude remains uncertain but the sign is stable under the already-defined analysis:

> freeze the sign and mark magnitude UNDETERMINED.

Do not turn unresolved magnitude into a reason for indefinite analysis.

---

# 11. PIPELINE-SENSITIVITY STATUS

The prior pipeline-sensitivity harness failed its null check.

That failure is itself the result.

Do not rebuild it in this cycle unless the existing frozen artifact cannot be interpreted.

Record:

> **PIPELINE-SENSITIVITY HARNESS: FAILED NULL CHECK — RETAINED AS A NEGATIVE RESULT.**

Do not relabel the failure as an opportunity for another instrument-building cycle.

---

# 12. WHO SAYS IT IS RIGHT?

The answer must specify the actual evidence layer.

For C-B8-001 report:

### Level 1
Definition.

### Level 2
Implementation.

### Level 3
Unit-test validation.

### Level 4
Observed experimental result.

### Level 5
Independent recomputation.

### Level 6
Adversarial/cross-model challenge.

Then identify the achieved independence level:

```
I1
I2
I2-CM
I3
```

Never equate Level 6 with I3.

Never equate I2-CM with external research.

---

# 13. WHO CAN SAY WE ARE WRONG?

This must be explicit.

For the current cycle:

> **I2-CM is the maximum available challenge mechanism.**

The I2-CM analyst may:

- fail to recover the estimate;
- recover a different estimand;
- identify an invalid inclusion rule;
- identify an aggregation error;
- weaken the interpretation;
- reproduce the claim;
- identify a previously missed confound.

If I2-CM disagrees:

> investigate and classify the disagreement.

Do not automatically declare the original analyst wrong.

Do not automatically declare the cross-model analyst right.

Determine the reason for disagreement from the frozen evidence.

---

# 14. WINDOW

The current claim-closure window is:

> **One closure cycle over the frozen dataset, ending after the amended inclusion rule has been recomputed and the I2-CM reconstruction has been frozen.**

No new experimental observations belong inside this window.

Q-B8-001 has no current execution window.

It remains:

> OPEN / UNSCHEDULED

---

# 15. Q-B8-001

Preserve the generated open question:

> **Given that relevance matters most when it actually discriminates (the target-2 moderator effect), what happens when discriminator strength is varied across a controlled range while target identity and message length are held constant, what observation would distinguish a genuine moderator effect from a target-composition artifact, when will we observe it (TBD, next cycle is not scheduled), who will observe it (I2-CM at most), and what observation would prove it wrong (no monotonic relationship between discriminator strength and gap)?**

This question is NOT to be answered in the present closure cycle.

It is a future entry point only if the lab deliberately opens a new cycle.

---

# 16. QUESTION-ENGINEERING REQUIREMENTS

Every future question must specify:

### Variable

What is changed?

### Held constant

What is prevented from changing?

### Window

When will the answer be observed?

### Auditor

Who or what will observe it?

### Independence level

I1, I2, I2-CM, or I3 ceiling.

### Falsifier

What observation would disconfirm the answer?

### Evidence boundary

What will the result NOT establish?

A question missing any required field is:

> **INCOMPLETE**

An unanswered question that cannot yet be scheduled is:

> **OPEN / UNSCHEDULED**

---

# 17. CHAOS TEST

For every load-bearing claim ask:

### Mathematical
Could the result be an identity?

### Structural
Could the environment force the result?

### Measurement
Could the statistic be incorrectly calculated?

### Conditioning
Does stratification change the result?

### Control
Does the control instantiate the intended null?

### Implementation
Could the code manufacture the result?

### Reproducibility
Does the exact frozen data reproduce it?

### Independence
Can a second analyst recover it without inherited framing?

### Interpretation
Does the evidence support the claimed mechanism?

### Scope
Is the claim being generalized beyond the world that generated it?

The strongest result is not the one that survives the most p-values.

It is the one that survives the most credible attacks.

---

# 18. CLAIM STATUS RULE

After amendment + recomputation + I2-CM, assign one status:

```
OBSERVED
REPRODUCED
SUPPORTED
SUGGESTIVE
UNDERPOWERED
NOT_DISCRIMINATING
FALSIFIED
RETRACTED
QUALIFIED
BOUNDARY_CONDITION
UNRESOLVED
SELF_AUDITED
I2-CM_RECONSTRUCTED
I3_EXTERNALLY_REVIEWED
```

Do not use a stronger status than the achieved evidence level permits.

---

# 19. FINAL CLOSURE QUESTION

Before declaring the cycle closed, answer:

> **Did we resolve a live scientific uncertainty, or did we merely improve documentation of an already-frozen result?**

Then answer:

> **Did the I2-CM analyst independently reconstruct the claim, or did it inherit the original framing?**

Then answer:

> **Did the target-2 amendment change the claim?**

Then answer:

> **Is additional work capable of discriminating a live explanation, or would it only refine a frozen quantity?**

If the latter:

> STOP.

---

# 20. STOPPING RULE

The cycle terminates when all of the following are true:

1. target-2 inclusion rule is frozen;
2. existing raw data are recomputed under that rule;
3. claim ledger is updated;
4. retractions remain visible;
5. I2-CM is completed or explicitly unavailable;
6. I3 is recorded as the ceiling;
7. Q-B8-001 remains OPEN / UNSCHEDULED;
8. no live explanation requires another test inside this cycle.

Do not add another experiment merely because an unresolved number remains.

The finding justifies the work.

The work does not justify more work.

---

# 21. REQUIRED ARTIFACTS

Create or update:

```
01_QUESTION.md
02_CONSTRUCT.md
03_MODEL.md
04_EXPERIMENT.md
05_RESULTS.json
06_RAW_ROWS.jsonl
07_RECOMPUTATION.md
08_CHAOS_REVIEW.md
09_FINDINGS.md
10_NEXT_QUESTION.md

audit/
    independence.md
    weighting.md
    retractions.md
    i2cm_reconstruction.md

amendments/
    target2-inclusion-rule.md

retractions/
    index.md

pre_fix/
post_fix/

CHECKSUMS.txt
REPORT.md
```

The exact file layout may differ if the existing repository has an established structure, but the evidence relationships must remain explicit.

---

# 22. FINAL RESEARCH PRINCIPLE

The laboratory has now learned an important distinction:

```
well documented
        ≠
independently recomputed

independently recomputed
        ≠
independently reasoned

cross-model reconstruction
        ≠
external research

checksum verified
        ≠
scientifically correct

large signal
        ≠
strong explanation
```

The purpose of this cycle is not to make the result look stronger.

It is to establish exactly how strong it is.

---

# 23. CLOSURE STATE MACHINE

```
PENDING
   ↓
AMENDMENT_FROZEN
   ↓
RECOMPUTED
   ↓
I2-CM_REQUESTED
   ↓
I2-CM_RECONSTRUCTED
   ↓
CLAIM_CLASSIFIED
   ↓
CYCLE_CLOSED
```

Alternative paths:

```
RECOMPUTED
   ↓
RETRACTED

I2-CM_RECONSTRUCTED
   ↓
DISAGREEMENT
   ↓
INVESTIGATE
   ↓
RETAIN / QUALIFY / RETRACT
```

At the ceiling:

```
I2-CM
   ↓
I3 CEILING REACHED
   ↓
STOP
```

Do not create an artificial I4.

---

# 24. FINAL QUESTION

Before closing the cycle, generate one answer to:

> **What did this cycle make independently knowable that was not independently knowable before it began?**

If the answer is:

> “Nothing; it only improved documentation.”

then record that honestly.

If the answer is:

> “The claim survived cross-model reconstruction under a frozen amendment and remains valid within the stated synthetic scope.”

then record that.

Either result closes the cycle.

---

# FINAL DIRECTIVE

**FREEZE THE AMENDMENT.**

**RECOMPUTE THE EXISTING DATA.**

**WRITE THE CLAIM LEDGER.**

**RUN I2-CM FROM THE FROZEN PACKAGE WITHOUT THE PRIOR REPORT.**

**CLASSIFY THE CLAIM.**

**DO NOT CHASE I3.**

**DO NOT ADD ANOTHER EXPERIMENT.**

**DO NOT TIGHTEN THE NUMBER AFTER FREEZE.**

Then close the cycle and leave Q-B8-001 open.

> **The finding justifies the work. The work does not justify more work.**
