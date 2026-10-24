# Plain-words glossary

For the AI to use in place of jargon. Explain a term the first time it comes up; do not ask the person to learn the list.

- **Apps Script**: Google's built-in way to write small programs that act on Sheets, Gmail, Calendar and Drive. It runs on Google's computers, not yours.
- **Trigger**: what makes the script start. A time (every Monday), an event (a cell is edited), or you pressing a button.
- **Simple trigger / installable trigger**: the simple kind is limited and runs with little set-up; the installable kind can do more and runs as the person who created it.
- **Scope**: one specific kind of access you grant (read a sheet, create email drafts). Narrow is safer than broad.
- **Authorization**: the screen where you say yes to the script's access. Read it.
- **Dry run**: pretending. It shows what would happen and changes nothing.
- **Idempotent (safe to repeat)**: running it twice has the same effect as running it once. This prevents duplicate emails and duplicate rows.
- **Lock**: a way to make sure two runs do not overlap.
- **Quota**: a daily limit set by Google.
- **Audit log**: a record of what the script did, so you can check later.
- **Rollback**: how to undo what it did.
- **Kill switch**: one easy way to stop it.
- **Consent**: the recipient agreed to be contacted this way.
- **Suppression list**: people who must never be contacted, whatever else says otherwise.
- **Contract (in this skill)**: a short written description, in a file, of what the automation will do, to whom, as whom, and how to stop it. It is agreed before the code is written.
- **Baseline**: what every automation gets. **Situational**: what depends on your circumstances and is decided together.
- **Receipt**: the record of a real test, proving that a run happened. It is self-reported and the validator can check only that it is complete.
- **Container-bound script**: a script that lives inside one specific sheet.
- **Webhook**: a way for another service to send data to a web address when something happens.
- **Concurrency**: many things happening at the same moment.
