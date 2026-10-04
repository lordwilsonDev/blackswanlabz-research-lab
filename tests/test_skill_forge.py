import json
import shutil
import sys
from pathlib import Path

import pytest

FORGE = Path(__file__).resolve().parent.parent / "skills" / "skill-forge"
sys.path.insert(0, str(FORGE / "scripts"))
import scaffold_skill as sc  # noqa: E402
import validate_skill as vs  # noqa: E402

DESC = ("Encode the Acme planning handbook as a skill. Use whenever the user asks about Acme quarterly "
        "planning, even without naming the handbook. Not for general project management questions.")


def make(tmp_path, name="acme-planning"):
    """A complete, valid skill (no TODOs), written by hand rather than scaffolded."""
    d = tmp_path / name
    (d / "references").mkdir(parents=True)
    (d / "SKILL.md").write_text(f"""---
name: {name}
description: {DESC}
metadata:
  version: 1.0.0
---

# Acme Planning

## Attribution

Acme Handbook by A. Author (2025).

## Core Directives

- **D-01 Plan quarterly.** Because cadence matters.
- **D-02 Review weekly.** Because drift compounds.

## Validation Checkpoints

- [ ] Plan exists.

## References

- `references/cadence.md`: when to read the cadence detail.

## Changelog

- **v1.0.0 (2026-10-04)**: initial.
""")
    (d / "references" / "cadence.md").write_text("# Cadence\n")
    (d / "config.toml").write_text('''[metadata]
name = "acme-planning"
version = "1.0.0"
author = "Maintainer"
license = "MIT"
created = "2026-10-04"
review_by = "2027-01-01"

[source]
title = "Acme Handbook"
authors = ["A. Author"]
redistribution = "permitted"
''')
    (d / "source-map.md").write_text("""| Directive | Source locator | Status | Note |
|---|---|---|---|
| D-01 | ch. 2 | SOURCE-CLAIM | |
| D-02 | ch. 3 | SOURCE-CLAIM | |
""")
    (d / "evals").mkdir()
    (d / "evals" / "results.md").write_text("trigger 8/8, task 3/3 vs baseline 1/3\n")
    return d


def errors(d, **kw):
    return vs.validate(d, **kw).errors


def test_complete_skill_passes_release(tmp_path):
    d = make(tmp_path)
    assert errors(d, release=True) == []


@pytest.mark.parametrize("mutate, expect", [
    (lambda d: (d / "SKILL.md").write_text((d / "SKILL.md").read_text().replace("metadata:\n  version: 1.0.0", "version: 1.0.0")), "not allowed by the platform"),
    (lambda d: (d / "SKILL.md").write_text((d / "SKILL.md").read_text().replace("name: acme-planning", "name: other-name")), "does not match directory"),
])
def test_frontmatter_rules(tmp_path, mutate, expect):
    d = make(tmp_path)
    mutate(d)
    if expect:
        assert any(expect in e for e in errors(d))


def test_description_limits(tmp_path):
    d = make(tmp_path)
    t = (d / "SKILL.md").read_text()
    (d / "SKILL.md").write_text(t.replace(DESC, "x" * 1100))
    assert any("limit is 1024" in e for e in errors(d))
    (d / "SKILL.md").write_text(t.replace(DESC, DESC + " <angle>"))
    assert any("angle brackets" in e for e in errors(d))
    (d / "SKILL.md").write_text(t.replace(DESC, "too short"))
    assert any("too short" in e for e in errors(d))


def test_directive_and_source_map_must_agree_both_ways(tmp_path):
    d = make(tmp_path)
    m = (d / "source-map.md").read_text()
    (d / "source-map.md").write_text(m.replace("| D-02 | ch. 3 | SOURCE-CLAIM | |\n", ""))
    assert any("D-02 has no row" in e for e in errors(d))
    (d / "source-map.md").write_text(m + "| D-09 | ch. 9 | SOURCE-CLAIM | |\n")
    assert any("D-09" in e and "not a directive" in e for e in errors(d))
    (d / "source-map.md").write_text(m.replace("SOURCE-CLAIM", "MAYBE", 1))
    assert any("status one of" in e for e in errors(d))


def test_unsourced_needs_ack_only_for_release(tmp_path):
    d = make(tmp_path)
    m = (d / "source-map.md").read_text()
    (d / "source-map.md").write_text(m.replace("| D-02 | ch. 3 | SOURCE-CLAIM | |", "| D-02 | none | UNSOURCED | my opinion |"))
    assert errors(d) == []
    assert any("ack:" in e for e in errors(d, release=True))
    (d / "source-map.md").write_text(m.replace("| D-02 | ch. 3 | SOURCE-CLAIM | |", "| D-02 | none | UNSOURCED | ack: user accepted 2026-10-04 |"))
    assert errors(d, release=True) == []


def test_reference_integrity_both_directions(tmp_path):
    d = make(tmp_path)
    (d / "references" / "orphan.md").write_text("x")
    assert any("orphan.md exists but SKILL.md never" in e for e in errors(d))
    (d / "references" / "orphan.md").unlink()
    (d / "references" / "cadence.md").unlink()
    assert any("cites references/cadence.md" in e for e in errors(d))


