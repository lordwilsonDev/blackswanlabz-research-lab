# BlackSwanLabz Research Lab v1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single repo that guides people (README) and an AI model (`llms.txt`/`AGENTS.md`) through all of Wilson's work, where every claim links to evidence and a script re-checks it.

**Architecture:** Hub + curated snapshots. Markdown content in seven numbered folders, each file carrying a front-matter header that records its source and pinned commit. A stdlib-only Python checker (`scripts/verify.py`, wrapped by `scripts/verify.sh`) enforces the rules — claim references, links, headers, size budget, secrets, pinned commits, cornerstone code frequency — locally and in GitHub Actions.

**Tech Stack:** Markdown; Python ≥3.11 stdlib (checker); pytest (tests only); `gh` CLI (online checks); GitHub Actions (`ubuntu-latest`, Python 3.12); `tokei` (optional line-count task).

**Spec:** `docs/specs/2026-09-28-research-lab-design.md` (commit `776fdb6`).

## Global Constraints

- Repo root: `~/projects/blackswanlabz-research-lab` (git, branch `main`, **no remote yet**). Never push or create a GitHub repo — publishing is Wilson's decision (spec §13 step 7).
- Local Python: `/opt/homebrew/Caskroom/miniforge/base/bin/python` (3.12.9, has pytest 9.1.1). Every command below uses `$PY`; set it once per shell: `PY=/opt/homebrew/Caskroom/miniforge/base/bin/python`.
- `scripts/verify.py` uses the standard library only.
- Licenses: CC BY 4.0 (writing/papers, `LICENSE`), MIT (scripts, `LICENSE-CODE`).
- Size budget: all text in the repo (excluding images/PDF/binaries and `.git`) stays under **150,000 tokens** (estimated as characters ÷ 4).
- Snapshot header keys: `source`, `captured` (YYYY-MM-DD), `status` ∈ {`active`, `archived`, `pending`}; optional `repo` + `commit` (pin), `vault-date`.
- Claim statuses: `verified`, `pending`, `retracted`. Pending is never restated as fact.
- "Lines committed" is never written as "lines of code" until C-002 is verified.
- **Nothing private:** no client material, no legal or family matters, no secrets/tokens, no personal notes about Wilson, no non-public business or fundraising material, no email addresses except `noreply` ones.
- Pinned commits must exist on the **remote** (check with `gh api repos/<repo>/commits/<sha>`); never pin a local-only commit (msb-v3 local `main` has unpushed `[do-not-push]` commits).
- ORCID stays blank in `CITATION.cff`.
- FCVE is **archived** (Wilson declared it dead 2026-09-19): describe as completed work, never as ongoing.
- Commit messages end with a `Co-Authored-By: <model that wrote the commit> <noreply@anthropic.com>` line naming the model that actually wrote it (e.g. `Claude Haiku 4.5`, `Claude Sonnet 5`, `Claude Opus 5.5`). Decided by Wilson 2026-09-28. The commit examples below show the Opus line; substitute your own model.

---

## File Structure

```
blackswanlabz-research-lab/
├── README.md                     Task 12 — the guided tour
├── llms.txt                      Task 13 — AI entry point
├── AGENTS.md                     Task 13 — rules for models
├── CLAIMS.md                     Task 6 (seed), extended in 8–11
├── CITATION.cff                  Task 1
├── LICENSE / LICENSE-CODE        Task 1
├── .gitignore                    Task 1
├── 00-thesis/                    Task 8
├── 01-cornerstone/               Task 6 (evidence), Task 7 (timeline)
├── 02-frameworks/                Task 9
├── 03-systems/                   Task 10
├── 04-papers/                    Task 11
├── 05-experiments/               Task 11
├── 06-proofs/                    Task 10
├── scripts/verify.py             Tasks 2–5 — all checks, one module
├── scripts/verify.sh             Task 5 — wrapper
├── tests/test_verify.py          Tasks 2–5
├── .github/workflows/verify.yml  Task 5
└── docs/specs/, docs/plans/      existing
```

`verify.py` is one module because every check shares the same inputs (repo root, CLAIMS) and the whole file stays under ~250 lines.

---

### Task 1: Scaffold

**Files:**
- Create: `LICENSE`, `LICENSE-CODE`, `CITATION.cff`, `.gitignore`, `tests/conftest.py`

**Interfaces:**
- Produces: `tests/conftest.py` puts `scripts/` on `sys.path` so tests can `import verify`.

- [ ] **Step 1: Create `.gitignore`**

```
__pycache__/
*.pyc
.pytest_cache/
.DS_Store
```

- [ ] **Step 2: Create `LICENSE` (CC BY 4.0)**

Download the official legal code text and save it verbatim:

```bash
cd ~/projects/blackswanlabz-research-lab
curl -fsSL https://creativecommons.org/licenses/by/4.0/legalcode.txt -o LICENSE
head -3 LICENSE
```
Expected: first lines contain `Attribution 4.0 International`. If the download fails, stop and report — do not hand-write license text.

- [ ] **Step 3: Create `LICENSE-CODE` (MIT)**

```
MIT License

Copyright (c) 2026 Lord Wilson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Applies to: scripts/ and tests/. All other content is licensed under CC BY 4.0 (see LICENSE).
```

- [ ] **Step 4: Create `CITATION.cff`**

```yaml
cff-version: 1.2.0
message: "If you use or build on this work, please cite it as below."
title: "BlackSwanLabz Research Lab"
type: dataset
authors:
  - family-names: "Wilson"
    given-names: "Lord"
    alias: "lordwilsonDev"
license: CC-BY-4.0
repository-code: "https://github.com/lordwilsonDev/blackswanlabz-research-lab"
date-released: "2026-09-28"
```
(No `orcid` key — Wilson has not registered one.)

- [ ] **Step 5: Create `tests/conftest.py`**

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
```

- [ ] **Step 6: Commit**

```bash
git add .gitignore LICENSE LICENSE-CODE CITATION.cff tests/conftest.py
git commit -m "chore: scaffold licenses, citation, test harness

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Checker — CLAIMS parsing and README claim references

**Files:**
- Create: `scripts/verify.py`
- Test: `tests/test_verify.py`

**Interfaces:**
- Produces:
  - `Claim` — frozen dataclass: `id: str, claim: str, evidence: str, how_to_check: str, status: str, checked: str`
  - `parse_claims(text: str) -> dict[str, Claim]` — raises `ValueError` on bad column count, bad status, or duplicate ID
  - `check_claim_refs(text: str, claims: dict[str, Claim], name: str = "README.md") -> list[str]`

Rules for `check_claim_refs`, per line:
1. Every `C-###` referenced must exist in `claims`.
2. A line containing a "big number" — a comma-grouped number (`32,543,981`) or a number followed by `%`, `M`, or `million` — must reference at least one claim.
3. If a line references a claim whose status is not `verified`, the line must contain the word `pending` or `retracted` (case-insensitive).

- [ ] **Step 1: Write the failing tests**

`tests/test_verify.py`:

```python
import pytest

import verify

CLAIMS_MD = """\
| ID | Claim | Evidence | How to check | Status | Checked |
|---|---|---|---|---|---|
| C-001 | 32,543,981 lines committed | code-frequency.json | verify.sh | verified | 2026-09-28 |
| C-002 | Own-source share of C-001 | tokei run | tokei | pending | 2026-09-28 |
"""


def test_parse_claims_reads_rows():
    claims = verify.parse_claims(CLAIMS_MD)
    assert set(claims) == {"C-001", "C-002"}
    assert claims["C-001"].status == "verified"
    assert claims["C-002"].evidence == "tokei run"


def test_parse_claims_rejects_bad_status():
    bad = "| C-009 | x | y | z | maybe | 2026-09-28 |\n"
    with pytest.raises(ValueError, match="C-009"):
        verify.parse_claims(bad)


def test_parse_claims_rejects_wrong_column_count():
    with pytest.raises(ValueError, match="C-009"):
        verify.parse_claims("| C-009 | x | y | verified |\n")


def test_parse_claims_rejects_duplicate_id():
    row = "| C-001 | x | y | z | verified | 2026-09-28 |\n"
    with pytest.raises(ValueError, match="duplicate"):
        verify.parse_claims(row + row)


def test_claim_refs_ok():
    claims = verify.parse_claims(CLAIMS_MD)
    text = "In Dec 2025, 32,543,981 lines were committed ([C-001](CLAIMS.md#c-001)).\n"
    assert verify.check_claim_refs(text, claims) == []


def test_claim_refs_flags_number_without_claim():
    claims = verify.parse_claims(CLAIMS_MD)
    errors = verify.check_claim_refs("We committed 32,543,981 lines.\n", claims)
    assert len(errors) == 1 and "README.md:1" in errors[0]


def test_claim_refs_flags_percent_and_million():
    claims = verify.parse_claims(CLAIMS_MD)
    assert verify.check_claim_refs("97% of cases\n", claims)
    assert verify.check_claim_refs("32.5 million lines\n", claims)
    assert verify.check_claim_refs("32.5M lines\n", claims)


def test_claim_refs_ignores_dates_and_small_numbers():
    claims = verify.parse_claims(CLAIMS_MD)
    assert verify.check_claim_refs("On 2025-12-14 we had 35 categories.\n", claims) == []


def test_claim_refs_flags_unknown_claim():
    claims = verify.parse_claims(CLAIMS_MD)
    errors = verify.check_claim_refs("See C-042.\n", claims)
    assert errors and "unknown claim C-042" in errors[0]


def test_claim_refs_requires_pending_word_for_pending_claim():
    claims = verify.parse_claims(CLAIMS_MD)
    assert verify.check_claim_refs("Own source is large (C-002).\n", claims)
    assert verify.check_claim_refs("Own-source share: pending (C-002).\n", claims) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `$PY -m pytest tests/test_verify.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'verify'`.

- [ ] **Step 3: Write minimal implementation**

`scripts/verify.py`:

```python
#!/usr/bin/env python3
"""Mechanical checks for the BlackSwanLabz Research Lab. Standard library only."""
from __future__ import annotations

import re
from dataclasses import dataclass

CLAIM_STATUSES = {"verified", "pending", "retracted"}
CLAIM_ROW = re.compile(r"^\|\s*(C-\d{3})\s*\|(.*)\|\s*$")
CLAIM_REF = re.compile(r"\bC-\d{3}\b")
BIG_NUMBER = re.compile(
    r"\b\d{1,3}(?:,\d{3})+\b"                     # 32,543,981
    r"|\b\d+(?:\.\d+)?\s?(?:%|M\b|million\b)"     # 97%  32.5M  32.5 million
)


@dataclass(frozen=True)
class Claim:
    id: str
    claim: str
    evidence: str
    how_to_check: str
    status: str
    checked: str


def parse_claims(text: str) -> dict[str, Claim]:
    claims: dict[str, Claim] = {}
    for line in text.splitlines():
        m = CLAIM_ROW.match(line)
        if not m:
            continue
        cid = m.group(1)
        cells = [c.strip() for c in m.group(2).split("|")]
        if len(cells) != 5:
            raise ValueError(f"{cid}: expected 6 columns, got {len(cells) + 1}")
        claim = Claim(cid, *cells)
        if claim.status not in CLAIM_STATUSES:
            raise ValueError(f"{cid}: status '{claim.status}' not in {sorted(CLAIM_STATUSES)}")
        if cid in claims:
            raise ValueError(f"{cid}: duplicate claim ID")
        claims[cid] = claim
    return claims


def check_claim_refs(text: str, claims: dict[str, Claim], name: str = "README.md") -> list[str]:
    errors: list[str] = []
    for n, line in enumerate(text.splitlines(), 1):
        refs = CLAIM_REF.findall(line)
        for ref in refs:
            if ref not in claims:
                errors.append(f"{name}:{n}: unknown claim {ref}")
        if BIG_NUMBER.search(line) and not refs:
            errors.append(f"{name}:{n}: number without claim reference: {line.strip()[:80]}")
        unverified = [r for r in refs if r in claims and claims[r].status != "verified"]
        lowered = line.lower()
        if unverified and "pending" not in lowered and "retracted" not in lowered:
            errors.append(f"{name}:{n}: {', '.join(unverified)} not verified but line doesn't say pending/retracted")
    return errors
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `$PY -m pytest tests/test_verify.py -q`
Expected: `10 passed`.

- [ ] **Step 5: Commit**

```bash
git add scripts/verify.py tests/test_verify.py
git commit -m "feat(verify): CLAIMS parsing and README claim-reference check

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Checker — snapshot headers, pins, and internal links

**Files:**
- Modify: `scripts/verify.py` (append)
- Test: `tests/test_verify.py` (append)

**Interfaces:**
- Consumes: nothing from Task 2 beyond the module.
- Produces:
  - `SNAPSHOT_DIRS: tuple[str, ...]` = `("00-thesis", "01-cornerstone", "02-frameworks", "03-systems", "04-papers", "05-experiments", "06-proofs")`
  - `parse_front_matter(text: str) -> dict[str, str] | None`
  - `check_snapshot_headers(root: Path) -> list[str]` — every `*.md` under `SNAPSHOT_DIRS` (recursive)
  - `collect_pins(root: Path) -> list[tuple[str, str, str]]` — `(relative_path, repo, commit)`
  - `check_links(root: Path) -> list[str]` — every `*.md` in the repo except under `.git/`

- [ ] **Step 1: Write the failing tests** (append to `tests/test_verify.py`)

```python
from pathlib import Path

GOOD_HEADER = """---
source: github.com/lordwilsonDev/msb-v3
repo: lordwilsonDev/msb-v3
commit: 0123456789abcdef0123456789abcdef01234567
captured: 2026-09-28
status: active
---
# MSB v3
"""


def write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return p


def test_front_matter_parsed():
    fm = verify.parse_front_matter(GOOD_HEADER)
    assert fm["status"] == "active" and fm["repo"] == "lordwilsonDev/msb-v3"


def test_front_matter_missing_returns_none():
    assert verify.parse_front_matter("# no header\n") is None


def test_snapshot_headers_ok(tmp_path):
    write(tmp_path, "03-systems/msb-v3.md", GOOD_HEADER)
    assert verify.check_snapshot_headers(tmp_path) == []


def test_snapshot_headers_missing_header(tmp_path):
    write(tmp_path, "02-frameworks/ail.md", "# AIL\n")
    errors = verify.check_snapshot_headers(tmp_path)
    assert errors and "02-frameworks/ail.md" in errors[0]


def test_snapshot_headers_bad_status_and_date(tmp_path):
    bad = GOOD_HEADER.replace("status: active", "status: done").replace("2026-09-28", "Sept 28")
    write(tmp_path, "03-systems/x.md", bad)
    errors = verify.check_snapshot_headers(tmp_path)
    assert any("status" in e for e in errors)
    assert any("captured" in e for e in errors)


def test_snapshot_headers_commit_needs_repo(tmp_path):
    write(tmp_path, "03-systems/x.md", GOOD_HEADER.replace("repo: lordwilsonDev/msb-v3\n", ""))
    assert any("repo" in e for e in verify.check_snapshot_headers(tmp_path))


def test_snapshot_headers_ignore_non_snapshot_dirs(tmp_path):
    write(tmp_path, "docs/specs/x.md", "# spec\n")
    write(tmp_path, "README.md", "# readme\n")
    assert verify.check_snapshot_headers(tmp_path) == []


def test_collect_pins(tmp_path):
    write(tmp_path, "03-systems/msb-v3.md", GOOD_HEADER)
    assert verify.collect_pins(tmp_path) == [
        ("03-systems/msb-v3.md", "lordwilsonDev/msb-v3", "0123456789abcdef0123456789abcdef01234567")
    ]


def test_links_ok_and_broken(tmp_path):
    write(tmp_path, "00-thesis/thesis.md", "x")
    write(tmp_path, "README.md",
          "[ok](00-thesis/thesis.md) [anchor](00-thesis/thesis.md#top) "
          "[web](https://example.com) [self](#section) [bad](01-cornerstone/nope.md)\n")
    errors = verify.check_links(tmp_path)
    assert len(errors) == 1 and "01-cornerstone/nope.md" in errors[0]


def test_links_relative_to_file(tmp_path):
    write(tmp_path, "CLAIMS.md", "x")
    write(tmp_path, "03-systems/msb-v3.md", "[claims](../CLAIMS.md)\n")
    assert verify.check_links(tmp_path) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `$PY -m pytest tests/test_verify.py -q`
Expected: FAIL — `AttributeError: module 'verify' has no attribute 'parse_front_matter'`.

- [ ] **Step 3: Implement** (append to `scripts/verify.py`; add `from pathlib import Path` to the imports at the top)

