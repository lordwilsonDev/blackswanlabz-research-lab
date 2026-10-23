---
source: authored for the public BlackSwanLabz research lab
captured: 2026-10-23
status: active
evidence: procedure, not outcome verification
---

# First Independent Use — From One Question to One Verified Result

**Audience:** Anyone with a question and an AI assistant that can read GitHub. No degree, programming experience, paid subscription, or installation of the full BlackSwanLabz stack is required to *begin*. Some tasks may require tools, credentials, paid inference, or specialized expertise to complete.

**Purpose:** Help a person who did not build BlackSwanLabz use its published methods to produce **one useful result**, see what was and wasn't verified, and optionally share an honest account. This is an alternative short entry point, **not a replacement** for the [full onboarding process](using-with-your-ai.md), [50-question OS bootstrap](../08-operations/50-question-os-bootstrap-v1.md), or existing skills.

## What this is—and is not

The research lab contains methods, source links, artifacts, evidence records and implementation references. This guide helps a new user apply an accessible part of that work with their own AI model. It **does not** claim to install local-only components, grant access to private files, turn a model response into a proven discovery, remove professional licensing requirements, or certify scientific accuracy.

Your first result can be modest: a corrected spreadsheet, a reproducible calculation, a working automation in a sandbox, a documented explanation of a hard concept, or a tested software change. Choose something **bounded and low-risk** before attempting consequential medical, legal, financial, physical or security actions.

## Start in five minutes

1. Open the [BlackSwanLabz Research Lab](https://github.com/lordwilsonDev/blackswanlabz-research-lab).
2. Give your AI the repository URL and the instruction below.
3. State **one problem you actually have** and what an observable useful outcome looks like.
4. Let the AI read the *relevant* sources and construct the smallest safe task, checking reuse before new construction.
5. Ask for a result, a test, and a receipt—not a congratulatory narrative.

### Copy and paste into Claude, Codex, Gemini or another capable assistant

```text
Act as my BlackSwanLabz first-use guide.

Read https://github.com/lordwilsonDev/blackswanlabz-research-lab
and begin with README.md, AGENTS.md, llms.txt, CLAIMS.md and
resources/using-with-your-ai.md. Honor repository status labels and
access boundaries. Use AIL at 02-frameworks/axiom-inversion-logic.md
and MoIE at 02-frameworks/moie.md when they help this particular task.

My problem: [ONE QUESTION OR PROBLEM]
Useful outcome: [WHAT I WANT TO OBSERVE]

Before building, find a reusable procedure, example, test or skill.
Do not assume inaccessible tools are installed or run.
Translate advanced material into clear language without removing
necessary technical or safety constraints.
Identify the load-bearing assumption; invert it meaningfully; show
what evidence could distinguish the alternatives. Do not treat
inversion as proof.

Produce the smallest bounded useful artifact or answer available
with my present access. Run relevant checks when possible. Otherwise
give exact reproducible commands and mark them NOT RUN.
Preserve errors and counterevidence. Separate model-generated claims,
retrieved evidence, executed results and my own understanding.
Do not ask routine permission at every step; ask before consequential
external actions, money, confidential information access or changes
that cannot be safely reversed.

At the end produce a compact FIRST-USE RECEIPT with:
question, sources/revisions, method, artifact, tests and outcomes,
human interventions, unresolved unknowns, status, and next use.
Never claim success just because the output looks convincing.
```

## The first-use procedure

**1. Reconstruct the question.** Define success without requiring the person to know the domain's jargon. Preserve the user's original question alongside the technical formulation.

**2. Discover existing capability.** Read the repository's actual evidence maps, source links and relevant skills. Reuse documented components. Do not confuse a link to an unavailable local runtime with accessible execution.

**3. Invert only where useful.** Apply AIL's identify → invert → mechanism → observable consequence → failure condition pattern. MoIE's roles are analytical perspectives; one model simulating five roles is not five independent reviewers. Compare the inversion to a fair conventional solution.

**4. Build or answer.** The person sets direction. The assistant retrieves sources, develops the minimal solution and explains the mechanism in accessible terms. Do not require the person to complete a doctoral curriculum first.

**5. Verify.** Test what can actually be tested. For factual claims, inspect primary sources. For software, run reproducible checks. For forecasts, record predictions before the outcome. If independent verification is unavailable, say so and retain the result as provisional.

**6. Transfer.** Save the artifact, reusable instruction, sources and receipt. A second person should be able to repeat the steps without relying on hidden conversation history. Keep privacy-sensitive content out of public reports.

## First-use receipt (copy for each trial)

```yaml
trial_id: "FIRST-USE-YYYYMMDD-001"
question_original: ""
problem_formulation: ""
desired_outcome: ""
repository_revision: ""
sources_and_permissions: []
existing_capability_reused: []
ail_moie_used: false
inversion_and_failure_condition: ""
artifact_location: ""
tests:
  - name: ""
    status: "NOT_RUN" # PASS | FAIL | NOT_RUN | BLOCKED
    evidence: ""
human_interventions: []
limitations_and_counterevidence: []
outcome_status: "UNVERIFIED" # UNVERIFIED | PARTIAL | VERIFIED_FOR_STATED_SCOPE | FAILED
could_another_person_repeat_this: "UNKNOWN"
next_action: ""
```

**Important:** `VERIFIED_FOR_STATED_SCOPE` does not mean professionally certified, generally correct across a discipline, or independently reproduced unless the receipt documents those additional checks.

## An example of appropriate scope

**Question:** "Can I automate a recurring calculation in my small business?"

**Possible result:** A script using a sample CSV, an explanation of the formula, comparison against hand-calculated sample rows and a repeatable command. If only sample data was tested, state **verified on the sample**, not "deployed to the business." If a needed API or file is unavailable, produce a bounded offline version rather than inventing access.

## When to use the longer process

For an organization-wide operating system, use the [50-question onboarding](using-with-your-ai.md). For a scientific claim, use the [lab verification skill](../.claude/skills/lab-verify/SKILL.md) and domain-appropriate evidence. For creating a reusable skill, inspect the [Skill Foundry](https://github.com/lordwilsonDev/blackswanlabz-skill-foundry) and its readiness boundaries. For actions requiring authorization, use existing MSB governance contracts where accessible.

## Share a result—without exposing yourself

The most useful public contribution is a concise, reproducible account: **what question you asked, what you tried, what worked, what failed and what you would change**. Remove names, proprietary materials, API keys and personal records. Do not present generated scientific hypotheses as discoveries until the required evidence exists.

You can share a public GitHub issue or discussion describing your own trial where the repository permits it. This guide does not claim that a submission channel, support commitment or independent reviewer is currently available.

**BlackSwanLabz's practical promise is access to a process for turning a question into a bounded, inspectable result—not a guarantee that every question has been solved.**
