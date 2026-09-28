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
    write(tmp_path, "README.md", "32,543,981 lines.\n")
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
    assert verify.TOKEN_BUDGET == 250_000