```python
SNAPSHOT_DIRS = (
    "00-thesis", "01-cornerstone", "02-frameworks", "03-systems",
    "04-papers", "05-experiments", "06-proofs",
)
SNAPSHOT_STATUSES = {"active", "archived", "pending"}
REQUIRED_KEYS = ("source", "captured", "status")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA = re.compile(r"^[0-9a-f]{7,40}$")
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def parse_front_matter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fm: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fm[key.strip()] = value.strip().strip('"')
    return fm


def _snapshot_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for d in SNAPSHOT_DIRS:
        if (root / d).is_dir():
            files.extend(sorted((root / d).rglob("*.md")))
    return files


def check_snapshot_headers(root: Path) -> list[str]:
    errors: list[str] = []
    for path in _snapshot_files(root):
        rel = path.relative_to(root).as_posix()
        fm = parse_front_matter(path.read_text())
        if fm is None:
            errors.append(f"{rel}: missing front-matter header")
            continue
        for key in REQUIRED_KEYS:
            if not fm.get(key):
                errors.append(f"{rel}: header missing '{key}'")
        if fm.get("status") and fm["status"] not in SNAPSHOT_STATUSES:
            errors.append(f"{rel}: status '{fm['status']}' not in {sorted(SNAPSHOT_STATUSES)}")
        if fm.get("captured") and not DATE.match(fm["captured"]):
            errors.append(f"{rel}: captured '{fm['captured']}' is not YYYY-MM-DD")
        if "commit" in fm:
            if not SHA.match(fm["commit"]):
                errors.append(f"{rel}: commit '{fm['commit']}' is not a hex SHA")
            if not fm.get("repo"):
                errors.append(f"{rel}: 'commit' requires 'repo'")
    return errors


def collect_pins(root: Path) -> list[tuple[str, str, str]]:
    pins: list[tuple[str, str, str]] = []
    for path in _snapshot_files(root):
        fm = parse_front_matter(path.read_text()) or {}
        if fm.get("repo") and fm.get("commit"):
            pins.append((path.relative_to(root).as_posix(), fm["repo"], fm["commit"]))
    return pins


def check_links(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        for n, line in enumerate(path.read_text().splitlines(), 1):
            for target in MD_LINK.findall(line):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target_path = target.split("#", 1)[0]
                if not (path.parent / target_path).exists():
                    errors.append(f"{rel}:{n}: broken link {target}")
    return errors
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `$PY -m pytest tests/test_verify.py -q`
Expected: `20 passed`.

- [ ] **Step 5: Commit**

```bash
git add scripts/verify.py tests/test_verify.py
git commit -m "feat(verify): snapshot headers, pin collection, internal links

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Checker — size budget and secrets/privacy scan

**Files:**
- Modify: `scripts/verify.py` (append)
- Test: `tests/test_verify.py` (append)

**Interfaces:**
- Produces:
  - `TOKEN_BUDGET: int = 150_000`
  - `text_token_estimate(root: Path) -> int` — sum of characters ÷ 4 over text files (suffixes `.md .txt .json .cff .sh .py .yml .yaml .csv`, plus `LICENSE*` and `llms.txt`), skipping `.git/`
  - `check_size(root: Path, budget: int = TOKEN_BUDGET) -> list[str]`
  - `check_secrets(root: Path) -> list[str]` — scans the same text files, skipping `tests/`

Secret/privacy patterns: GitHub tokens (`ghp_`, `gho_`, `github_pat_`), OpenAI/Anthropic keys (`sk-…`, `sk-ant-…`), AWS access keys (`AKIA…`), private-key blocks, Slack tokens (`xox?-`), and any email address that isn't a `noreply` address.

- [ ] **Step 1: Write the failing tests** (append)

```python
def test_size_under_and_over_budget(tmp_path):
    write(tmp_path, "README.md", "a" * 400)          # 100 tokens
    assert verify.text_token_estimate(tmp_path) == 100
    assert verify.check_size(tmp_path, budget=100) == []
    assert verify.check_size(tmp_path, budget=99)


def test_size_ignores_binaries_and_git(tmp_path):
    write(tmp_path, "README.md", "a" * 40)
    (tmp_path / "evidence.png").write_bytes(b"\x89PNG" + b"x" * 10_000)
    write(tmp_path, ".git/objects/blob.txt", "a" * 10_000)
    assert verify.text_token_estimate(tmp_path) == 10


def test_secrets_detects_tokens(tmp_path):
    fake_gh = "ghp_" + "A" * 36
    fake_ant = "sk-ant-" + "b" * 30
    write(tmp_path, "03-systems/x.md", f"token {fake_gh}\nkey {fake_ant}\n")
    errors = verify.check_secrets(tmp_path)
    assert len(errors) == 2 and all("03-systems/x.md" in e for e in errors)


def test_secrets_flags_personal_email_but_not_noreply(tmp_path):
    personal = "someone" + "@" + "gmail.com"
    write(tmp_path, "README.md", f"mail {personal}\nCo-Authored-By: Claude <noreply@anthropic.com>\n"
                                 "12345+user@users.noreply.github.com\n")
    errors = verify.check_secrets(tmp_path)
    assert len(errors) == 1 and "README.md:1" in errors[0]


def test_secrets_skips_tests_dir(tmp_path):
    write(tmp_path, "tests/test_x.py", "ghp_" + "A" * 36)
    assert verify.check_secrets(tmp_path) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `$PY -m pytest tests/test_verify.py -q`
Expected: FAIL — `AttributeError: module 'verify' has no attribute 'text_token_estimate'`.

- [ ] **Step 3: Implement** (append)

```python
TOKEN_BUDGET = 150_000
TEXT_SUFFIXES = {".md", ".txt", ".json", ".cff", ".sh", ".py", ".yml", ".yaml", ".csv"}
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs)_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{20,}"),
    "API key": re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}"),
    "AWS key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "Slack token": re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")


def _text_files(root: Path, skip_dirs: tuple[str, ...] = (".git",)) -> list[Path]:
    out: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in skip_dirs for part in path.relative_to(root).parts):
            continue
        if path.suffix in TEXT_SUFFIXES or path.name.startswith("LICENSE") or path.name == "llms.txt":
            out.append(path)
    return out


def text_token_estimate(root: Path) -> int:
    return sum(len(p.read_text(errors="replace")) for p in _text_files(root)) // 4


def check_size(root: Path, budget: int = TOKEN_BUDGET) -> list[str]:
    tokens = text_token_estimate(root)
    return [] if tokens <= budget else [f"size: ~{tokens:,} tokens exceeds budget {budget:,}"]


def check_secrets(root: Path) -> list[str]:
    errors: list[str] = []
    for path in _text_files(root, skip_dirs=(".git", "tests")):
        rel = path.relative_to(root).as_posix()
        for n, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(line):
                    errors.append(f"{rel}:{n}: possible {label}")
            for email in EMAIL.findall(line):
                if "noreply" not in email.lower():
                    errors.append(f"{rel}:{n}: email address {email}")
    return errors
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `$PY -m pytest tests/test_verify.py -q`
Expected: `25 passed`.

- [ ] **Step 5: Commit**

```bash
git add scripts/verify.py tests/test_verify.py
git commit -m "feat(verify): size budget and secrets/privacy scan

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Checker — online checks, CLI, wrapper, and CI

**Files:**
- Modify: `scripts/verify.py` (append)
- Create: `scripts/verify.sh`, `.github/workflows/verify.yml`
- Test: `tests/test_verify.py` (append)

**Interfaces:**
- Consumes: `parse_claims`, `check_claim_refs`, `check_links`, `check_snapshot_headers`, `collect_pins`, `check_size`, `check_secrets`.
- Produces:
  - `CORNERSTONE_REPO = "lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE"`, `CORNERSTONE_WEEK = 1765670400` (2025-12-14 00:00 UTC), `CORNERSTONE_ADDITIONS = 32_543_981`
  - `check_code_frequency(weeks: list[list[int]]) -> list[str]`
  - `check_pins(pins: list[tuple[str, str, str]], commit_exists: Callable[[str, str], bool]) -> list[str]`
  - `run(root: Path, online: bool) -> list[str]`
  - `main(argv: list[str] | None = None) -> int` — flags `--offline`, `--root PATH`; prints each error, then `OK` or `FAIL (n)`; returns 0/1

The GitHub stats endpoint returns HTTP 202 with an empty body while it computes; `gh_code_frequency` retries up to 6 times, 5 s apart.

- [ ] **Step 1: Write the failing tests** (append)

```python
def test_code_frequency_matches():
    weeks = [[1765670400, 32543981, -804], [1766275200, 0, 0]]
    assert verify.check_code_frequency(weeks) == []


