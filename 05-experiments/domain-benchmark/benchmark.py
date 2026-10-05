#!/usr/bin/env python3
"""Domain-Crossing & Domain-Depth Benchmark.

Standard-library-only reference implementation.
The program validates a domain ledger, derives breadth/depth/velocity metrics,
and generates a plain-language summary from the same structured evidence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any
import argparse
import json
import math
import sys


VALID_STATUS = {"CANDIDATE", "ACTIVE", "VERIFIED", "REJECTED", "UNKNOWN"}
LEVEL_MIN = 0
LEVEL_MAX = 10
BREADTH_THRESHOLD = 2


@dataclass
class LevelEvidence:
    level: int
    evidence_ids: list[str] = field(default_factory=list)
    verdict: str = "UNKNOWN"
    note: str = ""


@dataclass
class Domain:
    domain_id: str
    domain_name: str
    status: str
    max_level: int
    level_evidence: list[LevelEvidence] = field(default_factory=list)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_domains(payload: dict[str, Any]) -> list[Domain]:
    rows = payload.get("domains") or payload.get("candidate_domains") or []
    result: list[Domain] = []
    for row in rows:
        evidence = [
            LevelEvidence(
                level=int(e.get("level", 0)),
                evidence_ids=list(e.get("evidence_ids", [])),
                verdict=str(e.get("verdict", "UNKNOWN")),
                note=str(e.get("note", "")),
            )
            for e in row.get("level_evidence", [])
        ]
        result.append(
            Domain(
                domain_id=str(row["domain_id"]),
                domain_name=str(row["domain_name"]),
                status=str(row.get("status", row.get("initial_status", "UNKNOWN"))),
                max_level=int(row.get("max_level", 0)),
                level_evidence=evidence,
            )
        )
    return result


def validate(domains: list[Domain]) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    names: set[str] = set()
    for d in domains:
        if d.domain_id in ids:
            errors.append(f"duplicate domain_id: {d.domain_id}")
        ids.add(d.domain_id)
        if d.domain_name in names:
            errors.append(f"duplicate domain_name: {d.domain_name}")
        names.add(d.domain_name)
        if d.status not in VALID_STATUS:
            errors.append(f"{d.domain_id}: invalid status {d.status}")
        if not (LEVEL_MIN <= d.max_level <= LEVEL_MAX):
            errors.append(f"{d.domain_id}: max_level outside 0..10")
        seen_levels: set[int] = set()
        by_level: dict[int, LevelEvidence] = {}
        for ev in d.level_evidence:
            if not (LEVEL_MIN <= ev.level <= LEVEL_MAX):
                errors.append(f"{d.domain_id}: evidence level outside 0..10")
                continue
            if ev.level in seen_levels:
                errors.append(f"{d.domain_id}: duplicate evidence record for level {ev.level}")
            seen_levels.add(ev.level)
            by_level[ev.level] = ev
            if ev.level > 0 and not ev.evidence_ids:
                errors.append(f"{d.domain_id}: level {ev.level} missing evidence_ids")
            if ev.verdict not in {"SUPPORTED", "UNKNOWN", "REJECTED", "BLOCKED"}:
                errors.append(f"{d.domain_id}: invalid verdict {ev.verdict} at level {ev.level}")
        if d.max_level > 0:
            for level in range(1, d.max_level + 1):
                ev = by_level.get(level)
                if not ev or ev.verdict != "SUPPORTED":
                    errors.append(
                        f"{d.domain_id}: max_level {d.max_level} skips unsupported prerequisite level {level}"
                    )
            max_supported = max((l for l, ev in by_level.items() if ev.verdict == "SUPPORTED"), default=0)
            if max_supported != d.max_level:
                errors.append(
                    f"{d.domain_id}: max_level={d.max_level} but highest SUPPORTED level={max_supported}"
                )
        if d.max_level == 10:
            ev10 = by_level.get(10)
            if not ev10 or ev10.verdict != "SUPPORTED":
                errors.append(f"{d.domain_id}: L10 requires a supported level-10 evidence record")
            elif not any("PUBLIC" in eid.upper() or "RECORD" in eid.upper() or "DATA" in eid.upper() for eid in ev10.evidence_ids):
                errors.append(
                    f"{d.domain_id}: L10 evidence_ids should visibly encode public-record/data provenance"
                )
    return errors


def metrics(domains: list[Domain], start: date | None, cutoff: date | None) -> dict[str, float | int | None]:
    active = [d for d in domains if d.status != "REJECTED"]
    d2 = sum(d.max_level >= 2 for d in active)
    d4 = sum(d.max_level >= 4 for d in active)
    d6 = sum(d.max_level >= 6 for d in active)
    d7 = sum(d.max_level >= 7 for d in active)
    d8 = sum(d.max_level >= 8 for d in active)
    d9 = sum(d.max_level >= 9 for d in active)
    d10 = sum(d.max_level >= 10 for d in active)
    total_depth = sum(d.max_level for d in active if d.max_level >= 2)
    dde = sum(d.max_level / 10 for d in active if d.max_level >= 2)
    mean_depth = total_depth / d2 if d2 else None
    elapsed = None
    domain_velocity = None
    depth_velocity = None
    l10_velocity = None
    if start and cutoff:
        elapsed = (cutoff - start).days
        if elapsed > 0:
            domain_velocity = d2 / elapsed
            depth_velocity = total_depth / elapsed
            l10_velocity = d10 / elapsed
    return {
        "verified_domains_d2_plus": d2,
        "source_grounded_domains_d4_plus": d4,
        "artifact_domains_d6_plus": d6,
        "executed_domains_d7_plus": d7,
        "adversarial_domains_d8_plus": d8,
        "reconstructed_domains_d9_plus": d9,
        "public_record_empirical_domains_d10": d10,
        "total_depth_points": total_depth,
        "mean_depth": mean_depth,
        "domain_depth_equivalents": dde,
        "elapsed_days": elapsed,
        "domain_velocity_per_day": domain_velocity,
        "depth_velocity_per_day": depth_velocity,
        "l10_velocity_per_day": l10_velocity,
    }


def plain_language(metrics_out: dict[str, Any], domains: list[Domain]) -> str:
    deep = sorted(
        [d for d in domains if d.status != "REJECTED" and d.max_level >= 2],
        key=lambda d: (-d.max_level, d.domain_name),
    )
    lines = [
        "# What We Actually Did",
        "",
        f"We substantively worked in **{metrics_out['verified_domains_d2_plus']} different fields**.",
        f"**{metrics_out['executed_domains_d7_plus']}** of those reached something we actually ran.",
        f"**{metrics_out['adversarial_domains_d8_plus']}** reached deliberate break/falsification testing.",
        f"**{metrics_out['reconstructed_domains_d9_plus']}** reached a reproducible reconstruction.",
        f"**{metrics_out['public_record_empirical_domains_d10']}** reached the highest bar: an empirical test using public records/data.",
        "",
        f"Total depth across the fields: **{metrics_out['total_depth_points']} level-points**.",
        f"Average depth across counted fields: **{metrics_out['mean_depth']:.2f}**." if metrics_out['mean_depth'] is not None else "Average depth: not yet measurable.",
        "",
        "## Deepest Fields",
    ]
    for d in deep[:10]:
        lines.append(f"- **{d.domain_name.replace('_', ' ')}** — Level {d.max_level}/10")
    if metrics_out["elapsed_days"] is not None:
        lines += [
            "",
            f"This covers **{metrics_out['elapsed_days']} days**.",
            f"That is about **{metrics_out['domain_velocity_per_day']:.3f} new substantive domains per day**.",
        ]
    lines += [
        "",
        "### What the number does NOT mean",
        "A Level 10 does not automatically mean professional mastery, causal proof, or universal truth. It means the benchmark found the evidence required by this ladder.",
    ]
    return "\n".join(lines)


def scientific_summary(metrics_out: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Scientific Benchmark Summary",
            "",
            f"D2+ verified domains: {metrics_out['verified_domains_d2_plus']}",
            f"D4+ source-grounded domains: {metrics_out['source_grounded_domains_d4_plus']}",
            f"D6+ artifact domains: {metrics_out['artifact_domains_d6_plus']}",
            f"D7+ executed domains: {metrics_out['executed_domains_d7_plus']}",
            f"D8+ adversarial domains: {metrics_out['adversarial_domains_d8_plus']}",
            f"D9+ reconstructed domains: {metrics_out['reconstructed_domains_d9_plus']}",
            f"D10 public-record empirical domains: {metrics_out['public_record_empirical_domains_d10']}",
            f"Total depth points: {metrics_out['total_depth_points']}",
            f"Mean depth: {metrics_out['mean_depth'] if metrics_out['mean_depth'] is not None else 'UNKNOWN'}",
            f"Domain-depth equivalents: {metrics_out['domain_depth_equivalents']:.2f}",
            f"Elapsed days: {metrics_out['elapsed_days'] if metrics_out['elapsed_days'] is not None else 'UNKNOWN'}",
            f"Domain velocity/day: {metrics_out['domain_velocity_per_day'] if metrics_out['domain_velocity_per_day'] is not None else 'UNKNOWN'}",
            f"Depth velocity/day: {metrics_out['depth_velocity_per_day'] if metrics_out['depth_velocity_per_day'] is not None else 'UNKNOWN'}",
            f"L10 velocity/day: {metrics_out['l10_velocity_per_day'] if metrics_out['l10_velocity_per_day'] is not None else 'UNKNOWN'}",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("ledger", type=Path)
    p.add_argument("--start")
    p.add_argument("--cutoff")
    p.add_argument("--json-out", type=Path)
    args = p.parse_args(argv)

    payload = load_json(args.ledger)
    domains = parse_domains(payload)
    errors = validate(domains)
    if errors:
        print("VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    start = date.fromisoformat(args.start) if args.start else None
    cutoff = date.fromisoformat(args.cutoff) if args.cutoff else None
    if (start is None) != (cutoff is None):
        print("Both --start and --cutoff are required together.", file=sys.stderr)
        return 2
    if start and cutoff and cutoff < start:
        print("cutoff cannot precede start", file=sys.stderr)
        return 2

    out = metrics(domains, start, cutoff)
    print(scientific_summary(out))
    print("\n" + plain_language(out, domains))
    if args.json_out:
        args.json_out.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
