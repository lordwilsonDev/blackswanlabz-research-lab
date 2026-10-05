#!/usr/bin/env python3
"""Self-tests for the domain benchmark validator and metric engine."""
from __future__ import annotations

import json
import tempfile
from datetime import date
from pathlib import Path

from benchmark import Domain, LevelEvidence, metrics, validate


def assert_has(errors: list[str], needle: str) -> None:
    assert any(needle in e for e in errors), f"missing expected error: {needle}\n{errors}"


def test_clean_domain():
    d = Domain(
        "D-1",
        "formal_math",
        "VERIFIED",
        10,
        [
            LevelEvidence(i, [f"PUBLIC-DATA-E-{i}" if i == 10 else f"E-{i}"], "SUPPORTED")
            for i in range(1, 11)
        ],
    )
    assert validate([d]) == []


def test_no_skip():
    d = Domain(
        "D-1",
        "x",
        "VERIFIED",
        7,
        [LevelEvidence(1, ["E1"], "SUPPORTED"), LevelEvidence(7, ["E7"], "SUPPORTED")],
    )
    errors = validate([d])
    assert_has(errors, "skips unsupported prerequisite level 2")


def test_missing_evidence():
    d = Domain("D-1", "x", "VERIFIED", 4, [LevelEvidence(1, [], "SUPPORTED")])
    errors = validate([d])
    assert_has(errors, "level 1 missing evidence_ids")
    assert_has(errors, "highest SUPPORTED level=1")


def test_l10_public_record_guard():
    ev = [LevelEvidence(i, [f"E{i}"], "SUPPORTED") for i in range(1, 11)]
    d = Domain("D-1", "x", "VERIFIED", 10, ev)
    errors = validate([d])
    assert_has(errors, "L10 evidence_ids should visibly encode public-record/data provenance")


def test_rejected_domain_does_not_contribute_to_counts():
    good = Domain("D-1", "good", "VERIFIED", 6)
    bad = Domain("D-2", "bad", "REJECTED", 10)
    m = metrics([good, bad], date(2026, 7, 14), date(2026, 10, 3))
    assert m["verified_domains_d2_plus"] == 1
    assert m["artifact_domains_d6_plus"] == 1
    assert m["public_record_empirical_domains_d10"] == 0


def test_metric_math():
    a = Domain("D-1", "a", "VERIFIED", 10)
    b = Domain("D-2", "b", "VERIFIED", 5)
    c = Domain("D-3", "c", "VERIFIED", 2)
    m = metrics([a, b, c], date(2026, 7, 14), date(2026, 7, 24))
    assert m["verified_domains_d2_plus"] == 3
    assert m["total_depth_points"] == 17
    assert abs(m["mean_depth"] - (17 / 3)) < 1e-12
    assert abs(m["domain_depth_equivalents"] - 1.7) < 1e-12
    assert abs(m["domain_velocity_per_day"] - 0.3) < 1e-12


def main() -> int:
    tests = [
        test_clean_domain,
        test_no_skip,
        test_missing_evidence,
        test_l10_public_record_guard,
        test_rejected_domain_does_not_contribute_to_counts,
        test_metric_math,
    ]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} tests PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