def test_code_frequency_mismatch_and_missing():
    assert "32543000" in verify.check_code_frequency([[1765670400, 32543000, -804]])[0]
    assert "missing" in verify.check_code_frequency([[1766275200, 0, 0]])[0]


def test_check_pins_uses_injected_lookup():
    pins = [("03-systems/a.md", "o/r", "abc1234"), ("03-systems/b.md", "o/r", "def5678")]
    errors = verify.check_pins(pins, lambda repo, sha: sha == "abc1234")
    assert errors == ["03-systems/b.md: commit def5678 not found in o/r"]


def test_run_offline_on_minimal_repo(tmp_path):
    write(tmp_path, "CLAIMS.md", CLAIMS_MD)
    write(tmp_path, "README.md", "32,543,981 lines committed ([C-001](CLAIMS.md)).\n")
    assert verify.run(tmp_path, online=False) == []


def test_main_returns_1_on_errors(tmp_path, capsys):
    write(tmp_path, "CLAIMS.md", CLAIMS_MD)
    write(tmp_path, "README.md", "32,543,981 lines.\n")
    assert verify.main(["--offline", "--root", str(tmp_path)]) == 1
    assert "FAIL (1)" in capsys.readouterr().out
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `$PY -m pytest tests/test_verify.py -q`
Expected: FAIL — `AttributeError: module 'verify' has no attribute 'check_code_frequency'`.

- [ ] **Step 3: Implement** (append; add `import argparse, json, subprocess, sys, time` and `from typing import Callable` to the top imports)

```python
CORNERSTONE_REPO = "lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE"
CORNERSTONE_WEEK = 1765670400  # 2025-12-14 00:00 UTC
CORNERSTONE_ADDITIONS = 32_543_981


def check_code_frequency(weeks: list[list[int]]) -> list[str]:
    for ts, additions, _deletions in weeks:
        if ts == CORNERSTONE_WEEK:
            if additions != CORNERSTONE_ADDITIONS:
                return [f"C-001: week {ts} additions {additions} != {CORNERSTONE_ADDITIONS}"]
            return []
    return [f"C-001: week {CORNERSTONE_WEEK} missing from code frequency"]


def check_pins(pins: list[tuple[str, str, str]], commit_exists: Callable[[str, str], bool]) -> list[str]:
    return [f"{rel}: commit {sha} not found in {repo}"
            for rel, repo, sha in pins if not commit_exists(repo, sha)]


def gh_commit_exists(repo: str, sha: str) -> bool:
    result = subprocess.run(["gh", "api", f"repos/{repo}/commits/{sha}", "--jq", ".sha"],
                            capture_output=True, text=True)
    return result.returncode == 0


def gh_code_frequency(repo: str) -> list[list[int]]:
    for _ in range(6):
        result = subprocess.run(["gh", "api", f"repos/{repo}/stats/code_frequency"],
                                capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if isinstance(data, list) and data:
                return data
        time.sleep(5)
    raise RuntimeError(f"code frequency for {repo} unavailable after retries")


def run(root: Path, online: bool) -> list[str]:
    try:
        claims = parse_claims((root / "CLAIMS.md").read_text())
    except (OSError, ValueError) as exc:
        return [f"CLAIMS.md: {exc}"]
    errors = check_claim_refs((root / "README.md").read_text(), claims)
    errors += check_links(root)
    errors += check_snapshot_headers(root)
    errors += check_size(root)
    errors += check_secrets(root)
    if online:
        errors += check_pins(collect_pins(root), gh_commit_exists)
        try:
            errors += check_code_frequency(gh_code_frequency(CORNERSTONE_REPO))
        except RuntimeError as exc:
            errors.append(f"C-001: {exc}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify the research lab's claims and structure.")
    parser.add_argument("--offline", action="store_true", help="skip GitHub API checks")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args(argv)
    errors = run(args.root, online=not args.offline)
    for error in errors:
        print(error)
    print("OK" if not errors else f"FAIL ({len(errors)})")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `$PY -m pytest tests/test_verify.py -q`
Expected: `30 passed`.

- [ ] **Step 5: Create `scripts/verify.sh`**

```bash
#!/usr/bin/env bash
# Runs every lab check. Usage: scripts/verify.sh [--offline]
# Set PYTHON to choose the interpreter (default: python3, needs >= 3.11).
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"
exec "$PY" scripts/verify.py "$@"
```

Run: `chmod +x scripts/verify.sh`

- [ ] **Step 6: Create `.github/workflows/verify.yml`**

```yaml
name: verify
on:
  push:
  pull_request:
  schedule:
    - cron: "0 12 * * 1"   # weekly, Monday 12:00 UTC
  workflow_dispatch:
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pytest
      - run: python -m pytest tests -q
      - run: scripts/verify.sh
        env:
          GH_TOKEN: ${{ github.token }}
```

- [ ] **Step 7: Run the online checks against the real cornerstone**

Run: `$PY -c "import sys; sys.path.insert(0,'scripts'); import verify; print(verify.check_code_frequency(verify.gh_code_frequency(verify.CORNERSTONE_REPO)))"`
Expected: `[]`.

- [ ] **Step 8: Commit**

```bash
git add scripts/verify.py scripts/verify.sh tests/test_verify.py .github/workflows/verify.yml
git commit -m "feat(verify): online checks, CLI, wrapper, CI workflow

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: CLAIMS seed + cornerstone evidence

**Files:**
- Create: `CLAIMS.md`, `01-cornerstone/README.md`, `01-cornerstone/categories.md`, `01-cornerstone/evidence/code-frequency.json`, `01-cornerstone/evidence/code-frequency-export.csv`, `01-cornerstone/evidence/README.md`
- Create (temporary, replaced in Task 12): `README.md` containing only `# BlackSwanLabz Research Lab\n`

**Interfaces:**
- Produces: claim IDs `C-001`…`C-006` used by later tasks and the README.

- [ ] **Step 1: Capture the evidence files**

```bash
mkdir -p 01-cornerstone/evidence
gh api repos/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE/stats/code_frequency > 01-cornerstone/evidence/code-frequency.json
cp ~/Downloads/"Code frequency (1).csv" 01-cornerstone/evidence/code-frequency-export.csv
head -c 60 01-cornerstone/evidence/code-frequency.json
```
Expected: starts with `[[1765670400,32543981,-804]`. If the API returned `{}` (HTTP 202, still computing), wait 10 s and rerun.

Record the cornerstone HEAD for pinning:

```bash
gh api repos/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE/commits/master --jq '.sha + " " + .commit.author.date'
```
Use the full SHA printed as `CORNERSTONE_SHA` below.

- [ ] **Step 2: Create `01-cornerstone/evidence/README.md`**

```markdown
---
source: GitHub REST API + GitHub Insights "Code frequency" CSV export
repo: lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE
commit: CORNERSTONE_SHA
captured: 2026-09-28
status: active
---
# Cornerstone evidence

- `code-frequency.json` — raw response of `GET /repos/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE/stats/code_frequency`, captured 2026-09-28. Each row is `[week_start_unix, additions, deletions]`.
- `code-frequency-export.csv` — the same data exported from the repo's Insights page by Wilson on 2026-09-28.

The first row, `[1765670400, 32543981, -804]`, is the week starting 2025-12-14 00:00 UTC: 32,543,981 lines added. See [C-001](../../CLAIMS.md).

GitHub counts every line of every committed file (source, data, lock files, vendored code). How much of that is Wilson's own source is [C-002](../../CLAIMS.md), pending.
```
(Replace `CORNERSTONE_SHA` with the SHA from Step 1.)

- [ ] **Step 3: Create `CLAIMS.md`**

