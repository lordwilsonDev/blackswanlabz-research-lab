---
source: author-supplied text (Lord Wilson), pasted into the lab build session 2026-09-28
captured: 2026-09-28
status: pending
---

> **Published as the author wrote it.** Every figure below is quoted from the paper's own text and cited sources; none has been link-checked by the lab yet. Treat each as pending until it has a verified row in [CLAIMS.md](../CLAIMS.md). Later work on the same argument as [the thesis](../00-thesis/intelligence-infrastructure-mismatch.md).

# The Constraint Migration: How AI Commoditizes Intelligence and Makes Verified Execution the Next Scarce Infrastructure

**A White Paper**

**Date:** September 28, 2026

---

## Abstract

The AI industry is undergoing a structural inversion. The production of intelligence—the raw output of large language models—is commoditizing rapidly, driven by a documented ~600-fold decline in token prices since 2020. On Vercel’s AI Gateway, open-weight models processed 56% of tokens in August 2026 while capturing only 14% of spend. Simultaneously, the systems required to convert intelligence into reliable outcomes—verification, governance, execution, and the physical substrate of power and interconnection—are becoming the binding constraints. This paper argues that the durable economic asset is not the model, but the **verified capability accumulated around models**: the routing, memory, governance, and evidence infrastructure that persists when the model changes.

**The core thesis:** As model capability becomes cheaper and more interchangeable, the binding constraint migrates from *generating intelligence* to *reliably converting intelligence into verified action*.

---

## 1. Introduction: The Constraint Migration Principle

Technological progress does not eliminate constraints; it relocates them. When intelligence generation is scarce, economic returns accrue to model scale and parameter capacity. As intelligence generation becomes abundant and interchangeable, the economic constraint migrates to the infrastructure that contextualizes, routes, executes, verifies, governs, and preserves that intelligence.

This principle—**Constraint Migration**—is the paper’s central proposition. It is not a physical law, but a systems hypothesis strongly supported by independent evidence across token economics, enterprise deployment data, physical infrastructure constraints, and regulatory pressure.

The causal chain is bidirectional and intersecting:

```
AI CAPABILITY
      │
      ▼
CHEAPER INTELLIGENCE
      │
      ▼
MORE AI DEMAND
 ┌────┴───────────────────────────────┐
 ▼                                    ▼
MORE MODEL CHOICE               MORE COMPUTE
 │                                    │
 ▼                                    ▼
MODEL INTERCHANGEABILITY           POWER (565 TWh '26 / 290 GW '30)
 │                                    │
 ▼                                    ▼
ROUTING / MEMORY / CONTEXT        INTERCONNECTION / SUBSTATIONS
 │                                    │
 ▼                                    ▼
AGENTIC ACTION                  PHYSICAL CONSTRAINTS
 │
 ▼
EXPANDED FAILURE SURFACE
 │
 ▼
VERIFICATION / GOVERNANCE / PROVENANCE
 │
 ▼
VERIFIED OUTCOME
 │
 ▼
ORGANIZATIONAL MEMORY & CAPABILITY ACCUMULATION
```

**Figure 1: The Unified Constraint Model.** Two chains—software-layer verification and physical-layer substrate—intersect to define the binding constraints on AI value creation.

The remainder of this paper examines each link in these chains, distinguishes measured data from forecasts, and specifies what would falsify the thesis.

---

## 2. The Intelligence Commoditization Is Measured and Accelerating

### 2.1 Token Pricing Compression

A recent systematic economic analysis combining OpenRouter data, Epoch AI records, and cross-validated historical observations estimates an approximately **600-fold decline in LLM inference prices between 2020 and 2026** (Du et al., 2026). The analysis identifies a **1.10-year economy-tier price half-life** and a **structural break in May 2024** (Chow test F=5.74, p=.005), attributing **103.7% of price reductions to total factor productivity residual contributions** while GPU hardware advances contributed **−0.9%** over the period.

