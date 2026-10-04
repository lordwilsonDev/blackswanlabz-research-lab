# Source map for test-the-tests

Sources: **FB** = `docs/specs/2026-10-03-freebuff-question-blueprint-v1.1.md` (the lab's blueprint). **PRACTICE** = what was done and observed building the lab's validators in this repository.

| Directive | Source locator | Status | Note |
|---|---|---|---|
| D-01 | PRACTICE: meta_test.py baseline step; FB Part M8 (closure needs implementation passing) | AUTHOR-ADDITION | |
| D-02 | FB Part M2 (a test is evidence only if it exercised its target; TEST_NOT_EVIDENCE) | SOURCE-CLAIM | |
| D-03 | PRACTICE: first mutation run counted unexercised sites; separated after review | AUTHOR-ADDITION | |
| D-04 | FB Part M6 (no new defect is not all defects exhausted); PRACTICE equivalent-mutant triage | AUTHOR-ADDITION | |
| D-05 | FB Part M3 (negative control, mutation test); PRACTICE: three survivors closed with new tests | AUTHOR-ADDITION | |
| D-06 | PRACTICE: tool mutates temp copies only | AUTHOR-ADDITION | |
| D-07 | PRACTICE: a hung test (open port) showed unbounded runs need timeouts | AUTHOR-ADDITION | |
| D-08 | FB Part L2 (metrics tracked separately, never one score) | SOURCE-CLAIM | |
| D-09 | FB Part M1 (what each detector assumes and cannot catch) | AUTHOR-ADDITION | |
| D-10 | FB Part M7 (could the validator produce a false PASS?) | SOURCE-CLAIM | |
| D-11 | FB Part M6 (blind-spot inventory) | AUTHOR-ADDITION | |
