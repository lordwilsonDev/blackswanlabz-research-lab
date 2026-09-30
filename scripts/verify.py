#!/usr/bin/env python3
"""Mechanical checks for the BlackSwanLabz Research Lab. Standard library only."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

IGNORED_DIRS = (".git", ".superpowers", ".pytest_cache")
LINK_IGNORED_DIRS = IGNORED_DIRS + ("docs",)
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


def check_claim_ids(text: str, claims: dict[str, Claim], name: str = "README.md") -> list[str]:
    """Showcase rule: every claim ID a page mentions must exist in CLAIMS.md."""
    return [f"{name}:{n}: unknown claim {ref}"
            for n, line in enumerate(text.splitlines(), 1)
            for ref in CLAIM_REF.findall(line) if ref not in claims]


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


SNAPSHOT_DIRS = (
    "00-thesis", "01-cornerstone", "02-frameworks", "03-systems",
    "04-papers", "05-experiments", "06-proofs", "07-next", "08-operations",
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
        if any(part in LINK_IGNORED_DIRS for part in path.relative_to(root).parts):
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


TOKEN_BUDGET = 250_000
TEXT_SUFFIXES = {".md", ".txt", ".json", ".cff", ".sh", ".py", ".yml", ".yaml", ".csv"}
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs)_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{20,}"),
    "API key": re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}"),
    "AWS key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "Slack token": re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")


def _text_files(root: Path, skip_dirs: tuple[str, ...] = IGNORED_DIRS) -> list[Path]:
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
    for path in _text_files(root, skip_dirs=IGNORED_DIRS + ("tests",)):
        rel = path.relative_to(root).as_posix()
        for n, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(line):
                    errors.append(f"{rel}:{n}: possible {label}")
            for email in EMAIL.findall(line):
                if "noreply" not in email.lower():
                    errors.append(f"{rel}:{n}: email address {email}")
    return errors


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
    errors = check_claim_ids((root / "README.md").read_text(), claims)
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
    ok = "OK (offline: pin and code-frequency checks skipped)" if args.offline else "OK"
    print(ok if not errors else f"FAIL ({len(errors)})")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
