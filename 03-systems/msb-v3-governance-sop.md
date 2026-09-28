---
source: ~/projects/AI-Agents/msb-v3/docs/governance/MSB-ENT-SOP-001-…md (uncommitted in msb-v3 as of 2026-09-28)
captured: 2026-09-28
status: pending
---

> This is a written procedure. It describes how MSB v3 is meant to be operated; it is not evidence that each control is implemented or operating. Where a control maps to code in MSB v3, that mapping is not yet verified.

> Appendix A's self-assessment — including 'ahead of most early-stage vendors' — is the source's own and unverified.

The document below is copied verbatim, unedited, from the source file named above. Its own header marks it "DRAFT — NOT APPROVED" (version 0.1-draft), and its Appendix A lists which of the records it requires do not yet exist. It is part of [MSB v3](msb-v3.md); that page describes the code, this one describes the intended operating procedure.

---

# MSB v3

## Enterprise Trust, Security, Privacy, AI Governance & Service Operations Standard Operating Procedure

**Document ID:** MSB-ENT-SOP-001
**Version:** 0.1-draft
**Status:** DRAFT — NOT APPROVED. No control in this document is in effect until §47 is signed. Where this document says "must", read it as the target state; Appendix A shows what exists today.
**Effective Date:** [DATE OF APPROVAL]
**Owner:** [OWNER / SECURITY & OPERATIONS LEAD]
**Executive Approver:** [AUTHORIZED EXECUTIVE]
**Security Contact:** [SECURITY CONTACT]
**Privacy Contact:** [PRIVACY CONTACT / DPO, IF APPLICABLE]
**Emergency Contact:** [24/7 OR CONTRACTUAL EMERGENCY CONTACT]
**Provenance:** First draft generated with AI assistance (2026-09-25) and edited for packaging; content has not yet been reviewed by counsel or an independent security reviewer.
**Review Frequency:** At least annually and after material security, privacy, regulatory, architectural, or service changes

---

# 1. Purpose

This Standard Operating Procedure establishes the operational controls used to deploy, operate, secure, govern, support, recover, and retire MSB v3 for enterprise customers.

The purpose of this SOP is to ensure that MSB v3 can demonstrate, through documented evidence rather than assertions:

* what customer data is processed;
* where and by whom it is processed;
* which AI models and providers may receive which classes of data;
* how security and privacy incidents are detected, contained, investigated, and communicated;
* how models and material system changes are approved;
* how customers are onboarded, changed, and offboarded;
* how support incidents are classified and escalated;
* how service continuity is maintained when the primary operator or service component is unavailable;
* how security controls are integrated into engineering and release operations;
* and how evidence is retained for customer due diligence, audits, contracts, and internal review.

This SOP is an operational control document. It does not by itself constitute a certification to SOC 2, ISO/IEC 27001, ISO/IEC 42001, or legal compliance with any specific jurisdiction.

---

# 2. Scope

This SOP applies to:

* MSB v3 production software;
* customer deployments;
* MSB infrastructure and control-plane components;
* connected AI model providers;
* external tools and service providers;
* customer data;
* logs, telemetry, audit records, and evidence;
* source code and release artifacts;
* employees, contractors, operators, backup personnel, and approved service providers;
* security, privacy, AI governance, support, continuity, and incident-response activities.

This SOP applies whether MSB v3 is operated locally within a customer environment, through approved infrastructure, or through an approved hybrid architecture.

---

# 3. Control Principles

MSB v3 operates under the following principles.

### 3.1 Least Capability

The system uses the smallest mechanism capable of safely performing the task.

A deterministic rule, database operation, local process, or human decision is preferred over a general-purpose AI model when that mechanism is sufficient.

### 3.2 Data-Minimization by Route

Customer data is not sent to an external model or service merely because that service is available.

Routing must be determined by:

**data classification + approved provider + permitted purpose + customer contract + applicable law + technical controls.**

### 3.3 Explicit Authorization

No AI-generated output constitutes authorization for an irreversible or materially consequential action unless the applicable workflow explicitly permits that authority and the required verification controls have passed.

### 3.4 Evidence Over Assertion

A control is not considered operational merely because a policy says it exists.

A control must produce evidence such as:

* configuration;
* approval record;
* audit event;
* ticket;
* test result;
* review;
* signed record;
* or equivalent verifiable artifact.

### 3.5 Producer / Verifier Separation

The component producing an important result should not be the sole authority for declaring that result correct.

Where practical, verification must use a materially independent mechanism.

### 3.6 Fail Closed

The system must not silently convert:

* timeout → success;
* missing evidence → approval;
* unknown → acceptable;
* failed verification → verified;
* unauthorized request → authorized;
* unavailable operator → unrestricted execution.

### 3.7 Customer Environment Controls Take Precedence

Where a customer contract, security schedule, data-processing agreement, or regulatory requirement imposes a stricter control than this SOP, the stricter requirement applies for that customer.

---

# 4. Roles and Segregation of Duties

The following roles must exist even when one person temporarily holds multiple roles.

