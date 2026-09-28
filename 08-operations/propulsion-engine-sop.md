---
source: vault:10_Projects/BlackSwanLabz/SOPs/Propulsion-Engine-SOP.md
vault-date: 2026-09-01
captured: 2026-09-28
status: active
---


> **BlackSwanLabz SOP set** — SOP index  ·  **this doc:** UAC domain module for safety-critical physical systems — activated by the domain classifier, not a general BSL SOP
>
> Active: Master-SOP · Operator-SOP · Hardened-Blueprint-v2.1 · Day-to-Day-Operating-Manual · Complete-Client-Loop · Propulsion-Engine-SOP  ·  Superseded: Operating-Blueprint-v1 · Loop-v0.1

# PROPULSION // META-SYSTEMS ENGINEERING ENGINE SOP v1.0

## Purpose
To discover, design, stress‑test, and verify architectures for safety‑critical physical systems that must remain safe, recoverable, and operational under failure, attack, uncertainty, and partial systemic collapse. PROPULSION is the UAC domain module activated whenever the target profession involves physical safety risk.

## Activation
PROPULSION is triggered automatically by the UAC Domain Classifier when the target system type is:
- energy (generation, transmission, distribution)
- rail / transportation
- water / wastewater
- aviation / aerospace
- industrial control / manufacturing
- healthcare / medical devices
- data center physical infrastructure
- defense / public safety systems

Manual activation: `uac invoke propulsion --target <system>`

---

## 1. Core Protocol (15 Steps)

### Step 1 — Define the Battlefield
Collect: target system, mission, operating environment, failure consequence, current architecture. If any field is missing, flag as UNKNOWN rather than inventing.

### Step 2 — Map the Dominant Paradigm
Diagram inputs, sensors, decision flow, controller, command, actuator, physical system. Identify where failure can propagate.

### Step 3 — Extract Hidden Axioms
Find at least 10 unstated assumptions. Classify each by type (CONNECTIVITY, TRUST, CENTRALIZATION, CONSISTENCY, CORRECTNESS, HOMOGENEITY, AVAILABILITY, OBSERVABILITY, TIMING, HUMAN CONTROL). Assign confidence, failure condition, blast radius, reversibility, and dependencies.

### Step 4 — Perform Radical Inversion
For each high‑risk assumption, invert it. Perform second‑order inversion (invert the inverted architecture). Perform third‑order inversion (find the architecture that survives both failures).

### Step 5 — Search for Anomalies
Hunt across domains—biology, aviation, telecom, spacecraft, immune systems, financial networks—for systems that already survive without the dominant paradigm. Extract the mechanism, not the analogy.

### Step 6 — Mechanism Extraction
Convert analogies into engineering primitives: local autonomy, fault containment, reputation, signal propagation, degraded mode, redundancy, quorum, veto, isolation, recovery, adaptation.

### Step 7 — Build the Architecture
Construct the smallest architecture that implements the discovered mechanisms. Prefer simple deterministic safety mechanisms over complex intelligent ones. Separate intelligence, control, safety, and actuation.

### Step 8 — Authority Decomposition
Define read, write, propose, veto, actuate, isolate, and recover authority for every component. Create an explicit authority graph. Ensure no hidden central authority.

### Step 9 — Safety Kernel
Define the smallest deterministic layer that must remain trustworthy. It enforces invariants, state transitions, physical limits, rate limits, interlocks, fail‑safe states, and recovery conditions. It must function even if the AI disappears.

### Step 10 — Failure‑First Design
Simulate network failure, sensor failure, actuator failure, model failure, controller failure, malicious controller, corrupted data, false sensor data, clock failure, power loss, partial partition, multiple simultaneous failures, coordinated attack, and recovery failure. For each, define detection, containment, degradation, safe state, recovery, and recovery verification.

### Step 11 — Adversarial Self‑Attack
Attack the architecture: central coordination, local autonomy, safety kernel, communication, identity, sensors, actuators, recovery, human override, model outputs. Search for correlated failure, common‑mode failure, emergent failure, and adversarial feedback loops.