```markdown
# Claims

Every number or factual claim in this lab has a row here. **Status** is one of `verified` (checked, evidence linked), `pending` (not yet checked — never restate as fact), `retracted` (checked and found wrong — kept, not deleted).

Re-run the mechanical checks with `scripts/verify.sh`. Cells never contain the `|` character.

| ID | Claim | Evidence | How to check | Status | Checked |
|---|---|---|---|---|---|
| C-001 | 32,543,981 lines were added to GITHUB_AI_PROJECTS_PACKAGE in the week starting 2025-12-14 (net 32,543,027 to date) | [code-frequency.json](01-cornerstone/evidence/code-frequency.json) and Wilson's Insights export | `scripts/verify.sh` (online) compares the live API to 32,543,981 | verified | 2026-09-28 |
| C-002 | Breakdown of C-001 into own source code vs vendored code vs data | tokei run at a pinned commit | Task 15 of the v1 plan | pending | 2026-09-28 |
| C-003 | The package holds 208+ projects in 35 categories with 19,864 Python files and 649 external dependencies | the package's own README (self-reported) | recount from a checkout | pending | 2026-09-28 |
| C-004 | AIL+MoIE produces more novel hypotheses than compute-matched best-of-n baselines (H1c) | Hermes12 pre-registered benchmark | run the benchmark; experiment not yet run | pending | 2026-09-28 |
| C-005 | Adaptive Infrastructure `reproduce.py` reproduces `reproduce_results.txt` byte-for-byte | [blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE](https://github.com/lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE) (local write-up added in Task 11) | `python reproduce.py > out.txt; diff out.txt reproduce_results.txt` | verified | 2026-09-28 |
| C-006 | The Adaptive Infrastructure published numbers are correct: SSO inclination 97.59 deg at 550 km, period 95.65 min, 10 deg plane change 1,322 m/s, HHI 1864 to 3106, outbreak RR 7.39 and OR 18.42 | independent hand recomputation | recompute from the formulas in reproduce.py | verified | 2026-09-28 |
```


- [ ] **Step 4: Create `01-cornerstone/categories.md`**

Header:

```markdown
---
source: github.com/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE (top-level folders)
repo: lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE
commit: CORNERSTONE_SHA
captured: 2026-09-28
status: active
---
```

Body: a heading `# The 35 categories`, one sentence ("The package's top-level folders, as committed by 2025-12-14."), then a table `| # | Folder | What it holds |`. Fill it from the live tree:

```bash
gh api "repos/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE/contents?ref=CORNERSTONE_SHA" --jq '.[] | select(.type=="dir") | .name'
```
For "What it holds", read each category's README (`gh api repos/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE/contents/<folder>/README.md --jq .content | base64 -d | head -20`) and write one factual line drawn from it. If a folder has no README, write `No category README`.

- [ ] **Step 5: Create `01-cornerstone/README.md`**

Header as Step 4 (`source: github.com/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE`). Body sections:
1. `# The cornerstone: GITHUB_AI_PROJECTS_PACKAGE` — link to `https://github.com/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE`.
2. `## What the record shows` — 32,543,981 lines committed in the week of 2025-12-14 ([C-001](../CLAIMS.md)); the only later changes are +370/−520 lines in February 2026, so the package is essentially as committed in December 2025.
3. `## What it does not show` — commit dates prove existence *by* 2025-12-14, not when each project was first written; "lines committed" includes non-source files (breakdown pending, [C-002](../CLAIMS.md)); the package's own counts are self-reported ([C-003](../CLAIMS.md), pending).
4. `## Contents` — links to [categories.md](categories.md), [prediction-timeline.md](prediction-timeline.md), [evidence/](evidence/README.md).

(`prediction-timeline.md` is created in Task 7; until then `check_links` reports it broken — expected.)

- [ ] **Step 6: Run the checker**

Run: `$PY scripts/verify.py --offline`
Expected: exactly one error — `01-cornerstone/README.md:<n>: broken link prediction-timeline.md`. Anything else: fix before committing.

- [ ] **Step 7: Commit**

```bash
git add CLAIMS.md README.md 01-cornerstone
git commit -m "feat: seed CLAIMS and cornerstone evidence (C-001 verified)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Prediction timeline

**Files:**
- Create: `01-cornerstone/prediction-timeline.md`
- Modify: `CLAIMS.md` (one row per included timeline row, IDs continue from C-006)

**Interfaces:**
- Consumes: `01-cornerstone/categories.md` (category names), C-017 (date anchor 2025-12-18, the repo's first commit — supersedes an earlier draft that anchored on C-001's 2025-12-14 code-frequency week label).

Inclusion rule (spec §8): a row is included only if **both sides are dated and sourced** and the cornerstone date (2025-12-18) comes first. Candidate categories: `03-orchestration-coordination`, `09-swarm-collective`, `04-memory-knowledge`, `32-gateways-apis`, `16-communication-protocols`, `30-mini-mind`, `13-nanoapex`, `27-safety-recovery`, `11-sovereignty-security`, `31-monitoring-metrics`, `28-testing-synthesis`, `26-evolution-improvement`.

- [ ] **Step 1: Research each candidate**

For each candidate category, use WebSearch to find **one industry event dated after 2025-12-18** in that area (a product launch, standard release, or major publication), with a primary source (vendor blog, standards body, paper). Also record whether the area was **already established before 2025-12-18** and cite one source for that (e.g. MCP was announced by Anthropic in November 2024). Record in a scratch table: category · event · event date · source URL · already-established? · source URL.

Drop any candidate where no post-2025-12-18 event with a primary source is found.

- [ ] **Step 2: Write `01-cornerstone/prediction-timeline.md`**

```markdown
---
source: GITHUB_AI_PROJECTS_PACKAGE categories + dated public sources (URLs per row)
repo: lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE
commit: CORNERSTONE_SHA
captured: 2026-09-28
status: active
---
# Prediction timeline

By 2025-12-18 -- the repo's first commit ([C-017](../CLAIMS.md)) -- the package contained these categories. This table sets each one beside where the industry went **after** that date.

**How to read it.** A row is here only if both dates are sourced and the package date comes first. The last column says whether the area already existed before December 2025. Every included row is early convergence; none shows a first-of-its-kind prediction. Both the pre-anchor origin and the post-anchor event are listed for each row, not hidden.

| Category (by 2025-12-18) | Industry event after | Event date | Source | Area already established before 2025-12-18? | Claim |
|---|---|---|---|---|---|
```

One table row per surviving candidate, each with its own claim ID (`C-007`, `C-008`, …). After the table, a `## Excluded candidates` section listing each dropped category and why (e.g. "no post-2025-12-18 primary source found").

- [ ] **Step 3: Add one CLAIMS row per timeline row**

Format: `| C-0NN | <category> existed in the package by 2025-12-18 and <event> followed on <date> | [prediction-timeline.md](01-cornerstone/prediction-timeline.md) + <source URL> | open both sources; compare dates | verified | 2026-09-28 |`

- [ ] **Step 4: Run the checker**

Run: `$PY scripts/verify.py --offline`
Expected: `OK`.

- [ ] **Step 5: Commit**

```bash
git add 01-cornerstone/prediction-timeline.md CLAIMS.md
git commit -m "feat: prediction timeline with dated sources on both sides

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Thesis (needs Wilson's approval before commit)

**Files:**
- Create: `00-thesis/intelligence-infrastructure-mismatch.md`

**Source:** `~/Documents/Vault/10_Projects/BlackSwanLabz/BlackSwanLabz-Thesis-Intelligence-Infrastructure-Mismatch.md` (24.6 KB). The vault note holds the thesis text **plus** non-public business material. Only the thesis text is published.

- [ ] **Step 1: Read the source note in full and mark the boundary**

Identify where the thesis text ends and the non-public material begins. Everything that isn't the thesis argument itself is excluded.

- [ ] **Step 2: Create the snapshot**

```markdown
---
source: vault:10_Projects/BlackSwanLabz/BlackSwanLabz-Thesis-Intelligence-Infrastructure-Mismatch.md
vault-date: <the note's `updated:` frontmatter value>
captured: 2026-09-28
status: active
---
# The Intelligence Infrastructure Mismatch

*By Lord Wilson.*
```
followed by the thesis text **verbatim** (no edits). If the thesis contains statistics, append a `## Sources for figures` section listing each statistic and, for each, either its source as given in the original or `unsourced in original`.

- [ ] **Step 3: Privacy scan and checker**

Run: `$PY scripts/verify.py --offline`
Expected: `OK` (no email/secret hits). Then grep for excluded material:

```bash
grep -n -i -E "investor|fundrais|deck|valuation|term sheet|checklist" 00-thesis/intelligence-infrastructure-mismatch.md
```
Expected: no hits that belong to non-public material. A hit inside the thesis argument itself is fine — note it for Wilson.

- [ ] **Step 4: Stop for Wilson's approval**

Show Wilson the file path and the grep output. He decides whether the thesis is published. Do not commit until he says yes. If he says no, write instead a 5-sentence summary he approves, with the same header and `status: pending`.

- [ ] **Step 5: Commit (after approval)**