| Role                   | Responsibility                                                                 |
| ---------------------- | ------------------------------------------------------------------------------ |
| Service Owner          | Product authority, service decisions, commercial commitments                   |
| Security Lead          | Security controls, incidents, vulnerability management                         |
| Privacy Lead           | Data processing, privacy assessments, DPA coordination                         |
| AI Governance Lead     | Model inventory, model approvals, AI risk review                               |
| Operations Lead        | Deployment, operations, support, continuity                                    |
| Incident Commander     | Coordinates active incidents                                                   |
| Customer Lead          | Customer communication and service coordination                                |
| Independent Reviewer   | Reviews important security/model/release decisions                             |
| Backup Operator        | Executes documented continuity procedures when primary operator is unavailable |
| Legal/External Counsel | Regulatory interpretation and legally required notifications when engaged      |

For a solo-founder operation, one individual may temporarily hold multiple roles.

However:

> **role overlap does not eliminate the requirement for independent verification.**

Where personnel separation is impossible, independence must be achieved through a separate mechanism, external reviewer, documented secondary provider, or other compensating control.

---

# 5. Systems of Record

The following records must exist and have a defined owner.

1. Customer Registry
2. Data Processing Register
3. Subprocessor Register
4. Model / Provider Registry
5. Security Risk Register
6. Vulnerability Register
7. Incident Register
8. Customer Support Register
9. Change / Release Register
10. Access Register
11. Business Continuity Register
12. Evidence Ledger

The Evidence Ledger is the authoritative index connecting controls to proof.

---

# 6. Data Classification Standard

Every customer environment must assign data to one of the following classes.

## 6.1 Public

Information approved for public disclosure.

Examples:

* published documentation;
* public website material;
* publicly released source material.

**Permitted routing:** approved local or external services.

---

## 6.2 Internal

Non-public operational information that does not contain customer-sensitive or regulated information.

Examples:

* internal procedures;
* general operational notes;
* non-sensitive system documentation.

**Default routing:** local processing preferred. Approved external models may be used where contractual, security, and routing requirements permit.

---

## 6.3 Confidential

Business-sensitive or customer-sensitive information where unauthorized disclosure could cause material harm.

Examples:

* non-public customer documents;
* internal financial information;
* proprietary business information;
* non-public operational data.

**Default routing:** local processing unless the external provider is explicitly approved for this class.

---

## 6.4 Restricted / Regulated

Information subject to elevated contractual, legal, regulatory, or security requirements.

Examples may include:

* regulated personal information;
* credentials and secrets;
* authentication material;
* security incident evidence;
* privileged legal material;
* highly sensitive customer information;
* information specifically designated by a customer's contract.

**Default routing:** external AI processing is prohibited unless explicitly approved through the customer's applicable governance process and the technical/legal requirements have been satisfied.

---

# 7. AI Provider Routing Matrix

Every model provider must have an entry in the Model / Provider Registry.

Minimum fields:

| Field                     | Required |
| ------------------------- | -------- |
| Provider                  | Yes      |
| Model                     | Yes      |
| Version                   | Yes      |
| Purpose                   | Yes      |
| Approved Data Classes     | Yes      |
| Processing Location       | Yes      |
| Retention                 | Yes      |
| Training / Data-Use Terms | Yes      |
| DPA / Contract Status     | Yes      |
| Known Subprocessors       | Yes      |
| Security Documentation    | Yes      |
| Evaluation Status         | Yes      |
| Model Owner               | Yes      |
| Approval Date             | Yes      |
| Expiration / Review Date  | Yes      |
| Change-Review Trigger     | Yes      |

MSB v3 may support providers including local models and approved external providers such as DeepSeek, OpenAI, and Anthropic, but provider availability does **not** automatically mean that every customer data class may be sent to that provider.

DeepSeek's current Harness documentation, for example, states that its installed Harness processes and stores specified data locally by default, while invoking external models, tools, plugins, or services may cause data to be processed by those external providers. That reinforces the need for MSB's routing layer to treat external invocation as a distinct data-processing event. ([DeepSeek][2])

The authoritative control is MSB's approved provider registry plus the customer's contractual configuration.

---

# 8. Subprocessor Management

Where MSB uses a third party to process customer personal data on MSB's behalf, that provider must be assessed for subprocessor treatment under the applicable contractual and legal structure.

The following must be maintained for each subprocessor:

* legal entity name;
* service provided;
* categories of data processed;
* purpose;
* processing locations;
* applicable transfer mechanism;
* DPA / contractual status;
* security documentation;
* retention;
* relevant subprocessors of that provider where contractually relevant;
* date approved;
* customer notification status;
* replacement/decommission status.

The customer's DPA must identify or incorporate the applicable approved subprocessor mechanism.

Subprocessors may not be introduced into a production customer data path without the required contractual and governance review.

Provider lists must be maintained as living records rather than copied once into a static document. Vendor subprocessor lists can change over time, so MSB must maintain a review process. OpenAI, for example, maintains a current public subprocessor list. ([OpenAI][3])

---

# 9. Data Retention and Deletion

Every customer deployment must have a documented retention schedule for:

* customer source data;
* generated outputs;
* operational logs;
* security logs;
* audit records;
* backups;
* support records;
* incident evidence;
* contractual records.

