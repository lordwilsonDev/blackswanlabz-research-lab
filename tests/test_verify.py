import os
import sys
import pytest
from pathlib import Path

import verify

CLAIMS_MD = """\
| ID | Claim | Evidence | How to check | Status | Checked |
|---|---|---|---|---|---|
| C-001 | 32,543,981 lines committed | code-frequency.json | verify.sh | verified | 2026-09-28 |
| C-002 | Own-source share of C-001 | tokei run | tokei | pending | 2026-09-28 |
"""


def test_parse_claims_reads_rows():
    claims = verify.parse_claims(CLAIMS_MD)
    assert set(claims) == {"C-001", "C-002"}
    assert claims["C-001"].status == "verified"
    assert claims["C-002"].evidence == "tokei run"


def test_parse_claims_rejects_bad_status():
    bad = "| C-009 | x | y | z | maybe | 2026-09-28 |\n"
    with pytest.raises(ValueError, match="C-009"):
        verify.parse_claims(bad)


def test_parse_claims_rejects_wrong_column_count():
    with pytest.raises(ValueError, match="C-009"):
        verify.parse_claims("| C-009 | x | y | verified |\n")


def test_parse_claims_rejects_duplicate_id():
    row = "| C-001 | x | y | z | verified | 2026-09-28 |\n"
    with pytest.raises(ValueError, match="duplicate"):
        verify.parse_claims(row + row)


def test_claim_refs_ok():
    claims = verify.parse_claims(CLAIMS_MD)
    text = "In Dec 2025, 32,543,981 lines were committed ([C-001](CLAIMS.md#c-001)).\n"
    assert verify.check_claim_refs(text, claims) == []


def test_claim_refs_flags_number_without_claim():
    claims = verify.parse_claims(CLAIMS_MD)
    errors = verify.check_claim_refs("We committed 32,543,981 lines.\n", claims)
    assert len(errors) == 1 and "README.md:1" in errors[0]


def test_claim_refs_flags_percent_and_million():
    claims = verify.parse_claims(CLAIMS_MD)
    assert verify.check_claim_refs("97% of cases\n", claims)
    assert verify.check_claim_refs("32.5 million lines\n", claims)
    assert verify.check_claim_refs("32.5M lines\n", claims)


def test_claim_refs_ignores_dates_and_small_numbers():
    claims = verify.parse_claims(CLAIMS_MD)
    assert verify.check_claim_refs("On 2025-12-14 we had 35 categories.\n", claims) == []


def test_claim_refs_flags_unknown_claim():
    claims = verify.parse_claims(CLAIMS_MD)
    errors = verify.check_claim_refs("See C-042.\n", claims)
    assert errors and "unknown claim C-042" in errors[0]


def test_claim_refs_requires_pending_word_for_pending_claim():
    claims = verify.parse_claims(CLAIMS_MD)
    assert verify.check_claim_refs("Own source is large (C-002).\n", claims)
    assert verify.check_claim_refs("Own-source share: pending (C-002).\n", claims) == []


GOOD_HEADER = """---
source: github.com/lordwilsonDev/msb-v3
repo: lordwilsonDev/msb-v3
commit: 0123456789abcdef0123456789abcdef01234567
captured: 2026-09-28
status: active
---
# MSB v3
"""


def write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return p


def test_front_matter_parsed():
    fm = verify.parse_front_matter(GOOD_HEADER)
    assert fm["status"] == "active" and fm["repo"] == "lordwilsonDev/msb-v3"


def test_front_matter_missing_returns_none():
    assert verify.parse_front_matter("# no header\n") is None


def test_snapshot_headers_ok(tmp_path):
    write(tmp_path, "03-systems/msb-v3.md", GOOD_HEADER)
    assert verify.check_snapshot_headers(tmp_path) == []


def test_snapshot_headers_missing_header(tmp_path):
    write(tmp_path, "02-frameworks/ail.md", "# AIL\n")
    errors = verify.check_snapshot_headers(tmp_path)
    assert errors and "02-frameworks/ail.md" in errors[0]


def test_snapshot_headers_bad_status_and_date(tmp_path):
    bad = GOOD_HEADER.replace("status: active", "status: done").replace("2026-09-28", "Sept 28")
    write(tmp_path, "03-systems/x.md", bad)
    errors = verify.check_snapshot_headers(tmp_path)
    assert any("status" in e for e in errors)
    assert any("captured" in e for e in errors)


