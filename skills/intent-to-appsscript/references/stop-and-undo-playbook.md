# Stop and undo playbook

Give the person these steps in plain words before anything is deployed, and again at handoff. Menu names change; if a name below does not match what they see, trust the screen and tell the skill so the guide can be fixed **[recheck all menu names]**.

## Stop it (fastest first)
1. **Use the built-in switch** if the contract has one (a checkbox or cell that makes the script do nothing).
2. **Delete or disable the trigger.** Open the script, find the Triggers list (the clock icon in the editor), and delete the trigger for the job. This stops future runs.
3. **Remove the script's access.** In your Google Account's security settings, find the third-party and connected-app access list, find the script, and remove its access.
4. **Remove the script.** Delete the project, or its code, only after steps 2 and 3, and only after you have saved a copy.
5. **If it is sending something you cannot stop**, remove the trigger first and then tell the people who may have received it.

## Undo what it did
- **Rows written by mistake:** use the sheet's version history to restore an earlier version, or delete the rows labeled with that run.
- **Drafts created:** delete the drafts; they have not been sent.
- **Emails already sent:** cannot be recalled. Send a correction and fix the cause.
- **Files moved or shared:** move them back and re-check who has access.

## After a stop
- Write down what went wrong, in one paragraph, before restarting.
- Restart in dry-run mode.
- Re-run the contract's tests on a copy.
