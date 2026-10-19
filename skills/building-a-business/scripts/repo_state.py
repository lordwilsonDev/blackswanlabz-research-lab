#!/usr/bin/env python3
"""Read a lab-style repo at a git ref and report what exists versus what is marked as running.

Standard library only. Reads through `git show`/`git ls-tree`, so it never touches the working tree.

  repo_state.py --repo ~/projects/blackswanlabz-research-lab            # markdown, ref origin/master
  repo_state.py --repo PATH --ref HEAD --json                           # machine-readable
  repo_state.py --repo PATH --ci                                        # add latest GitHub Actions result (needs gh)

It reports what the files SAY. It does not verify them. Treat every banner as the repo's own words.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict

AREAS = {
    "00-thesis": "thesis",
    "01-cornerstone": "evidence base",
    "02-frameworks": "methods",
    "03-systems": "systems",
    "04-papers": "papers / white papers",
    "05-experiments": "experiments",
    "06-proofs": "proofs",
    "07-next": "roadmap (not built)",
    "08-operations": "business SOPs / operations",
    "docs": "specs, plans, protocols",
    "skills": "skills",
    ".claude/skills": "skills",
}

BANNERS = [
    ("current-state note", re.compile(r"^(?!\\).*\bCURRENT STATE\b")),
    ("not approved", re.compile(r"NOT APPROVED", re.I)),
    ("not run", re.compile(r"\*\*Not run\.?\*\*|experiment (is )?not yet run|NOT YET RUN|No experiment has been run|no result exists", re.I)),
    ("hard stop", re.compile(r"HARD[ -]STOP|BLOCKED_FOR_NEW_RUNS")),
    ("target, not running", re.compile(r"none of that automation exists|not built yet|planned, not built|describe the target system|DRAFT. NOT APPROVED", re.I)),
    ("not public / local-only", re.compile(r"not yet public|local-only|no remote|repo not yet public", re.I)),
    ("private evidence", re.compile(r"(?<!/)private repo|code is in a private", re.I)),
]
CLAIM_ROW = re.compile(r"^\|\s*(C-\d{3})\s*\|(.*)\|\s*$")


def git(repo: str, *args: str) -> str:
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {r.stderr.strip()[:200]}")
    return r.stdout


def front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm


def area_of(path: str) -> str:
    for prefix in sorted(AREAS, key=len, reverse=True):
        if path == prefix or path.startswith(prefix + "/"):
            return prefix
    return path.split("/", 1)[0] if "/" in path else "(root)"


def analyse(repo: str, ref: str) -> dict:
    sha = git(repo, "rev-parse", "--short", ref).strip()
    paths = git(repo, "ls-tree", "-r", "--name-only", ref).splitlines()
    md = [p for p in paths if p.endswith(".md") and not p.startswith("docs/plans/")]
    areas: dict[str, dict] = defaultdict(lambda: {"files": 0, "words": 0, "status": Counter(), "docs": []})
    banners: list[dict] = []
    claims: Counter = Counter()
    pending: list[str] = []
    retracted: list[str] = []

    for p in paths:
        areas[area_of(p)]["files"] += 1

    for p in md:
        text = git(repo, "show", f"{ref}:{p}")
        a = areas[area_of(p)]
        words = len(text.split())
        a["words"] += words
        fm = front_matter(text)
        status = fm.get("status", "no header")
        a["status"][status] += 1
        a["docs"].append({"path": p, "words": words, "status": status})
        if p == "CLAIMS.md":
            for line in text.splitlines():
                m = CLAIM_ROW.match(line)
                if m:
                    cells = [c.strip() for c in m.group(2).split("|")]
                    st = cells[-2]
                    claims[st] += 1
                    if st == "pending":
                        pending.append(m.group(1))
                    if st == "retracted":
                        retracted.append(m.group(1))
            continue
        hit_kinds = set()
        for n, line in enumerate(text.splitlines(), 1):
            for kind, rx in BANNERS:
                if kind not in hit_kinds and rx.search(line):
                    hit_kinds.add(kind)
                    banners.append({"path": p, "line": n, "kind": kind, "text": line.strip()[:200]})

    skills = sorted({p.split("/")[-2] for p in paths if p.endswith("SKILL.md")})
    return {
        "ref": ref,
        "sha": sha,
        "files": len(paths),
        "claims": {"total": sum(claims.values()), "by_status": dict(claims), "pending": pending, "retracted": retracted},
        "areas": {
            k: {
                "label": AREAS.get(k, k),
                "files": v["files"],
                "words": v["words"],
                "status": dict(v["status"]),
                "docs": sorted(v["docs"], key=lambda d: -d["words"]),
            }
            for k, v in sorted(areas.items())
        },
        "banners": banners,
        "skills": skills,
    }


def latest_ci(repo: str) -> str:
    try:
        url = git(repo, "remote", "get-url", "origin").strip()
        m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
        if not m:
            return "no GitHub remote"
        r = subprocess.run(["gh", "run", "list", "-R", m.group(1), "-L", "3", "--json", "conclusion,headSha,createdAt"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            return f"gh unavailable: {r.stderr.strip()[:100]}"
        return ", ".join(f"{x['conclusion'] or 'running'}@{x['headSha'][:7]}" for x in json.loads(r.stdout)) or "no runs"
    except SystemExit as e:
        return str(e)


def render(d: dict, ci: str | None) -> str:
    out = [f"# Repo state at {d['ref']} ({d['sha']}): {d['files']} files", ""]
    c = d["claims"]
    if c["total"]:
        out += ["## Claims ledger", f"{c['total']} rows: {c['by_status']}",
                f"pending: {', '.join(c['pending'])}" if c["pending"] else "pending: none",
                f"retracted: {', '.join(c['retracted'])}" if c["retracted"] else "retracted: none", ""]
    else:
        out += ["## Claims ledger", "none found (no CLAIMS.md rows). Nothing in this repo is marked verified.", ""]
    if ci is not None:
        out += ["## CI (latest runs)", ci, ""]
    out += ["## Areas (what the repo says each is)"]
    for k, a in d["areas"].items():
        if a["files"]:
            st = ", ".join(f"{s}: {n}" for s, n in a["status"].items()) or "no markdown"
            out.append(f"- **{k}** ({a['label']}): {a['files']} files, {a['words']:,} words; page status: {st}")
    out += ["", "## State banners (the repo's own words; quote, don't paraphrase)"]
    if d["banners"]:
        for b in d["banners"]:
            out.append(f"- [{b['kind']}] {b['path']}:{b['line']}: {b['text']}")
    else:
        out.append("- none found. Absence of a banner is not evidence that something runs.")
    out += ["", "## Skills in repo", ", ".join(d["skills"]) or "none", ""]
    biz = d["areas"].get("08-operations")
    if biz:
        out += ["## Business docs (08-operations), largest first"] + [
            f"- {x['path']} ({x['words']:,} words, status: {x['status']})" for x in biz["docs"][:12]] + [""]
    pap = d["areas"].get("04-papers")
    if pap:
        out += ["## Papers"] + [f"- {x['path']} (status: {x['status']})" for x in pap["docs"]] + [""]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--ref", default="origin/master")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--ci", action="store_true")
    a = ap.parse_args()
    d = analyse(a.repo, a.ref)
    ci = latest_ci(a.repo) if a.ci else None
    if a.ci:
        d["ci"] = ci
    print(json.dumps(d, indent=2) if a.json else render(d, ci))
    return 0


if __name__ == "__main__":
    sys.exit(main())
