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
- `commits.json` — reduced from the full paginated response of `GET /repos/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE/commits`, captured 2026-09-28 (`gh api repos/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE/commits --paginate`), then stripped to `sha`, `author_date`, `message`, `html_url` per commit and sorted oldest-first (the raw API response also carries contributor email addresses, which this lab does not copy in per its no-personal-data rule). 10 commits total. The earliest is `d24145dfa1e9be62ef83e5262b85d3219b02c32c`, authored 2025-12-18T19:05:15Z, message "Initial commit: AI Projects Collection - 208 projects across 35 categories" — the repo's actual first commit, and the true existence anchor. See [C-017](../../CLAIMS.md).

The `code-frequency.json` first row, `[1765670400, 32543981, -804]`, is the week starting 2025-12-14 00:00 UTC (Dec 14–20): 32,543,981 lines added. That week bucket includes the 2025-12-18 initial commit but the bucket label itself is not the existence date — see [C-001](../../CLAIMS.md) for the line-count claim and [C-017](../../CLAIMS.md) for the existence-anchor claim.

GitHub counts every line of every committed file (source, data, lock files, vendored code). The breakdown into categories is [C-002](../../CLAIMS.md), verified; see [../line-breakdown.md](../line-breakdown.md).
- `line-breakdown.json` — output of `scripts/cornerstone_breakdown.py` run on the streamed tarball of the pinned commit (no clone), captured 2026-09-28.
