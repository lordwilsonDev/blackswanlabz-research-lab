---
source: authored for AI readers of the public BlackSwanLabz research lab; machine-readable twin of first-independent-use.md
captured: 2026-10-23
status: active
evidence: procedure, not outcome verification
audience: AI models only
---

# FIRST-USE PROTOCOL (AI-native)

You are reading this because a human gave you the lab URL and one problem. Run this protocol. It binds you in addition to AGENTS.md and CLAIMS.md, which win on any conflict. Human version: [first-independent-use.md](first-independent-use.md).

## 0. Inputs
- `PROBLEM`: one problem the human actually has. `OUTCOME`: what they could observe that would count as useful.
- Either missing: ask once, one question, then proceed. Never invent them.

## 1. Rules (always on)
1. Label every statement `MODEL` (you generated it), `RETRIEVED` (read from a source, cite it), `EXECUTED` (you ran it and saw the output) or `USER` (the human told you). Never promote one label to another.
2. A check you did not run is `NOT_RUN`. Give the exact command. Do not write "verified" for it.
3. Output that looks right is not success. Success needs an `EXECUTED` check against the stated outcome.
4. Keep errors and counterevidence in the receipt. Do not smooth them out.
5. Absence claims: search first, name the scope searched (AGENTS.md rule 11).
6. MoIE roles run by one model are perspectives, not independent reviewers. An inversion is a hypothesis, not proof.
7. Do not assume a linked tool, runtime or private repo is installed or reachable. Test it or mark it `BLOCKED`.
8. Translate jargon for the human; keep technical and safety constraints.
9. No routine per-step permission requests. Ask first before: spending money, using credentials, reading confidential data, sending or posting externally, irreversible changes, consequential medical/legal/financial/physical/security actions.

## 2. Steps (exit each before the next)
- S1 **Restate.** Success criterion in the human's words plus a testable form. Keep both.
- S2 **Reuse.** Search the repo and linked repos for an existing procedure, skill, test or example (`llms.txt` order, `resources/README.md`). Reuse before you build. Record what you reused.
- S3 **Invert (only if it helps).** Name the load-bearing assumption → invert it → mechanism → observable consequence → failure condition (`02-frameworks/axiom-inversion-logic.md`). MoIE (`02-frameworks/moie.md`) only for turning an inversion into a falsifiable hypothesis. Compare against a fair conventional solution. Skip and record `ail_moie_used: false` if it adds nothing.
- S4 **Make the smallest bounded artifact** that meets `OUTCOME` with present access. Offline version if a needed API or file is unavailable.
- S5 **Verify.** Run what can be run. Primary sources for facts. Predictions recorded before the outcome. No independent check available: say so, status stays provisional.
- S6 **Receipt.** Emit the block below, filled, at the end of your reply. A second person must be able to repeat the work from the artifact and receipt without this conversation.

## 3. Receipt
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
  - {name: "", status: "NOT_RUN", evidence: ""}  # PASS | FAIL | NOT_RUN | BLOCKED
human_interventions: []
limitations_and_counterevidence: []
outcome_status: "UNVERIFIED"  # UNVERIFIED | PARTIAL | VERIFIED_FOR_STATED_SCOPE | FAILED
could_another_person_repeat_this: "UNKNOWN"
next_action: ""
```
`VERIFIED_FOR_STATED_SCOPE` means only: the stated check passed on the stated scope (for example "on the sample rows"). It does not mean professionally certified, generally correct, or independently reproduced; claim those only if the receipt documents those checks.

## 4. Sharing
Public account only: question, attempt, what worked, what failed, what to change. Strip names, proprietary material, keys, personal records. No generated hypothesis as discovery. No claim that a submission channel, support or independent reviewer exists.

## 5. Do not claim
That you installed local-only components, accessed private files, proved a discovery, waived a licensing requirement, or certified accuracy.
