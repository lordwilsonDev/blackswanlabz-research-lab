# AIL and MoIE review of intent-to-appsscript v0.2.0

Recorded 2026-10-25. Method follows the lab's own definitions (`02-frameworks/axiom-inversion-logic.md` and `moie.md`): an inversion is a generator, not evidence, so each one was turned into a prediction and tried against the real validator. The MoIE experts below are analytical passes by one reviewer, not independent agents. Whether this method beats a plain review is still the lab's open question (claim C-004, pending); here it was used as a structured checklist, and its output was checked by running code, not by argument.

## 1. Inversion Critic: assumptions inverted

For each: assumption, why it matters, inversion, the observable consequence predicted, the condition where the inversion should fail.

| ID | Load-bearing assumption | Inversion, and the prediction | Should fail if |
|---|---|---|---|
| A1 | Non-empty text carries information | A placeholder or invisible text passes. Predict: `TODO`, `tbd`, `n/a`, a zero-width space validate. | the validator checks content |
| A2 | Names in a list identify one thing each | Duplicates hide a failure; odd members crash. Predict: a FAIL followed by a PASS of the same name passes; a list inside `tests` raises. | names are checked for uniqueness and type |
| A3 | Exact string match finds broad scopes and sending actions | Another spelling slips past. Predict: `https://mail.google.com` (no slash), `Send_Email`, `email_send` bypass the rules. | values are normalized |
| A4 | A PASS receipt means the real thing ran live | Predict: a dry-run receipt, or a receipt for another deployed version, verifies. | the receipt records mode and version |
| A5 | An evidence field makes a PASS credible | Predict: `evidence: ""` passes. | evidence is required |
| A6 | JSON means one thing | Predict: a duplicate `status` key silently takes the last value; `--hash` crashes on an array. | duplicates are refused |
| A7 | The contract covers what the skill promises | Predict: a contract with no rollback and no success measure validates, though the Mission promises both. | those fields are required |
| A8 | The validator never crashes on hostile shapes | Predict: wrong-typed values in any field, under any status, raise. | every path is guarded |
| A9 | The hash binds a receipt to its contract | Predict: fields excluded from the hash allow a material change. | excluded fields carry no behavior |
| A10 | A receipt path inside the folder is trustworthy | Predict: absolute paths, symlinks, directories, `..`, the contract itself get through. | containment is enforced |
| A11 | "Blocking question" and "explicit authorization" are understood | Predict: two readers disagree about what counts. | both are defined in the skill |
| A12 | Time is unambiguous | Predict: time zone, daylight saving and overlapping runs are unaddressed. | the inversions list covers time |

## 2. Positive Deviant Scout: what was real (probes run against v0.2.0)

First run: 23 probes, 13 failures and 2 errors. After widening the crash probe to every status: 24 probes, 15 failures and 2 errors.

| ID | Outcome |
|---|---|
| A1 | **Confirmed.** Placeholders and invisible text validated. |
| A2 | **Confirmed**, with a correction to my own method: the first crash probe varied fields under one status and found nothing (**prediction refuted by a probe that was too narrow**). Run under every status, a list inside `tests` raised `TypeError: unhashable` in `LOCAL_TESTED`. Duplicate names also hid a FAIL. |
| A3 | **Confirmed.** `https://mail.google.com`, `Send_Email`, `email_send` and similar bypassed the rules. |
| A4 | **Confirmed.** A dry-run receipt and a receipt for another version both verified. |
| A5 | **Confirmed.** Empty evidence passed. |
| A6 | **Confirmed.** Duplicate keys took the last value; `--hash` raised on a non-object. |
| A7 | **Confirmed.** No rollback or success measure was required. |
| A8 | **Confirmed** (see A2). |
| A9 | **Held, no defect.** The excluded fields (status, evidence, version, authorization) are meant to change. Version drift is covered by the new `deployed_version` match instead. |
| A10 | **Held.** Absolute path, symlink, directory, `..`, self-reference and `.` were all rejected. |
| A11, A12 | Not testable by the validator; fixed in the text (below). |

## 3. Mechanism Synthesizer: three root causes

1. **The validator trusted shape over content.** Placeholders, spellings, duplicates and wrong types all passed because the checks asked "is a value there?" not "is it a real value?" (A1, A2, A3, A8).
2. **A receipt proved less than it looked.** It did not say live versus dry, which version, or show evidence (A4, A5, A6).
3. **The skill promised more than the contract required.** Rollback, a success measure and clear definitions were in the prose but not in the checks (A7, A11, A12).

## 4. Fixes (v0.3.0)

Fifteen defects, fourteen in the validator and one gap between promise and contract:

1. Placeholders (`TODO`, `TBD`, `N/A`, `fixme`, `xxx`, `none yet`, anything starting todo/tbd/fixme) and text with no letter or digit are rejected, after Unicode normalization.
2. Duplicate check names in a receipt are rejected.
3. Duplicate names in `test_results` are rejected.
4. Duplicate contract `tests` are rejected.
5. Non-text list members are problems, not crashes.
6. Scopes are compared case-insensitively, ignoring a trailing slash; calendar, contacts, and read-only Gmail and Drive scopes are now broad.
7. Sending is recognised by words in the action name in any spelling, including `email`, `message`, `dispatch`, unless the action is clearly a draft.
8. External and destructive actions are recognised the same way when deployed without authorization.
9. A dry-run receipt cannot verify.
10. A receipt must match the contract's `deployed_version`.
11. `VERIFIED_IN_SCOPE` requires a `deployed_version`.
12. A PASS check needs evidence.
13. Duplicate JSON keys are refused (exit 2).
14. `--hash` on a non-object exits 2 instead of raising; `validate` can no longer raise at all.
15. `rollback` and `success_measure` are now required contract fields.

Text fixes: "blocking question" and "explicit authorization" are defined; the inversions list gained time (A12) and "the record shows what ran"; D-18 and D-19 added.

## 5. Red Team: attacks on the fixes

| Attack | Result |
|---|---|
| Fullwidth `ＴＯＤＯ` as a placeholder | Accepted at first. **Fixed** (Unicode normalization). |
| `dispatch_mail`, `email_everyone` as send actions | Accepted at first. **Fixed** (soft sending words, with a draft exemption). |
| Full calendar and contacts scopes | Accepted at first. **Fixed** (added to the broad list). |
| `quota = "asdf"` or `"to do later"` | **Accepted. Not fixable:** the validator cannot judge meaning. |
| `t0do` (leetspeak) | **Accepted.** Chasing spellings has no end. |
| A hand-written receipt with `evidence: "see log"` and `executed_by: "x1"` | **Accepted. Not fixable here:** a receipt is self-reported. |

The three unfixable cases are recorded as tests (`test_known_limits_are_real_limits`) so they cannot be quietly forgotten.

## 6. Prediction Generator: what would show this review is wrong

- A hostile input that makes `validate` raise or return an empty list when it should not. The probes in `tests/test_adversarial.py` try 18 values in every field under all six statuses; one counterexample would refute "never raises".
- A mutation of the validator that the 58 tests do not notice. The run at the time of writing caught all 191 (0 survivors).
- A real automation whose contract passes this validator yet does harm. Not tested: no automation has been deployed with this skill.

## 7. Residual risk (what this review did not and cannot fix)

- The validator checks form, never truth or meaning.
- The broad-scope and sending-word lists are not exhaustive; the contract author must still justify scopes.
- "Post" and "message" over-flag by design.
- Google documentation was rechecked from page summaries on 2026-10-24.
- No model has run the skill on a real task, and no Apps Script was generated or deployed.