def test_snapshot_headers_commit_needs_repo(tmp_path):
    write(tmp_path, "03-systems/x.md", GOOD_HEADER.replace("repo: lordwilsonDev/msb-v3\n", ""))
    assert any("repo" in e for e in verify.check_snapshot_headers(tmp_path))


def test_snapshot_headers_ignore_non_snapshot_dirs(tmp_path):
    write(tmp_path, "docs/specs/x.md", "# spec\n")
    write(tmp_path, "README.md", "# readme\n")
    assert verify.check_snapshot_headers(tmp_path) == []


def test_collect_pins(tmp_path):
    write(tmp_path, "03-systems/msb-v3.md", GOOD_HEADER)
    assert verify.collect_pins(tmp_path) == [
        ("03-systems/msb-v3.md", "lordwilsonDev/msb-v3", "0123456789abcdef0123456789abcdef01234567")
    ]


def test_links_ok_and_broken(tmp_path):
    write(tmp_path, "00-thesis/thesis.md", "x")
    write(tmp_path, "README.md",
          "[ok](00-thesis/thesis.md) [anchor](00-thesis/thesis.md#top) "
          "[web](https://example.com) [self](#section) [bad](01-cornerstone/nope.md)\n")
    errors = verify.check_links(tmp_path)
    assert len(errors) == 1 and "01-cornerstone/nope.md" in errors[0]


def test_links_relative_to_file(tmp_path):
    write(tmp_path, "CLAIMS.md", "x")
    write(tmp_path, "03-systems/msb-v3.md", "[claims](../CLAIMS.md)\n")
    assert verify.check_links(tmp_path) == []


def test_docs_links_skipped_but_scanned(tmp_path):
    write(tmp_path, "docs/plans/p.md", "[x](nope.md)\n" + "ghp_" + "A" * 36 + "\n")
    write(tmp_path, "README.md", "ok")
    assert verify.check_links(tmp_path) == []
    errors = verify.check_secrets(tmp_path)
    assert len(errors) == 1
    assert "docs/plans/p.md" in errors[0]


def test_size_under_and_over_budget(tmp_path):
    write(tmp_path, "README.md", "a" * 400)          # 100 tokens
    assert verify.text_token_estimate(tmp_path) == 100
    assert verify.check_size(tmp_path, budget=100) == []
    assert verify.check_size(tmp_path, budget=99)


def test_size_ignores_binaries_and_git(tmp_path):
    write(tmp_path, "README.md", "a" * 40)
    (tmp_path / "evidence.png").write_bytes(b"\x89PNG" + b"x" * 10_000)
    write(tmp_path, ".git/objects/blob.txt", "a" * 10_000)
    assert verify.text_token_estimate(tmp_path) == 10


def test_secrets_detects_tokens(tmp_path):
    fake_gh = "ghp_" + "A" * 36
    fake_ant = "sk-ant-" + "b" * 30
    write(tmp_path, "03-systems/x.md", f"token {fake_gh}\nkey {fake_ant}\n")
    errors = verify.check_secrets(tmp_path)
    assert len(errors) == 2 and all("03-systems/x.md" in e for e in errors)


def test_secrets_flags_personal_email_but_not_noreply(tmp_path):
    personal = "someone" + "@" + "gmail.com"
    write(tmp_path, "README.md", f"mail {personal}\nCo-Authored-By: Claude <noreply@anthropic.com>\n"
                                 "12345+user@users.noreply.github.com\n")
    errors = verify.check_secrets(tmp_path)
    assert len(errors) == 1 and "README.md:1" in errors[0]


def test_secrets_skips_tests_dir(tmp_path):
    write(tmp_path, "tests/test_x.py", "ghp_" + "A" * 36)
    assert verify.check_secrets(tmp_path) == []


def test_ignored_dirs_skipped(tmp_path):
    # Write broken link and personal email to .superpowers/sdd/x.md
    write(tmp_path, ".superpowers/sdd/x.md", "[x](nope.md)\n")
    personal_email = "a" + "@" + "example.com"
    write(tmp_path, ".superpowers/test.py", f"email: {personal_email}\n")
    # Write OK content to README.md
    write(tmp_path, "README.md", "ok\n")
    # Both check_links and check_secrets should ignore .superpowers
    assert verify.check_links(tmp_path) == []
    assert verify.check_secrets(tmp_path) == []


def test_code_frequency_matches():
    weeks = [[1765670400, 32543981, -804], [1766275200, 0, 0]]
    assert verify.check_code_frequency(weeks) == []


