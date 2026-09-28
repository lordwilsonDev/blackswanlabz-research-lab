---
source: vault:30_Architecture/FDE-Customer-Intake-Environment-Discovery-SOP-v1.3.md
captured: 2026-09-28
status: active
---

# FDE CUSTOMER INTAKE & ENVIRONMENT DISCOVERY SOP

## Version 1.3
## Status: FROZEN RESEARCH BASELINE + NORTH STAR MEASUREMENT OVERLAY
## Classification: Operational Standard Operating Procedure
## Use: All new FDE engagements
## Owner: Black Swan Labs
## Primary Systems: Customer Intake → Pre-Flight → FDE Kernel → Four-Layer Capability Architecture (L1–L4) → North Star (Intelligence → Decision → Intervention+Verification → Compounding)

### Operating Principle

> **Discover before designing. Verify before assuming. Authorize before accessing.**

### Version 1.3 Overlay Note

Version 1.3 preserves the v1.2 frozen baseline in full and adds a North Star measurement overlay: the SOP is positioned within the four-layer North Star architecture (Intelligence → Decision → Intervention+Verification → Compounding), and the SOP receives its own OKRs, KPIs, measurement discipline, and shared-goal statement.

The review that produced v1.2 found coverage and operationalization gaps, not a demonstrated need for an additional architectural layer. The North Star overlay does not change that conclusion. It makes the SOP's own performance measurable against the outcome it is supposed to serve.

The following remain architectural non-negotiables:

* No silent assumptions.
* No authority inference.
* No evidence substitution.
* No cosmetic readiness.
* No unbounded claims.
* No unauthorized access.
* No architectural expansion without a discriminating experiment or verified architectural gap.
* No undeclared Layer 6.
* The canonical capability architecture remains **L1–L4**.
* The North Star remains **four layers**. The SOP is the Intelligence-layer intake function; it is not a fifth layer.

Version 1.3 is intentionally frozen as a stable research baseline with measurement overlay. Known limitations are preserved as documented limitations rather than being silently eliminated.

---

# CHANGELOG — v1.2 → v1.3

### Added

1. **§51 — North Star Architecture Mapping.** Positions the SOP within the four-layer North Star (Intelligence → Decision → Intervention+Verification → Compounding).
2. **§52 — SOP OKRs.** Four objectives, eighteen key results, quarterly/cycle-bounded.
3. **§53 — SOP KPIs.** Six categories (Intelligence, Decision, Intervention, Value, Client, System), thirty-plus ongoing tracking metrics.
4. **§54 — Measurement Discipline for the SOP Itself.** Applies the North Star baseline→result discipline to the SOP's own performance.
5. **§55 — North Star Shared Goal for the SOP.** Expresses the SOP's shared goal in both the client's terms and BlackSwanLabz's terms.
6. Updated frozen state to v1.3 with OKR/KPI/measurement fields.

### Preserved from v1.2

* Authority-before-environment ordering.
* Risk-tiered intake depth I0–I4.
* Evidence vocabulary and Evidence Reliability separation.
* Universal Claim Control Rule.
* Common record header.
* Pre-Flight readiness gate (M ∧ O ∧ E ∧ A ∧ D ∧ R ∧ U ∧ C ∧ T).
* Change-Initiation Gate.
* Re-entry.
* Shadow IT discovery.
* System-of-record declaration and conflict adjudication.
* AI data-use authorization matrix.
* Sample-data chain of custody.
* Negative-knowledge carry-forward.
* Exit/offboarding.
* Four-layer canonical architecture.
* §31 classification rule (A–E).
* No architectural additions without evidence.
* Appendix A adversarial acceptance tests (A1–A7).
* Appendix B frozen test result.
* No-percentage-completeness rule.
* DecisionStateSnapshot replaces ReasoningSnapshot.
* Explicit prohibition on private chain-of-thought storage.

---

# §1 — PURPOSE

The FDE Customer Intake & Environment Discovery SOP establishes the controlled procedure by which Black Swan Labs determines what is actually required before an engineering team designs, builds, integrates, deploys, or operates an AI-enabled workflow.

The SOP converts an initial customer request into a verified operational understanding of:

* mission;
* desired outcome;
* stakeholders;
* workflow;
* systems;
* environment;
* authority;
* data;
* AI capabilities;
* dependencies;
* constraints;
* risks;
* evidence requirements;
* unknowns;
* assumptions;
* success criteria;
* testing requirements;
* failure and recovery requirements;
* engineering handoff requirements;
* change and revalidation conditions.

The SOP is not an implementation procedure.

Black Swan Labs determines **what should be built, why, under what conditions, with what evidence, authority, safeguards, tests, and acceptance criteria**.

Customer engineering teams remain responsible for architecture, implementation, integration, deployment, and operational ownership unless a separate authorization explicitly establishes otherwise.

---

# §2 — GOVERNING PRINCIPLE & MATERIALITY

## §2.1 Governing Principle

> **Discover before designing. Verify before assuming. Authorize before accessing.**

The FDE must not design against an environment that has not been sufficiently understood.

Customer statements are valuable inputs but are not automatically verified facts.

System observations are evidence but do not automatically establish organizational authority.

Documentation establishes provenance but does not automatically establish reliability.

Reasoning does not create authority.

---

## §2.2 Materiality Test

A fact, condition, dependency, constraint, unknown, assumption, or classification is **material** if treating it incorrectly could change any of the following:

* mission scope;
* required capabilities;
* operating envelope;
* authority structure;
* risk classification;
* evidence requirements;
* acceptance criteria;
* engineering handoff;
* permitted action;
* consequence of failure.

### Falsification Test

Ask:

> **If this fact were wrong, could the mission, requirement, operating conditions, authority, evidence burden, risk, or acceptance test change?**

If **yes**, it is material.

If **no**, it may remain contextual information.

Every material determination must be represented in the appropriate register.

---

## §2.3 Intake Depth

### I0 — Exploratory

No customer data, no environment access, exploratory discussion only.

Minimum:

* mission;
* desired outcome;
* basic scope;
* authority boundary;
* prohibition on sensitive collection.

### I1 — Advisory

Analysis, recommendations, or decision support without external execution.

Required:

* mission;
* workflow;
* systems;
* stakeholders;
* constraints;
* basic risk;
* data classification.

### I2 — Design / Sandbox Prototype

Prototype or design work using controlled environments.

Required:

* full workflow;
* access requirements;
* data;
* systems;
* dependencies;
* unknowns;
* assumptions;
* validation plan.

### I3 — Operational / Production-Adjacent

Live workflow support or production-adjacent operation.

Required:

* full SOP;
* authority matrix;
* security/privacy;
* incident handling;
* rollback;
* evidence;
* acceptance;
* monitoring.

### I4 — High Consequence

Regulated, safety-critical, critical infrastructure, high-value financial, security-sensitive, or otherwise high-consequence work.

Required:

* full SOP;
* specialist review;
* formal assurance case where appropriate;
* independent validation;
* enhanced change control;
* heightened evidence requirements.

---

## §2.3.1 Provisional vs Verified Intake Tier

Every engagement receives a **PROVISIONAL INTAKE TIER** at initiation.

The provisional tier is based on the **highest reasonably foreseeable consequence** implied by the initial mission and requested action.