def test_version_must_match_everywhere(tmp_path):
    d = make(tmp_path)
    (d / "config.toml").write_text((d / "config.toml").read_text().replace('version = "1.0.0"', 'version = "1.1.0"'))
    assert any("config.toml version 1.1.0" in e for e in errors(d))
    d2 = make(tmp_path, "acme-two")
    (d2 / "SKILL.md").write_text((d2 / "SKILL.md").read_text().replace("**v1.0.0 (2026-10-04)**", "**v0.9.0 (2026-10-04)**"))
    assert any("no entry for version 1.0.0" in e for e in errors(d2))


def test_rights_unknown_warns_in_draft_and_blocks_release(tmp_path):
    d = make(tmp_path)
    (d / "config.toml").write_text((d / "config.toml").read_text().replace('"permitted"', '"unknown"'))
    r = vs.validate(d)
    assert r.errors == [] and any("rights are unknown" in w for w in r.warnings)
    assert any("rights are unknown" in e for e in errors(d, release=True))
    (d / "config.toml").write_text((d / "config.toml").read_text().replace('"unknown"', '"maybe"'))
    assert any("must be permitted, restricted, or unknown" in e for e in errors(d))


def test_release_requires_review_by_and_eval_results(tmp_path):
    d = make(tmp_path)
    (d / "config.toml").write_text((d / "config.toml").read_text().replace('review_by = "2027-01-01"\n', ""))
    assert any("review_by" in e for e in errors(d, release=True))
    (d / "evals" / "results.md").unlink()
    assert any("evals/results.md" in e for e in errors(d, release=True))
    assert errors(d) == []                                  # non-release: only a warning


def test_line_limits(tmp_path):
    d = make(tmp_path)
    t = (d / "SKILL.md").read_text()
    (d / "SKILL.md").write_text(t + "\n" * 550)
    r = vs.validate(d)
    assert r.errors == [] and any("target 500" in w for w in r.warnings)
    (d / "SKILL.md").write_text(t + "\n" * 850)
    assert any("hard limit" in e for e in errors(d))


def test_traces_must_be_valid_and_free_of_personal_data(tmp_path):
    d = make(tmp_path)
    (d / "traces").mkdir()
    (d / "traces" / "a.jsonl").write_text('{"ok": 1}\nnot json\n')
    assert any("not valid JSON" in e for e in errors(d))
    (d / "traces" / "a.jsonl").write_text('{"note": "contact jane@example.com"}\n')
    assert any("email address" in e for e in errors(d))
    (d / "traces" / "a.jsonl").write_text('{"k": "sk-ant-abcdefghijklmnopqrstuvwxyz"}\n')
    assert any("secret" in e for e in errors(d))


def test_missing_sections_and_files_fail(tmp_path):
    d = make(tmp_path)
    (d / "SKILL.md").write_text((d / "SKILL.md").read_text().replace("## Validation Checkpoints", "## Other"))
    assert any("Validation Checkpoints" in e for e in errors(d))
    (d / "source-map.md").unlink()
    (d / "config.toml").unlink()
    es = errors(d)
    assert any("source-map.md not found" in e for e in es) and any("config.toml not found" in e for e in es)


def test_scaffold_is_valid_draft_but_not_release(tmp_path):
    out = sc.scaffold(tmp_path, "new-skill", "New Skill", "Maint", "The Book", "A. Author", today="2026-10-04")
    r = vs.validate(out, draft=True)
    assert r.errors == [], r.errors
    assert any("TODO(" in w for w in r.warnings)
    assert vs.validate(out).errors                           # strict: placeholders are errors
    assert any("rights are unknown" in e for e in errors(out, release=True))
    assert json.loads((out / "evals" / "trigger-evals.json").read_text().replace("TODO(", "TODO_(")) is not None


def test_scaffold_refuses_overwrite_and_bad_input(tmp_path):
    sc.scaffold(tmp_path, "new-skill", "T", "M", "Book", "Auth")
    with pytest.raises(FileExistsError):
        sc.scaffold(tmp_path, "new-skill", "T", "M", "Book", "Auth")
    for bad in ("Bad Name", "-x", "a--b", "x" * 65):
        with pytest.raises(ValueError):
            sc.scaffold(tmp_path, bad, "T", "M", "Book", "Auth")
    with pytest.raises(ValueError):
        sc.scaffold(tmp_path, "ok-name", "T", "M", 'Book "quoted"', "Auth")


def test_skill_forge_validates_itself():
    r = vs.validate(FORGE, draft=True)
    assert r.errors == [], r.errors


def test_cli_exit_codes(tmp_path, capsys):
    d = make(tmp_path)
    assert vs.main([str(d), "--release"]) == 0
    (d / "source-map.md").unlink()
    assert vs.main([str(d)]) == 1
    assert vs.main([str(d), "--draft", "--release"]) == 2