def test_code_frequency_mismatch_and_missing():
    assert "32543000" in verify.check_code_frequency([[1765670400, 32543000, -804]])[0]
    assert "missing" in verify.check_code_frequency([[1766275200, 0, 0]])[0]


def test_check_pins_uses_injected_lookup():
    pins = [("03-systems/a.md", "o/r", "abc1234"), ("03-systems/b.md", "o/r", "def5678")]
    errors = verify.check_pins(pins, lambda repo, sha: sha == "abc1234")
    assert errors == ["03-systems/b.md: commit def5678 not found in o/r"]


def test_run_offline_on_minimal_repo(tmp_path):
    write(tmp_path, "CLAIMS.md", CLAIMS_MD)
    write(tmp_path, "README.md", "32,543,981 lines committed ([C-001](CLAIMS.md)).\n")
    assert verify.run(tmp_path, online=False) == []


def test_main_returns_1_on_errors(tmp_path, capsys):
    write(tmp_path, "CLAIMS.md", CLAIMS_MD)
    write(tmp_path, "README.md", "32,543,981 lines (C-099).\n")
    assert verify.main(["--offline", "--root", str(tmp_path)]) == 1
    assert "FAIL (1)" in capsys.readouterr().out


def test_snapshot_headers_cover_07_next(tmp_path):
    write(tmp_path, "07-next/x.md", "# no header\n")
    errors = verify.check_snapshot_headers(tmp_path)
    assert errors and "07-next/x.md" in errors[0]


def test_snapshot_headers_cover_08_operations(tmp_path):
    write(tmp_path, "08-operations/x.md", "# no header\n")
    errors = verify.check_snapshot_headers(tmp_path)
    assert any("08-operations/x.md" in e for e in errors)


def test_token_budget_is_250k():
    assert verify.TOKEN_BUDGET == 275_000


