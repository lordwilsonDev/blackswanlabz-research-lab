import pytest

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