### Step 12 — Falsifiable Predictions
State measurable predictions: Time to Containment (TTC), Blast Radius (BR), False Rejection Rate (FR), Successful Recovery Rate (SR), Loss‑of‑Communication Resilience (LCR), Correlated‑Attack Resilience (CAR). Define baseline, experiment, and refutation criteria.

### Step 13 — Minimum Viable Simulation
Build the smallest simulation that can falsify the core hypothesis. Include normal system, centralized baseline, proposed architecture, fault injection, attack injection, network partition, recovery, and metrics.

### Step 14 — Maturity Gate
Classify the result:
- L0 — Concept
- L1 — Mechanism
- L2 — Formal Model
- L3 — Simulation (adversarial simulation passes)
- L4 — Hardware‑in‑the‑Loop
- L5 — Independent Verification
- L6 — Controlled Pilot
- L7 — Production

Never describe L0–L2 as production‑ready.

### Step 15 — Final Architecture Review
Produce discovered inversion, core mechanism, architecture, authority model, safety model, failure model, threat model, falsification, remaining unknowns, and next experiment.

---

## 2. Output Contract

Every PROPULSION output must distinguish:

```text
KNOWN          — verified by independent evidence
INFERRED       — deduced from known facts
HYPOTHESIZED   — plausible but untested
UNVERIFIED     — claimed but not independently confirmed
FALSIFIED      — proven wrong by experiment
```

The final deliverable is a **PROPULSION Architecture Report** conforming to the BUH DNA schema, tagged with domain `safety-critical`, and stored in the Axiom Library with full Merkle audit trail.

---

## 3. Integration with Existing Stack

| PROPULSION Component | Sovereign Component |
|----------------------|---------------------|
| Assumption Extraction + Inversion | AIL Protocol (Steps 0‑5) |
| Three‑Order Inversion | Recursive Axiom Descent (RAD) |
| Cross‑Domain Anomaly Search | Positive Deviant Scout + SRAH |
| Mechanism Extraction | Mechanism Synthesizer (MoIE) |
| Authority Decomposition | Human Decision Broker + Permission Matrix |
| Safety Kernel | Guardian Protocol + Constitutional Firewall |
| Failure‑First Design | Chaos Testing + Digital Twin Simulator |
| Adversarial Self‑Attack | PAP Threat Model + Red‑Team scenarios |
| Falsifiable Predictions | Falsification Theatricality Score (FTS) + Golden Mission |
| Maturity Gate (L0‑L7) | BUH Lifecycle + UAC Skill Lifecycle |
| Output Contract | Evidence Model (6‑state) |

---

## 4. Domain Module Implementation

PROPULSION is deployed as `uac/domains/propulsion.py`. It is invoked when the UAC Domain Classifier detects a safety‑critical physical system. The module:

1. Runs the full 15‑step protocol.
2. Outputs a structured PROPULSION Architecture Report conforming to the BUH DNA schema.
3. Stores the result in the Axiom Library with domain tag `safety-critical`.
4. Schedules a STAR job to re‑run the adversarial self‑attack monthly.

---

## 5. Monthly Adversarial Audit (STAR Job)

```yaml
id: "propulsion-monthly-adversarial-audit"
name: "PROPULSION Adversarial Self-Attack"
schedule: "0 3 1 * *"
tasks:
  - id: "reload_dna"
    skill: "axiom_library_load"
    target: "{{dna_id}}"
  - id: "run_adversarial_attack"
    skill: "propulsion_step_11"
    depends_on: ["reload_dna"]
  - id: "compare_results"
    skill: "propulsion_step_12"
    depends_on: ["run_adversarial_attack"]
  - id: "update_maturity_gate"
    skill: "propulsion_step_14"
    depends_on: ["compare_results"]
  - id: "store_report"
    skill: "axiom_library_ingest"
    depends_on: ["update_maturity_gate"]
```

---

## 6. Activation

To manually invoke PROPULSION on a target system:

> `uac invoke propulsion --target "regional power grid" --mission "maintain service during partial cyber compromise" --environment "mixed legacy/IP-based SCADA" --consequence "cascading outage affecting 500K customers"`

The module will execute all 15 steps and return a structured architecture report with maturity gate L0‑L7.
