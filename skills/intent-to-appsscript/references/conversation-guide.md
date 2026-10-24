# Working through it together

Read this at the start, and whenever you are unsure what to ask next. The skill gives the baseline; the person's situation decides the rest. Your job is to ask well, recommend with reasons, and record what they decide.

## Contents
1. How to work with the person
2. The baseline, in plain words
3. The questions that depend on the situation
4. Different situations, different emphasis
5. Decisions that are always the person's
6. A short example
7. Teach-back

## 1. How to work with the person

- **One question at a time.** A wall of twelve questions gets guesses. Ask the one that changes the most, then the next.
- **Say why you are asking.** "I'm asking who else can see this sheet, because it decides how careful the script must be with the data."
- **Recommend, then wait.** Give your suggestion and the reason in a sentence, offer the alternative, and let them choose. Never record a choice they did not make.
- **Use their words.** Match their level. If they say "the thing that runs every Monday", say that, and introduce "trigger" only when it helps.
- **Do not ask what you can look up.** Read the sheet's headers, the existing scripts and the documentation first.
- **Do not re-ask.** If they have said it, use it, and quote it back if there is doubt.
- **Unknown stays unknown.** If they do not know, write it in `missing_critical_facts` and say what it blocks.

## 2. The baseline, in plain words

Every automation gets these, whatever the situation. Tell the person early, so they know what to expect. They cannot be skipped.

| Item | What you tell them | Field |
|---|---|---|
| Their request, as they said it | "I'll keep your exact words next to my reading of them, so we can both check I understood." | `source_utterance`, `intent` |
| Who owns it | "Who is responsible for this, and whose account will it run as?" | `owner`, `identity` |
| When it runs | "What starts it, and is exact timing important?" | `trigger` |
| What it reads, and what it does | "Where does it look, and what does it do with what it finds?" | `input`, `action`, `destination` |
| What it may touch | "The smallest set of permissions that gets the job done, listed so you can see them." | `permissions` |
| What happens when it fails | "If something goes wrong, does it stop, retry, tell you?" | `failure_policy` |
| How you know it worked | "What would you check to see it did what you wanted?" | `success_measure` |
| How to undo it | "If it does something you don't want, how do we put things back?" | `rollback` |
| How to stop it | "One clear way to turn it off." | `disable` |
| How we'll test it | "The cases we'll try before trusting it, including the awkward ones." | `tests` |
| Safe first run | "The first run only shows what it would do. Nothing changes until you say so." | `dry_run` |
| What we don't know yet | "Anything we're unsure about is written down, not guessed." | `missing_critical_facts` |
| Your decisions | "Each choice that was yours is recorded as yours." | `decisions` |

## 3. The questions that depend on the situation

For each, propose an answer or propose that it does not apply, say why, and ask. Mark it not applicable only if they agree and you can write the reason.

| Item | Ask | Often applies when | Often does not apply when | Cannot be waived when |
|---|---|---|---|---|
| `predicate` | "Which rows or items should it act on, and which not?" | only some items qualify | it always handles the whole range | |
| `transformation` | "Does it change the data on the way through?" | it reformats, calculates or drafts | it copies as-is | |
| `idempotency` | "If it runs twice, what stops it doing the thing twice?" | it creates, sends, appends | it only reads | it sends, deletes, modifies or shares |
| `audit_log` | "Do you want a record of what it did?" | other people depend on it, or it acts for you while you are away | nothing leaves the sheet and the output is itself the record | it sends, deletes, modifies or shares |
| `data_retention` | "Does it keep personal or sensitive data, and for how long?" | it handles names, addresses, messages | no personal data | |
| `quota` | "Roughly how much will it do per run and per day?" | batches, many emails, many files | a handful of items | |
| `consent_policy`, `rate_limit` | "Who has agreed to be contacted, and how many may go out?" | the action sends or posts | it only drafts or stays internal | (required when sending) |

## 4. Different situations, different emphasis

- **Just for them, inside one sheet.** Keep it short. Focus on trigger timing, a safe first run, and undo. Several situational items will not apply, and that is fine.
- **For a team, or others depend on it.** Spend time on ownership (what if the owner leaves?), the audit trail, who is told when it fails, and the stop switch.
- **It sends or posts anything.** Slow down. Consent, rate limits, drafts-before-send, idempotency, and a clear deployment decision. Ask who is on the receiving end.
- **It deletes or overwrites.** Rollback first: what is the backup, and how long is it kept?
- **Personal or sensitive data.** What is stored, where, for how long, and who can read the logs. Keep content out of logs.
- **One-off.** Ask whether a script is worth it at all, or whether doing it by hand once, a formula, or a filter is simpler.
- **Not sure Apps Script is right.** Say so honestly, give the alternatives with their costs, and let them choose.

## 5. Decisions that are always the person's

Record each in `decisions` with `decided_by` set to `user` or `user_after_ai_recommendation`. Never set it to the AI.

- Which tool (routing), and accepting that Apps Script runs on Google's infrastructure.
- Which permissions to grant.
- Whether it may send anything, and to whom.
- Which situational items do not apply in their case.
- Anything irreversible.
- **Deployment.** Ask in a direct sentence naming the account and what will happen, and record their words in `quote`.

## 6. A short example

> **Person:** When I mark a row READY in my lead sheet I want an email drafted.
> **AI:** Got it. I'll write that down as you said it and check my reading with you. Quick question first: should the email just be saved as a draft for you to look at, or sent automatically? I'd suggest drafts: you see every email before it goes, and it needs fewer permissions. Do you want drafts?
> **Person:** Drafts. I want to read them.
> **AI:** Good, I've recorded that as your choice. One more thing that changes how careful we need to be: does the sheet contain anyone's email address or personal details?
> **Person:** Yes, customers.
> **AI:** Then I'll keep message text out of any logs, and we should only draft for people who agreed to hear from you. Is there a column that shows that?

Notice: one question, a reason, a recommendation, the choice recorded as theirs.

## 7. Teach-back

At the end, ask: "Can you tell me in your own words what this does, when it runs, and how you'd stop it?" If they cannot, explain the part they missed and ask again. An automation its owner cannot stop or explain is not finished.

## Careful or fast

Ask this before anything else. Use the wording in `SKILL.md`, "Choose the working mode first", including the warning in bold; do not soften it. If they ask which to pick: careful for anything that emails people, touches shared or sensitive data, or runs on a schedule unattended; fast is reasonable for a private, small, reversible job they will check themselves. In fast mode, still list every guess at the top of the draft.