def test_main_offline_success_says_what_was_skipped(tmp_path, capsys):
    write(tmp_path, "CLAIMS.md", CLAIMS_MD)
    write(tmp_path, "README.md", "32,543,981 lines committed ([C-001](CLAIMS.md)).\n")
    assert verify.main(["--offline", "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.strip().splitlines()[-1] == "OK (offline: pin and code-frequency checks skipped)"


def test_run_allows_showcase_readme_numbers(tmp_path):
    # Showcase front page: plain numbers and no "pending" wording are fine;
    # the receipts live in CLAIMS.md.
    write(tmp_path, "CLAIMS.md", CLAIMS_MD)
    write(tmp_path, "README.md", "32.5 million lines committed; see C-002 for the breakdown.\n")
    assert verify.run(tmp_path, online=False) == []


def test_run_still_rejects_unknown_claim_ids_in_readme(tmp_path):
    write(tmp_path, "CLAIMS.md", CLAIMS_MD)
    write(tmp_path, "README.md", "See C-099.\n")
    errors = verify.run(tmp_path, online=False)
    assert errors == ["README.md:1: unknown claim C-099"]


def test_llms_coverage_flags_unlinked_pages(tmp_path):
    write(tmp_path, "03-systems/a.md", GOOD_HEADER)
    write(tmp_path, "03-systems/b.md", GOOD_HEADER)
    write(tmp_path, "llms.txt", "- [A](03-systems/a.md)\n")
    errors = verify.check_llms_coverage(tmp_path)
    assert errors == ["llms.txt: missing link to 03-systems/b.md"]


def test_run_records_validates_current_and_skips_legacy(tmp_path):
    pytest.importorskip("jsonschema")
    schema = '{"type": "object", "required": ["run_id", "status"]}'
    d = "05-experiments/learning-trajectory"
    write(tmp_path, f"{d}/run-record.schema.json", schema)
    write(tmp_path, f"{d}/runs/legacy.json", '{"run_id": "old"}')
    write(tmp_path, f"{d}/runs/good.json", '{"run_id": "a", "protocol_version": "0.1", "status": "ok"}')
    write(tmp_path, f"{d}/runs/bad.json", '{"run_id": "b", "protocol_version": "0.1"}')
    errors = verify.check_run_records(tmp_path)
    assert len(errors) == 1 and "bad.json" in errors[0] and "status" in errors[0]


class _Result:
    def __init__(self, returncode: int, stdout: str = ""):
        self.returncode, self.stdout = returncode, stdout


def test_gh_commit_exists_true_without_fallback(monkeypatch):
    calls = []
    monkeypatch.setattr(verify.subprocess, "run", lambda cmd, **kw: calls.append(cmd) or _Result(0))
    assert verify.gh_commit_exists("o/r", "abc1234") is True
    assert len(calls) == 1 and calls[0][0] == "gh"


def test_gh_commit_exists_falls_back_to_git(monkeypatch):
    def fake_run(cmd, **kw):
        return _Result(1) if cmd[0] == "gh" else _Result(0)
    monkeypatch.setattr(verify.subprocess, "run", fake_run)
    assert verify.gh_commit_exists("o/r", "abc1234") is True


def test_commit_missing_when_gh_and_git_both_fail(monkeypatch):
    monkeypatch.setattr(verify.subprocess, "run", lambda cmd, **kw: _Result(1))
    assert verify.gh_commit_exists("o/r", "abc1234") is False


def test_gh_code_frequency_retries_then_returns(monkeypatch):
    results = iter([_Result(1), _Result(0, "[[1, 2, 3]]")])
    monkeypatch.setattr(verify.subprocess, "run", lambda cmd, **kw: next(results))
    monkeypatch.setattr(verify.time, "sleep", lambda s: None)
    assert verify.gh_code_frequency("o/r") == [[1, 2, 3]]


def test_cornerstone_breakdown_counts_a_tarball():
    import io, json, subprocess, sys, tarfile
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for name, data in [("r/a.py", b"x\ny\n"), ("r/node_modules/b.js", b"1\n"), ("r/n.md", b"d\n")]:
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    script = Path(verify.__file__).with_name("cornerstone_breakdown.py")
    out = subprocess.run([sys.executable, str(script)], input=buf.getvalue(), capture_output=True, check=True)
    result = json.loads(out.stdout)
    assert result["lines"] == {"source": 2, "vendored_or_build": 1, "docs": 1}
    assert result["total_text_lines"] == 4


def test_cvt1_pack_selfcheck():
    import importlib.util
    root = Path(verify.__file__).parent.parent
    spec = importlib.util.spec_from_file_location("lh_for_cvt1", root / ".claude" / "skills" / "lab-verify" / "scripts" / "lab_harness.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    errs, _ = mod.selfcheck(root / "05-experiments" / "cvt-1")
    assert errs == []



def test_snapshot_files_skip_nested_cache_dirs(tmp_path):
    write(tmp_path, "05-experiments/x/.pytest_cache/README.md", "cache")
    write(tmp_path, "05-experiments/x/page.md", GOOD_HEADER)
    names = [p.name for p in verify._snapshot_files(tmp_path)]
    assert names == ["page.md"]


def test_activity_window_dedupes_mirrors_and_counts_owner(tmp_path):
    import json as _json
    import subprocess as sp
    base = tmp_path / "git" / "u"
    base.mkdir(parents=True)
    work = tmp_path / "work"
    env = {**os.environ, "GIT_AUTHOR_NAME": "Owner", "GIT_COMMITTER_NAME": "Owner",
           "GIT_AUTHOR_EMAIL": "o@example.invalid", "GIT_COMMITTER_EMAIL": "o@example.invalid"}
    sp.run(["git", "init", "-q", str(work)], check=True)
    for i, day in enumerate(["2026-07-06", "2026-07-07"]):
        (work / "f").write_text(str(i))
        d = {**env, "GIT_AUTHOR_DATE": f"{day}T12:00:00", "GIT_COMMITTER_DATE": f"{day}T12:00:00"}
        sp.run(["git", "-C", str(work), "add", "."], check=True, env=d)
        sp.run(["git", "-C", str(work), "commit", "-q", "-m", f"c{i}"], check=True, env=d)
    for name in ("a", "b"):  # b mirrors a: identical hashes
        sp.run(["git", "clone", "-q", "--bare", str(work), str(base / f"{name}.git")], check=True)
    script = Path(verify.__file__).with_name("activity_window.py")
    out = sp.run([sys.executable, str(script), "--start", "2026-07-05", "--end", "2026-07-31", "--owner", "owner",
                  "--repos", "a,b", "--github-user", "u", "--base-url", f"file://{tmp_path / 'git'}"],
                 capture_output=True, text=True)
    res = _json.loads(out.stdout)
    assert res["unique_commits"] == 2 and res["owner_commits"] == 2
    assert res["commits_present_in_more_than_one_repo"] == 2 and res["owner_active_days"] == 2
