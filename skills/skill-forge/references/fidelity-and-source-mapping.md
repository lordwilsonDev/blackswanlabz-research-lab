# Fidelity and source mapping

Read this at step 5. The aim is that a reviewer can pick any directive and find, in under a minute, where the source says it or be told it is the skill author's addition.

## Locators

A locator names a place a person can go: chapter and section, page, heading, line range, or a quoted opening phrase. "The book" is not a locator. For a source with no stable pagination, use heading path plus the first few words of the passage.

## Statuses

- `SOURCE-CLAIM`: the source states it. Check that the directive does not make the claim stronger than the source does. Hedges ("often", "in our experience", "preliminary") must survive.
- `AUTHOR-ADDITION`: you added it (a workflow step, a guard, a clarification). Fine, but it must never be presented as the source's teaching.
- `UNSOURCED`: you cannot find the passage. Do not ship it silently. Release mode requires `ack:` in the note, recording that the user accepted it as is.

## Typical drift to look for in review

| Drift | Example | Check |
|---|---|---|
| Hardened hedge | Source: "tends to"; directive: "always" | Compare modality words |
| Dropped scope | Source applies to firms over 50 staff; directive is unconditional | Compare conditions |
| Merged claims | Two separate results become one rule | One claim per directive |
| Invented number | A threshold the source never gives | Every number needs a locator |
| Lost attribution | A named test becomes anonymous | Compare names against Attribution |
| Opinion as source | Skill author's preference labelled SOURCE-CLAIM | Spot-check statuses |

## Review procedure

1. The validator confirms every directive has a row and every row has a directive.
2. A reviewer who did not draft the skill opens the source and checks at least five `SOURCE-CLAIM` rows, chosen at random, plus every number.
3. Record the reviewer, date and rows checked in the Note column of those rows (for example "checked 2026-10-04 by R").