After discovery of:

* mission;
* consequence;
* authority;
* environment;
* data;
* operational action;

the FDE determines the **VERIFIED INTAKE TIER**.

### Rule

> **The highest justified tier governs the assurance burden.**

If new information increases consequence or authority requirements, escalation is mandatory.

De-escalation requires:

* documented rationale;
* evidence supporting the lower classification;
* customer accountable-owner confirmation.

Tier assignment is therefore not a permanent intake label.

It is a controlled state transition.

---

## §2.4 Evidence Status

Evidence-bearing records may use:

* CUSTOMER-STATED
* DOCUMENTED
* SYSTEM-VERIFIED
* INFERRED
* ASSUMED
* UNKNOWN
* UNRESOLVED
* DISPUTED
* NOT-APPLICABLE
* SUPERSEDED

Evidence status answers:

> **What is the epistemic state of this record?**

It does **not** answer:

> **How reliable is the evidence?**

---

## §2.4.1 Evidence Reliability

Evidence reliability is recorded separately.

Possible values:

* HIGH
* MEDIUM
* LOW
* UNKNOWN

Reliability is claim-specific.

The reliability determination considers, where applicable:

* provenance;
* source identity;
* independence;
* freshness;
* completeness;
* corroboration;
* chain of custody;
* applicability;
* internal consistency;
* external consistency;
* known conflicts;
* measurement quality;
* vendor/version relevance;
* environmental relevance.

A record may therefore be:

> **DOCUMENTED + LOW RELIABILITY**

or:

> **CUSTOMER-STATED + HIGH RELIABILITY**

depending on the evidence available and the claim being evaluated.

---

## §2.5 Universal Claim Control Rule

For every material externally meaningful claim:

> **CLAIM → SOURCE → APPLICABILITY → VERIFICATION → STATUS → PROVENANCE**

This applies to claims concerning:

* system of record;
* administrator identity;
* organizational authority;
* API availability;
* AI provider capabilities;
* AI data use;
* production status;
* legal permission;
* regulatory applicability;
* contractual requirements;
* customer requirements;
* vendor guarantees;
* security controls;
* data ownership;
* retention requirements;
* deployment permissions.

No authoritative classification becomes fact merely because a customer or operator asserted it.

---

## §2.6 Common Record Header

All material records should include:

* engagement_id;
* record_id;
* record_type;
* version;
* status;
* owner;
* accountable_customer_owner;
* created_at;
* updated_at;
* classification;
* source_status;
* reliability_status where applicable;
* applicability_status where applicable;
* verification_method where applicable;
* evidence_references;
* dependencies;
* revalidation_triggers;
* last_verified_at;
* supersedes where applicable;
* superseded_by where applicable.

---

# §3 — CORE RULES

## §3.1 No Silent Assumptions

If the FDE does not know something material, it must be:

* asked;
* investigated;
* marked UNKNOWN;
* explicitly assumed with falsification conditions;
* or declared out of scope.

It may not silently become a fact.

---

## §3.2 Ask Only What Matters

Questions should be driven by:

* materiality;
* consequence;
* decision impact;
* evidence requirements;
* authority;
* dependency;
* engineering impact.

The SOP is not a questionnaire for its own sake.

---

## §3.3 Credentials Are Not Intake Data

Credentials, secrets, tokens, passwords, private keys, and authentication material are not collected as ordinary intake information.

Access must be separately authorized and controlled.

---

## §3.4 Authorization Before Access

The existence of technical access does not establish authorization to use that access.

Authorization must be established before inspection or action.

---

## §3.5 Verify Before Engineering

Engineering requirements must not be treated as established when their material premises remain unverified.

---

## §3.6 Adversarial / Fraudulent Intake

If there is reason to suspect:

* fake authority;
* misrepresentation;
* reconnaissance;
* credential harvesting;
* pressure to bypass verification;
* unauthorized access attempts;

the FDE must:

1. stop the affected activity;
2. mark the engagement:

   **BLOCKED — ADVERSARIAL-INTAKE-SUSPECTED**
3. preserve the relevant record;
4. avoid disclosing internal suspicion unnecessarily;
5. escalate internally;
6. resume only through authorized resolution.

---

## §3.7 Discovery Incident

If discovery reveals:

* active breach;
* regulatory violation;
* unsafe condition;
* legal exposure;
* material security incident;

the FDE must:

1. stop the affected discovery surface;
2. avoid unauthorized remediation;
3. notify the appropriate customer owner;
4. record observation, time, source, and scope;
5. avoid contacting third parties without authority;
6. mark unresolved/disputed facts appropriately;
7. continue unaffected discovery only if safe and authorized.

---

## §3.8 FDE Refusal Authority

The FDE may:

* refuse access;
* require tier escalation;
* require additional authorization;
* declare work blocked;
* declare work out of scope;
* decline the mission;
* stop discovery.

Customer preference does not override Black Swan's safety, authorization, evidence, or operating-envelope requirements.

---

# §4 — ENGAGEMENT RECORD & VERSIONING

Every engagement receives a unique engagement record.

The record must track:

* engagement identity;
* customer identity;
* accountable owner;
* scope;
* version;
* lifecycle state;
* intake tier;
* material changes;
* approvals;
* revalidation triggers.

### Review

Unless a shorter period is required by consequence or engagement conditions, active intake records receive review at least every **14 days** during extended discovery.

---

# §5 — IDENTITY & MULTI-ENTITY HANDLING

Identify:

* legal customer;
* operating entity;
* business unit;
* system owner;
* data owner;
* accountable customer owner;
* engineering owner;
* security/privacy owner;
* external vendors;
* other materially affected entities.

Where multiple entities participate, authority and obligations must not be assumed to transfer automatically between them.

---

# §6 — COMMUNICATION

Establish:

* primary communication channel;
* accountable customer owner;
* technical contact;
* escalation contact;
* emergency contact where appropriate;
* decision-making authority;
* expected response time;
* documentation location.

Material decisions must be recorded rather than left solely in informal communication.

---

# §7 — MISSION

Record:

* customer's stated mission;
* desired outcome;
* business/operational objective;
* current problem;
* why the problem matters;
* deadline;
* decision owner;
* intended action;
* consequences of failure;
* success criteria.

Preserve the customer's request exactly before interpreting it.

---

# §8 — CURRENT WORKFLOW

Map the actual workflow.

For each node record:

* actor;
* action;
* system;
* input;
* output;
* decision;
* authority;
* dependency;
* failure mode;
* evidence;
* timing;
* manual workaround.

### Shadow Process Rule

Discover actual operational behavior, not merely officially documented process.

Look for:

* spreadsheets;
* personal email;
* local scripts;
* manual exports;
* unofficial SaaS;
* undocumented APIs;
* side databases;
* human workarounds;
* tribal knowledge.

> **Official architecture and actual operating architecture are not assumed to be identical.**

---

# §9 — AUTHORITY DISCOVERY

Authority must be discovered **before environment access**.

For each material authority relationship record:

* authority_id;
* holder;
* scope;
* system/domain;
* delegated_from;
* delegation_evidence;
* valid_from;
* valid_until;
* revocation_method;
* verification_method;
* verification_evidence;
* disputes;
* status.

Statuses:

* CLAIMED
* VERIFIED
* DISPUTED
* REVOKED
* EXPIRED

### Authority Verification

Possible evidence:

* documented delegation;
* corporate registry;
* board resolution;
* higher-authority attestation;
* contract;
* regulatory designation;
* documented organizational policy.

### Critical distinction

The following are separate claims:

1. **The person has technical permissions.**
2. **The person has organizational authority.**
3. **The person has authority to grant Black Swan access.**

One does not automatically establish the others.

### Authority Tie-Breaker

If authorities conflict:

1. identify the claimed scopes;
2. identify verified authority;
3. compare scope;
4. escalate to the highest verified applicable authority;
5. block the affected action if authority remains unresolved.

---

# §10 — COMPUTING ENVIRONMENT

Record where applicable:

* operating system;
* version;
* build;
* patch status;
* update status;
* supported/current status;
* relevant local software;
* local execution constraints.

Unsupported or materially outdated environments must be flagged.

---

# §11 — HARDWARE

Record relevant:

* CPU;
* RAM;
* storage;
* GPU/accelerator;
* device constraints;
* performance constraints;
* availability;
* physical deployment requirements.

Do not infer capacity from device names alone.

---

# §12 — NETWORK

Record:

* network architecture;
* internet access;
* segmentation;
* firewall;
* VPN;
* proxy;
* DNS;
* inbound/outbound restrictions;
* required endpoints;
* latency/bandwidth constraints.

---

# §13 — CLOUD

Record:

* providers;
* accounts;
* subscriptions;
* regions;
* environments;
* tenancy;
* access boundaries;
* services;
* dependencies;
* billing ownership;
* relevant provider restrictions.

---

# §14 — WORKSPACE

Identify operational workspaces and tools.

Explicitly discover shadow IT.

Record:

* official systems;
* unofficial systems;
* personal accounts;
* shared drives;
* local files;
* spreadsheets;
* scripts;
* manual exports;
* personal communication channels;
* undocumented integrations.

---

# §15 — BUSINESS APPLICATION INVENTORY

Inventory relevant:

* ERP;
* WMS;
* CRM;
* HR;
* finance;
* ticketing;
* communication;
* analytics;
* document systems;
* identity systems;
* custom applications;
* external portals.

---

## §15.1 — SYSTEM-OF-RECORD DECLARATION

For each material business fact identify the authoritative source.

Examples:

| Business fact       | Candidate system       |
| ------------------- | ---------------------- |
| Inventory balance   | ERP / WMS / other      |
| Order status        | ERP / WMS / OMS        |
| Employee identity   | HR / identity provider |
| Security permission | identity/access system |

If systems disagree:

> **Do not resolve by assumption, seniority, or majority vote.**

Record each competing claim.

---

## §15.2 — SYSTEM-OF-RECORD CONFLICT PROCEDURE

When competing systems claim authority over the same business fact:

1. preserve all claims;
2. identify the evidence supporting each claim;
3. identify the accountable business owner;
4. determine the precise proposition in dispute;
5. identify a discriminating observation or authoritative source;
6. perform the observation only with appropriate authorization;
7. record the resolution method;
8. record the resulting status;
9. propagate unresolved uncertainty to dependent requirements.

If no reliable resolution is available:

> **STATUS = DISPUTED / UNRESOLVED**

Do not manufacture certainty.

---

# §16 — WMS DISCOVERY

Where a WMS is material, determine:

* vendor;
* version;
* deployment;
* integrations;
* APIs;
* authentication;
* workflows;
* source-of-record role;
* data flows;
* manual workarounds;
* operational dependencies;
* failure modes;
* support status;
* licensing constraints.

An asserted API is not an established API capability until appropriately verified.

---

# §17 — THIRD PARTIES

Identify:

* vendors;
* 3PLs;
* contractors;
* SaaS providers;
* consultants;
* integration partners;
* data processors;
* infrastructure providers.

Record dependencies, contractual constraints, permissions, service guarantees, and material external obligations.

---

# §18 — DATA

For each material data asset record:

* asset_id;
* owner;
* location;
* system;
* classification;
* PII;
* sensitive PII;
* permitted use;
* prohibited use;
* minimization requirement;
* retention;
* deletion/return;
* access;
* provenance;
* evidence status;
* reliability;
* revalidation requirements.

---

## §18.1 — AI DATA-USE AUTHORIZATION MATRIX

AI use must be classified separately for:

* inference;
* RAG;
* evaluation;
* fine-tuning;
* foundation-model training;
* provider retention;
* provider telemetry;
* human review;
* model improvement;
* logging.

Record:

* approved models;
* prohibited models;
* approved providers;
* prohibited providers;
* approval owner;
* approval evidence;
* data classes permitted;
* data classes prohibited.

Customer permission alone does not override applicable contractual, regulatory, legal, or organizational obligations.

---

# §19 — AI ENVIRONMENT

Identify:

* models;
* providers;
* local models;
* APIs;
* orchestration;
* vector stores;
* agents;
* tools;
* evaluation infrastructure;
* logging;
* monitoring;
* model versions;
* fallback systems;
* human review.

Record material capabilities as claims requiring appropriate verification.

---

# §20 — SECURITY & PRIVACY

Assess:

* identity;
* access;
* least privilege;
* secrets;
* encryption;
* network exposure;
* logging;
* monitoring;
* data handling;
* retention;
* incident response;
* privacy requirements.

---

# §21 — LEGAL / REGULATORY / CONTRACTUAL

Regulatory or contractual classification must not be self-declared as established fact without appropriate evidence.

Use:

> **Potential Obligation → Applicability Question → Evidence → Applicability Decision → Requirement → Control → Test**

Applicability must be recorded.

Where legal or regulatory interpretation exceeds FDE competence, escalate to qualified counsel or appropriate specialist authority.

---

# §22 — RESOURCES & BUDGET

Record:

* budget;
* personnel;
* engineering capacity;
* infrastructure;
* software;
* licenses;
* time;
* specialist expertise;
* customer availability.

Do not assume resources exist because the customer desires an outcome.

---

# §23 — TIMELINE

Record:

* requested deadline;
* operational deadline;
* dependency deadlines;
* approval deadlines;
* testing window;
* deployment window;
* revalidation window.

A customer-provided deadline is:

**CUSTOMER-REQUESTED**

until appropriately established.

---

# §24 — EXISTING TOOLS / AUTOMATION

Inventory:

* current automation;
* scripts;
* agents;
* integrations;
* macros;
* APIs;
* workflows;
* monitoring;
* reporting;
* manual processes.

Determine whether the requested capability already exists.

---

# §25 — OPERATING ENVIRONMENT

Record:

* production;
* sandbox;
* staging;
* development;
* pilot;
* offline;
* network constraints;
* physical environment;
* staffing;
* operating hours;
* maintenance windows;
* external dependencies.

---

# §26 — FAILURE & CONSEQUENCE

Do not accept:

> "We'd just fix it."

Instead determine:

1. Who notices?
2. How quickly?
3. Who is notified?
4. What is the operational impact?
5. What is the financial/legal/regulatory/security impact?
6. What does recovery cost?
7. Who has authority to intervene?

Consequence classification requires sufficient evidence for the material answers.

---

