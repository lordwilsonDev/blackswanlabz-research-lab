#!/usr/bin/env python3
"""Validate a knowledge-encoding skill package. Standard library only (Python 3.11+).

Checks what a machine can check: platform-valid frontmatter, required sections,
directive-to-source coverage, reference integrity, version consistency, rights
recording, and privacy of traces. It cannot judge whether the skill is faithful to its
source or any good; that needs the source-map review and the evals.

Modes:
  default   errors fail; TODO placeholders and missing eval results are errors too
  --draft   TODO placeholders and missing eval results are warnings (work in progress)
  --release additionally requires known redistribution rights, review_by, evals/results.md,
            and an `ack:` on every UNSOURCED directive

Exit code: 0 = no errors, 1 = errors, 2 = could not run.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
REQUIRED_SECTIONS = ("Core Directives", "Validation Checkpoints", "References", "Changelog")
SOFT_LINES, HARD_LINES = 500, 800
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
DIRECTIVE = re.compile(r"\*\*(D-\d{2,3})\b")
MAP_ROW = re.compile(r"^\|\s*(D-\d{2,3})\s*\|(.*)\|\s*$")
BACKTICK_PATH = re.compile(r"`((?:references|templates|scripts|examples|evals)/[^`\s]+)`")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
SECRET = re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}|\b(?:ghp|gho|ghu|ghs)_[A-Za-z0-9]{36}\b|\bAKIA[0-9A-Z]{16}\b")
STATUSES = {"SOURCE-CLAIM", "AUTHOR-ADDITION", "UNSOURCED"}
KNOWN_RIGHTS = {"permitted", "restricted"}


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def soft(self, msg: str, draft: bool) -> None:
        (self.warnings if draft else self.errors).append(msg)


def parse_frontmatter(text: str) -> dict:
    """Frontmatter subset: `key: value` lines plus one nested block under `metadata:`."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError("no frontmatter")
    out: dict = {}
    current: dict | None = None
    for raw in m.group(1).split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  ") and current is not None:
            k, _, v = raw.strip().partition(":")
            current[k.strip()] = v.strip().strip("\"'")
            continue
        k, sep, v = raw.partition(":")
        if not sep:
            raise ValueError(f"unparseable frontmatter line: {raw!r}")
        k, v = k.strip(), v.strip()
        if v == "":
            current = out.setdefault(k, {})
        else:
            current = None
            if v[0] in "|>":
                raise ValueError(f"{k}: use a single-line value, not a block scalar")
            out[k] = v[1:-1] if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'" else v
    return out


def section(text: str, title: str) -> str | None:
    m = re.search(rf"^##\s+{re.escape(title)}\s*$", text, re.M)
    if not m:
        return None
    rest = text[m.end():]
    n = re.search(r"^##\s+", rest, re.M)
    return rest[: n.start()] if n else rest


