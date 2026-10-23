# Official Apps Script references

Read this before relying on a trigger, scope or quota behavior, and again before deploying.

- Installable triggers: https://developers.google.com/apps-script/guides/triggers/installable
- Simple triggers: https://developers.google.com/apps-script/guides/triggers/
- OAuth scopes and least privilege: https://developers.google.com/apps-script/concepts/scopes
- Service quotas and limits: https://developers.google.com/apps-script/guides/services/quotas
- Authorization: https://developers.google.com/apps-script/guides/services/authorization

## What was rechecked (2026-10-24)

A fetch of the pages above, partly from summaries of truncated pages, found:

| Claim | Result |
|---|---|
| Script and API edits do not fire edit triggers | Confirmed (simple triggers page; example is `Range.setValue()`) |
| Installable triggers run as the account that created them | Confirmed |
| Time-driven triggers do not fire at an exact minute (a 9 AM trigger may run between 9 and 10 AM) | Confirmed |
| 20 triggers per user per script | Confirmed (quotas page) |
| Email recipients per day: 100 consumer, 1,500 Workspace (e.g. MailApp) | Confirmed for sending; **the pages say nothing about a draft-creation limit** |
| Use the narrowest, least-permissive scopes | Confirmed (scopes page, verbatim) |

Draft creation has no documented limit in what was fetched, so a contract that creates drafts should cap its batch size and recheck at deployment. These numbers can change; recheck them when you deploy.
