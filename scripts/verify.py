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