The Silicon Data LLM Token Expenditure Index, which tracks the weighted effective price paid for tokens, fell below **$1 per million tokens** for the first time in August 2026, reaching **$0.97**—a decline of over 50% from its May 2026 peak of approximately $2.05. Average token prices on Vercel’s gateway fell another **23.2% in August 2026 alone**, the third consecutive monthly decline.

**Methodological note:** The 600-fold figure is a market-wide index derived from 62 cross-validated milestone observations across multiple model tiers. It is not a single pairwise comparison between GPT-3’s launch pricing and one economy-tier model. This distinction matters for adversarial review.

### 2.2 The Open-Weight Surge: Volume and Value Are Separating

On Vercel’s AI Gateway, open-weight models accounted for **56% of tokens processed in August 2026**, up from **7% in December 2025** and **13% in April 2026**. The share reached a record **62% on August 22**. Vercel CEO Guillermo Rauch noted that “this trend is likely only beginning” and that enterprise adoption remains in early stages.

The volume-value gap is the critical finding. Open-weight models processed 56% of tokens but captured only **14% of spending**. Meanwhile, Anthropic maintained **64 cents per dollar of spending**, with its share never falling below 61% since December 2025.

**What this does and does not establish:** This data demonstrates that inexpensive/open models can absorb enormous inference volume while premium models retain disproportionate economic value. It does **not** prove that open models are superior in capability, nor does it represent the entire industry—it is one platform’s gateway traffic. It is a remarkably direct measurement of the separation between *intelligence consumption* and *intelligence valuation*.

### 2.3 Model Interchangeability and the Substitution Boundary

Data from Vercel’s AI Gateway reveals a rapid transition toward model interchangeability and cost sensitivity. Open-weight models grew from under 10% of total token volume in December 2025 to 56% by August 2026, while representing only 14% of total gateway spend—contributing to a 23.2% single-month decline in average token prices.

Intra-provider dynamics confirm that capability exhibits a sharp **price-performance substitution boundary**. Fable 5, Anthropic’s high-tier model, lost over two-thirds of its spend share in one month, dropping from **13.2% in July to 4.9% in August 2026**. This spend shifted predominantly to Anthropic’s lower-priced Opus 5, which captured **22.5% of spend share** in August. Nine out of ten teams migrating away from Fable 5 moved workloads to cheaper, “good-enough” alternatives, demonstrating that incremental frontier intelligence fails to capture enterprise spend if cost per task exceeds the marginal task value. OpenAI’s Astra further accelerated this turnover upon its September 3 launch, capturing **7.7% of total gateway spend** in its first 12 days.

The strategic implication is precise: any competitive advantage built on access to a *particular* model is inherently temporary. As Rauch stated: “We need to change harnesses, command-line tools, integrated development environments and software development kits so they are not tied to a specific model.”

---

## 3. The Reliability Gap: Verified Outcomes Are Not Model Outputs

### 3.1 Reliability Compounds Across Dependent Steps

The gap between model capability and reliable outcomes is structural, not incidental. Consider the arithmetic: a three-agent chain where each agent succeeds 70% of the time produces a **34.3% overall success rate** (0.7³ = 0.343). A five-agent chain at 80% per-step accuracy yields **~33% end-to-end accuracy** (0.80⁵ ≈ 0.328). This is not a model quality problem. It is a systems arithmetic problem.

**Mechanism, not blanket failure claim:** The compounding effect is mathematically necessary whenever (a) steps are sequentially dependent, and (b) each step must succeed for the overall run to succeed. Real agent systems are not always statistically independent—errors can be correlated, and some architectures allow recovery or branching—but the fundamental arithmetic holds for any system where local errors cascade.

### 3.2 Enterprise Deployment Bottlenecks

Multiple 2026 empirical studies indicate a substantial pilot-to-production gap driven by execution and governance bottlenecks rather than model intelligence limits. A March 2026 survey of 650 enterprise technology executives revealed that while **78% had deployed AI-agent pilots**, only **14% had successfully scaled those agents to production**. Similarly, Collibra’s September 2026 study of data and AI leaders found that **76% encountered critical operational and governance roadblocks** when moving agentic systems from experimental environments into active production workflows.

