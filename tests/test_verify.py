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