def validate(root: Path, draft: bool = False, release: bool = False) -> Result:
    r = Result()
    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        r.err("SKILL.md not found")
        return r
    text = skill_md.read_text(encoding="utf-8")
    try:
        fm = parse_frontmatter(text)
    except ValueError as e:
        r.err(f"frontmatter: {e}")
        return r

    # --- platform frontmatter rules -------------------------------------------------
    extra = set(fm) - ALLOWED_FRONTMATTER
    if extra:
        r.err(f"frontmatter keys not allowed by the platform: {sorted(extra)} (put version/triggers under metadata or config.toml)")
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name or "") or len(name) > 64:
        r.err(f"name {name!r} must be kebab-case, at most 64 characters")
    elif name != root.name:
        r.err(f"name {name!r} does not match directory {root.name!r}")
    if not desc:
        r.err("description is empty")
    else:
        if len(desc) > 1024:
            r.err(f"description is {len(desc)} characters; the limit is 1024")
        if "<" in desc or ">" in desc:
            r.err("description must not contain angle brackets")
        if len(desc) < 80:
            r.err("description is too short to trigger reliably (say what it does and when to use it)")
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    version = meta.get("version", "")
    if not SEMVER.match(version):
        r.err("metadata.version must be MAJOR.MINOR.PATCH")

    # --- size and sections ----------------------------------------------------------
    n_lines = len(text.splitlines())
    if n_lines > HARD_LINES:
        r.err(f"SKILL.md is {n_lines} lines (hard limit {HARD_LINES}); move depth into references/")
    elif n_lines > SOFT_LINES:
        r.warnings.append(f"SKILL.md is {n_lines} lines (target {SOFT_LINES} or fewer)")
    for title in REQUIRED_SECTIONS:
        if section(text, title) is None:
            r.err(f"missing section '## {title}'")

    # --- placeholders ---------------------------------------------------------------
    todo_files = [p for p in root.rglob("*") if p.is_file() and p.suffix in {".md", ".toml", ".json"}
                  and "evals" not in p.relative_to(root).parts[:1] and "TODO(" in p.read_text(errors="replace")]
    for p in sorted(todo_files):
        r.soft(f"unresolved TODO( placeholder in {p.relative_to(root)}", draft)

    # --- directives <-> source map --------------------------------------------------
    directives = set(DIRECTIVE.findall(section(text, "Core Directives") or ""))
    if not directives:
        r.err("Core Directives has no IDs (write each as '- **D-01 ...**')")
    smap = root / "source-map.md"
    rows: dict[str, list[str]] = {}
    if not smap.is_file():
        r.err("source-map.md not found (every directive needs a source locator)")
    else:
        for line in smap.read_text(encoding="utf-8").splitlines():
            m = MAP_ROW.match(line)
            if m:
                rows[m.group(1)] = [c.strip() for c in m.group(2).split("|")]
        for d in sorted(directives - set(rows)):
            r.err(f"{d} has no row in source-map.md")
        for d in sorted(set(rows) - directives):
            r.err(f"source-map.md lists {d}, which is not a directive in SKILL.md")
        for d, cells in sorted(rows.items()):
            if len(cells) < 3 or cells[1] not in STATUSES:
                r.err(f"source-map.md {d}: need locator | status | note, status one of {sorted(STATUSES)}")
                continue
            locator, status, note = cells[0], cells[1], cells[2]
            if status == "UNSOURCED" and release and "ack:" not in note:
                r.err(f"{d} is UNSOURCED without an 'ack:' from the user in release mode")
            if status != "UNSOURCED" and (not locator or locator.startswith("TODO(")):
                r.soft(f"{d} has no source locator", draft)

    # --- reference integrity --------------------------------------------------------
    cited = set(BACKTICK_PATH.findall(text))
    for path in sorted(cited):
        if path == "evals/results.md":
            continue  # produced by step 7; its absence is reported by the evals check below
        if not any(c in path for c in "*<{") and not (root / path).exists():
            r.err(f"SKILL.md cites {path}, which does not exist")
    for sub in ("references", "templates"):
        d = root / sub
        if d.is_dir():
            for f in sorted(p for p in d.iterdir() if p.is_file()):
                rel = f"{sub}/{f.name}"
                if rel not in cited:
                    r.err(f"{rel} exists but SKILL.md never says when to read/use it")

    # --- config.toml, version, rights ------------------------------------------------
    cfg_path = root / "config.toml"
    if not cfg_path.is_file():
        r.err("config.toml not found")
    else:
        try:
            cfg = tomllib.loads(cfg_path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as e:
            r.err(f"config.toml: {e}")
            cfg = {}
        m, s = cfg.get("metadata", {}), cfg.get("source", {})
        for k in ("author", "license", "version", "created"):
            if not m.get(k):
                r.err(f"config.toml [metadata].{k} is missing")
        if m.get("version") and version and m["version"] != version:
            r.err(f"config.toml version {m['version']} != SKILL.md metadata.version {version}")
        for k in ("title", "authors", "redistribution"):
            if not s.get(k):
                r.err(f"config.toml [source].{k} is missing")
        rights = s.get("redistribution", "")
        if rights not in KNOWN_RIGHTS | {"unknown"}:
            r.err("config.toml [source].redistribution must be permitted, restricted, or unknown")
        if rights == "unknown":
            msg = "source redistribution rights are unknown: keep this skill private until they are settled"
            (r.err if release else r.warnings.append)(msg)  # type: ignore[operator]
        if release and not m.get("review_by"):
            r.err("release requires [metadata].review_by (when the encoded knowledge must be rechecked)")

    # --- changelog --------------------------------------------------------------------
    if version and f"v{version}" not in (section(text, "Changelog") or "") and f"{version}" not in (section(text, "Changelog") or ""):
        r.err(f"Changelog has no entry for version {version}")

    # --- evals --------------------------------------------------------------------------
    if release and not (root / "evals" / "results.md").is_file():
        r.err("release requires evals/results.md (trigger and task eval outcomes against a baseline)")
    elif not release and not (root / "evals" / "results.md").is_file():
        r.soft("no evals/results.md yet: effectiveness is unmeasured", True)

    # --- privacy of traces/examples ------------------------------------------------------
    for sub in ("traces", "examples"):
        d = root / sub
        if not d.is_dir():
            continue
        for f in sorted(d.rglob("*")):
            if not f.is_file():
                continue
            body = f.read_text(errors="replace")
            if f.suffix == ".jsonl":
                for i, line in enumerate(body.splitlines(), 1):
                    if line.strip():
                        try:
                            json.loads(line)
                        except json.JSONDecodeError:
                            r.err(f"{f.relative_to(root)}:{i} is not valid JSON")
            if EMAIL.search(body):
                r.err(f"{f.relative_to(root)} contains an email address (traces/examples must not carry personal data)")
            if SECRET.search(body):
                r.err(f"{f.relative_to(root)} contains something shaped like a secret")
    if (cfg_path.is_file() and (root / "schema.json").is_file()):
        try:
            json.loads((root / "schema.json").read_text())
        except json.JSONDecodeError as e:
            r.err(f"schema.json: {e}")
    return r


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("skill_dir", type=Path)
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--release", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.draft and a.release:
        print("--draft and --release are mutually exclusive", file=sys.stderr)
        return 2
    try:
        res = validate(a.skill_dir.resolve(), draft=a.draft, release=a.release)
    except Exception as e:  # unknown state is never a pass
        print(f"validator error: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps({"errors": res.errors, "warnings": res.warnings, "pass": not res.errors}, indent=2))
    else:
        for e in res.errors:
            print(f"ERROR   {e}")
        for w in res.warnings:
            print(f"WARNING {w}")
        print("PASS" if not res.errors else f"FAIL ({len(res.errors)} errors)")
    return 1 if res.errors else 0


if __name__ == "__main__":
    sys.exit(main())