Retention must be based on:

**business need + contractual requirement + legal requirement + security need.**

No data may be retained indefinitely merely because storage is inexpensive.

## Deletion Procedure

Upon expiration, termination, or approved deletion request:

1. Confirm customer identity and authorization.
2. Identify all customer-associated data stores.
3. Identify active and backup copies.
4. Freeze relevant records where legal hold or incident preservation applies.
5. Delete or render inaccessible the customer data according to the contract.
6. Verify deletion.
7. Record the date, operator, systems affected, method, and evidence.
8. Provide customer confirmation where contractually required.

Deletion verification must distinguish:

**application deletion** from **backup expiration**.

A statement that data was "deleted" must identify which layer was deleted and the applicable backup lifecycle.

---

# 10. Data Processing Agreements

Before production processing of customer personal data, the required contractual package must be complete.

Depending on the relationship and applicable law, the package may include:

* MSA;
* DPA;
* security addendum;
* subprocessor schedule;
* data transfer terms;
* confidentiality terms;
* SLA;
* data retention/deletion terms;
* incident notification terms.

Under GDPR, the processor must notify the controller without undue delay after becoming aware of a personal-data breach; the controller generally has a 72-hour deadline for notifying the supervisory authority where the Article 33 conditions apply. These are different obligations and must not be collapsed into one generic "72-hour breach rule." ([EUR-Lex][4])

---

# 11. Security Incident and Breach Notification SOP

## 11.1 Incident Definition

A security incident is any event that may affect:

* confidentiality;
* integrity;
* availability;
* authenticity;
* authorization;
* customer data;
* infrastructure;
* credentials;
* model security;
* or contractual security commitments.

A personal-data breach is a specific subset involving accidental or unlawful destruction, loss, alteration, unauthorized disclosure, or unauthorized access to personal data. ([European Data Protection Board][5])

---

## 11.2 Severity

### SEV-1 Critical

Examples:

* confirmed unauthorized access to customer Restricted data;
* active compromise;
* material customer-wide outage;
* stolen administrative credentials;
* destructive event affecting production or customer data.

**Target:**

Detection acknowledgement: ≤ 15 minutes
Incident Commander assigned: ≤ 30 minutes
Containment decision: ≤ 60 minutes
Customer communication: according to contract and applicable law; internal target is to begin material-customer notification within 24 hours of confirmation, sooner when required.

### SEV-2 High

Examples:

* suspected compromise;
* material service degradation;
* high-risk vulnerability;
* incorrect access control;
* suspected unauthorized model routing.

**Target:**

Acknowledgement ≤ 1 hour
Investigation initiated ≤ 2 hours
Customer communication as contractually required.

### SEV-3 Moderate

Examples:

* limited security issue;
* non-critical control failure;
* isolated customer impact.

**Target:**

Acknowledgement ≤ 1 business day.

### SEV-4 Low

Examples:

* informational event;
* minor configuration defect;
* low-risk anomaly.

**Target:**

Tracked during normal operations.

---

# 12. Incident Response Order

The incident commander follows this sequence:

### Step 1 — Detect

Record:

* time detected;
* source;
* affected system;
* suspected impact;
* initial evidence.

### Step 2 — Preserve

Preserve:

* logs;
* audit records;
* system state;
* relevant configuration;
* communications;
* hashes or forensic artifacts where appropriate.

Do not destroy evidence while attempting remediation.

### Step 3 — Contain

Examples:

* revoke credential;
* disable connector;
* stop model route;
* isolate service;
* suspend affected customer operation;
* block malicious source.

### Step 4 — Classify

Determine:

* security incident or not;
* customer impact;
* personal-data involvement;
* regulated-data involvement;
* contractual notification requirement;
* potential legal obligation;
* provider/subprocessor involvement.

### Step 5 — Establish Notification Chain

Default order:

**Incident Commander → Security Lead → Service Owner → Privacy/Legal → affected customer → regulator/data subjects where applicable**

The exact order may change when the applicable contract or law requires earlier notification.

### Step 6 — Investigate

Determine:

* what happened;
* how it happened;
* what was affected;
* what was not affected;
* whether compromise remains active;
* whether other customers could be affected.

### Step 7 — Remediate

Remove the underlying cause.

A patch that only hides the symptom does not close the incident.

### Step 8 — Verify

Independent verification must confirm:

* containment;
* restored security boundary;
* restored service;
* corrective action;
* no obvious recurrence.

### Step 9 — Communicate

Customer communication must separate:

**Known facts**

from

**current assessment**

from

**unknowns**

from

**actions taken**

from

**next update time**.

Do not wait for perfect certainty before issuing a contractually or legally required initial notice.

### Step 10 — Close

Incident closure requires:

* root cause;
* impact assessment;
* corrective action;
* evidence;
* customer communication record;
* lessons learned;
* control update;
* owner;
* due date for remaining actions.

NIST SP 800-61 Rev. 3 explicitly treats incident response as part of broader cybersecurity risk management and aligns it with CSF 2.0. ([NIST][6])

---

# 13. Customer Notification Template Requirements