```bash
git add 00-thesis
git commit -m "feat: thesis snapshot (Intelligence Infrastructure Mismatch)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Frameworks

**Files:**
- Create: `02-frameworks/north-star.md`, `02-frameworks/axiom-inversion-logic.md`, `02-frameworks/moie.md`, `02-frameworks/acts-5-act-research.md`, `02-frameworks/adaptive-infrastructure.md`
- Modify: `CLAIMS.md` for any number stated in these files

The vault notes behind these contain business-internal material (pricing, clients, offers). Framework files are **condensed, faithful summaries**: quote defining sentences verbatim, summarize the rest, add no new claims. Each file ends with a `## Sources` list of every source it drew from.

Header template (fill per file):

```markdown
---
source: <primary source path or repo URL>
vault-date: <source note `updated:` value, for vault sources>
repo: <owner/name, for repo sources>
commit: <full remote SHA, for repo sources>
captured: 2026-09-28
status: active
---
```

Get remote SHAs with: `gh api repos/<owner>/<repo>/commits/<branch> --jq .sha` (msb-v3: `main`; blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE: `main`).

- [ ] **Step 1: `north-star.md`** (~400–700 words)

Sources: `~/Documents/Vault/10_Projects/BlackSwanLabz/BlackSwanLabz-North-Star-Architecture.md`, `~/Documents/Vault/30_Architecture/North-Star-FDE-Cybernetic-Loop.md`.
Sections: `# North Star` · the one-sentence North Star quoted verbatim (it begins "Help businesses continuously improve by finding operational truth…") · `## The five parts` (find truth, prove with measurement, intervene where it matters, business gets better, people get better) · `## Decision before automation` (DO NOTHING / IMPROVE / AUTOMATE) · `## The control loop` (from the FDE note) · `## Sources`. Exclude KPIs tied to specific clients, pricing, and offers.

- [ ] **Step 2: `axiom-inversion-logic.md`** (~400–700 words)

Sources: `~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/Axiom-Forge-Director.md`, `~/acts_mixture_of_inversion_experts/01_AIL_ACT/000_README_FIRST.md`, `~/projects/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE/ail_research_loop/spec.md` §7 ("AIL Procedure").
Sections: `# Axiom Inversion Logic (AIL)` · `## The move` (find load-bearing assumptions, invert them, re-derive) · `## The Axiom Forge phases` (the 11 phases, listed) · `## What keeps it honest` (inversion is permissive on hypotheses, strict on claims; falsification conditions) · `## What is not yet shown` — quote the ACTS self-assessment point that the "100% success rate" and "23+ domains" claims are not evidenced in the package (`~/acts_mixture_of_inversion_experts/09_META/000_ASSESSMENT_AND_HONEST_STATUS.md`), and link [C-004](../CLAIMS.md) (pending) · `## Sources`.

- [ ] **Step 3: `moie.md`** (~400–700 words)

Sources: `~/Documents/Vault/30_Architecture/diagrams/Sovereign-Stack-Tooling/wiki/MoIE-Framework-2.0-revised.md`, `~/acts_mixture_of_inversion_experts/03_MOIE_CRYSTAL/000_README_FIRST.md`, `spec.md` §8 ("MoIE Procedure"), `09_META/000_ASSESSMENT_AND_HONEST_STATUS.md` (the five-agent sequence).
Sections: `# Mixture of Inversion Experts (MoIE)` · `## The five experts` (Inversion Critic → Positive Deviant Scout → Mechanism Synthesizer → Red Team → Prediction Generator, one line each) · `## Crystal: from hypothesis to test` · `## The open question` — MoIE vs compute-matched best-of-n is untested ([C-004](../CLAIMS.md), pending), with the pre-registered falsification condition quoted from `~/acts_mixture_of_inversion_experts/98_HERMES12_BENCHMARK/README.md` · `## Sources`.

- [ ] **Step 4: `acts-5-act-research.md`** (~500–800 words)

Sources: `~/Documents/Vault/30_Architecture/Scientific-Research-Apparatus/index.md` and its `raw-source/ail-act-research-SKILL.md`, `raw-source/worked-example-Act-I.md` … `-Act-V.md`.
Sections: `# ACTS — the 5-Act research method` · table of Acts I–V (title + one line each, from the index) · `## Worked example: AIL-AI-SMB-001` (the question, what each Act produced, the falsification test FT-001 — defined, not completed) · `## Human decision gate` (Act V stops and asks) · `## Sources`.

- [ ] **Step 5: `adaptive-infrastructure.md`** (~500–800 words)

Sources: `~/projects/AI-Agents/msb-v3/docs/blueprints/2026-08-11-adaptive-build-environment.md`, `~/Documents/Vault/10_Projects/msb-v3/MSB-v3.md` (section "Meta-System: Project Compiler above the Kernel"), `github.com/lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE` (root README, `ail_research_loop/README.md`, `ail_audit_chain/README.md`) pinned to its remote `main` SHA.
Sections: `# Adaptive Infrastructure` · `## The thesis: the system owns the workflow, the model is a swappable worker` · `## Meta-System` (MSL, context compiler, failure compiler, recursive decomposition; small-model scoreboard: 8 of 9 delegated functions correct — add claim `C-0NN`, status `pending`, evidence "author-reported in vault MSB-v3 note; run records not in lab") · `## Generate → verify: the research loop and audit chain` (link to the repo; release gates DRAFT…FINAL-READY/BLOCKED) · `## Open` (spec 12+3 states vs execution plan 15 states not reconciled) · `## Sources`.

- [ ] **Step 6: Checker**

Run: `$PY scripts/verify.py --offline`
Expected: `OK`. Then run the online pin check: `$PY scripts/verify.py` — expected `OK` (all pinned SHAs exist remotely).

- [ ] **Step 7: Commit**

```bash
git add 02-frameworks CLAIMS.md
git commit -m "feat: frameworks — North Star, AIL, MoIE, ACTS, Adaptive Infrastructure

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 10: Systems and proofs

**Files:**
- Create: `03-systems/msb-v3.md`, `03-systems/fcve.md`, `06-proofs/README.md`
- Modify: `CLAIMS.md`

- [ ] **Step 1: Pin and count MSB v3 at a remote commit**

```bash
MSB_SHA=$(gh api repos/lordwilsonDev/msb-v3/commits/main --jq .sha); echo $MSB_SHA
SCR=/private/tmp/claude-501/-Users-lordwilson/329cb066-c2d4-470f-b418-2124072d1355/scratchpad
git -C ~/projects/AI-Agents/msb-v3 fetch -q origin main
git -C ~/projects/AI-Agents/msb-v3 worktree add -q "$SCR/msb-pin" "$MSB_SHA"
(cd "$SCR/msb-pin" && $PY -m pytest --collect-only -q 2>/dev/null | tail -1)
git -C ~/projects/AI-Agents/msb-v3 worktree remove --force "$SCR/msb-pin"
```
Record the collected-test count. (This does not modify Wilson's working tree; the worktree is removed afterward.)

- [ ] **Step 2: Write `03-systems/msb-v3.md`** (~500–800 words)

Header: `source: github.com/lordwilsonDev/msb-v3`, `repo: lordwilsonDev/msb-v3`, `commit: <MSB_SHA>`, `captured: 2026-09-28`, `status: active`.
Sources: repo `README.md` + `README-OUTSIDERS.md`, vault `10_Projects/msb-v3/MSB-v3.md`.
Sections: `# MSB v3 — governed, local-first agent runtime` · `## What it is` (from README) · `## Why it matters to the thesis` (verification layer: governance brakes, evidence chains, claims gate `verify-claims.py`) · `## Evidence` — test count collected at the pin (new claim, `verified`, how to check = Step 1 command); MVP closed 2026-09-24 (claim, `pending`, evidence = vault note, author-reported); 2026-08-16 audit results (claim, `pending`, author-reported) · `## Honest limits` (the build-vs-converge pattern named in the audit, stated neutrally: subsystems added faster than closed; `gateway/` had no canonical-path caller as of 2026-08-27) · `## Sources`.

- [ ] **Step 3: Pin FCVE and gather its proof facts**

