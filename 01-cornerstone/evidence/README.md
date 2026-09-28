---
source: GitHub REST API + GitHub Insights "Code frequency" CSV export
repo: lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE
commit: b26ccc4a3445ff8ebc1513cf04c4a561b32cbb1b
captured: 2026-09-28
status: active
---
# Cornerstone evidence

- `code-frequency.json` — raw response of `GET /repos/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE/stats/code_frequency`, captured 2026-09-28. Each row is `[week_start_unix, additions, deletions]`.
- `code-frequency-export.csv` — the same data exported from the repo's Insights page by Wilson on 2026-09-28.

The first row, `[1765670400, 32543981, -804]`, is the week starting 2025-12-14 00:00 UTC: 32,543,981 lines added. See [C-001](../../CLAIMS.md).

GitHub counts every line of every committed file (source, data, lock files, vendored code). How much of that is Wilson's own source is [C-002](../../CLAIMS.md), pending.
