---
source: github.com/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE
repo: lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE
commit: b26ccc4a3445ff8ebc1513cf04c4a561b32cbb1b
captured: 2026-09-28
status: active
---
# Line breakdown of the cornerstone (C-002)

Breaks the 32.5 million committed lines ([C-001](../CLAIMS.md)) into categories. Raw output: [evidence/line-breakdown.json](evidence/line-breakdown.json). Tool: [scripts/cornerstone_breakdown.py](../scripts/cornerstone_breakdown.py).

## Method

GitHub's tarball of the pinned commit was streamed straight into a Python script (stdlib only); no clone, nothing written to disk except the JSON summary.

```
gh api repos/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE/tarball/b26ccc4a3445ff8ebc1513cf04c4a561b32cbb1b | python scripts/cornerstone_breakdown.py > breakdown.json
```

Each text file's lines are counted (newline count, plus one if the last line has no newline). Files with a NUL byte in the first 8 KB are treated as binary and skipped (18,579 files). Each file gets exactly one category, checked in this order:

1. **vendored_or_build**: any parent directory is named `node_modules`, `site-packages`, `.venv`, `venv`, `env`, `vendor`, `dist`, `build`, `__pycache__`, `.git`, `third_party`, `external`, `.tox`, `target`, `.next`, `bower_components`, or ends in `.egg-info` / `.dist-info`.
2. **lockfile**: `package-lock.json`, `yarn.lock`, `poetry.lock`, `Pipfile.lock`, `Cargo.lock`, `pnpm-lock.yaml`, `uv.lock`.
3. **minified**: `.min.js`, `.min.css`, `.map` (none found).
4. **source**: `Makefile`, `Dockerfile`, or extension `.py .sh .js .ts .tsx .jsx .rs .go .swift .java .c .h .cpp .hpp .rb .html .css .scss .sql .mk .toml .cfg .ini .ejs .d .hcl .tf`.
5. **docs**: `.md .rst .adoc`.
6. **config**: `.yaml .yml`.
7. **data**: `.json .jsonl .csv .tsv .txt .log .xml .ndjson .parquet .pkl .npy`.
8. **other_text**: everything else.

## By category

| Category | Lines | Files |
|---|---:|---:|
| vendored_or_build | 24,471,508 | 160,307 |
| source | 5,074,633 | 14,208 |
| data | 1,919,024 | 26,033 |
| docs | 1,008,083 | 6,332 |
| lockfile | 49,581 | 12 |
| config | 3,320 | 42 |
| other_text | 16,878 | 411 |
| **Total text lines** | **32,543,027** | |

The total equals GitHub's net additions for the repo (32,544,351 added minus 1,324 deleted across all weeks in code-frequency.json = net 32,543,027), which corroborates [C-001](../CLAIMS.md). The stream was run twice (once by the lab build, once independently) and the JSON output was byte-identical.

## Source lines by language

| Language | Lines |
|---|---:|
| Python (.py) | 4,278,278 |
| Shell (.sh) | 744,646 |
| TypeScript (.ts) | 18,760 |
| Rust (.rs) | 17,180 |
| HTML | 6,473 |
| JavaScript (.js) | 5,667 |
| CSS | 961 |
| Other (.tsx, .swift, Dockerfile, .toml, .sql, Makefile, .jsx, .ejs, .hcl, .ini) | 2,668 |

## What this does not show

"Source outside vendored and build folders" is a folder-name and extension rule, not proof that every line was hand-written. It may include:

- copied libraries that sit outside the standard vendor folder names;
- generated files;
- AI-assisted or AI-generated code.

The 744,646 shell lines in particular have not been examined. Whether the source lines were written for the package rather than copied or generated is a separate open claim ([C-045](../CLAIMS.md), pending). Directory-name rules (env, external, target, build and so on) can misclassify project code that happens to sit in such folders. Binary files (18,579) are not counted at all. Line counts include blank lines and comments; this is not a tokei-style code/comment/blank split.