```bash
gh api repos/lordwilsonDev/fcve/commits/main --jq .sha
gh api repos/lordwilsonDev/ico-collatz-verification --jq '.default_branch'
gh api repos/lordwilsonDev/ico-collatz-verification/commits/$(gh api repos/lordwilsonDev/ico-collatz-verification --jq .default_branch) --jq .sha
gh api repos/leanprover/lean4export/pulls/52 --jq '.state + " merged=" + (.merged|tostring) + " " + .title'
gh api repos/ammkrn/nanoda_lib/pulls/36 --jq '.state + " merged=" + (.merged|tostring) + " " + .title'
gh api "repos/lordwilsonDev/fcve/contents/deliverables" --jq '.[].name'
```
Record every output. The test count: `gh api "repos/lordwilsonDev/fcve/git/trees/<FCVE_SHA>?recursive=1" --jq '[.tree[].path | select(test("(^|/)test_[^/]*\\.py$"))] | length'` gives the number of test files; state it as "test files", not tests, unless you run the suite.

- [ ] **Step 4: Write `03-systems/fcve.md`** (~400–700 words)

Header: `repo: lordwilsonDev/fcve`, `commit: <FCVE_SHA>`, `status: archived`.
Sections: `# FCVE — Formal Claim Verification Engine (archived 2026-09-19)` · `## What it did` (verification runs VCE-001/002 through gates; decisions recorded as superseding events, never rewritten; reports state what evidence permits, decision lives in the receipt) · `## What it produced` (deliverables list from Step 3; PROMOTE decisions recorded by Wilson) · `## Upstream contributions` (the two PRs with their real state from Step 3) · `## Why it is archived` (Wilson closed it 2026-09-19 to focus on MSB v3; the repo remains public and restorable) · `## Sources`. Every number gets a CLAIMS row.

- [ ] **Step 5: Write `06-proofs/README.md`**

Header: `source: lordwilsonDev/fcve deliverables + lordwilsonDev/ico-collatz-verification`, `repo: lordwilsonDev/ico-collatz-verification`, `commit: <ICO_SHA>`, `status: archived`.
Sections: `# Proofs` · one subsection per FCVE deliverable from Step 3 (name, what claim it verified, decision recorded, link to it on GitHub at the pinned SHA: `https://github.com/lordwilsonDev/fcve/tree/<FCVE_SHA>/deliverables/<name>`) · `## Lean / Collatz verification` (what `ico-collatz-verification` contains, from its README) · `## Upstream patches` (the two PRs, state from Step 3).

- [ ] **Step 6: Checker (offline then online)**

Run: `$PY scripts/verify.py --offline && $PY scripts/verify.py`
Expected: `OK` twice.

- [ ] **Step 7: Commit**

```bash
git add 03-systems 06-proofs CLAIMS.md
git commit -m "feat: systems (MSB v3 active, FCVE archived) and proofs

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 11: Papers and experiments

**Files:**
- Create: `04-papers/README.md`, `04-papers/epistemic-state-transition-question-engineering.md`, `04-papers/ail-moie-recursive-research-protocol.md`, `05-experiments/README.md`, `05-experiments/adaptive-infrastructure-reproduce.md`, `05-experiments/research-loop-reference-tests.md`, `05-experiments/hermes12-benchmark.md`
- Modify: `CLAIMS.md`

- [ ] **Step 1: `04-papers/epistemic-state-transition-question-engineering.md`**

Source: `~/Documents/Vault/30_Architecture/Epistemic-State-Transition-Question-Engineering-Research-White-Paper-v1.0.md` (33.9 KB). Header with `source: vault:30_Architecture/…`, `vault-date`, `captured`, `status: active`. Body: the paper **verbatim**. Before committing, read it fully and confirm it contains no client names, personal matters, or secrets; if it does, stop and ask Wilson.

- [ ] **Step 2: `04-papers/ail-moie-recursive-research-protocol.md`**

Header: `repo: lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE`, `commit: <ADAPTIVE_SHA>`, `status: active`. Body: a short page — what the PDF is, link to it at the pinned SHA (`https://github.com/lordwilsonDev/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE/blob/<ADAPTIVE_SHA>/AIL_MoIE_Recursive_Research_Protocol.pdf`), and a link to the machine-readable spec (`…/blob/<ADAPTIVE_SHA>/ail_research_loop/spec.md`). Extract the PDF's section headings with `$PY -c "import pypdf; …"` only if pypdf is installed; otherwise describe it from `ail_research_loop/README.md`.

- [ ] **Step 3: `04-papers/README.md`**

Header: `source: index of papers`, `captured`, `status: active`. Body: a table `| Paper | Status | Where |` with rows:
- Epistemic State Transition Question Engineering — v1.0 — [local copy](epistemic-state-transition-question-engineering.md)
- AIL + MoIE Recursive Research Protocol — v1.0 — [page](ail-moie-recursive-research-protocol.md)
- *Axiom Inversion Logic and the Mixture of Inversion Experts* (AIL-WP-2026-08-005) — **text not located** — referenced by the Hermes12 benchmark; no copy found on this machine or in the repos as of 2026-09-28. Listed so its absence is visible.

- [ ] **Step 4: Re-run and record the Adaptive Infrastructure reproduction**

```bash
SCR=/private/tmp/claude-501/-Users-lordwilson/329cb066-c2d4-470f-b418-2124072d1355/scratchpad
cd ~/projects/blackswanlabz-AI-ADAPTIVE-INFRASTRUCTURE && git pull -q && git rev-parse HEAD
$PY reproduce.py 2>/dev/null > "$SCR/repro.txt"; diff "$SCR/repro.txt" reproduce_results.txt && echo IDENTICAL
cd ail_research_loop && $PY -m unittest test_reference.py 2>&1 | tail -1; cd ~/projects/blackswanlabz-research-lab
```
Expected: a SHA, `IDENTICAL`, `OK`.

- [ ] **Step 5: `05-experiments/adaptive-infrastructure-reproduce.md`**

Header pinned to that SHA. Body: what `reproduce.py` computes (orbit/SSO, power, thermal, revisit simulation, HHI), the command, the result (`IDENTICAL`, date, Python/numpy versions from `$PY -c "import sys,numpy;print(sys.version.split()[0],numpy.__version__)"`), the note that numpy on Apple Silicon prints spurious matmul warnings and the simulation contains zero NaN/Inf values, and the hand-checked values ([C-005](../CLAIMS.md), [C-006](../CLAIMS.md)). Then change C-005's Evidence cell in `CLAIMS.md` to `[adaptive-infrastructure-reproduce.md](05-experiments/adaptive-infrastructure-reproduce.md)`.

- [ ] **Step 6: `05-experiments/research-loop-reference-tests.md`**

Header pinned to the same SHA. Body: the 8 tests (names from `test_reference.py`), result `OK`, the smoke-run fix from PR #1, and the open state-machine inconsistency. Add a CLAIMS row: `C-0NN | The AIL research-loop reference implementation passes its 8 unit tests | this page | cd ail_research_loop; python -m unittest test_reference.py | verified | 2026-09-28`.

- [ ] **Step 7: `05-experiments/hermes12-benchmark.md`**

