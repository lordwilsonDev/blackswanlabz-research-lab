# Source intake and rights

Read this at step 1, and again whenever authorship or terms are unclear. Skill Forge records what the user says about rights; it does not decide them and is not legal advice.

## What to establish

1. **Who made the source**, with the exact names it credits, including contributors and the sources it borrows from.
2. **Who made the skill's source text available to you**, and what they are to the source (author, licensee, a reader with a copy).
3. **What terms the source is under**, quoted if written down.
4. **What the user intends**: private use, internal team, or public release.

## Decision table

| Situation | What to do |
|---|---|
| The user is the author or owns the rights | Record that in `permission_note`. Set `redistribution = "permitted"`. |
| The source states a permissive license (MIT, CC BY, etc.) | Record the license and the credit line it requires. Include the license text or a link and the copyright line. Set `permitted`. |
| The source states a restrictive license or "all rights reserved" | Encode only for private use and short quoted excerpts. Set `restricted`. Do not publish. |
| Terms are unstated or conflicting | Set `unknown`. Keep the skill private. Ask the user to confirm with the author. `--release` refuses. |
| The package claims a license but ships none, or its text claims ownership by others | Treat as conflicting. Record both statements. Ask. |

## What goes in config.toml

`[source]` holds `title`, `authors`, `publisher`, `url`, `accessed`, `source_license`, `redistribution`, `permission_note` and `required_credit`. `[metadata]` holds the skill package's own license, which may differ from the source's. A skill that paraphrases a copyrighted book is not automatically free to publish under the maintainer's license.

## Credit

Copy the source's own credit text. Do not abbreviate a contributor list or reorder it. If the source credits others for specific ideas (a named test, a ladder, a statistic), carry those credits into the skill wherever the idea appears.
