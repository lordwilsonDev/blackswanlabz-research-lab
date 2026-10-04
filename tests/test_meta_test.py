import ast
import json
import sys
import textwrap
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parent.parent / "skills" / "test-the-tests" / "scripts"
sys.path.insert(0, str(TOOL))
import meta_test as mt  # noqa: E402

SRC = textwrap.dedent('''\
    """doc"""
    def f(a, b):
        """inner doc"""
        if a > 3 and b:
            return a + 100
        return None

    msg = f"{1 + 2}"
    if __name__ == "__main__":
        if f(1, 2) == 5:
            pass
''')


def test_executable_lines_skips_docstrings():
    lines = mt.executable_lines(ast.parse(SRC))
    assert 1 not in lines and 3 not in lines          # docstrings
    assert {2, 4, 5, 6}.issubset(lines)


def test_sites_cover_each_operator_and_skip_main_guard_and_fstrings():
    descs = [d for _, _, d in mt.enumerate_sites(SRC, None)]
    assert any("Gt -> LtE" in d for d in descs)
    assert any("And -> Or" in d for d in descs)
    assert any("return value -> None" in d for d in descs)
    assert any("100 -> 101" in d for d in descs)
    assert any("branch removed" in d for d in descs) and any("branch forced" in d for d in descs)
    assert not any("Eq -> NotEq" in d for d in descs)  # inside the __main__ guard
    assert not any("1 + 2" in d or "2 -> 3" in d for d in descs)  # f-string untouched


def test_each_mutant_is_valid_python_and_differs_by_exactly_one_site():
    sites = mt.enumerate_sites(SRC, None)
    originals = ast.unparse(ast.parse(SRC))
    seen = set()
    for idx, _, _ in sites:
        mutated = mt.apply_mutant(SRC, idx, None)
        ast.parse(mutated)
        assert mutated != originals
        seen.add(mutated)
    assert len(seen) == len(sites)                    # every site yields a distinct mutant


def test_not_removal_and_allowed_lines():
    src = "def g(x):\n    return not x\n"
    assert any("'not' removed" in d for _, _, d in mt.enumerate_sites(src, None))
    assert mt.enumerate_sites(src, {99}) == []        # only allowed lines are mutated
    with pytest.raises(ValueError):
        mt.apply_mutant(src, 50, None)


def test_audit_flags_missing_assert_tautology_and_missing_import(tmp_path):
    f = tmp_path / "test_x.py"
    f.write_text(textwrap.dedent('''\
        import os
        def test_none():
            x = 1
        def test_taut():
            assert True
        def test_self():
            y = 2
            assert y == y
        def test_ok():
            assert 1 + 1 == 2
        def test_raises():
            import pytest
            with pytest.raises(ValueError):
                int("x")
    '''))
    found = mt.audit_test_file(f, {"target"})
    text = "\n".join(found)
    assert "test_none: no assertion" in text
    assert "assert always true" in text and "compares a value with itself" in text
    assert "imports none of its targets" in text
    assert "test_ok" not in text and "test_raises" not in text


# ---- end to end on a tiny project -------------------------------------------------
TARGET = textwrap.dedent('''\
    def clamp(x, hi):
        if x > hi:
            return hi
        return x

    def spin(n):
        i = 0
        while i < n:
            i += 1
        return i

    def never_called(v):
        if v == 7:
            return "seven"
        return "other"
''')
STRONG = textwrap.dedent('''\
    import target
    def test_clamp():
        assert target.clamp(5, 3) == 3
        assert target.clamp(3, 3) == 3
        assert target.clamp(2, 3) == 2
    def test_spin():
        assert target.spin(3) == 3
''')
WEAK = textwrap.dedent('''\
    import target
    def test_clamp_runs():
        target.clamp(5, 3)
        assert True
    def test_spin():
        assert target.spin(3) == 3
''')


def project(tmp_path, tests):
    (tmp_path / "target.py").write_text(TARGET)
    (tmp_path / "test_target.py").write_text(tests)
    (tmp_path / "meta-test.toml").write_text(
        '[[suite]]\nname = "tiny"\ntargets = ["target.py"]\ntests = ["test_target.py"]\ntimeout = 20\n')
    return tmp_path


def run(root, tmp_path, **kw):
    s = mt.load_suites(root, root / "meta-test.toml")[0]
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    return mt.run_suite(root, s, kw.get("max", 0), 1, 2, scratch)


def test_strong_suite_scores_high_and_weak_suite_leaves_survivors(tmp_path):
    strong = run(project(tmp_path / "a", STRONG) if (tmp_path / "a").mkdir() is None else None, tmp_path / "a", max=0)
    weak = run(project(tmp_path / "b", WEAK) if (tmp_path / "b").mkdir() is None else None, tmp_path / "b", max=0)
    assert strong.baseline_ok and weak.baseline_ok
    assert strong.score == 1.0, [r for r in strong.results if r.outcome == "SURVIVED"]
    assert weak.score < strong.score
    surv = [r for r in weak.results if r.outcome == "SURVIVED"]
    assert surv and all(r.line in (2, 3, 4) for r in surv)      # all in clamp()


def test_unexercised_code_is_reported_separately_not_scored(tmp_path):
    (tmp_path / "x").mkdir()
    rep = run(project(tmp_path / "x", STRONG), tmp_path / "x")
    not_run = [r for r in rep.results if r.outcome == "NOT_EXERCISED"]
    assert not_run and all(r.line in (12, 13, 14) for r in not_run)   # never_called()
    executed, total = rep.coverage["target.py"]
    assert executed < total


def test_infinite_loop_mutant_counts_as_caught_by_timeout(tmp_path):
    (tmp_path / "y").mkdir()
    rep = run(project(tmp_path / "y", STRONG), tmp_path / "y")
    assert any(r.outcome == "TIMEOUT" and "Lt -> GtE" in r.desc for r in rep.results)


def test_run_never_modifies_the_working_tree(tmp_path):
    (tmp_path / "z").mkdir()
    root = project(tmp_path / "z", WEAK)
    before = {p.name: p.read_text() for p in root.glob("*.py")}
    run(root, tmp_path / "z")
    assert {p.name: p.read_text() for p in root.glob("*.py")} == before


def test_red_baseline_stops_everything(tmp_path):
    (tmp_path / "r").mkdir()
    root = project(tmp_path / "r", STRONG.replace("== 3\n    ", "== 99\n    ", 1))
    rep = run(root, tmp_path / "r")
    assert not rep.baseline_ok and rep.results == []


def test_cli_exit_codes_and_report_files(tmp_path):
    (tmp_path / "c").mkdir()
    root = project(tmp_path / "c", WEAK)
    out = tmp_path / "out"
    assert mt.main(["audit", "--root", str(root)]) == 1                         # assert True
    assert mt.main(["run", "--root", str(root), "--jobs", "2", "--out", str(out), "--min-score", "0.99"]) == 1
    data = json.loads((out / "meta-test-report.json").read_text())
    assert data[0]["suite"] == "tiny" and (out / "meta-test-report.md").read_text().startswith("# Meta-test report")
    assert mt.main(["run", "--root", str(tmp_path / "nope")]) == 2              # cannot load config
