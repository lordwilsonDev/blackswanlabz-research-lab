#!/usr/bin/env python3
"""PZS Memory Promotion Validator (spec v1.0). Standard library only.

Read-only and fail-closed: it never edits notes, and any invariant it cannot
check is reported as a failure, never as a pass. The one writer is `generate`,
which renders INDEX.md and STATS.md from the notes; `alloc-id` appends to the
ID ledger.

Workspace layout under --root:
    03_COMPLETED/**/*.md          completed notes (frontmatter id CAND-...)
    41_MEMORY_CANDIDATES/**/*.md  optional transient queue
    42_PERMANENT_MEMORY/**/*.md   permanent memory (frontmatter id MEM-...) + INDEX.md
    state/ids.lock                append-only ID ledger, one ID per line
    DISPOSITION_LOG.md            JSON-lines audit trail ('#' lines ignored)
    CHANGELOG.md                  must carry '## YYYY-MM-DD' headings
    STATS.md                      generated

Exit code is the lowest-numbered failing category (spec section 19).
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import re
import subprocess
import sys
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

CAND_ID = re.compile(r"^CAND-\d{4}-\d{2}-\d{2}-\d{3}$")
MEM_ID = re.compile(r"^MEM-\d{4}$")
DISPOSITIONS = ("PROMOTE", "KEEP_COMPLETED", "MERGE", "SUPERSEDED", "REJECT", "NEEDS_REVIEW")
MEM_STATUSES = ("ACTIVE", "SUPERSEDED", "DEMOTED")
REVIEW_WINDOW_DAYS = 14
MIX_ALERT_SHARE = 0.80
MIX_MIN_SAMPLE = 5

CHECK_CODES = {
    "structure": 1, "ids": 2, "dispositions": 3, "review_expiry": 4,
    "provenance": 5, "references": 6, "supersession": 7, "merges": 8,
    "index": 9, "stats": 9, "changelog": 9, "staleness": 10, "retrieval_contract": 11,
}
EXIT_INTERNAL = 12


# --------------------------------------------------------------------------
# Restricted frontmatter parser. Anything outside the supported subset raises,
# because an unparsed note is unknown state, not a pass.
# --------------------------------------------------------------------------
class FrontmatterError(ValueError):
    pass


KEY_LINE = re.compile(r"^([A-Za-z_][\w-]*):(?:\s+(.*))?$")


def _scalar(text: str):
    text = text.strip()
    if text in ("", "null", "~"):
        return None
    if text[0] in "|>&*!":
        raise FrontmatterError(f"unsupported YAML construct: {text!r}")
    if text in ("[]", "{}"):
        return [] if text == "[]" else {}
    if text.startswith("["):
        if not text.endswith("]"):
            raise FrontmatterError(f"unterminated inline list: {text!r}")
        return [_scalar(p) for p in text[1:-1].split(",") if p.strip()]
    if text[0] in "\"'":
        if len(text) < 2 or text[-1] != text[0]:
            raise FrontmatterError(f"unterminated quote: {text!r}")
        return text[1:-1]
    if text in ("true", "false"):
        return text == "true"
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    return text


def _tokens(lines: list[str]) -> list[tuple[int, str]]:
    out = []
    for raw in lines:
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise FrontmatterError("tab indentation")
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        out.append((len(raw) - len(raw.lstrip(" ")), raw.strip()))
    return out


def _parse_map(toks, i, indent):
    out: dict = {}
    while i < len(toks) and toks[i][0] == indent:
        text = toks[i][1]
        m = KEY_LINE.match(text)
        if not m or text.startswith("- "):
            raise FrontmatterError(f"expected 'key: value', got {text!r}")
        key, rest = m.group(1), m.group(2)
        if key in out:
            raise FrontmatterError(f"duplicate key {key!r}")
        i += 1
        if rest is not None and rest.strip() != "":
            out[key] = _scalar(rest)
        elif i < len(toks) and toks[i][0] > indent:
            if toks[i][1].startswith("- "):
                out[key], i = _parse_list(toks, i, toks[i][0])
            else:
                out[key], i = _parse_map(toks, i, toks[i][0])
        else:
            out[key] = None
    if i < len(toks) and toks[i][0] > indent:
        raise FrontmatterError(f"unexpected indentation at {toks[i][1]!r}")
    return out, i


def _parse_list(toks, i, indent):
    out: list = []
    while i < len(toks) and toks[i][0] == indent and toks[i][1].startswith("- "):
        rest = toks[i][1][2:].strip()
        if KEY_LINE.match(rest):
            toks[i] = (indent + 2, rest)  # item is a map; first key sits at indent+2
            item, i = _parse_map(toks, i, indent + 2)
            out.append(item)
        else:
            out.append(_scalar(rest))
            i += 1
    return out, i


def parse_frontmatter(text: str) -> tuple[dict, str]:
    lines = text.replace("\r\n", "\n").split("\n")
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("no opening '---'")
    try:
        end = next(n for n in range(1, len(lines)) if lines[n].strip() == "---")
    except StopIteration:
        raise FrontmatterError("no closing '---'") from None
    toks = _tokens(lines[1:end])
    meta, i = _parse_map(toks, 0, toks[0][0]) if toks else ({}, 0)
    if i != len(toks):
        raise FrontmatterError("trailing unparsed frontmatter")
    return meta, "\n".join(lines[end + 1:])


# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------
@dataclass
class Note:
    kind: str            # "CAND" | "CAND_QUEUE" | "MEM"
    path: Path
    rel: str
    meta: dict
    body: str

    @property
    def id(self) -> str:
        return str(self.meta.get("id"))

    def seq(self, key: str) -> list:
        v = self.meta.get(key)
        return list(v) if isinstance(v, list) else []


@dataclass
class Failure:
    check: str
    subject: str
    message: str

    @property
    def code(self) -> int:
        return CHECK_CODES[self.check]


@dataclass
class Report:
    root: Path
    today: date
    failures: list[Failure] = field(default_factory=list)
    alerts: list[str] = field(default_factory=list)
    completed: list[Note] = field(default_factory=list)
    queue: list[Note] = field(default_factory=list)
    memory: list[Note] = field(default_factory=list)
    log: list[dict] | None = None

    def fail(self, check: str, subject: str, message: str) -> None:
        self.failures.append(Failure(check, subject, message))


def body_hash(body: str) -> str:
    return "sha256:" + hashlib.sha256(body.strip().encode()).hexdigest()


def file_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def parse_date(value, subject: str, label: str, rep: Report) -> date | None:
    try:
        if isinstance(value, str):
            return date.fromisoformat(value)
    except ValueError:
        pass
    rep.fail("structure", subject, f"{label} is not an ISO date: {value!r}")
    return None


# --------------------------------------------------------------------------
# Loading and structure
# --------------------------------------------------------------------------
def _load_dir(rep: Report, rel_dir: str, kind: str, required: bool, skip: tuple[str, ...] = ()) -> list[Note]:
    base = rep.root / rel_dir
    if not base.is_dir():
        if required:
            rep.fail("structure", rel_dir, "required directory is missing")
        return []
    notes = []
    for p in sorted(base.rglob("*.md")):
        if p.name in skip:
            continue
        rel = str(p.relative_to(rep.root))
        try:
            meta, body = parse_frontmatter(p.read_text(encoding="utf-8"))
        except (FrontmatterError, UnicodeDecodeError) as e:
            rep.fail("structure", rel, f"unparseable frontmatter: {e}")
            continue
        notes.append(Note(kind, p, rel, meta, body))
    return notes


def _need(rep: Report, n: Note, keys: tuple[str, ...]) -> bool:
    ok = True
    for k in keys:
        if n.meta.get(k) in (None, "", []):
            rep.fail("structure", n.rel, f"missing required field '{k}'")
            ok = False
    return ok


def _check_completed_structure(rep: Report, n: Note) -> bool:
    ok = _need(rep, n, ("id", "sources", "status"))
    if n.meta.get("status") not in (None, "COMPLETED"):
        rep.fail("structure", n.rel, f"status must be COMPLETED, got {n.meta.get('status')!r}")
        ok = False
    d = n.meta.get("disposition")
    if not isinstance(d, dict):
        rep.fail("dispositions", n.rel, "missing disposition block")
        return False
    if d.get("value") is None:
        rep.fail("dispositions", n.rel, "missing disposition.value")
        return False
    if d["value"] not in DISPOSITIONS:
        rep.fail("dispositions", n.rel, f"unknown disposition {d['value']!r}")
        return False
    needed = ["decided_at", "decided_by"]
    if d["value"] == "NEEDS_REVIEW":
        needed += ["owner", "review_by"]
    for k in needed:
        if d.get(k) in (None, ""):
            rep.fail("dispositions", n.rel, f"disposition.{k} is required for {d['value']}")
            ok = False
    for k in ("decided_at", "review_by"):
        if d.get(k) is not None:
            ok = (parse_date(d[k], n.rel, f"disposition.{k}", rep) is not None) and ok
    for i, s in enumerate(n.seq("sources")):
        if not isinstance(s, dict) or not all(s.get(k) for k in ("path", "commit", "content_hash")):
            rep.fail("structure", n.rel, f"sources[{i}] needs path, commit, content_hash")
            ok = False
    return ok


def _check_memory_structure(rep: Report, n: Note) -> bool:
    ok = _need(rep, n, ("id", "status", "created_at", "last_verified", "verify_by",
                        "sources", "owner", "category", "verify_interval_days"))
    if n.meta.get("status") not in (None, *MEM_STATUSES):
        rep.fail("structure", n.rel, f"unknown memory status {n.meta.get('status')!r}")
        ok = False
    for k in ("created_at", "last_verified", "verify_by"):
        if n.meta.get(k) is not None:
            ok = (parse_date(n.meta[k], n.rel, k, rep) is not None) and ok
    iv = n.meta.get("verify_interval_days")
    if iv is not None and not (isinstance(iv, int) and not isinstance(iv, bool) and iv > 0):
        rep.fail("structure", n.rel, "verify_interval_days must be a positive integer")
        ok = False
    for i, s in enumerate(n.seq("sources")):
        if not isinstance(s, dict) or not all(s.get(k) for k in ("id", "commit", "content_hash")):
            rep.fail("structure", n.rel, f"sources[{i}] needs id, commit, content_hash")
            ok = False
    for k in ("supersedes", "superseded_by", "merged_from"):
        v = n.meta.get(k)
        if v is not None and not isinstance(v, list):
            rep.fail("structure", n.rel, f"{k} must be a list")
            ok = False
    if n.meta.get("status") == "DEMOTED":
        dm = n.meta.get("demotion")
        if not isinstance(dm, dict) or not all(dm.get(k) for k in ("reason", "decided_at", "decided_by", "destination")):
            rep.fail("structure", n.rel, "DEMOTED requires demotion{reason, decided_at, decided_by, destination}")
            ok = False
    return ok


def load(root: Path, today: date) -> Report:
    rep = Report(root=root, today=today)
    completed = _load_dir(rep, "03_COMPLETED", "CAND", required=True)
    rep.queue = _load_dir(rep, "41_MEMORY_CANDIDATES", "CAND_QUEUE", required=False)
    memory = _load_dir(rep, "42_PERMANENT_MEMORY", "MEM", required=True, skip=("INDEX.md",))
    rep.completed = [n for n in completed if _check_completed_structure(rep, n)]
    rep.memory = [n for n in memory if _check_memory_structure(rep, n)]
    return rep


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------
def check_ids(rep: Report) -> None:
    ledger_path = rep.root / "state" / "ids.lock"
    ledger: set[str] = set()
    if not ledger_path.is_file():
        rep.fail("ids", "state/ids.lock", "ID ledger is missing; cannot establish that IDs were allocated")
    else:
        for line in ledger_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line in ledger:
                rep.fail("ids", "state/ids.lock", f"duplicate ledger entry {line}")
            ledger.add(line)
    seen: dict[str, str] = {}
    for n in rep.completed + rep.memory:
        pat = CAND_ID if n.kind == "CAND" else MEM_ID
        if not pat.match(n.id):
            rep.fail("ids", n.rel, f"malformed id {n.id!r}")
            continue
        if n.id in seen:
            rep.fail("ids", n.rel, f"duplicate id {n.id} (also {seen[n.id]})")
        seen[n.id] = n.rel
        if ledger_path.is_file() and n.id not in ledger:
            rep.fail("ids", n.rel, f"{n.id} was never allocated in the ledger")
    cand_ids = {n.id for n in rep.completed}
    for q in rep.queue:
        if q.id not in cand_ids:
            rep.fail("ids", q.rel, f"candidate {q.id} has no completed note")


def check_dispositions(rep: Report) -> None:
    for n in rep.completed:
        v = n.meta["disposition"]["value"]
        if v == "PROMOTE":
            backing = [m for m in rep.memory
                       if m.meta["status"] in ("ACTIVE", "SUPERSEDED")
                       and any(isinstance(s, dict) and s.get("id") == n.id for s in m.seq("sources"))]
            if not backing:
                rep.fail("dispositions", n.rel, "PROMOTE has no ACTIVE/SUPERSEDED MEM citing this item as a source")
        elif v == "MERGE" and not n.seq("merged_into"):
            rep.fail("dispositions", n.rel, "MERGE requires merged_into")
        elif v == "SUPERSEDED" and not n.seq("superseded_by"):
            rep.fail("dispositions", n.rel, "SUPERSEDED requires superseded_by")
        elif v == "REJECT":
            if not _log_has(rep, n.id, "REJECT"):
                rep.fail("dispositions", n.rel, "REJECT is not recorded in DISPOSITION_LOG.md")
    cand = {n.id: n for n in rep.completed}
    for m in rep.memory:
        if m.meta["status"] == "DEMOTED":
            continue
        for s in m.seq("sources"):
            c = cand.get(s["id"])
            if c is None:
                continue  # reference check reports it
            v = c.meta["disposition"]["value"]
            ok = v == "PROMOTE" or (v == "MERGE" and m.id in c.seq("merged_into")) \
                or (v == "SUPERSEDED" and m.id in c.seq("superseded_by"))
            if not ok:
                rep.fail("dispositions", m.rel,
                         f"silent promotion: source {c.id} has disposition {v}, not PROMOTE/MERGE into {m.id}")


def _log_events(rep: Report) -> list[dict]:
    p = rep.root / "DISPOSITION_LOG.md"
    if not p.is_file():
        return []
    out = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                rep.fail("structure", "DISPOSITION_LOG.md", f"non-JSON log line: {line[:60]!r}")
    return out


def _log_has(rep: Report, cand_id: str, value: str) -> bool:
    if rep.log is None:
        rep.log = _log_events(rep)
    return any(e.get("candidate_id") == cand_id and
               value in (e.get("disposition"), e.get("new_disposition")) for e in rep.log)


def check_review_expiry(rep: Report) -> None:
    for n in rep.completed:
        d = n.meta["disposition"]
        if d["value"] != "NEEDS_REVIEW":
            continue
        due = date.fromisoformat(d["review_by"])
        if due < rep.today:
            rep.fail("review_expiry", n.rel, f"review_by {due} has passed; resolve to KEEP_COMPLETED and log NEEDS_REVIEW_EXPIRED")
        decided = date.fromisoformat(d["decided_at"])
        if due > decided + timedelta(days=REVIEW_WINDOW_DAYS):
            rep.alerts.append(f"REVIEW_WINDOW_EXCEEDS_DEFAULT {n.id}: {(due - decided).days} days > {REVIEW_WINDOW_DAYS}")


_git_cache: dict[tuple[str, str], bool] = {}


def _commit_exists(root: Path, commit: str) -> bool:
    key = (str(root), commit)
    if key not in _git_cache:
        r = subprocess.run(["git", "-C", str(root), "cat-file", "-e", f"{commit}^{{commit}}"],
                           capture_output=True)
        _git_cache[key] = r.returncode == 0
    return _git_cache[key]


def check_provenance(rep: Report) -> None:
    cand = {n.id: n for n in rep.completed}
    for n in rep.completed:
        for s in n.seq("sources"):
            p = (rep.root / s["path"]).resolve()
            if rep.root.resolve() not in p.parents or not p.is_file():
                rep.fail("provenance", n.rel, f"source path does not resolve inside root: {s['path']}")
                continue
            if file_hash(p) != s["content_hash"]:
                rep.fail("provenance", n.rel, f"PROVENANCE_DRIFT: {s['path']} hash differs from recorded content_hash")
            if not _commit_exists(rep.root, str(s["commit"])):
                rep.fail("provenance", n.rel, f"commit {s['commit']} not found (or root is not a git repo)")
    for m in rep.memory:
        for s in m.seq("sources"):
            c = cand.get(s["id"])
            if c is not None and body_hash(c.body) != s["content_hash"]:
                rep.fail("provenance", m.rel, f"PROVENANCE_DRIFT: body of {s['id']} changed since recorded")
            if not _commit_exists(rep.root, str(s["commit"])):
                rep.fail("provenance", m.rel, f"commit {s['commit']} not found (or root is not a git repo)")


def check_references(rep: Report) -> None:
    cand = {n.id for n in rep.completed}
    mem = {n.id for n in rep.memory}

    def need(subject: str, field_: str, ref, pool: set[str], pat: re.Pattern) -> None:
        if not isinstance(ref, str) or not pat.match(ref) or ref not in pool:
            rep.fail("references", subject, f"{field_} -> {ref!r} does not resolve")

    for n in rep.completed:
        for k in ("merged_into", "superseded_by"):
            for r in n.seq(k):
                need(n.rel, k, r, mem, MEM_ID)
    for m in rep.memory:
        for k in ("supersedes", "superseded_by"):
            for r in m.seq(k):
                need(m.rel, k, r, mem, MEM_ID)
        for r in m.seq("merged_from"):
            need(m.rel, "merged_from", r, cand, CAND_ID)
        for s in m.seq("sources"):
            need(m.rel, "sources.id", s["id"], cand, CAND_ID)
        dm = m.meta.get("demotion")
        if isinstance(dm, dict) and not (rep.root / str(dm["destination"])).exists():
            rep.fail("references", m.rel, f"demotion.destination {dm['destination']} does not exist")


def supersession_edges(rep: Report) -> dict[str, set[str]]:
    edges: dict[str, set[str]] = {m.id: set() for m in rep.memory}
    for m in rep.memory:
        for b in m.seq("superseded_by"):
            if b in edges:
                edges[m.id].add(b)
        for a in m.seq("supersedes"):
            if a in edges:
                edges[a].add(m.id)
    return edges


def check_supersession(rep: Report) -> None:
    mem = {m.id: m for m in rep.memory}
    for m in rep.memory:
        if m.id in m.seq("superseded_by") or m.id in m.seq("supersedes"):
            rep.fail("supersession", m.rel, "self-reference")
        for b in m.seq("superseded_by"):
            if b in mem and m.id not in mem[b].seq("supersedes"):
                rep.fail("supersession", m.rel, f"superseded_by {b}, but {b}.supersedes does not list {m.id}")
        for a in m.seq("supersedes"):
            if a in mem and m.id not in mem[a].seq("superseded_by"):
                rep.fail("supersession", m.rel, f"supersedes {a}, but {a}.superseded_by does not list {m.id}")
        has_succ = bool(m.seq("superseded_by"))
        if has_succ and m.meta["status"] == "ACTIVE":
            rep.fail("supersession", m.rel, "has superseded_by but status is ACTIVE")
        if m.meta["status"] == "SUPERSEDED" and not has_succ:
            rep.fail("supersession", m.rel, "status SUPERSEDED without superseded_by")
        if len(m.seq("superseded_by")) > 1 and m.meta.get("allow_fork") is not True:
            rep.fail("supersession", m.rel, "ambiguous fork: multiple superseded_by without allow_fork: true")
    edges = supersession_edges(rep)
    state: dict[str, int] = {}

    def dfs(u: str, path: list[str]) -> None:
        state[u] = 1
        for v in sorted(edges[u]):
            if state.get(v) == 1:
                rep.fail("supersession", u, "FAIL_SUPERSESSION_CYCLE: " + " -> ".join(path + [u, v]))
            elif v not in state:
                dfs(v, path + [u])
        state[u] = 2

    for u in sorted(edges):
        if u not in state:
            dfs(u, [])


def resolve_head(rep: Report, mem_id: str) -> str:
    """Follow superseded_by to the current head. Assumes check_supersession passed."""
    edges = supersession_edges(rep)
    seen = set()
    while edges.get(mem_id) and mem_id not in seen:
        seen.add(mem_id)
        mem_id = sorted(edges[mem_id])[0]
    return mem_id


def check_merges(rep: Report) -> None:
    mem = {m.id: m for m in rep.memory}
    cand = {n.id: n for n in rep.completed}
    for n in rep.completed:
        if n.meta["disposition"]["value"] != "MERGE":
            continue
        for t in n.seq("merged_into"):
            m = mem.get(t)
            if m is None:
                continue
            if m.meta["status"] == "DEMOTED":
                rep.fail("merges", n.rel, f"merge target {t} is DEMOTED")
            if n.id not in m.seq("merged_from"):
                rep.fail("merges", n.rel, f"{t}.merged_from does not list {n.id}")
            if not any(s.get("id") == n.id for s in m.seq("sources")):
                rep.fail("merges", n.rel, f"{n.id} vanished from {t} provenance (not in sources)")
    for m in rep.memory:
        src_ids = {s["id"] for s in m.seq("sources")}
        for c_id in m.seq("merged_from"):
            c = cand.get(c_id)
            if c is None:
                continue
            if c.meta["disposition"]["value"] != "MERGE" or m.id not in c.seq("merged_into"):
                rep.fail("merges", m.rel, f"hidden merge: {c_id} is not dispositioned MERGE into {m.id}")
            if c_id not in src_ids:
                rep.fail("merges", m.rel, f"merged_from {c_id} missing from sources")


def check_staleness(rep: Report) -> None:
    for m in rep.memory:
        if m.meta["status"] != "ACTIVE":
            continue
        verified = date.fromisoformat(m.meta["last_verified"])
        due = date.fromisoformat(m.meta["verify_by"])
        if verified > rep.today:
            rep.fail("staleness", m.rel, "last_verified is in the future")
        if due > verified + timedelta(days=m.meta["verify_interval_days"]):
            rep.fail("staleness", m.rel, "verify_by exceeds last_verified + verify_interval_days")
        if due < rep.today:
            rep.fail("staleness", m.rel, f"STALE_MEMORY: verify_by {due} has passed")


def check_retrieval_contract(rep: Report) -> None:
    if not (rep.root / "42_PERMANENT_MEMORY" / "INDEX.md").is_file():
        rep.fail("retrieval_contract", "42_PERMANENT_MEMORY/INDEX.md", "INDEX.md is missing")
    for m in rep.memory:
        if m.meta["status"] == "ACTIVE" and not (m.seq("sources") and m.meta.get("owner")):
            rep.fail("retrieval_contract", m.rel, "ACTIVE memory must expose provenance and owner")


# --- generated artifacts ---------------------------------------------------
def render_index(rep: Report) -> str:
    rows = [
        f"| {m.id} | {m.meta.get('title', m.path.stem)} | {m.meta['status']} | "
        f"{m.meta['last_verified']} | {m.meta['verify_by']} |"
        for m in sorted(rep.memory, key=lambda x: x.id) if m.meta["status"] == "ACTIVE"
    ]
    return ("# Permanent Memory Index\n\n<!-- generated by memory_validator.py generate; do not edit -->\n\n"
            "| ID | Title | Status | Verified | Verify by |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n")


def compute_counts(rep: Report) -> dict:
    disp = {v: 0 for v in DISPOSITIONS}
    for n in rep.completed:
        disp[n.meta["disposition"]["value"]] += 1
    mem = {s: sum(1 for m in rep.memory if m.meta["status"] == s) for s in MEM_STATUSES}
    stale = sum(1 for m in rep.memory
                if m.meta["status"] == "ACTIVE" and date.fromisoformat(m.meta["verify_by"]) < rep.today)
    return {
        "completed": len(rep.completed), "candidates": len(rep.queue), "dispositions": disp,
        "memory": mem, "stale_memory": stale,
        "broken_provenance": sum(1 for f in rep.failures if f.check == "provenance"),
        "broken_references": sum(1 for f in rep.failures if f.check == "references"),
    }


def render_stats(rep: Report, generated: str) -> str:
    c = compute_counts(rep)
    d, m = c["dispositions"], c["memory"]
    return "\n".join([
        "PZS MEMORY STATISTICS", f"Generated: {generated}", "",
        f"Completed: {c['completed']}", f"Promoted: {d['PROMOTE']}", f"Merged: {d['MERGE']}",
        f"Superseded: {d['SUPERSEDED']}", f"Keep Completed: {d['KEEP_COMPLETED']}",
        f"Rejected: {d['REJECT']}", f"Needs Review: {d['NEEDS_REVIEW']}", "",
        "Permanent Memory:", f"Active: {m['ACTIVE']}", f"Superseded: {m['SUPERSEDED']}",
        f"Demoted: {m['DEMOTED']}", "", f"Stale: {c['stale_memory']}",
        f"Broken Provenance: {c['broken_provenance']}", f"Broken References: {c['broken_references']}", ""])


def _strip_generated(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines() if not ln.startswith("Generated:")]


def check_generated(rep: Report) -> None:
    index = rep.root / "42_PERMANENT_MEMORY" / "INDEX.md"
    active = {m.id for m in rep.memory if m.meta["status"] == "ACTIVE"}
    known = {m.id for m in rep.memory}
    if index.is_file():
        rows = re.findall(r"^\|\s*(MEM-\d{4})\s*\|", index.read_text(), re.M)
        for dup in sorted({r for r in rows if rows.count(r) > 1}):
            rep.fail("index", "INDEX.md", f"duplicate row {dup}")
        for r in sorted(set(rows) - known):
            rep.fail("index", "INDEX.md", f"lists nonexistent {r}")
        for r in sorted(active - set(rows)):
            rep.fail("index", "INDEX.md", f"missing ACTIVE {r}")
        if not any(f.check == "index" for f in rep.failures) and \
                [ln.strip() for ln in index.read_text().splitlines()] != [ln.strip() for ln in render_index(rep).splitlines()]:
            rep.fail("index", "INDEX.md", "out of date; run `generate`")
    else:
        rep.fail("index", "INDEX.md", "missing; run `generate`")
    stats = rep.root / "STATS.md"
    if not stats.is_file():
        rep.fail("stats", "STATS.md", "missing; run `generate`")
    elif _strip_generated(stats.read_text()) != _strip_generated(render_stats(rep, "")):
        rep.fail("stats", "STATS.md", "does not match recomputed counts; run `generate`")
    log = rep.root / "CHANGELOG.md"
    if not log.is_file():
        rep.fail("changelog", "CHANGELOG.md", "missing")
        return
    dates = [date.fromisoformat(x) for x in re.findall(r"^##\s+(\d{4}-\d{2}-\d{2})\b", log.read_text(), re.M)]
    latest_change = [date.fromisoformat(n.meta["disposition"]["decided_at"]) for n in rep.completed]
    for m in rep.memory:
        latest_change += [date.fromisoformat(m.meta["created_at"]), date.fromisoformat(m.meta["last_verified"])]
    if latest_change and (not dates or max(dates) < max(latest_change)):
        rep.fail("changelog", "CHANGELOG.md", f"latest entry {max(dates) if dates else None} predates latest change {max(latest_change)}")


# --- alerts (never failures) -----------------------------------------------
def collect_alerts(rep: Report) -> None:
    def mix(label: str, values: list[str]) -> None:
        if len(values) < MIX_MIN_SAMPLE:
            return
        for v in DISPOSITIONS:
            share = values.count(v) / len(values)
            if share > MIX_ALERT_SHARE:
                rep.alerts.append(f"DISPOSITION_MIX {label}: {v} is {share:.0%} of {len(values)} decisions")

    mix("cycle", [n.meta["disposition"]["value"] for n in rep.completed])
    by: dict[str, list[str]] = {}
    for n in rep.completed:
        by.setdefault(str(n.meta["disposition"]["decided_by"]), []).append(n.meta["disposition"]["value"])
    for who, vals in sorted(by.items()):
        mix(f"reviewer {who}", vals)


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------
CHECKS = (
    ("ids", check_ids), ("dispositions", check_dispositions), ("review_expiry", check_review_expiry),
    ("provenance", check_provenance), ("references", check_references),
    ("supersession", check_supersession), ("merges", check_merges),
    ("staleness", check_staleness), ("retrieval_contract", check_retrieval_contract),
)


def validate(root: Path, today: date) -> tuple[Report, dict]:
    rep = load(root, today)
    for _, fn in CHECKS:
        fn(rep)
    if not any(f.check == "structure" and f.subject in ("03_COMPLETED", "42_PERMANENT_MEMORY") for f in rep.failures):
        check_generated(rep)  # after the others: STATS embeds their failure counts
    collect_alerts(rep)
    failed = {f.check for f in rep.failures}
    names = ["structure", *[c for c, _ in CHECKS], "index", "stats", "changelog"]
    result = {
        "run_id": uuid.uuid4().hex,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "today": today.isoformat(),
        "counts": compute_counts(rep),
        "checks": {c: ("FAIL" if c in failed else "PASS") for c in names},
        "alerts": rep.alerts,
        "failures": [{"check": f.check, "code": f.code, "subject": f.subject, "message": f.message}
                     for f in rep.failures],
        "exit_code": min((f.code for f in rep.failures), default=0),
    }
    return rep, result


def retrieve(rep: Report) -> list[dict]:
    """Retrieval contract: ACTIVE heads only, with provenance and verification status."""
    out = []
    for m in sorted(rep.memory, key=lambda x: x.id):
        if m.meta["status"] != "ACTIVE":
            continue
        out.append({
            "id": m.id, "path": m.rel, "owner": m.meta["owner"], "sources": m.seq("sources"),
            "last_verified": m.meta["last_verified"], "verify_by": m.meta["verify_by"],
            "stale": date.fromisoformat(m.meta["verify_by"]) < rep.today,
        })
    return out


def alloc_id(root: Path, kind: str, on: date) -> str:
    ledger = root / "state" / "ids.lock"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with open(ledger, "a+") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.seek(0)
        ids = [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
        if kind == "cand":
            prefix = f"CAND-{on.isoformat()}-"
            n = max((int(i[len(prefix):]) for i in ids if i.startswith(prefix)), default=0) + 1
            new = f"{prefix}{n:03d}"
        else:
            n = max((int(i[4:]) for i in ids if MEM_ID.match(i)), default=0) + 1
            new = f"MEM-{n:04d}"
        fh.write(new + "\n")
        fh.flush()
    return new


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("validate", "generate", "retrieve", "alloc-id"):
        p = sub.add_parser(name)
        p.add_argument("--root", type=Path, default=Path("."))
        p.add_argument("--today", type=date.fromisoformat, default=None)
        if name == "validate":
            p.add_argument("--out", type=Path, help="write the machine-readable result here")
            p.add_argument("--json", action="store_true", help="print the full result as JSON")
        if name == "alloc-id":
            p.add_argument("kind", choices=("cand", "mem"))
    args = ap.parse_args(argv)
    today = args.today or date.today()
    root = args.root.resolve()
    try:
        if args.cmd == "alloc-id":
            print(alloc_id(root, args.kind, today))
            return 0
        rep, result = validate(root, today)
        if args.cmd == "generate":
            blocking = [f for f in rep.failures
                        if f.check not in ("index", "stats", "changelog") and not f.subject.endswith("INDEX.md")]
            if blocking:
                print("refusing to generate from a corpus that fails validation:", file=sys.stderr)
                for f in blocking:
                    print(f"  [{f.check}] {f.subject}: {f.message}", file=sys.stderr)
                return min(f.code for f in blocking)
            (root / "42_PERMANENT_MEMORY" / "INDEX.md").write_text(render_index(rep))
            (root / "STATS.md").write_text(render_stats(rep, datetime.now(timezone.utc).isoformat(timespec="seconds")))
            print("wrote 42_PERMANENT_MEMORY/INDEX.md and STATS.md")
            return 0
        if args.cmd == "retrieve":
            if result["exit_code"]:
                print(f"corpus fails validation (exit {result['exit_code']}); refusing to serve memory", file=sys.stderr)
                return result["exit_code"]
            print(json.dumps(retrieve(rep), indent=2))
            return 0
        if args.out:
            args.out.write_text(json.dumps(result, indent=2) + "\n")
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            for f in rep.failures:
                print(f"FAIL [{f.check}:{f.code}] {f.subject}: {f.message}")
            for a in rep.alerts:
                print(f"ALERT {a}")
            print("PASS" if result["exit_code"] == 0 else f"FAIL (exit {result['exit_code']})")
        return result["exit_code"]
    except Exception as e:  # unknown state is never success
        print(f"INTERNAL_VALIDATOR_ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        return EXIT_INTERNAL


if __name__ == "__main__":
    sys.exit(main())