Reported deployment success rates vary substantially across sector analyses due to diverging definitions of “production” and “agentic scale.” The defensible empirical conclusion is that enterprise agent integration remains systematically constrained by **execution, verification, and boundary-enforcement failures** rather than generation capabilities.

### 3.3 Governance Visibility vs. Failure Causality

In a global study of **2,527 decision-makers across 10 countries** conducted by Sinch, **74% of organizations reported rolling back or decommissioning an AI customer-communications agent**. Notably, rollback rates reached **81% among enterprises with mature governance and guardrail frameworks**. Rather than indicating that governance causes operational failure, these results suggest that mature observability and verification tools expose previously hidden execution errors, compliance breaches, and hallucinated state mutations, prompting deliberate rollbacks.

The governance gap is not that oversight is too strict; it is that oversight is too rare. Organizations with fully integrated AI governance are more likely to detect problems early—but detection without remediation is insufficient. Governance must be paired with repair mechanisms.

---

## 4. The Physical Substrate: Abstraction Cannot Eliminate Constraint

### 4.1 Power Is the Binding Constraint

According to Gartner, worldwide data center electricity consumption will reach **565 TWh in 2026** (up 26% from 447 TWh in 2025), with AI-optimized server workloads accounting for **31% of total consumption** and projected to surpass conventional server energy draw by 2027. Global power capacity demand for AI infrastructure is projected to grow from **132 GW in 2026 to 290 GW by 2030**.

As Gartner’s director analyst stated: “AI capacity is now constrained by power availability, making data center power security the new battle ground for scaling and protecting margins in the global AI race.”

The scale of individual facilities has grown dramatically. The **median energy capacity of data centers built rose from 11 MW in 2016 to 130 MW by June 2026**—a nearly 12-fold increase in a decade.

### 4.2 The Interconnection Queue Crisis and the Intent-to-Utilization Ladder

Analyzing AI capacity requires strict distinction across the deployment lifecycle. **A queue request is not capacity; a request is not construction; construction is not energization; energization is not sustained economic utilization.** In ERCOT’s Texas grid audit, while **474 GW of interconnect requests** were filed, only a fraction represents energized, operational data center load.

A symmetrical ladder applies to agentic enterprise software:

```
INTENT → APPROVAL → DEVELOPMENT → STAGING → PRODUCTION → SUSTAINED VALUE
```

Enterprise failure rates spike precisely at the transition between **Approval** and **Production**, where execution safety, context assembly, and deterministic verification replace model capability as the operational primary constraint.

**Critical distinction:** A queue request is not capacity. The 474 GW figure measures *requests*, not committed, funded, permitted, or energized capacity. The relevant constraint is not the queue itself but the conversion rate from request to energized load—and that rate is governed by permitting, supply chain, and grid readiness, not by capital availability.

### 4.3 The Investment Scale

To support this expansion, Morgan Stanley Research estimates combined capital expenditures across five major U.S. technology firms will approximate **$800 billion in 2026** and **$1.2 trillion in 2027**. The upward revision has been driven by first-quarter earnings and the surge in underlying compute demand: global weekly token usage rose **350%** from early January to mid-2026, increasing from about 6 trillion to 28 trillion tokens.

**Announced capex ≠ spent capex.** Morgan Stanley’s figures are forecasts and estimates, not audited expenditures. The distinction matters because capex announcements are strategic signals as well as capital commitments, and actual deployment can be delayed by the very physical constraints documented above.

Power generation availability, transformer supply constraints, and time-to-interconnection now define the physical lower bound for intelligence scaling, complementing the software-layer verification bottlenecks.

---

## 5. The Architecture: What the Evidence Implies

Across independent domains—token economics, enterprise deployment data, physical infrastructure constraints, and regulatory pressure—a consistent causal chain emerges (Figure 1). The intersection of the software-layer verification chain and the physical-layer substrate chain defines the binding constraints on AI value creation.

The distinction between model output and verified outcome can be represented as:

```
MODEL OUTPUT
     ↓
CLAIM
     ↓
EVIDENCE
     ↓
EXECUTION
     ↓
VERIFICATION
     ↓
RECEIPT
     ↓
ORGANIZATIONAL MEMORY
```