Every material incident notice must contain, to the extent known:

* incident identifier;
* detection date/time;
* affected service;
* affected customer;
* nature of incident;
* known data categories;
* known or estimated scope;
* current containment status;
* customer actions required;
* MSB actions underway;
* known unknowns;
* next update commitment;
* security contact.

Where facts remain incomplete, the notice must explicitly say so.

---

# 14. AI / Model Governance SOP

MSB maintains an AI system and model inventory.

For each approved model:

1. Define intended use.
2. Define prohibited use.
3. Define permitted data classes.
4. Identify provider.
5. Identify data-processing location.
6. Review provider terms.
7. Review privacy/security documentation.
8. Evaluate relevant failure modes.
9. Establish output-verification requirements.
10. Approve the model.
11. Record the approval.
12. Monitor production performance.
13. Reassess after material change.

ISO/IEC 42001 establishes requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System, making it useful as the management-system reference point for this governance layer. ([ISO][7])

NIST AI RMF 1.0 organizes AI risk management around **Govern, Map, Measure, and Manage**, with governance operating across the lifecycle. ([NIST AI Resource Center][8])

---

# 15. Model Change Approval

The following are material model changes:

* provider change;
* model-family change;
* model-version change where behavior may materially change;
* hosting-location change;
* retention-policy change;
* data-use/training-policy change;
* major system-prompt change;
* safety-policy change;
* routing-policy change;
* capability expansion;
* new tool access;
* new customer data class;
* new autonomous authority.

Material changes require:

**change request → impact assessment → testing → approval → controlled release → verification → evidence.**

A model version must never be treated as equivalent to a previous version merely because the API interface remains the same.

---

# 16. AI Output Verification

AI output must be classified by consequence.

### Low Consequence

Examples:

* formatting;
* summarization;
* drafting.

May use automated checks.

### Medium Consequence

Examples:

* customer-facing recommendations;
* classification;
* workflow routing.

Requires defined validation rules.

### High Consequence

Examples:

* security actions;
* financial actions;
* legal conclusions;
* irreversible state changes;
* access authorization.

Requires an independent verification mechanism and/or authorized human approval.

AI confidence alone is never sufficient evidence of correctness.

---

# 17. AI Risk Review

Each customer use case must answer:

* What is the AI intended to do?
* What is it not allowed to do?
* What data enters the system?
* Which model receives the data?
* What can the model cause to happen?
* What happens if it is wrong?
* How is wrong output detected?
* Who can override it?
* What is the escalation state?
* What evidence is retained?

The AI RMF emphasizes continual risk management through the AI lifecycle rather than a one-time assessment. ([NIST AI Resource Center][8])

---

# 18. EU AI Act Applicability Review

For customers subject to the EU AI Act, MSB must maintain a deployment-specific applicability assessment.

The review must identify, at minimum:

* role in the AI value chain;
* whether MSB is acting as provider, deployer, or another relevant actor;
* intended purpose;
* affected users;
* risk category;
* applicable transparency requirements;
* documentation requirements;
* human-oversight requirements where applicable;
* applicable customer responsibilities;
* provider responsibilities;
* downstream provider dependencies.

As of **2 August 2026**, the European Commission states that the AI Office and Member State authorities begin implementing, supervising, and enforcing the AI Act, and transparency rules under Article 50 apply from that date. Applicability depends on the particular system and use case, so MSB must perform a deployment-specific assessment rather than claim universal AI Act compliance. ([Digital Strategy][9])

---

# 19. Customer Deployment SOP

## 19.1 Pre-Deployment Gate

Before installation, collect:

* customer owner;
* technical contact;
* security contact;
* privacy contact where applicable;
* deployment architecture;
* approved network paths;
* approved data classes;
* approved AI providers;
* approved jurisdictions;
* credentials/configuration requirements;
* support schedule;
* backup expectations;
* RTO/RPO requirements;
* contract and DPA status.

Deployment may not proceed while required contractual or security gates remain blocked.

---

## 19.2 Installation

Record:

* version;
* release identifier;
* deployment environment;
* configuration;
* enabled connectors;
* model providers;
* data routes;
* privileged accounts;
* installation operator;
* installation date;
* validation result.

---

## 19.3 Proof of Life

Every deployment must pass a proof-of-life checklist:

1. Service starts.
2. Health endpoint succeeds.
3. Authentication works.
4. Intended customer data path works.
5. Unauthorized path is denied.
6. Audit event is created.
7. Required model route behaves as configured.
8. Verification path succeeds.
9. Backup/recovery assumptions are checked.
10. Customer acceptance is recorded.

---

# 20. Customer Offboarding SOP

Upon termination:

1. Freeze new processing.
2. Confirm authorized termination request.
3. Inventory customer data and credentials.
4. Disable connectors.
5. Revoke privileged access.
6. Export customer-retained artifacts where contractually required.
7. Delete application data according to contract.
8. Process backups according to retention policy.
9. Revoke provider/API credentials where dedicated to customer.
10. Verify access termination.
11. Verify deletion where applicable.
12. Produce an offboarding record.
13. Send customer confirmation.

