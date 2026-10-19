---
name: building-a-business
description: Use when a person wants to start, structure, or improve a business (or research group) and needs goals, a North Star, OKRs, KPIs, business functions, or SOPs worked out in plain language; when asked to apply the BlackSwanLabz lab's business, research, or white-paper material to a new business; or when a business or research repo must be read to learn what exists versus what is only designed.
---

# Building a Business

**Type:** meta-skill, a compiler plus router. It turns a person's intent into a small set of business artifacts, grounds them in what a repo actually contains, and hands each job to the skill that does it best. It does the thinking order; other skills do the specialist work.

**Core principle:** separate *designed* from *running* from *proven*. A plan is not a result. Never invent a number.

## Steps (one question at a time, plain words, "unknown" is an allowed answer)

0. **Prerequisite.** **REQUIRED SUB-SKILL:** use `surfacing-unasked-questions` before step 1; its disclosures and up to three questions come first.
1. **Ground.** Search the vault first (`vault-search`). If a lab or business repo exists, run
   `python3 skills/building-a-business/scripts/repo_state.py --repo <path> [--ci]`.
   Read its banners and claims counts aloud as the repo's own words. No repo? Skip.
2. **Intent.** Run the starter interview in `references/interview.md`. Keep an intent state: confirmed / inferred / provisional / unknown / conflicted. Ask the next question that most reduces risk. Follow the interview rules in that file (read-back, probe absolutes, declared vs verified, real vs imagined).
3. **Metrics.** Draft North Star, then OKRs, then KPIs from `references/metrics.md`. Every metric gets a baseline (or "measure first"), source, owner, cadence, and a paired guardrail.
4. **Functions.** Size to the person's tier in `references/functions-and-sops.md`. "Not yet" is a valid answer for most functions.
5. **SOPs.** Write only for work done repeatedly; 3 to 5 first. Mark each DRAFT (designed, not run).
6. **Evidence.** When a claim needs support, label it: observed / documented / declared / inferred / hypothesis / unknown. Route research below.
7. **Decide.** Fill a decision card (option, evidence, risk, cost, revisit date). Include "do nothing". Human approves anything consequential.

Save outputs to a folder the person chooses (default `business-os/`): `intent.md`, `metrics.md`, `functions.md`, `sops/`, `decisions.md`.

## Route, don't reimplement (confirm each skill exists before invoking)

| Need | Skill |
|---|---|
| Should I pursue this? | governed-innovation-lite |
| Tradeoffs for a solo founder | solo-founder, one-person-ai-business |
| Map a process into an SOP | process-mapper, operations:process-doc, operations:runbook |
| Risk, change, status | operations:risk-assessment, operations:change-request, operations:status-report |
| Finance, legal | finance:*, legal:* (always say professional review is needed) |
| Research with sources | srse-acquiring-sources, srse-validating-adversarially, srse-calibrating-confidence |
| Documents, sheets, decks | anthropic-skills:docx, xlsx, pptx |
| Before saying done | superpowers:verification-before-completion, closer |

## Rules

- Not a licensed legal, tax, or investment advisor. Name where a professional is required.
- A lab document is a design unless a run, claim row, or banner says otherwise. Quote the banner.
- No fabricated figures, customers, or results. Unknown stays unknown.
- Ask before any outward action (sending, publishing, paying, signing up).
- Keep it proportional: a one-person business gets one page per artifact, not a Fortune 500 manual.

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing 20 KPIs | Three to seven, each paired with a guardrail |
| Target numbers with no baseline | Write "baseline: measure first" |
| Calling hours saved "money saved" | Capacity released is not value until it is converted |
| Treating repo sections as working systems | Re-read the banners and claim statuses |
| Building every function now | Build the ones the next 90 days need |