# §27 — SUCCESS CRITERIA

Every material success metric should define:

* metric;
* definition;
* baseline;
* target;
* threshold;
* measurement window;
* source;
* owner;
* frequency.

A metric without an operational definition is not an acceptance criterion.

---

# §28 — UNKNOWN REGISTER

Each material unknown receives:

* unknown_id;
* description;
* why it matters;
* affected records;
* dependency centrality;
* owner;
* resolution method;
* evidence required;
* consequence if unresolved;
* current status;
* resolution deadline where applicable;
* revalidation trigger.

Statuses include:

* UNKNOWN;
* OPEN;
* PARTIALLY RESOLVED;
* RESOLVED;
* UNRESOLVABLE;
* OUT-OF-SCOPE.

---

## §28.1 — MATERIAL UNKNOWN PROPAGATION

Material uncertainty propagates through dependent records.

If:

```text
UPSTREAM UNKNOWN
        ↓
REQUIREMENT
        ↓
ENGINEERING DESIGN
        ↓
ACCEPTANCE TEST
        ↓
DECISION
```

then the downstream record cannot silently become verified merely because it has been documented.

### Rule

> **A documented requirement is not necessarily a verified requirement.**

If a downstream requirement materially depends on:

* UNKNOWN;
* ASSUMED;
* CUSTOMER-STATED;
* DISPUTED;
* UNVERIFIED;
* unreliable evidence;

the downstream record inherits an appropriate uncertainty state unless the dependency is explicitly demonstrated to be non-material.

The dependency and rationale must be recorded.

---

## §28.2 — ENVIRONMENTAL FACT CONFLICT

Environmental factual disagreement is distinct from authority disagreement.

Examples:

* Operations says system A is used.
* IT says system B is used.
* Management says system C is authoritative.

Procedure:

1. preserve each claim;
2. identify sources;
3. identify evidence;
4. identify affected decisions;
5. identify a discriminating observation;
6. obtain authorization for observation;
7. update the state if resolved;
8. retain DISPUTED/UNRESOLVED if not resolved;
9. propagate uncertainty.

Do not resolve environmental facts by:

* majority vote;
* seniority alone;
* operator preference;
* model confidence.

---

# §29 — ASSUMPTIONS

Every material assumption records:

* assumption_id;
* statement;
* type;
* source;
* rationale;
* affected records;
* falsification condition;
* invalidation trigger;
* owner;
* status.

Allowed outcomes:

* VERIFY;
* FALSIFY;
* RETAIN TEMPORARILY.

> **An assumption without a falsification condition is a belief wearing a lab coat.**

---

# §30 — INTEGRATION MAP

Map relationships among:

* mission;
* workflow;
* systems;
* data;
* people;
* authority;
* AI;
* dependencies;
* requirements;
* risks;
* evidence;
* tests.

The integration map must expose material upstream/downstream relationships.

---

# §31 — ACCESS REQUIREMENTS

For each access requirement record:

* access_id;
* system;
* purpose;
* scope;
* requested permissions;
* minimum required privilege;
* requester;
* approving authority;
* authorization evidence;
* validity period;
* revocation method;
* status.

### Classification Rule

Every architectural or procedural finding must be classified as:

**A — Already Represented**

Existing capability adequately represents the requirement.

**B — Existing Concept**

The concept exists but requires clarification, configuration, or explicit representation.

**C — Mission-Specific Compiled Artifact**

A deliverable, register, workflow, or configuration derived from existing architecture.

**D — Engineering Implementation Detail**

Required implementation behavior that does not alter the architecture.

**E — Genuine Architectural Gap**

A capability cannot be represented within the existing architecture and its absence materially prevents required behavior.

Only **E** justifies architectural modification.

---

# §32 — CUSTOMER DOCUMENTS

Record:

* document;
* owner;
* version;
* date;
* source;
* applicability;
* evidence status;
* reliability;
* supersession;
* relevant requirements;
* conflicts.

Documents are evidence, not automatically truth.

---

# §33 — ENVIRONMENT VERIFICATION

Where environment verification is authorized:

* inspect;
* record observation;
* record evidence;
* record verification method;
* record timestamp;
* record environment/version.

If authorization is refused:

> **SYSTEM-VERIFIED cannot be assigned.**

The highest justified epistemic status must be retained.

Material refusal propagates to dependent Pre-Flight requirements.

---

# §34 — PRE-FLIGHT READINESS

Pre-Flight readiness is governed by the conjunction:

**M ∧ O ∧ E ∧ A ∧ D ∧ R ∧ U ∧ C ∧ T**

Where:

* **M** — Mission sufficiently defined
* **O** — Operating envelope sufficiently defined
* **E** — Evidence sufficient for required claims
* **A** — Authority established for required actions
* **D** — Dependencies sufficiently understood
* **R** — Risks and consequences sufficiently characterized
* **U** — Material unknowns are bounded and controlled
* **C** — Constraints sufficiently defined
* **T** — Tests/acceptance criteria sufficiently defined

### Critical clarification

**Pre-Flight Ready does not mean there are no unknowns.**

It means every material remaining unknown is:

* documented;
* owned;
* consequence-understood;
* appropriately bounded;
* assigned a resolution method;
* acceptable for the current stage;
* prevented from silently contaminating downstream decisions.

If a critical variable fails, status becomes:

* CLARIFICATION REQUIRED;
* BLOCKED;
* or REVALIDATION REQUIRED.

---

## §34.1 — MINIMUM SUFFICIENT DISCOVERY TEST

Discovery is sufficient when:

> **Additional reasonably available discovery is no longer expected to materially change the mission, scope, required capabilities, operating envelope, authority, risk classification, evidence requirements, acceptance criteria, or engineering handoff.**

This is a **stopping criterion**, not a completeness percentage.

The FDE must not report:

> "87% intake complete."

Instead use state-based status.

---

## §34.2 — NO COSMETIC READINESS

The FDE may not declare readiness merely because:

* the questionnaire is complete;
* documents exist;
* the customer is satisfied;
* a deadline is approaching;
* the engineer wants to start;
* most questions have answers.

Readiness depends on material sufficiency.

---

# §35 — ENGINEERING HANDOFF PACKAGE

The handoff should contain, as applicable:

1. Executive decision
2. Mission record
3. User input
4. Requirement register
5. Prerequisite register
6. Dependency graph
7. Capability requirements
8. Risk/consequence register
9. Authority register
10. Evidence requirements
11. Evidence register
12. Assumption register
13. Unknown/gap register
14. Question register
15. Decision log
16. Alternatives considered
17. Test/validation plan
18. Failure/recovery plan
19. Operating envelope
20. Readiness determination
21. Remaining risks
22. Action plan
23. Audit trail
24. Provenance manifest
25. Revalidation triggers

The exact package may be compressed or expanded without changing the underlying information requirements.

---

# §36 — KERNEL ENTRY

Once Pre-Flight satisfies the required gate, the engagement may enter the FDE Kernel.

Kernel entry maps:

**MISSION → REQUIREMENTS → DEPENDENCIES → AUTHORITY → EVIDENCE → RISKS → TESTS → ACTION**

The Kernel must preserve traceability back to the intake.

---

## §36.1 — CHANGE-INITIATION GATE

Before material execution:

**Pre-Flight Complete**
→ **Mission Graph / Requirements**
→ **Change Impact**
→ **Authority**
→ **Test / Sandbox / Rollback**
→ **Customer Approval**
→ **Execution**
→ **Verification**
→ **Acceptance**
→ **Monitoring**

### Critical distinction

> **Discovery authorization ≠ deployment authorization.**

A person authorized to help investigate a system is not automatically authorized to approve production changes.

---

## §36.2 — CHANGE IMPACT TEST

When a material change occurs, ask whether it could alter:

* mission;
* scope;
* capability requirements;
* environment;
* data;
* authority;
* risk;
* evidence;
* acceptance;
* operating envelope;
* dependencies;
* failure/recovery assumptions.

If yes:

> **REVALIDATION REQUIRED**

The engagement must re-enter the appropriate discovery/Pre-Flight state.

---

# §37 — STOP CONDITIONS

Stop or block when:

* authority is unresolved;
* access is unauthorized;
* evidence is materially insufficient;
* critical dependency is unknown;
* risk exceeds authorized tier;
* operating envelope is exceeded;
* material contradiction remains unresolved;
* required test cannot be performed;
* recovery is undefined for a consequential action;
* external obligation prohibits the action;
* customer requests bypass of mandatory controls.

---

# §38 — PRIVACY & DATA MINIMIZATION

Collect only information necessary for the mission.

Prefer:

* synthetic data;
* masked data;
* samples;
* minimum necessary records;
* controlled environments.

Do not collect sensitive information merely because it might be useful later.

---

## §38.1 — SAMPLE-DATA CHAIN OF CUSTODY

For sample data record:

* source;
* owner;
* collection time;
* collector;
* authorization;
* transformation;
* transfer;
* storage;
* access;
* deletion/return;
* integrity evidence.

---

# §39 — OPERATOR QUALITY CHECK

Before handoff, ask:

> **If I disappeared tomorrow, could another competent operator reconstruct why this engagement was classified, what remains unknown, who has authority, what evidence supports the requirements, what would block action, and what must happen next?**

If not, the record is incomplete.

---

# §40 — CUSTOMER CONFIRMATION

Customer confirmation records that the customer reviewed the relevant representation.

Customer confirmation does not automatically establish truth.

Where the customer attests without independent verification:

> **CUSTOMER-ATTESTED — UNVERIFIED**

must remain available as a status.

---

# §41 — ENGAGEMENT STATES

Allowed lifecycle states:

* DRAFT
* CLARIFICATION REQUIRED
* BLOCKED
* READY
* ACTIVE
* REVALIDATION REQUIRED
* SUSPENDED
* COMPLETE
* RETIRED
* SUPERSEDED

---

## §41.1 — RE-ENTRY

Re-entry is mandatory when material change could alter:

* mission;
* scope;
* requirements;
* evidence;
* authority;
* consequence;
* environment;
* acceptance;
* operating envelope.

Re-entry begins at the earliest affected stage rather than automatically restarting the entire engagement.

---

# §42 — CORE FLOW

**CUSTOMER REQUEST**

↓

**MISSION**

↓

**PROVISIONAL TIER**

↓

**AUTHORITY**

↓

**ENVIRONMENT**

↓

**WORKFLOW**

↓

**DATA / SYSTEMS / DEPENDENCIES**

↓

**RISKS / CONSEQUENCES**

↓

**EVIDENCE**

↓

**UNKNOWN / ASSUMPTION CONTROL**

↓

**CAPABILITY REQUIREMENTS**

↓

**TEST / ACCEPTANCE**

↓

**MINIMUM SUFFICIENT DISCOVERY**

↓

**PRE-FLIGHT**

↓

**FDE KERNEL**

↓

**ENGINEERING HANDOFF**

↓

**CUSTOMER ENGINEERING**

↓

**CHANGE / EXECUTION**

↓

**VERIFICATION**

↓

**ACCEPTANCE**

↓

**MONITORING / REVALIDATION**

---

# §43 — BLACK SWAN RULE

Black Swan Labs may conclude:

> **No technical intervention is currently justified.**

The FDE is not required to produce an AI solution merely because the customer requested AI.

The correct output may instead be:

* process correction;
* data governance;
* system consolidation;
* authority clarification;
* evidence acquisition;
* workflow redesign;
* human process improvement;
* no action;
* deferred action.

---

# §44 — REPRODUCIBILITY

A competent independent operator should be able to reconstruct:

* what was requested;
* what was discovered;
* what was verified;
* what was inferred;
* what was assumed;
* what remained unknown;
* why the tier was assigned;
* who had authority;
* why the requirements were selected;
* what evidence supported them;
* what tests were required;
* why the engagement reached its state.

### No Percentage Completeness

The SOP does not use an overall "intake completeness percentage."

Readiness is represented through controlled states and gates.

---

# §45 — FINAL DEFINITION

> **The Black Swan FDE Customer Intake & Environment Discovery SOP is a controlled method for converting an initial customer objective into a verified operational model, explicit capability and engineering requirements, bounded uncertainty, evidence-backed decisions, authorized action boundaries, testable acceptance criteria, and a reproducible engineering handoff.**

Its purpose is not to eliminate uncertainty.

Its purpose is to make uncertainty:

* visible;
* classified;
* bounded;
* consequentially understood;
* owned;
* testable;
* and prevented from silently becoming false certainty.

---

# §46 — EXIT / OFFBOARDING

At engagement completion:

1. revoke temporary access;
2. verify credential/access termination where applicable;
3. return or delete customer data according to authorization;
4. record retention requirements;
5. transfer required artifacts;
6. document unresolved risks;
7. document outstanding actions;
8. confirm ownership;
9. preserve required audit records;
10. capture applicable negative knowledge;
11. record customer acceptance where applicable;
12. close the engagement.

---

# §47 — RECORD-TO-KERNEL OBJECT MAPPING

| Intake concept           | Kernel object         |
| ------------------------ | --------------------- |
| Authority                | AuthorityGrant        |
| Time/deadline            | TemporalConstraint    |
| Cost                     | CostRecord            |
| Resources                | ResourceAllocation    |
| Dispute                  | DisputeRecord         |
| State change             | StateTransition       |
| Gate                     | Gate                  |
| Auditable decision state | DecisionStateSnapshot |
| Data                     | DataAsset             |
| AI capability            | AICapability          |
| Access                   | AccessGrant           |
| Constraint               | Constraint            |
| Evidence/provenance      | ProvenanceRecord      |

## §47.1 — DecisionStateSnapshot

The Kernel must not require storage of private model chain-of-thought.

A DecisionStateSnapshot records the externally auditable state necessary to reconstruct the decision:

* mission;
* question;
* known facts;
* unknowns;
* assumptions;
* hypotheses;
* evidence;
* evidence status;
* evidence reliability;
* alternatives;
* constraints;
* authority;
* risk;
* decision status;
* externally expressible rationale;
* provenance;
* timestamp;
* model/system version where relevant.

> **Auditability requires decision-state provenance, not private chain-of-thought capture.**

---

# §48 — NEGATIVE KNOWLEDGE CARRY-FORWARD

Failed approaches, discovered limitations, rejected assumptions, and known environmental failure modes should be retained where useful.