The offboarding record must identify what was:

* returned;
* deleted;
* retained by legal obligation;
* retained temporarily in backups;
* or excluded from deletion because of legal hold.

---

# 21. Support, SLA and Escalation SOP

Every enterprise customer must have a documented service schedule.

The contract must specify:

* support hours;
* emergency channel;
* severity definitions;
* response targets;
* update cadence;
* escalation path;
* maintenance windows;
* planned-change notice;
* service exclusions;
* customer dependencies.

## Default Internal Targets

| Severity | Example                        | Response Target |
| -------- | ------------------------------ | --------------: |
| SEV-1    | Critical outage/security event |          15 min |
| SEV-2    | Major degradation              |          1 hour |
| SEV-3    | Material defect                |  1 business day |
| SEV-4    | Low-priority issue             | 2 business days |

These are **operational targets**, not contractual commitments until incorporated into an executed SLA.

**Solo-operator period (see §43).** Until a tested Backup Operator or external support arrangement exists, the SEV-1/SEV-2 figures above cannot be met around the clock by one person and must not be offered as 24/7 targets. During this period the offered schedule is: **[PROPOSED — owner to set: support hours, e.g. business hours in the customer's time zone; SEV-1 response within [N] business hours; out-of-hours SEV-1 handled by fail-closed controls (§3.6) plus next-business-hours response].** The table above becomes the offered target only once staffing supports it.

---

# 22. Escalation Tree

### Level 1

Service operator investigates.

### Level 2

Service Owner / Engineering Lead.

### Level 3

Security / Privacy / AI Governance.

### Level 4

External specialist or backup operator.

### Level 5

Legal counsel / customer executive escalation / regulatory authority as applicable.

An escalation must never terminate merely because the primary operator is unavailable.

---

# 23. Business Continuity SOP

This is a mandatory enterprise control.

MSB must explicitly document what happens when the primary founder/operator cannot perform duties.

## 23.1 Primary Continuity Controls

At minimum:

* documented operating procedures;
* source-code repository access;
* infrastructure documentation;
* encrypted credential recovery procedure;
* customer registry;
* deployment records;
* provider registry;
* incident contacts;
* contract repository;
* recovery procedures;
* named backup operator or service partner;
* succession/handover procedure.

---

# 24. Founder Unavailability

If the primary operator is unavailable:

1. Backup operator is activated.
2. Access authority is transferred according to predefined procedure.
3. Active incidents are reviewed.
4. Customer commitments are identified.
5. Production operations are stabilized.
6. No new high-risk capability is introduced.
7. Enterprise customers are notified only when contractually or operationally necessary.
8. Business-critical services continue under restricted change authority.
9. Normal change authority resumes after primary or designated successor returns.

---

# 25. Code Escrow / Handover

For enterprise customers requiring continuity protection, MSB may use:

* code escrow;
* designated backup operator;
* managed handover partner;
* customer-held deployment package;
* documented build and recovery instructions.

The continuity package must contain enough information for an authorized successor to understand:

* how the system starts;
* how it is configured;
* where data is located;
* how backups are restored;
* how credentials are rotated;
* how customer deployments are identified;
* how incidents are handled;
* how releases are performed;
* which external providers are dependencies.

A continuity plan is not considered tested merely because the documentation exists.

---

# 26. Continuity Test

At least annually, and after material architectural changes, perform a continuity exercise.

The exercise must test:

> **"Can an authorized person other than the primary operator restore, operate, or safely hand over the service using only the approved continuity package?"**

Evidence must include:

* scenario;
* participants;
* systems tested;
* failures discovered;
* elapsed time;
* missing information;
* corrective actions;
* final result.

---

# 27. Recovery Objectives

Each enterprise deployment must define:

**RTO — Recovery Time Objective**

and

**RPO — Recovery Point Objective**

MSB may not advertise a universal RTO/RPO until it has been established and tested for the relevant deployment architecture.

---

# 28. Security Program SOP

The security program covers:

* identity and access management;
* privileged access;
* credential management;
* key management;
* vulnerability management;
* secure development;
* release security;
* logging and monitoring;
* incident response;
* backup and recovery;
* vendor risk;
* security review;
* data protection;
* change management.

ISO/IEC 27001:2022 specifies requirements for an Information Security Management System, while NIST CSF 2.0 provides a lifecycle-oriented structure of Govern, Identify, Protect, Detect, Respond, and Recover. ([ISO][10])

---

# 29. Access Control

All privileged access must follow:

* least privilege;
* unique accounts;
* strong authentication;
* minimum necessary permissions;
* access logging;
* periodic review;
* immediate removal upon termination.

Shared privileged accounts are prohibited unless technically unavoidable and specifically controlled.

Emergency access must be logged and reviewed.

---

# 30. Credential and Key Management

Secrets must not be stored in:

* source code;
* public repositories;
* customer documentation;
* plaintext operational notes.

Keys must be:

* inventoried;
* scoped;
* rotated according to risk/contract;
* revoked when no longer required;
* protected at rest;
* monitored for accidental disclosure.

Compromised credentials are treated as security incidents.

---

# 31. Vulnerability Management

Vulnerabilities are classified based on:

* exploitability;
* exposure;
* affected asset;
* customer impact;
* data sensitivity;
* active exploitation;
* compensating controls.

Critical vulnerabilities affecting exposed production systems must receive immediate triage.

High-risk vulnerabilities require documented remediation or risk acceptance.

Risk acceptance must identify:

* risk;
* owner;
* rationale;
* compensating control;
* expiration/review date.

No vulnerability may remain unresolved indefinitely without an explicit owner.

---

# 32. Secure Release SOP

A release must pass:

1. source review;
2. automated tests;
3. lint/static analysis where applicable;
4. type checks where applicable;
5. security checks;
6. migration review;
7. deployment validation;
8. health check;
9. rollback determination;
10. release evidence.

Material security or AI changes additionally require the appropriate security/model review.

---

# 33. Change Management

Changes are classified:

### Standard

Low-risk, repeatable, pre-approved.

### Normal

Requires documented review and approval.

### Emergency

Required to address active outage or security threat.

Emergency changes must be documented retrospectively and reviewed after stabilization.

---

# 34. Logging and Auditability

Security-relevant events must generate auditable records where technically feasible.

Minimum event categories include:

* authentication;
* authorization;
* privileged action;
* configuration change;
* model route;
* provider selection;
* policy decision;
* security event;
* deployment;
* release;
* data deletion;
* incident action.

Audit records must support reconstruction of:

**who → did what → when → to which system/resource → under what authority → with what result.**

---

# 35. Evidence Ledger

Every important control must have:

**Control → Evidence → Owner → Review Date → Status**

Example:

| Control               | Evidence              | Status   |
| --------------------- | --------------------- | -------- |
| Approved model        | Model approval record | [STATUS] |
| Subprocessor approval | DPA + register        | [STATUS] |
| Access review         | Access review record  | [STATUS] |
| Incident response     | Incident drill        | [STATUS] |
| Backup recovery       | Recovery test         | [STATUS] |
| Offboarding           | Deletion verification | [STATUS] |
| Release security      | Release record        | [STATUS] |
| Continuity            | Handover exercise     | [STATUS] |

This prevents the classic enterprise failure mode:

> "We have a policy" without evidence that the policy operates.

---

# 36. Customer Security Questionnaire Evidence Pack

MSB should maintain a reusable evidence package containing, subject to confidentiality:

* security overview;
* architecture overview;
* data-flow diagram;
* data classification policy;
* retention/deletion policy;
* DPA;
* subprocessor register;
* AI governance policy;
* model inventory;
* vulnerability policy;
* access-control policy;
* incident-response policy;
* business-continuity policy;
* disaster-recovery summary;
* secure-development policy;
* change-management policy;
* support/SLA;
* privacy statement;
* security contacts;
* penetration/security assessment evidence where available;
* independent audit/certification evidence where actually obtained.

This package is what turns the answer from:

> "Yes, we have security."

into:

> "Here is the policy, here is the control, here is who owns it, and here is the evidence."

SOC 2 reporting covers controls relevant to areas including security, availability, processing integrity, confidentiality, and privacy, making those domains useful organizing categories for an enterprise evidence pack. ([AICPA & CIMA][11])

---

# 37. Framework Alignment

MSB should maintain a framework crosswalk.

| MSB Control Domain  | NIST AI RMF      | NIST CSF 2.0       | ISO 42001       | ISO 27001                      | SOC 2                                |
| ------------------- | ---------------- | ------------------ | --------------- | ------------------------------ | ------------------------------------ |
| AI governance       | Govern           | Govern             | AIMS            | Security governance interfaces | Security / Privacy                   |
| AI inventory        | Map              | Identify / Govern  | AIMS            | Asset management               | Security / Privacy                   |
| AI testing          | Measure          | Detect / Identify  | AIMS            | Secure development             | Processing Integrity                 |
| AI risk treatment   | Manage           | Protect / Respond  | AIMS            | Risk treatment                 | Security / Availability              |
| Access control      | —                | Protect            | AIMS interfaces | Access control                 | Security                             |
| Incident response   | —                | Respond            | AIMS interfaces | Incident management            | Security / Availability              |
| Business continuity | —                | Recover            | AIMS interfaces | Continuity                     | Availability                         |
| Vendor/subprocessor | Govern           | Govern / Identify  | AIMS            | Supplier relationships         | Security / Confidentiality / Privacy |
| Data lifecycle      | Map / Manage     | Identify / Protect | AIMS            | Information protection         | Confidentiality / Privacy            |
| Release management  | Measure / Manage | Protect            | AIMS            | Change / development           | Processing Integrity                 |

This is an **alignment map**, not a claim that completing this SOP automatically satisfies every requirement of those standards.

NIST explicitly describes the CSF as an outcome-oriented framework rather than a single prescriptive implementation process. ([NIST][12])

---

# 38. Control Exceptions

Any departure from this SOP requires:

* requested control exception;
* affected system;
* reason;
* risk;
* compensating control;
* owner;
* expiration date;
* approval authority.

Permanent undocumented exceptions are prohibited.

---

# 39. Control Failure

When a control fails:

**Detect → Contain → Assess → Correct → Verify → Record**

Repeated control failure requires examination of the underlying architecture rather than repeated manual workarounds.

---

# 40. Annual Enterprise Control Review

At least annually, the owner must review:

* all policies;
* all subprocessors;
* all AI providers;
* data classifications;
* retention schedules;
* incident history;
* vulnerability history;
* access reviews;
* continuity tests;
* recovery tests;
* support performance;
* customer contractual changes;
* regulatory changes;
* material architectural changes.

The review must produce:

**Approved / Modified / Retired / New Control**

for every material control.

---

# 41. Mandatory Operational Records

The following records are required for enterprise operation:

### Governance

* Master SOP
* organizational roles
* risk register
* exception register

### Privacy

* data-processing register
* data classification matrix
* retention schedule
* deletion records
* DPA
* subprocessor register

### AI

* AI system inventory
* model inventory
* provider register
* model approvals
* evaluation records
* model change records
* AI risk assessments

### Security

* access reviews
* vulnerability register
* security review records
* incident register
* incident postmortems
* release security records

### Operations

* deployment checklist
* customer configuration
* support tickets
* SLA records
* change records
* continuity exercise
* recovery exercise
* offboarding records

### Evidence

* evidence ledger
* control owners
* review dates
* verification records

---

# 42. Enterprise Acceptance Gate

MSB v3 is not considered enterprise-ready for a customer deployment until the following minimum conditions are true:

## Security

* [ ] privileged access documented
* [ ] credential management documented
* [ ] vulnerability process documented
* [ ] release security documented
* [ ] incident process tested

## Privacy

* [ ] data classifications defined
* [ ] retention defined
* [ ] deletion defined
* [ ] DPA completed where required
* [ ] subprocessor register maintained

## AI

* [ ] model inventory maintained
* [ ] approved data routes defined
* [ ] model change approval defined
* [ ] output verification defined
* [ ] AI applicability assessment performed where required

## Operations

* [ ] onboarding procedure tested
* [ ] offboarding procedure tested
* [ ] support severity matrix defined
* [ ] SLA defined
* [ ] escalation chain defined

## Continuity

* [ ] backup operator identified
* [ ] handover package exists
* [ ] recovery procedure documented
* [ ] continuity test completed
* [ ] RTO/RPO defined where contractually required

## Evidence

* [ ] evidence ledger operational
* [ ] control owner assigned
* [ ] review dates assigned
* [ ] outstanding gaps explicitly recorded

---

# 43. Known Limitation: Solo-Founder Dependency

MSB must not represent a single-person organization as having organizational resilience it does not possess.

Until a tested backup operator, external support arrangement, code escrow arrangement, or equivalent continuity mechanism exists:

* the key-person dependency must be recorded;
* customer contracts must not promise unsupported 24/7 availability;
* recovery objectives must reflect actual capability;
* enterprise customers must receive accurate continuity information;
* material dependency must remain visible in the risk register.

The correct enterprise answer is not:

> "We don't have that problem."

It is:

> **"Here is the dependency, here is the compensating control, here is who takes over, and here is the last time we tested it."**

---

# 44. Final Control Model

MSB's enterprise operating loop is:

**REQUEST**

→ **CLASSIFY**

→ **AUTHORIZE**

→ **ROUTE**

→ **EXECUTE**

→ **VERIFY**

→ **EVIDENCE**

→ **AUDIT**

→ **MONITOR**

→ **ESCALATE**

→ **RECOVER**

→ **LEARN**

The enterprise policy layer must therefore become an extension of the same control-plane philosophy used inside the product.

---

# 45. Enterprise Principle

MSB v3 does not treat enterprise trust as a PDF collection.

It treats trust as an operational system.

**Policy defines the expected behavior.**

**Code enforces technical behavior where possible.**

**Contracts define customer obligations and boundaries.**

**Logs provide evidence.**

**Independent verification tests the claims.**

**Incident response handles failure.**

**Continuity handles unavailable people or systems.**

**Governance determines when the system may act.**

**The evidence ledger connects all of it.**

---

# 46. Adoption Rule

This SOP becomes operational only when every mandatory placeholder is replaced with a real:

* person;
* contact;
* provider;
* contract;
* system;
* evidence source;
* retention period;
* escalation path;
* or approved exception.

A blank field is not a control.

An untested procedure is not a capability.

A policy without evidence is an assertion.

A system without recovery is a dependency.

A model without routing governance is an uncontrolled data path.

**Enterprise readiness is achieved when the organization can demonstrate the control—not merely describe it.**

---

# 47. Approval

**Document Owner:** __________________________

**Security Owner:** __________________________

**Privacy Owner:** __________________________

**Service Owner:** __________________________

**Executive Approver:** __________________________

**Effective Date:** __________________________

**Next Review Date:** __________________________

**Version:** 0.1-draft

**Approval Status:** __________________________

---

# 48. References

[1]: https://www.nist.gov/itl/ai-risk-management-framework "AI Risk Management Framework | NIST"
[2]: https://www.deepseek.com/harness/data-processing/ "DeepSeek Harness | Data Processing Statement"
[3]: https://openai.com/policies/sub-processor-list/ "OpenAI Sub-processor list"
[4]: https://eur-lex.europa.eu/eli/reg/2016/679/ "EUR-Lex - 02016R0679-20160504 - EN - EUR-Lex"
[5]: https://www.edpb.europa.eu/topics/security-data-breaches/personal-data-breaches_en "Personal data breaches | European Data Protection Board"
[6]: https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations "NIST Revises SP 800-61: Incident Response Recommendations and Considerations for Cybersecurity Risk Management | NIST"
[7]: https://committee.iso.org/cms/live/live/en/sites/isoorg/contents/news/insights/AI/what-is-ai-all-you-need-to-know/newsBody/standard-reference/standard-reference%40/81230.html "ISO/IEC 42001:2023 - AI management systems"
[8]: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ "AI RMF Core - AIRC"
[9]: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai "AI Act | Shaping Europe's digital future - European Union"
[10]: https://committee.iso.org/cms/live/live/en/sites/isoorg/home/insights-news/resources/iso-42001-explained-what-it-is/MAIN%20after/row-content/row-content-col1/standards/standard-reference-1%40/82875.html "ISO/IEC 27001:2022 - Information security management systems"
[11]: https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2 "System and Organization Controls: SOC Suite of Services | Resources | AICPA & CIMA"
[12]: https://www.nist.gov/cyberframework/faqs "Frequently Asked Questions | NIST"

**Regulatory anchors — verify at approval.** At drafting: NIST AI RMF 1.0 is the published version (a revision is in progress); NIST CSF 2.0 is current; ISO/IEC 42001:2023 and ISO/IEC 27001:2022 are the relevant management-system standards; the EU AI Act's general application date is 2 August 2026. Proposals to delay parts of the AI Act (notably high-risk obligations) were under discussion — confirm current status against the official EU source [9] before relying on any date in §18.

---

# Appendix A — Record Status at Drafting (2026-09-25)

What §36 and §41 require, against what exists in this repository today. **EXISTS** = a document or mechanism is present (not necessarily complete). **PARTIAL** = something related exists but does not meet the record as defined here. **MISSING** = nothing found. Verified by file presence and document headers only; not an audit.

| Required record (§41 / §36) | Status | Where / note |
|---|---|---|
| Master SOP | PARTIAL | this document (DRAFT) |
| Organizational roles | PARTIAL | §4 defines roles; no named holders |
| Risk register | PARTIAL | `governance/attack-matrix-2026-08-27.md` (safety/resilience, status: in-progress) — not a business risk register |
| Exception register | MISSING | |
| Data-processing register | MISSING | |
| Data classification matrix | PARTIAL | §6 defines classes; no per-customer matrix |
| Retention schedule / deletion records | MISSING | |
| DPA | MISSING | template required |
| Subprocessor register | MISSING | |
| AI system inventory / provider register | PARTIAL | `governance/capability-registry-v1.md`, `provider-plugins.md`, `adr/002-pluggable-provider-seam.md`, `local-inference.md` — technical registries, lacking §7 data-class / DPA / retention fields |
| Model approvals / model change records | MISSING | |
| Evaluation records | PARTIAL | test suite + `releases/` baselines; no per-model evaluation record |
| AI risk assessments | MISSING | |
| Access reviews | MISSING | |
| Vulnerability register | PARTIAL | `releases/HARDENING-AUDIT.md` (H1–H15) |
| Security review records | EXISTS | `operations/vesta-security-review.md` (AI reviewer — not independent per §4), `releases/HARDENING-AUDIT.md` |
| Incident register / postmortems | PARTIAL | `releases/failure-report-v0.3.0-rc1.md` (deliberate-failure test, not an incident) |
| Release security records | EXISTS | `releases/PRODUCTION-BASELINE.md`, `releases/*` baselines, `PRODUCTION-READINESS.md` |
| Deployment checklist / customer configuration | PARTIAL | `QUICKSTART.md`, `PREREQUISITES.md` — operator setup, not a customer deployment gate |
| Support tickets / SLA records | MISSING | |
| Change records | PARTIAL | git history + `adr/`; no change-request form |
| Continuity / recovery exercise | PARTIAL | `operations/disaster-recovery.md` — self-described as honest and "not good news"; no recorded exercise |
| Offboarding records | MISSING | |
| Evidence ledger | EXISTS | `adr/003-evidence-spine-hash-chain.md`, `operations/merkle-receipts.md` — technical audit chain |
| Authority / approval model | EXISTS | `governance/authority-model.md` (ActionGate dual-governance) |
| Ops runbook | EXISTS | `ops-runbook.md` |
| Independent audit / certification | MISSING | none obtained — do not claim |
| Named Backup Operator / code escrow | MISSING | key-person dependency per §43 |

**Reading this table:** the engineering controls (evidence chain, authority model, release baselines, security review) are real and ahead of most early-stage vendors. The organizational records (registers, DPA, forms, named roles, independent review, continuity) are the gap. Closing that gap is mostly templates plus a first real entry in each — see the controlled-templates list in §36.
