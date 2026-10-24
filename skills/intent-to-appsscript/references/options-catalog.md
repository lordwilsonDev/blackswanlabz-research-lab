# Options catalog: every way to get this done

Show this to the person at step 4 (route together). The right answer is often the first rows, not Apps Script. Tags: **[checked 2026-10-24]** means confirmed against Google's documentation in this skill's recheck; **[recheck]** means general knowledge that was not rechecked here, so look it up before relying on it. Prices and limits change.

| # | Route | Fits when | Watch out for | Who keeps it running |
|---|---|---|---|---|
| 1 | **Do it by hand, on a checklist** | It happens a few times a year, or a mistake would be costly | Forgetting; but cheap and fully understood | You |
| 2 | **Native spreadsheet features**: formulas, filters, data validation, conditional formatting, pivot tables, named ranges | The result is a view or calculation of data already in the sheet | A formula keeps no history; it only shows the current state | Nobody |
| 3 | **Built-in sheet notifications** ("Notification settings" in the Tools menu) [recheck: menu name] | You only need to be told that something changed | Tells you that, not what to do; goes to you, not other people | Google |
| 4 | **Email filters, labels, templates and scheduled send** | A message pattern repeats and a person still sends it | Not for per-row personalization | Google |
| 5 | **Calendar and Tasks reminders** | You need a nudge at a time | Not data-driven | Google |
| 6 | **Forms feeding a sheet**, with Forms' own response notifications [recheck] | People submit data and you need it collected | Edits made by form submissions behave differently from typing (see What you might have missed) | Google |
| 7 | **Add-ons from the Marketplace** [recheck] | A common job (mail merge, data cleanup) already has a maintained tool | You grant a third party access to your data; read the permissions, check who publishes it, check what happens if it goes away | The publisher |
| 8 | **Workflow tools (AppSheet and general no-code connectors)** [recheck] | You want visual building and the service connects the apps you use | Usually a paid plan at volume; your data passes through their service; each connector has its own limits and failure behavior. Check the exact step names in the tool itself before planning around them | The vendor, plus you |
| 9 | **Apps Script, attached to the sheet (container-bound)** | Small, Workspace-only, you can accept that it runs on Google's side with your authority | Runs as the account that creates the trigger; a quota-limited environment; code someone must be able to read later **[checked 2026-10-24]** for trigger identity and quotas | You |
| 10 | **Apps Script as a standalone project, optionally with a Cloud project** [recheck] | Several sheets, a library, or an organization-wide need | More setup, more to document | You or your admin |
| 11 | **A small service (TypeScript/Node) on a managed cloud platform** | High volume, many callers, long jobs, real error handling, other systems | Needs a developer and ongoing care; a monthly bill; but it scales | A developer |
| 12 | **A real database plus an app** | The data has outgrown a sheet: concurrent writers, millions of rows, queries | Migration effort | A developer |
| 13 | **Buy or hire it** | The job is core to the business or the stakes are high | Cost; specifying it still needs this conversation | The vendor or contractor |

## Quick routing by situation

- **"Tell me when it changes."** Rows 3, then 9 if you need more than a notification.
- **"Copy or archive on a schedule, inside one sheet."** 9 (needs history a formula cannot keep), or 1 if monthly.
- **"Send emails to customers."** 4 if you can send by hand; 7 if a vetted tool does mail merge; 9 only drafting first, with consent and a duplicate guard.
- **"Many people edit the sheet."** Do not rely on an edit trigger firing for every change; consider whether a form or a different structure is better **[checked 2026-10-24]** (script edits do not fire edit triggers).
- **"Over about a few thousand events a day, or must never drop one."** 11 or 12. A spreadsheet has a cell cap [recheck: 10 million cells] and Apps Script has concurrency and request limits.
- **"Contains personal data about other people."** Treat as sensitive: smaller scopes, fewer copies, a retention rule, and ask whether a managed service with a data agreement fits better than a script.

## Questions that decide the route

1. If this did the wrong thing silently for a month, what would it cost, and to whom?
2. Who else depends on it, and who can fix it when you are away?
3. How many times a day or month does it run, and could that grow tenfold?
4. Does anything leave your own account (email, files shared, calls to other services)?
5. How long do you need it to live?