Each negative-knowledge record should include:

* lesson_id;
* originating engagement;
* originating date;
* environment;
* vendor;
* version;
* conditions;
* observed outcome;
* evidence references;
* confidence;
* reliability;
* applicability criteria;
* non-applicability criteria;
* known limitations;
* decay condition;
* revalidation trigger;
* current status.

Negative knowledge must not be generalized beyond its demonstrated applicability.

---

# §49 — CANONICAL ARCHITECTURE MAPPING

The SOP maps into the canonical Black Swan architecture.

## Customer Discovery Charter

**P1 — Intent, Outcome & Accountability**

Mapped to:

* §7 Mission
* §27 Success Criteria
* §40 Customer Confirmation

**P2 — Domain, Scope & Operating Envelope**

Mapped to:

* §8 Workflow
* §10–§17 Environment
* §25 Operating Environment

**P3 — Risk, Consequence & Assurance**

Mapped to:

* §26 Failure & Consequence
* §20 Security/Privacy
* §21 Legal/Regulatory
* §34 Pre-Flight

**P4 — Authority, Action & Control**

Mapped to:

* §9 Authority
* §31 Access
* §36 Change-Initiation Gate
* §37 Stop Conditions

**P5 — Evidence, Validation & Claim Control**

Mapped to:

* §2 Evidence
* §18 Data
* §21 Applicability
* §28 Unknowns
* §29 Assumptions
* §32 Documents
* §33 Verification
* §35 Engineering Handoff

---

## Four-Layer Capability Architecture

### L1 — Capability Map

Determines:

> **What must exist?**

### L2 — Competency & Evidence Matrix

Determines:

> **What does actual competence look like, and what proves it?**

### L3 — Executable Development Program

Determines:

> **How is required capability acquired and demonstrated?**

### L4 — Domain Expertise & Engineering

Determines:

> **How is the domain operationally modeled, practiced, tested, calibrated, and applied?**

The FDE SOP feeds requirements and environmental knowledge into these existing layers.

### Architectural Boundary

> **This SOP does not declare a Layer 6.**

Operational control, execution, change, monitoring, and assurance are represented through the existing FDE Kernel and established architectural primitives.

---

# §50 — VERSION CONTROL & ARCHITECTURAL DISCIPLINE

Any future proposed modification must first be classified:

**A — Already Represented**
**B — Existing Concept**
**C — Mission-Specific Artifact**
**D — Engineering Detail**
**E — Genuine Architectural Gap**

Only **E** can justify architectural modification.

A proposed new concept must demonstrate:

1. the existing architecture cannot represent the required behavior;
2. the limitation is material;
3. the limitation is reproducible;
4. the proposed addition resolves the limitation;
5. the addition does not duplicate an existing primitive.

> **An SOP without a discriminating test is a reading exercise.**

---

# §51 — NORTH STAR ARCHITECTURE MAPPING

The FDE SOP is positioned within the four-layer North Star architecture.

## The North Star

> **Help businesses continuously improve by finding operational truth, proving it with measurement, and intervening where it matters — so the business gets better and the people inside it get better at what they do.**

## Layer 1 — Intelligence

**What it is:** The system that finds operational truth — public research, workflow discovery, business DNA, competitor movement, customer journey, employee friction, error intelligence, MoIE adversarial analysis.

**What the SOP contributes:** The SOP **is** the Intelligence-layer intake function for a specific customer engagement. It discovers mission, workflow, systems, environment, authority, data, dependencies, risks, unknowns, assumptions, evidence requirements, success criteria, and testing requirements. It produces the signals, evidence, contradictions, hypotheses, opportunity candidates, and decision-card inputs that Layer 1 requires.

**What the SOP does not claim:** The SOP does not discover operational truth about Black Swan itself, about the market, or about competitors. Those are separate Intelligence-layer activities. The SOP discovers operational truth about the **customer's environment** so that the rest of the North Star can operate on a real basis.

## Layer 2 — Decision

**What it is:** The system that converts intelligence into a choice. Every opportunity receives the five dimensions, the decision card, and one of three outcomes: DO NOTHING / IMPROVE / AUTOMATE.

**What the SOP contributes:** The SOP produces the evidence, impact, readiness, economics, and risk inputs that the decision layer requires. The SOP's mission, workflow, authority, environment, data, risks, unknowns, evidence requirements, capability requirements, success criteria, and acceptance criteria are the raw material for the five-dimension decision card.

**Critical rule:** The SOP does not make the DO NOTHING / IMPROVE / AUTOMATE decision. It makes the decision **possible** by establishing what is actually true. The decision card (wherever it lives in the architecture) chooses the outcome.

## Layer 3 — Intervention + Verification

**What it is:** The system that does the simplest thing that works, then proves whether it worked. Baseline → change → observation → comparison → result.

**What the SOP contributes:** The SOP establishes the baseline (where measurable), the success criteria with operational definitions, the measurement plan, and the acceptance tests that Layer 3 will use. The SOP's value-conversion engine inputs (capacity released, conversion path, economic value) are identified during intake so that Layer 3 can measure honestly.

**Critical rule:** The SOP does not perform the intervention. It sets up the intervention to be measurable. If the SOP cannot establish a baseline or success criteria, Layer 3 cannot produce a credible result.

## Layer 4 — Compounding

**What it is:** The layer that makes results accumulate — the client's people get better at the direction they want the business to go, and Black Swan's internal assets (pattern library, regional intelligence, client memory, reusable patterns, decision cards) compound with every engagement.

**What the SOP contributes:** The SOP's negative-knowledge carry-forward (§48), reusable intake patterns, decision-card inputs, and verified operational models compound internally. Each engagement makes the next intake faster and more accurate — if the measurement discipline is maintained.

## What the SOP is not

* The SOP is not a fifth North Star layer.
* The SOP is not Layer 6.
* The SOP is not a substitute for the Decision layer.
* The SOP is not a substitute for the Intervention+Verification layer.
* The SOP is the Intelligence-layer intake function that makes the rest of the North Star possible for a specific engagement.

---

# §52 — SOP OKRS

OKRs are quarterly or cycle-bounded. Objectives are directional. Key results are measurable. Baseline before target.

## Objective 1

**Every intake produces verified operational truth, not assumptions dressed as facts.**

### KR1.1

**% of material facts verified (SYSTEM-VERIFIED or DOCUMENTED with appropriate reliability) before engineering handoff.**

Target: **100% of material facts in I2+ engagements.**

Baseline: measured per cycle.

### KR1.2

**% of engagements where authority was established before environment access.**

Target: **100%.**

Baseline: measured per cycle.

### KR1.3

**% of engagements with a complete unknown register (every material unknown has owner, resolution method, evidence required, consequence if unresolved).**

Target: **100% of I2+ engagements.**

Baseline: measured per cycle.

### KR1.4

**% of engagements where system-of-record conflicts were adjudicated (not assumed away).**

Target: **100% of conflicts discovered.**

Baseline: measured per cycle.

### KR1.5

**Mean time from intake start to Pre-Flight Ready.**

Target: **baseline first, then improve.**

Baseline: measured per cycle. Do not target a number before the baseline exists.

---

## Objective 2

**The SOP prevents false certainty and silent assumption contamination.**

