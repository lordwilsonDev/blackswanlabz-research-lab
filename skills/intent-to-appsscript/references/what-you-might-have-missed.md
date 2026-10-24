# What you might have missed

A checklist for the AI to run through with the person, one theme at a time, before the contract is final. Not every item applies; say which do not, and why, and record them as not applicable. Tags as in `options-catalog.md`.

## Ownership and survival
- **Who owns the script and the trigger?** An installable trigger runs as the account that created it **[checked 2026-10-24]**. If that person leaves, is suspended, or loses access, the automation stops or acts with the wrong authority.
- **Backup person.** Name someone who knows it exists and how to switch it off.
- **Shared sheet you do not own.** Triggers and scripts need edit rights; the owner may not want code on their sheet. Ask the owner.
- **Review date.** Put a date to look at it again. Automations nobody remembers are the ones that hurt.

## Triggers and timing
- Script and API edits do not fire edit triggers **[checked 2026-10-24]**. Imports, pasted ranges, form submissions and add-on writes may behave differently **[recheck]**.
- Time-driven triggers can run late within a window **[checked 2026-10-24]**. Design for a late or double run.
- Time zones and daylight-saving changes **[recheck]**: set the script's time zone deliberately and test around a clock change if timing matters.
- A single run has a time limit **[recheck: about 6 minutes for a standard account]**. Large batches need a checkpoint to resume.
- Two runs at once. Use a lock so one finishes before the next starts.

## The data
- Someone renames a tab, inserts a column, or changes a header. Does the script read by name or by position, and what does it do when it cannot find what it expects? It should stop and tell you.
- Formulas versus values: a script that reads a formula cell gets its result; one that writes over it destroys the formula.
- Blank rows, trailing spaces, mixed date formats, numbers stored as text, errors like `#N/A`.
- Hidden rows and filtered views.
- Version history exists in Sheets **[recheck]** and is your undo for sheet data, but not for emails already sent.

## People outside the sheet
- Consent: did these people agree to be contacted this way? A column in a sheet is a record, not a proof. Laws differ by country; this skill is not legal advice.
- An opt-out path that actually works, and a suppression list that overrides everything.
- Wrong-recipient and wrong-name errors: show the first few results to the owner before anything goes out.
- Bounce and complaint handling: who reads the replies?

## Access and permissions
- Read the permissions screen Google shows when the script asks for access; if it asks for far more than the job needs (all of Gmail, all of Drive), stop and narrow the scopes **[checked 2026-10-24]**.
- A Workspace admin may restrict scripts, add-ons or external sharing. Ask before building something an administrator will block.
- Secrets (passwords, API keys) go in script properties or a secret manager, never in the code or in the sheet **[recheck]**.

## Failure and visibility
- How will you find out it failed? Do not rely on checking. Add a failure alert to a person who will see it.
- Keep a short log of what ran and what it did, without personal data or message text in it.
- A visible stop switch: a cell, a checkbox, or one documented step.
- A heartbeat: if nothing has run in the expected window, someone should be told.

## Limits and cost
- Email, trigger, and runtime quotas differ between consumer and Workspace accounts **[checked 2026-10-24 for emails and triggers]**. Draft-creation quotas were not documented in what was fetched; cap your batch size.
- Cost of your time to maintain it. A script that saves ten minutes a month and costs an afternoon to fix every quarter is a loss.

## Testing
- Test on a copy first, with dummy data and your own email addresses.
- Include the ugly cases: an empty row, a duplicate, a row with a missing value, a row someone edits twice.
- A test that shows the dry-run output proves the plan, not the effects.

## Handover
- One page: what it does, when it runs, as whom, what it touches, how to stop it, how to undo it, who to call. The "beginner script" in `SKILL.md` is this page.
