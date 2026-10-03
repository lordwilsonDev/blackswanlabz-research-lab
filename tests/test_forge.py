import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LABF = ROOT / ".claude" / "skills" / "lab-forge"
spec = importlib.util.spec_from_file_location("forge", LABF / "scripts" / "forge.py")
forge = importlib.util.module_from_spec(spec)
sys.modules["forge"] = forge
spec.loader.exec_module(forge)


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    (r / "05-experiments").mkdir(parents=True)
    (r / "05-experiments" / "README.md").write_text("# Experiments\n\n| Experiment | Result | Claim |\n|---|---|---|\n")
    (r / "CLAIMS.md").write_text("# Claims\n\n| ID | Claim | Evidence | How to check | Status | Checked |\n|---|---|---|---|---|---|\n"
                                 "| C-009 | existing | e | h | pending | 2026-10-01 |\n")
    (r / "llms.txt").write_text("# Lab\n\n## Experiments\n- [Experiments index](05-experiments/README.md): index.\n\n## Proofs\n- [Proofs](06-proofs/README.md): p.\n")
    return r


def run(*args):
    return forge.main(list(args))


def test_new_executable_creates_pack_skill_ledger_and_index(repo, capsys):
    run("new", "demo", "--type", "executable", "--claim", "A small model with feedback beats resampling.", "--repo", str(repo))
    d = repo / "05-experiments" / "demo"
    assert (d / "prereg.json").exists() and (d / "tasks.json").exists() and (d / "README.md").exists()
    sk = (repo / ".claude" / "skills" / "run-demo" / "SKILL.md").read_text()
    assert sk.startswith("---\nname: run-demo\n") and "lab_harness.py" in sk
    assert "| C-010 |" in (repo / "CLAIMS.md").read_text()
    assert "(05-experiments/demo/README.md)" in (repo / "llms.txt").read_text()
    assert "(demo/README.md)" in (repo / "05-experiments" / "README.md").read_text()
    assert "pending" in (d / "README.md").read_text()


def test_new_refuses_to_overwrite(repo):
    run("new", "demo", "--type", "rubric", "--claim", "c", "--repo", str(repo))
    with pytest.raises(SystemExit, match="never overwrites"):
        run("new", "demo", "--type", "rubric", "--claim", "c", "--repo", str(repo))


def test_check_flags_fill_markers_then_passes_when_complete(repo, capsys):
    run("new", "demo", "--type", "executable", "--claim", "Claim text.", "--repo", str(repo))
    assert run("check", "demo", "--repo", str(repo)) == 1
    out = capsys.readouterr().out
    assert "FILL markers" in out and "NOT READY" in out
    d = repo / "05-experiments" / "demo"
    prereg = json.loads((d / "prereg.json").read_text())
    prereg.update(question="q", hypothesis="h", falsification="f", limits=["l"], stopping_rule="s")
    (d / "prereg.json").write_text(json.dumps(prereg))
    tasks = [{"id": f"t{i}", "function": "inc", "prompt": "Write inc(x) returning x + 1.", "visible": "assert inc(1) == 2",
              "hidden": "assert inc(5) == 6", "ref": "def inc(x):\n    return x + 1"} for i in range(5)]
    (d / "tasks.json").write_text(json.dumps(tasks))
    assert run("check", "demo", "--repo", str(repo)) == 0
    assert "READY TO LOCK" in capsys.readouterr().out


def test_check_catches_hidden_tests_that_add_nothing(repo, capsys):
    run("new", "demo", "--type", "executable", "--claim", "Claim text.", "--repo", str(repo))
    d = repo / "05-experiments" / "demo"
    prereg = json.loads((d / "prereg.json").read_text())
    prereg.update(question="q", hypothesis="h", falsification="f", limits=["l"], stopping_rule="s")
    (d / "prereg.json").write_text(json.dumps(prereg))
    tasks = [{"id": f"t{i}", "function": "inc", "prompt": "p", "visible": "assert inc(1) == 2", "hidden": "assert inc(1) == 2",
              "ref": "def inc(x):\n    return x + 1"} for i in range(5)]
    (d / "tasks.json").write_text(json.dumps(tasks))
    assert run("check", "demo", "--repo", str(repo)) == 1
    assert "hidden adds nothing" in capsys.readouterr().out


def test_rubric_pack_needs_controls_and_missing_skill_is_reported(repo, capsys):
    run("new", "rub", "--type", "rubric", "--claim", "A treatment beats baselines.", "--repo", str(repo))
    shutil.rmtree(repo / ".claude" / "skills" / "run-rub")
    run("check", "rub", "--repo", str(repo))
    out = capsys.readouterr().out
    assert "controls.json missing" in out and "run-rub skill missing" in out


def test_skill_regenerates_for_existing_pack_and_yaml_is_safe(repo):
    run("new", "rub", "--type", "rubric", "--claim", 'Colons: and "quotes" in a claim.', "--repo", str(repo))
    shutil.rmtree(repo / ".claude" / "skills" / "run-rub")
    run("skill", "rub", "--repo", str(repo))
    head = (repo / ".claude" / "skills" / "run-rub" / "SKILL.md").read_text().split("---")[1]
    desc = [l for l in head.splitlines() if l.startswith("description:")][0]
    assert desc.startswith('description: "') and desc.endswith('"') and '""' not in desc[14:-1]


def test_real_packs_are_ready_to_lock():
    assert forge.main(["check", "cvt-1", "--repo", str(ROOT)]) == 0
    assert forge.main(["check", "ail-moie-h1c-001", "--repo", str(ROOT)]) == 0


def test_generalized_rubric_arms_run_end_to_end(tmp_path):
    spec2 = importlib.util.spec_from_file_location("lab_rubric2", ROOT / ".claude" / "skills" / "lab-verify" / "scripts" / "lab_rubric.py")
    lr = importlib.util.module_from_spec(spec2)
    sys.modules["lab_rubric2"] = lr
    spec2.loader.exec_module(lr)
    d = tmp_path / "gen"
    d.mkdir()
    prereg = json.loads((LABF / "templates" / "rubric-prereg.template.json").read_text())
    prompts = json.loads((LABF / "templates" / "rubric-prompts.template.json").read_text())
    # the template is deliberately unfilled; fill just enough to run the plumbing
    prereg.update(question="q", hypothesis="h", falsification="f", limits=["l"])
    prompts = {k: v.replace("FILL", "x") for k, v in prompts.items()}
    (d / "prereg.json").write_text(json.dumps(prereg))
    (d / "prompts.json").write_text(json.dumps(prompts))
    (d / "questions.json").write_text(json.dumps([{"id": f"Q{i}", "text": f"question {i}"} for i in range(8)]))
    import argparse
    ns = lambda **kw: argparse.Namespace(**kw)
    lr.cmd_lock(ns(dir=str(d)))
    lr.cmd_run(ns(dir=str(d), adapter="fakegen", note="", resume=False))
    lr.cmd_blind(ns(dir=str(d)))
    for j in ("J1", "J2"):
        lr.cmd_judge(ns(dir=str(d), adapter="fakejudge:effect=1:noise=1", judge_id=j))
    lr.cmd_analyze(ns(dir=str(d)))
    a = json.loads((d / "ANALYSIS.json").read_text())
    assert set(a["contrasts"]) == {"B1-bon", "B2-bon"} and a["n_questions"] == 8