### KR2.1

**Number of material unknowns that propagated to downstream decisions without being flagged.**

Target: **0.**

Baseline: measured per cycle.

### KR2.2

**% of downstream requirements that correctly inherited uncertainty state when dependent on UNKNOWN / ASSUMED / CUSTOMER-STATED / DISPUTED / UNVERIFIED evidence.**

Target: **100%.**

Baseline: measured per cycle.

### KR2.3

**Number of incidents where unauthorized access occurred during discovery.**

Target: **0.**

Baseline: measured per cycle.

### KR2.4

**% of engagements where the minimum sufficient discovery test was applied before declaring Pre-Flight Ready.**

Target: **100%.**

Baseline: measured per cycle.

### KR2.5

**% of engagements where NO COSMETIC READINESS was avoided (readiness based on material sufficiency, not questionnaire completion).**

Target: **100%.**

Baseline: measured per cycle.

---

## Objective 3

**The SOP feeds the North Star pipeline honestly — every engagement produces a real decision input, including DO NOTHING.**

### KR3.1

**% of engagements where the SOP output produced a complete decision-card input (evidence, impact, readiness, economics, risk dimensions all addressable).**

Target: **100% of I2+ engagements.**

Baseline: measured per cycle.

### KR3.2

**Number of DO NOTHING recommendations produced from intake discovery (with full written rationale).**

Target: **tracked, not avoided; minimum 1 per cycle where warranted.**

Baseline: measured per cycle. If the count is zero for a cycle, that is a signal to investigate, not a success to celebrate.

### KR3.3

**% of engagements where baseline measurement was established (or explicitly marked unmeasurable with reason) before any intervention recommendation.**

Target: **100%.**

Baseline: measured per cycle.

### KR3.4

**% of consequential engagements (I3+) where value-conversion engine inputs (capacity released, conversion path, economic value) were identified during intake.**

Target: **100% of I3+ engagements.**

Baseline: measured per cycle.

---

## Objective 4

**The SOP compounds — each engagement makes the next one better.**

### KR4.1

**Negative knowledge records created per engagement.**

Target: **≥ 1 per engagement where a failure, limitation, or rejected assumption occurred.**

Baseline: measured per cycle.

### KR4.2

**Reusable intake patterns/templates applied to new engagements.**

Target: **tracked and growing; baseline first.**

Baseline: measured per cycle.

### KR4.3

**Mean intake discovery time trending down while verification quality (KR1.1, KR1.2) holds.**

Target: **measured, not assumed; improvement demonstrated, not claimed.**

Baseline: measured per cycle. This KR is invalid until KR1.1 and KR1.2 have baselines.

### KR4.4

**% of engagements where adversarial intake scenarios (A1–A7) were checked.**

Target: **100% of I2+ engagements.**

Baseline: measured per cycle.

---

## OKR Integrity Rules

1. **Baseline before target.** No KR receives a target number before its baseline exists.
2. **No direct hours-to-dollars leap.** If an OKR claims value, the value-conversion engine is applied.
3. **Honest reporting.** If a cycle's result is less than hoped, report it. The OKR exists to make the gap visible, not to hide it.
4. **Measurement continues.** OKRs are tracked per cycle, not declared once.
5. **DO NOTHING is a legitimate outcome.** An intake that produces a DO NOTHING recommendation with full rationale is a successful engagement, not a failed one.

---

# §53 — SOP KPIS

KPIs are ongoing tracking metrics. They tell whether the SOP is working, not just whether a customer is happy.

## Intelligence KPIs

**Does the SOP find operational truth?**

* Opportunities for operational truth found per engagement (signals, contradictions, unknowns, dependencies discovered).
* Material facts verified vs. material facts remaining CUSTOMER-STATED / UNVERIFIED at Pre-Flight.
* System-of-record conflicts discovered per engagement.
* Shadow IT / hidden dependencies discovered per engagement.
* Tribal knowledge reconstructed per engagement.
* Public / external signals with cited sources per deliverable (where applicable).

## Decision KPIs

**Does the SOP produce a real decision input?**

* Decision-card-ready outputs per engagement (target: 100% of I2+).
* DO NOTHING recommendations from intake (target: real, tracked, not avoided).
* IMPROVE recommendations from intake (target: tracked).
* AUTOMATE candidates identified from intake (target: tracked; not every intake produces one).
* Decision cards with five dimensions scored (target: 100% of opportunities advanced).

## Intervention KPIs

**Does the SOP set up verifiable intervention?**

* Baseline established before intervention recommendation (target: 100%).
* Success criteria with operational definition (metric, definition, baseline, target, threshold, measurement window, source, owner, frequency) — target: 100% of material success criteria.
* Acceptance tests defined before handoff (target: 100% of I2+).
* Value-conversion engine inputs identified during intake (target: 100% of consequential engagements).

## Value KPIs

**Does the SOP enable real value claims?**