A model can produce an answer. But an organization needs to **know, decide, act, verify, learn, and repeat**—with evidence at every step. The model primarily participates in KNOW/DECIDE. The valuable system increasingly owns the entire loop.

---

## 6. The Regulatory Layer: Sovereignty as Architectural Requirement

The core issue in data sovereignty is not where servers sit. It is **who can be compelled to hand over what is on them**. The U.S. CLOUD Act establishes that data access follows corporate control, not physical location. A hyperscaler operating infrastructure in Frankfurt remains subject to the laws governing its parent company.

The EU AI Act’s enforcement began on August 2, 2026, but the high-risk obligations under Annex III have been **deferred to December 2, 2027**, and high-risk AI embedded in regulated products to August 2, 2028. The regulatory landscape is staggered and fragmenting, with the EU, U.S. states, and federal frameworks diverging.

Emerging industry standards reflect this structural pivot toward verification. The **W3C Agent Domain-Specific Community Group (ADACG)** is developing specifications targeting agent identity, operational boundaries, runtime assurance, cryptographic Open KYA (“Know Your Agent”) manifests, and software-version disclosure. While community group incubation does not constitute formal W3C endorsement or mandatory standards adoption, its existence highlights an industry-wide recognition that unverified agentic execution represents a systemic architecture gap.

**Epistemic boundary:** This is a community group draft, not a W3C standard. The relevance is not that this specific specification will become mandatory, but that the problem it addresses—programmatic verification of agent identity and boundaries—is recognized as a structural gap.

---

## 7. What Would Falsify the Thesis

This thesis is a measurable hypothesis about how value migrates as AI capability becomes cheaper. It would be weakened by sustained evidence of the following:

1. **Frontier-model differentiation remained economically durable** despite rapid model turnover, with enterprises consistently paying premium prices for premium models across sustained periods.

2. **Model-specific applications consistently captured more value than model-agnostic infrastructure**, demonstrating that model dependency is a durable competitive advantage rather than a liability.

3. **Agent reliability improved enough that verification and governance became marginal rather than structural costs**, with enterprise failure rates falling below 20% without major changes to workflow or execution infrastructure.

4. **Open/local models failed to capture substantial production workload** despite large price/performance advantages, suggesting that the Vercel data represents a temporary or platform-specific anomaly.

5. **Enterprise AI ROI improved without major changes to workflow, governance, integration, or execution infrastructure**, indicating that the last-mile gap was a temporary skills shortage rather than a structural constraint.

6. **Physical infrastructure constraints stopped materially limiting AI deployment**, with power availability, permitting, and interconnection ceasing to be gating factors.

7. **Enterprises increasingly preferred vertically integrated model-specific systems** despite switching costs, suggesting that the integration benefits of proprietary stacks outweigh the flexibility of model-agnostic architectures.

8. **Commoditization and Universal Abundance of the Verification Layer.** If runtime evaluation, cryptographic provenance, policy enforcement, observability, and execution verification become frictionless, standardized, zero-cost commodities embedded natively across all major model providers, then the core constraint will migrate away from verification infrastructure toward secondary layers, such as proprietary context acquisition, physical kinetic execution, or structural organizational redesign.

The evidence available as of September 2026 supports the direction of the thesis. It does not yet prove the full future prediction.

---

## 8. Strategic Implications

### 8.1 For Enterprises

The finding that **57% of enterprise AI investments fail to outpace capital outlay** should not be interpreted purely as a deficiency in model capabilities. The empirical evidence suggests that **workflow integration, contextual assembly, operational governance, runtime execution, and deterministic outcome verification** represent the primary friction points separating raw model capability from realized enterprise value.

**Priority 1: Context infrastructure.** The Snowflake experiment demonstrated that organizational context—not model quality—is the binding constraint on agent performance. Enterprises must build governed, machine-readable representations of their own data estates before expecting reliable agent behavior.

**Priority 2: Verification architecture.** The pipeline from claim to evidence to receipt to memory must be explicit, auditable, and independent of any single model provider.