Header: `source: ~/acts_mixture_of_inversion_experts/98_HERMES12_BENCHMARK/README.md` (local; ACTS has no git remote), `captured`, `status: pending`. Body: conditions C1–C5 and the compute-matched arms, hypotheses H1/H1c/H2/H3, success criterion (Holm-adjusted p < 0.05 and Hedges' g > 0.5 on H1c), the binding falsification condition quoted verbatim, and the status line **"Harness validated; experiment not yet run. No result exists."** linked to [C-004](../CLAIMS.md).

- [ ] **Step 8: `05-experiments/README.md`**

Header: `source: index of experiments`, `captured`, `status: active`. Body: table `| Experiment | Result | Claim |` linking the three pages above plus MSB v3's test collection (link to `../03-systems/msb-v3.md`).

- [ ] **Step 9: Checker and commit**

Run: `$PY scripts/verify.py --offline && $PY scripts/verify.py` — expected `OK` twice.

```bash
git add 04-papers 05-experiments CLAIMS.md
git commit -m "feat: papers and experiments (incl. pre-registered, not-yet-run benchmark)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 12: README — the guided tour

**Files:**
- Modify: `README.md` (replace the one-line placeholder from Task 6)

**Interfaces:**
- Consumes: every claim ID created in Tasks 6–11 and every folder page.

- [ ] **Step 1: Write `README.md`** following spec §4 exactly, stop by stop:

```markdown
# BlackSwanLabz Research Lab

[![verify](https://github.com/lordwilsonDev/blackswanlabz-research-lab/actions/workflows/verify.yml/badge.svg)](https://github.com/lordwilsonDev/blackswanlabz-research-lab/actions/workflows/verify.yml)

> **Intelligence is becoming abundant. Verification isn't. This lab is the evidence.**

Every number here links to [CLAIMS.md](CLAIMS.md). If a claim isn't verified, it says *pending*.
```

Then seven `##` sections, in this order and with these titles:
1. `## 1. The problem` — 4–6 sentences summarizing the thesis (intelligence abundant → scarcity moves to verification, permissions, accountability, absorption); link [00-thesis/](00-thesis/intelligence-infrastructure-mismatch.md).
2. `## 2. The prediction` — "In the week of 2025-12-14, 32,543,981 lines were committed across 35 categories ([C-001](CLAIMS.md))." One sentence on the package being frozen since. One sentence on what's pending (C-002, C-003 — the line must contain "pending"). Link to [01-cornerstone/prediction-timeline.md](01-cornerstone/prediction-timeline.md) with a 3-row excerpt of the timeline table (rows copied exactly, claim IDs included).
3. `## 3. The principles` — one line each for North Star, AIL, MoIE, ACTS, Adaptive Infrastructure, each linking its `02-frameworks/` file.
4. `## 4. The proof` — MSB v3 (active, test count with its claim ID), FCVE (archived; what it proved; upstream PRs), links to `03-systems/` and `06-proofs/`.
5. `## 5. Papers and tests` — links to `04-papers/README.md` and `05-experiments/README.md`; one line stating the AIL+MoIE benchmark is pre-registered and **pending** ([C-004](CLAIMS.md)) with its falsification condition in one sentence.
6. `## 6. Check everything` — `scripts/verify.sh` usage (`PYTHON=python3.12 scripts/verify.sh`, `--offline`), what it checks (the 7 checks from spec §11), and that CI runs it on every push and weekly.
7. `## 7. For AI readers` — "Start with [llms.txt](llms.txt). Rules: [AGENTS.md](AGENTS.md)."

Close with `## License` (CC BY 4.0 for writing, MIT for scripts) and `## Cite` (link [CITATION.cff](CITATION.cff)).

Every line with a comma-grouped number, `%`, `M`, or `million` must carry a claim ID; every line citing a non-verified claim must contain "pending".

- [ ] **Step 2: Checker**

Run: `$PY scripts/verify.py --offline`
Expected: `OK`. (The badge URL is external and not link-checked; it resolves once Wilson publishes.) `llms.txt` and `AGENTS.md` links are broken until Task 13 — if those are the only errors, proceed.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "feat: README guided tour (problem-first)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 13: AI entry point

**Files:**
- Create: `llms.txt`, `AGENTS.md`

- [ ] **Step 1: Write `llms.txt`** (llmstxt.org format)

```markdown
# BlackSwanLabz Research Lab

> Lord Wilson's work in one place: a thesis (intelligence becomes abundant; verification becomes scarce), the December 2025 cornerstone package, the frameworks (North Star, Axiom Inversion Logic, Mixture of Inversion Experts, ACTS, Adaptive Infrastructure), the systems that implement them (MSB v3 active, FCVE archived), papers, experiments, and proofs. CLAIMS.md is the authority on what is verified.

Read in this order.

## Thesis
- [The Intelligence Infrastructure Mismatch](00-thesis/intelligence-infrastructure-mismatch.md): the problem statement.

## Cornerstone
```
…then one `## ` section per folder in reading order (Cornerstone, Frameworks, Systems, Papers, Experiments, Proofs, Claims), each listing **every** file in that folder as `- [Title](path): one-line description`. Generate the file list with `ls` per folder so none is missed. End with:

```markdown
## Optional
- [Design spec](docs/specs/2026-09-28-research-lab-design.md): how and why the lab is built.
- [Implementation plan](docs/plans/2026-09-28-research-lab-v1.md): the build steps.
```

- [ ] **Step 2: Write `AGENTS.md`**

```markdown
# Instructions for AI models reading this repository

1. **CLAIMS.md is authoritative.** A statement is established only if its claim row says `verified`.
2. **Pending is not verified.** Never restate a `pending` claim as fact. Say it is pending.
3. **Retracted claims stay visible.** Report them as retracted; do not use them as support.
4. **"Lines committed" is not "lines of code."** C-001 counts every committed line; the source-code share is C-002.
5. **Code lives in the linked repos at the pinned commits** named in each file's header (`repo`, `commit`). This repo holds explanations and evidence, not the code.
6. **FCVE is archived** (2026-09-19). Describe it as completed work.
7. **Reading order:** see [llms.txt](llms.txt).
8. **To check anything mechanically:** `scripts/verify.sh` (add `--offline` without network).
```

- [ ] **Step 3: Checker**

Run: `$PY scripts/verify.py --offline`
Expected: `OK`.

- [ ] **Step 4: Commit**

```bash
git add llms.txt AGENTS.md
git commit -m "feat: AI entry point (llms.txt, AGENTS.md)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 14: Final gate and hand-off to Wilson

**Files:**
- Modify: `~/Documents/Vault/10_Projects/BlackSwanLabz-Research-Lab.md` (status + next steps)

- [ ] **Step 1: Full test + online verification**

```bash
$PY -m pytest tests -q
PYTHON=$PY scripts/verify.sh
$PY -c "import sys; sys.path.insert(0,'scripts'); import verify, pathlib; print(verify.text_token_estimate(pathlib.Path('.')))"
```
Expected: all tests pass; `OK`; token estimate < 150000.

- [ ] **Step 2: Spec coverage check**

Walk spec §4–§12 and confirm each item exists: README stops 0–7; folders 00–06 populated; snapshot headers (verify passes); prediction timeline with inclusion rule; CLAIMS seeded C-001…C-006 plus new rows; `llms.txt` + `AGENTS.md`; `verify.sh` + CI; licenses + `CITATION.cff` without ORCID. List anything missing and fix it before continuing.

- [ ] **Step 3: Update the vault note**

In `~/Documents/Vault/10_Projects/BlackSwanLabz-Research-Lab.md`: set `phase: built-awaiting-review`, `updated: <today>`, and replace `## Next steps` with: (1) Wilson reviews the repo; (2) Wilson decides whether to create `lordwilsonDev/blackswanlabz-research-lab` and push; (3) C-002 line breakdown (Task 15) when disk allows.

- [ ] **Step 4: Stop and report to Wilson**

Report: commit list (`git log --oneline`), verify output, claims count by status (`grep -c "| verified |" CLAIMS.md`, same for pending/retracted), anything skipped and why. **Do not create the GitHub repo or push.** Ask Wilson whether to publish.

---

### Task 15 (optional, gated on disk): C-002 line breakdown

Run only when the machine running it has **≥ 12 GiB free** (`df -h ~`). The cornerstone repo is ~1.9 GB packed (GitHub `size` field: 1,973,988 KB). As of 2026-09-28 this Mac had 8.7 GiB free — **do not run here**; use the VM or another machine with `tokei` installed.

**Files:**
- Create: `01-cornerstone/evidence/tokei.json`, `01-cornerstone/line-breakdown.md`
- Modify: `CLAIMS.md` (C-002 → `verified` or `retracted` with the result), `01-cornerstone/README.md`, `README.md` stop 2 if the headline wording changes

- [ ] **Step 1: Count at the pinned commit**

```bash
git clone --no-checkout https://github.com/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE.git /tmp/gapp
git -C /tmp/gapp checkout -q CORNERSTONE_SHA
tokei /tmp/gapp --output json > 01-cornerstone/evidence/tokei.json
tokei /tmp/gapp --exclude '**/node_modules/**' --exclude '**/site-packages/**' --exclude '**/.venv/**' --exclude '**/venv/**' --exclude '**/vendor/**'
rm -rf /tmp/gapp
```

- [ ] **Step 2: Write `01-cornerstone/line-breakdown.md`**

Header pinned to `CORNERSTONE_SHA`. Body: total code/comments/blanks by language (from `tokei.json`), the same with vendored directories excluded, and the difference. State plainly which number is "lines of code written for the package" and which is "lines committed."

- [ ] **Step 3: Update C-002 and wording**

Set C-002 to `verified` with the numbers. If the README headline should change (e.g. "32.5M lines committed, of which N lines of source code"), change it with the new claim ID. Run `PYTHON=$PY scripts/verify.sh` — expected `OK`.

- [ ] **Step 4: Commit**

```bash
git add 01-cornerstone CLAIMS.md README.md
git commit -m "feat: C-002 line breakdown of the cornerstone (tokei)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