* Capacity-released measurements identified during intake (hours/week, errors/month, cycle time, etc.).
* Conversion-path observations identified during intake (what would the freed capacity become?).
* Economic value claims traceable to intake-established baselines (target: 100% of value claims traceable).
* Value claims that would have been direct hours-to-dollars leaps (target: 0 — caught by the SOP's measurement discipline).

## Client KPIs

**Is the client getting value from the discovery?**

* Charter reviewed and confirmed by customer.
* CUSTOMER-ATTESTED — UNVERIFIED rate (how often the customer attests without independent verification — tracked, not hidden).
* Customer's own measurement of the thing that mattered (faster response, fewer errors, etc.) — tracked post-intervention.
* Willingness to continue / discuss another opportunity (post-engagement).
* Client satisfaction (qualitative + client's own measure).

## System KPIs

**Is the SOP itself healthy and compounding?**

* Engagement state distribution (DRAFT / CLARIFICATION REQUIRED / BLOCKED / READY / ACTIVE / REVALIDATION REQUIRED / SUSPENDED / COMPLETE / RETIRED / SUPERSEDED).
* Mean time in each state.
* % of engagements entering FDE Kernel with Pre-Flight Ready (target: 100% of kernel entries).
* Re-entry events triggered by material change (tracked — visible, not hidden).
* Offboarding completion rate (target: 100%).
* Negative knowledge carry-forward rate (target: ≥ 1 per failure/limitation engagement).
* Adversarial test pass rate (A1–A7 — tracked per engagement where applicable).
* Security findings (open / resolved).
* New patterns added to intake pattern library.
* Reusable patterns applied to new engagements.

---

# §54 — MEASUREMENT DISCIPLINE FOR THE SOP ITSELF

The North Star's measurement discipline applies to the SOP's own performance, not just to client interventions.

## 1. Baseline before improvement

The SOP's own KPIs (mean intake time, verification rate, etc.) must be measured before any "improvement" to the SOP is claimed. Not estimated.

## 2. Same measurement after

Same method, same definition, same timeframe.

## 3. Explicit comparison

"Before: X. After: Y. Difference: Z." Not buried in prose.

## 4. Value-conversion engine applied to the SOP

If a SOP improvement claims time savings, was the capacity converted? Into what? Not faked into a savings number.

## 5. Honest reporting

If a SOP change did not help, report it. The measurement exists to make the gap visible, not to defend the change.

## 6. Measurement continues

The SOP's KPIs are tracked per cycle, not declared once and forgotten.

---

# §55 — NORTH STAR SHARED GOAL FOR THE SOP

The North Star's shared goal is expressed in the client's terms AND Black Swan's terms, and they are the same goal from opposite sides.

## For the client

> **We're trying to understand your business accurately enough to decide what's worth doing — and what isn't — with the reasoning visible, so you don't spend money fixing imaginary problems or automating things that should be left alone.**

## For Black Swan

> **Did we find operational truth about this customer's business, prove it with measurement where we could, and identify what's worth intervening on — so the rest of the North Star pipeline has a real basis to work from?**

## The two are the same goal

The client wants accurate understanding + real decisions. Black Swan wants to deliver that. The SOP's KPIs and OKRs are the shared language that keeps both sides honest.

## The shared goal, restated for the SOP

Every FDE intake, at its best, delivers this:

1. **A clearer picture of what's actually happening** in the customer's operation — mission, workflow, systems, environment, authority, data, dependencies, risks, unknowns, assumptions, success criteria. The customer understands their own operation better than they did before.
2. **A decision-ready basis** — the intake output can be scored on the five dimensions (evidence, impact, readiness, economics, risk) and one of DO NOTHING / IMPROVE / AUTOMATE can be chosen with the reasoning visible.
3. **A measurable setup** — baseline established (or explicitly marked unmeasurable), success criteria with operational definitions, acceptance tests defined, value-conversion inputs identified. The intervention layer can measure honestly.
4. **A compoundable record** — negative knowledge carried forward, reusable patterns captured, decision-card inputs preserved. The next intake is easier.
5. **A continuing basis for watching** — the intake record is the starting point for the monthly report, the competitor snapshot, the customer-journey tracking, the error intelligence, the opportunity backlog. The discovery does not end when the handoff is done.

That is the North Star, delivered through the intake function. One engagement at a time, measured, proven, and compounding.

---

# APPENDIX A — ADVERSARIAL ACCEPTANCE TESTS

These scenarios are acceptance tests for the SOP, not additional architecture.

---

## A1 — Fake Authority

### Scenario

A person claims to be IT management and requests production access.

Evidence reveals only technical account privileges.

### Required behavior

The SOP must distinguish:

* technical permission;
* organizational authority;
* authority to grant Black Swan access.

Unverified authority must not become VERIFIED.

**Expected state:** BLOCKED / AUTHORITY VERIFICATION REQUIRED.

---

## A2 — Split Reality

### Scenario

Management, Operations, IT, and Warehouse each identify a different system as the source of truth.

### Required behavior

The SOP must:

* preserve competing claims;
* record evidence;
* identify the disputed proposition;
* seek a discriminating observation;
* avoid majority-vote resolution;
* preserve DISPUTED if unresolved;
* propagate uncertainty.

**Expected state:** DISPUTED until adequately resolved.

---

## A3 — Hidden Dependency

### Scenario

Customer identifies one official WMS, but actual workflow depends on:

* spreadsheets;
* 3PL portal;
* personal email;
* undocumented API;
* ERP.

### Required behavior

The SOP must discover actual workflow dependencies and prevent the official system inventory from being mistaken for the complete operational environment.

**Expected state:** environment/workflow expanded; dependencies recorded.

---

## A4 — Material Unknown Propagation

### Scenario

Customer states that an API exists, but verification is refused.

The requested engineering solution depends on that API.

### Required behavior

The API cannot become SYSTEM-VERIFIED.

The dependent integration requirement must retain appropriate uncertainty.

**Expected state:** dependent engineering requirement not fully verified.

---

## A5 — Tier Escalation

### Scenario

An initially advisory chatbot is later discovered to control inventory transactions in production.

### Required behavior

The engagement must transition from its provisional classification to the appropriate verified higher-assurance tier.

**Expected state:** VERIFIED TIER ESCALATION.

---

## A6 — Post-Pre-Flight Change

### Scenario

After Pre-Flight, the customer changes:

* WMS;
* API;
* cloud provider;
* data-retention policy.

### Required behavior

The change must undergo impact assessment.

If material:

**REVALIDATION REQUIRED**

---

## A7 — Offboarding

### Scenario

The engagement ends after Black Swan has had temporary access to systems and customer data.

### Required behavior

The SOP must produce a controlled exit covering:

* access revocation;
* data handling;
* retention;
* artifact ownership;
* unresolved risks;
* handoff;
* closure.

---

# APPENDIX B — FROZEN TEST RESULT

Version 1.1 was subjected to adversarial execution across:

1. fake authority;
2. split organizational reality;
3. hidden operational dependencies;
4. material unknown propagation;
5. tier escalation;
6. post-Pre-Flight environmental change;
7. offboarding;
8. conflicting data-use authorization;
9. unjustified AI solution request;
10. tribal-knowledge reconstruction.

The test identified **refinements and coverage gaps**, including:

* system-of-record conflict adjudication;
* dependency-aware uncertainty propagation;
* provisional/verified tier distinction;
* stronger universal provenance.

These were incorporated into v1.2.

v1.3 incorporates the North Star measurement overlay (§51–§55) without changing the v1.2 operational baseline or the v1.2 adversarial test result.

No demonstrated architectural failure requiring an additional capability layer was established by either v1.2 or v1.3.

---

# FINAL FROZEN STANDARD

## Black Swan FDE Intake Doctrine

> **The customer defines the mission.**
> **Discovery defines the environment.**
> **Scope constrains the claim.**
> **Consequence determines the proof burden.**
> **Authority constrains action.**
> **Evidence determines what may be established.**
> **Dependencies determine what can safely be inferred.**
> **Unknowns remain visible until resolved or bounded.**
> **Tests determine whether the system actually works.**
> **Changes trigger revalidation when they can change the decision.**
> **The engineering team receives requirements—not guesses.**

## North Star Overlay

> **The SOP finds operational truth (Intelligence).**
> **The SOP feeds the decision (Decision).**
> **The SOP sets up verifiable intervention (Intervention+Verification).**
> **The SOP compounds internally (Compounding).**
> **The SOP does not become a fifth layer.**

### Frozen State

**VERSION:** 1.3
**STATUS:** FROZEN RESEARCH BASELINE + NORTH STAR MEASUREMENT OVERLAY
**ARCHITECTURE:** FOUR LAYERS + FDE KERNEL + NORTH STAR INTELLIGENCE/DECISION/INTERVENTION/COMPOUNDING MAPPING
**ADDITIONAL LAYER DECLARED:** NONE
**OKRS:** DEFINED (§52)
**KPIS:** DEFINED (§53)
**MEASUREMENT DISCIPLINE:** APPLIED TO SOP ITSELF (§54)
**SHARED GOAL:** DEFINED (§55)
**ADVERSARIAL TEST:** COMPLETED (Appendix A)
**KNOWN LIMITATIONS:** PRESERVED
**REOPEN CONDITION:** DEMONSTRATED MATERIAL FAILURE, VERIFIED COVERAGE GAP, OR DISCRIMINATING EXPERIMENT

> **Discover before designing. Verify before assuming. Authorize before accessing.**
>
> **Building is breaking.**
>
> **The model can propose. The experiment decides.**