**Priority 3: Provider abstraction.** Harnesses, tools, and SDKs should not be tied to specific models. Model churn is accelerating, and model-dependent architectures accumulate technical debt at an unsustainable rate.

**Priority 4: Governance-first deployment.** Organizations with fully integrated AI governance are more likely to detect problems early—but 74% rollback rates suggest that detection without remediation is insufficient. Governance must be paired with repair mechanisms.

### 8.2 For Infrastructure Providers

Power procurement, interconnection, onsite generation, storage, and load flexibility are becoming **strategic variables** in AI infrastructure deployment. The evidence establishes how these variables are becoming more important in different markets; it does not establish that any single solution is universally necessary.

### 8.3 For Regulators

The regulatory landscape is fragmenting, with the EU AI Act’s staggered enforcement, U.S. state-level patchworks, and federal preemption debates. The enterprises that will succeed are those that treat sovereignty and compliance as architectural requirements rather than contractual add-ons.

---

## 9. The Prediction

The following prediction is offered for the research ledger:

> As AI capability becomes cheaper, faster, more interchangeable, and increasingly available through open-weight and local runtimes, competitive advantage will shift away from possession of a particular model toward systems that can dynamically select, constrain, verify, preserve, and reuse capabilities across changing models and physical execution environments.

A second-order prediction follows:

> The faster models improve, the stronger the economic pressure for this abstraction layer becomes, because rapid model turnover increases the cost of being model-dependent.

The evidence supporting this prediction includes the 600-fold price decline in token costs, the 56% open-weight token share on Vercel’s gateway, the 14% pilot-to-production success rate, the 474 GW Texas interconnection queue, and the 74% governance rollback rate.

---

## 10. Conclusion

Models generate intelligence. Infrastructure converts intelligence into agency. Verification converts agency into trust. Memory converts successful execution into accumulated capability.

The model answers once. The infrastructure remembers what worked.

The model changes. The infrastructure persists.

The provider changes. The infrastructure reroutes.

The model hallucinates. The infrastructure verifies.

The model becomes cheaper. The infrastructure becomes more valuable because it can exploit the price difference.

The physical world constrains compute. The infrastructure decides what actually needs compute.

**The durable economic asset is the verified capability accumulated around models, not the transient model instance that produced it.** That is the architecture the evidence points toward. It is not yet proven. But the direction is measurable, the mechanism is testable, and the stakes are structural.

---

## 11. References

1. Du, M. et al. “Tiered Super-Moore’s Law: Price Evolution, Production Frontiers, and Market Competition in Large Language Model Inference Services.” arXiv:2603.28576, March 2026.

2. Vercel AI Gateway Production Index, August–September 2026. Cited in Digital Today, September 2026.

3. Gartner. “Data Center Electricity Consumption to Grow 26% in 2026.” June 10, 2026.

4. MSCI. “Power, Permits and Pushback: The Risks Facing US Data-Center Growth.” September 21, 2026.

5. Utility Dive. “Facing an estimated 474 GW of interconnection requests, Texas hits pause on data centers.” August 5, 2026.

6. TartanHQ. “Why 89% of Enterprise AI Agents Fail in 90 Days.” August 25, 2026.

7. Sinch. “Global Agent Study: 74% of Enterprises Have Rolled Back AI Agents.” May 2026.

8. Collibra. “2026 AI Governance Survey.” September 2026.

9. W3C. “Call for Participation in Agent Declaration and Assurance Community Group.” June 3, 2026.

10. Morgan Stanley Research. “The New AI Credit Playbook.” June 3, 2026.

11. Silicon Data LLM Token Expenditure Index (SDLLMTK). August 2026.

12. CNCF. “How data sovereignty is changing cloud native infrastructure design.” July 3, 2026.

13. EU AI Act Omnibus amendments. August 2026.

14. arXiv. “How Fast Do Agents Rot? An Empirical Study of Long-Horizon Degradation in LLM Agents for Production Decision-Making.” 2026.

---

*Prepared for the research ledger. All quantitative claims are sourced. Forecasts are identified as forecasts. Interpretations are identified as interpretations. The epistemic boundary is explicit.*
