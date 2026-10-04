#!/usr/bin/env python3
"""Scaffold a knowledge-encoding skill from the templates. Standard library only.

    scaffold_skill.py --name my-skill --out ./skills --source-title "The Book" \
        --source-author "A. Author" --author "You"

Creates <out>/<name>/ with SKILL.md, config.toml, source-map.md, intake.md,
references/, evals/trigger-evals.json. Refuses to overwrite an existing directory.
Every field that needs a human decision is a TODO( placeholder, and rights default to
"unknown", so a fresh scaffold passes `validate_skill.py --draft` and fails a release check.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
FILES = {
    "SKILL.md.tmpl": "SKILL.md",
    "config.toml.tmpl": "config.toml",
    "source-map.md.tmpl": "source-map.md",
    "intake.md.tmpl": "intake.md",
    "trigger-evals.json.tmpl": "evals/trigger-evals.json",
}


def render(text: str, values: dict[str, str]) -> str:
    def sub(m: re.Match) -> str:
        key = m.group(1)
        if key not in values:
            raise KeyError(f"template placeholder {{{{{key}}}}} has no value")
        return values[key]
    return re.sub(r"\{\{(\w+)\}\}", sub, text)


def scaffold(out: Path, name: str, title: str, author: str, source_title: str,
             source_author: str, today: str | None = None) -> Path:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        raise ValueError(f"name {name!r} must be kebab-case, at most 64 characters")
    for label, value in (("title", title), ("author", author), ("source-title", source_title),
                         ("source-author", source_author)):
        if not value.strip() or any(c in value for c in '"\n\\'):
            raise ValueError(f"--{label} must be non-empty and contain no quotes, backslashes or newlines")
    target = out / name
    if target.exists():
        raise FileExistsError(f"{target} already exists; read it and snapshot it instead of overwriting")
    values = {"name": name, "title": title, "author": author, "source_title": source_title,
              "source_author": source_author, "date": today or date.today().isoformat()}
    (target / "references").mkdir(parents=True)
    (target / "evals").mkdir()
    for tmpl, dest in FILES.items():
        (target / dest).write_text(render((TEMPLATES / tmpl).read_text(encoding="utf-8"), values), encoding="utf-8")
    (target / "references" / "TODO(name).md").write_text(
        "# TODO(topic)\n\nTODO(depth that does not belong in SKILL.md, with a table of contents if over 300 lines)\n",
        encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--name", required=True)
    ap.add_argument("--out", type=Path, default=Path("."))
    ap.add_argument("--title")
    ap.add_argument("--author", required=True, help="who maintains the skill")
    ap.add_argument("--source-title", required=True)
    ap.add_argument("--source-author", required=True, help="the source's authors, exactly as it credits them")
    a = ap.parse_args(argv)
    try:
        path = scaffold(a.out, a.name, a.title or a.name.replace("-", " ").title(), a.author,
                        a.source_title, a.source_author)
    except (ValueError, FileExistsError, KeyError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    print(f"created {path}\nnext: fill intake.md, then run validate_skill.py --draft {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
