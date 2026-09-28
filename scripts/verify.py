#!/usr/bin/env python3
"""Mechanical checks for the BlackSwanLabz Research Lab. Standard library only."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

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
