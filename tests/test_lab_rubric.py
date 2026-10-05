import http.server
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "lab-verify"
spec = importlib.util.spec_from_file_location("lab_rubric", SKILL / "scripts" / "lab_rubric.py")
lr = importlib.util.module_from_spec(spec)
sys.modules["lab_rubric"] = lr
spec.loader.exec_module(lr)


def ns(**kw):
    import argparse
    return argparse.Namespace(**kw)


@pytest.fixture
def pack(tmp_path):
    d = tmp_path / "pack"
    shutil.copytree(ROOT / "05-experiments" / "ail-moie-h1c-001", d,
                    ignore=shutil.ignore_patterns("LOCK.json", "gen.jsonl", "RUN.json", "plan.json", "blind_*", "ratings.jsonl",
                                                  "ANALYSIS.json", "REPORT.md", "controls.json", "README.md"))
    return d


def run_to_judged(d, effect=1.5, noise=1.0, judges=("J1", "J2"), gen="fakegen"):
    lr.cmd_lock(ns(dir=str(d)))
    lr.cmd_run(ns(dir=str(d), adapter=gen, note="t", resume=False))
    lr.cmd_blind(ns(dir=str(d)))
    for j in judges:
        lr.cmd_judge(ns(dir=str(d), adapter=f"fakejudge:effect={effect}:noise={noise}", judge_id=j))


def test_holm_and_hedges_and_signflip():
    assert lr.holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
    assert lr.hedges_g([1.0, 1.0, 1.0]) == 999.0
    assert lr.hedges_g([-1.0, -1.0]) == 0.0
    rnd = random.Random(1)
    assert lr.signflip_p([1.0] * 10, rnd) == pytest.approx(1 / 1024)
    assert lr.signflip_p([-1.0] * 10, rnd) == 1.0


def test_krippendorff_alpha_known_cases():
    assert lr.krippendorff_alpha([[1, 1], [4, 4], [7, 7]]) == pytest.approx(1.0)
    assert lr.krippendorff_alpha([[1], [2]]) is None
    low = lr.krippendorff_alpha([[1, 7], [7, 1], [1, 7], [7, 1]])
    assert low < 0


def test_parse_rating():
    assert lr.parse_rating('sure {"novelty": 5, "coherence": 3} done') == (5.0, 3.0)
    assert lr.parse_rating('{"novelty": 9, "coherence": 3}') is None
    assert lr.parse_rating("no json") is None


def test_extract_final_truncates_and_flags():
    text, ok, trunc = lr.extract_final("blah\nFINAL HYPOTHESIS: " + "w " * 30, 10)
    assert ok and trunc and len(text.split()) == 10
    assert lr.extract_final("no marker here\n\nlast para", 50)[1] is False


def test_validate_rejects_incomplete_prereg(pack):
    p = json.loads((pack / "prereg.json").read_text())
    p["limits"] = []
    errs = lr.validate(p, json.loads((pack / "questions.json").read_text()), json.loads((pack / "prompts.json").read_text()))
    assert any("limits" in e for e in errs)


def test_pipeline_end_to_end_with_fakes_is_not_evidence(pack, capsys):
    run_to_judged(pack)
    items = json.loads((pack / "blind_items.json").read_text())
    assert len(items) == 12 * 2 * 7
    assert not any("arm" in it for it in items)
    lr.cmd_analyze(ns(dir=str(pack)))
    out = capsys.readouterr().out
    assert "NOT EVIDENCE" in out and "n/a (fake generator)" in out
    a = json.loads((pack / "ANALYSIS.json").read_text())
    assert a["judges"] == ["J1", "J2"] and a["decision"] == "n/a (fake generator)"
    for ratio in a["cost_ratio_vs_treatment"].values():
        assert 0.8 <= ratio <= 1.2
    lr.cmd_report(ns(dir=str(pack)))
    assert "NOT EVIDENCE" in (pack / "REPORT.md").read_text()


def test_compute_matching_plan_has_positive_n(pack):
    lr.cmd_lock(ns(dir=str(pack)))
    lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="", resume=False))
    plan = json.loads((pack / "plan.json").read_text())
    assert plan and all(v["n"] >= 1 for v in plan.values())


def test_run_refuses_after_edit_and_second_run(pack):
    lr.cmd_lock(ns(dir=str(pack)))
    original = (pack / "questions.json").read_text()
    q = json.loads(original)
    q[0]["text"] += " (edited)"
    (pack / "questions.json").write_text(json.dumps(q))
    with pytest.raises(SystemExit, match="goalposts moved"):
        lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="", resume=False))
    (pack / "questions.json").write_text(original)  # byte-exact restore passes the lock again
    lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="", resume=False))
    with pytest.raises(SystemExit, match="already exists"):
        lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="", resume=False))


def test_analyze_refuses_incomplete_ratings(pack):
    lr.cmd_lock(ns(dir=str(pack)))
    lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="", resume=False))
    lr.cmd_blind(ns(dir=str(pack)))
    (pack / "ratings.jsonl").write_text("")
    with pytest.raises(SystemExit, match="INCOMPLETE RATINGS"):
        lr.cmd_analyze(ns(dir=str(pack)))


def test_same_adapter_judge_is_flagged(pack):
    run_to_judged(pack, judges=("J1",), gen="fakegen")
    ratings = [json.loads(l) for l in (pack / "ratings.jsonl").read_text().splitlines()]
    assert all(r["same_as_generator"] is False for r in ratings)  # fakegen != fakejudge adapter string
    rows = [dict(r, same_as_generator=True) for r in ratings]
    (pack / "ratings.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    lr.cmd_analyze(ns(dir=str(pack)))
    assert any("JUDGE NOT INDEPENDENT" in f for f in json.loads((pack / "ANALYSIS.json").read_text())["flags"])


def test_decide_planted_effect_vs_null():
    p = {"comparison": {"treatment": "T", "controls": ["A", "B", "C"]}, "coherence_margin": 0.5,
         "primary": {"alpha": 0.05, "min_g": 0.5}}
    rnd = random.Random(3)

    def sim(effect):
        scores = {arm: {q: (rnd.gauss(4 + (effect if arm == "T" else 0), 1.0), rnd.gauss(4, 1.0)) for q in range(12)} for arm in "TABC"}
        return lr.decide(scores, p, rnd)["h1c_supported"]
    assert sum(sim(3.0) for _ in range(10)) >= 9
    assert sum(sim(0.0) for _ in range(10)) == 0


def test_import_ratings_from_csv(pack, tmp_path):
    lr.cmd_lock(ns(dir=str(pack)))
    lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="", resume=False))
    lr.cmd_blind(ns(dir=str(pack)))
    import csv
    src = tmp_path / "h.csv"
    rows = list(csv.DictReader(open(pack / "blind_items.csv", newline="")))
    for r in rows[:3]:
        r["novelty_1to7"], r["coherence_1to7"] = "5", "6"
    with open(src, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    lr.cmd_import(ns(dir=str(pack), file=str(src), judge_id="H1"))
    got = [json.loads(l) for l in (pack / "ratings.jsonl").read_text().splitlines()]
    assert len(got) == 3 and got[0]["judge"] == "H1" and got[0]["judge_adapter"] == "human"


def test_ollama_adapter_fails_closed_on_context_overflow():
    class H(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            self.rfile.read(int(self.headers["Content-Length"]))
            out = json.dumps({"message": {"content": "x"}, "eval_count": 1, "prompt_eval_count": 8190}).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(out)
        def log_message(self, *a):
            pass
    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    env = {**os.environ, "OLLAMA_HOST": f"http://127.0.0.1:{srv.server_port}", "OLLAMA_NUM_CTX": "8192"}
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "ollama_adapter.py")], input="hi", capture_output=True, text=True, env=env, timeout=30)
    srv.shutdown()
    assert r.returncode != 0 and "context overflow" in r.stderr


def test_resume_completes_an_interrupted_run_and_records_it(pack):
    lr.cmd_lock(ns(dir=str(pack)))
    lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="n", resume=False))
    lines = (pack / "gen.jsonl").read_text().splitlines()
    (pack / "gen.jsonl").write_text("\n".join(lines[:60]) + "\n")  # simulate an interruption partway
    lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="n", resume=True))
    rows = [json.loads(l) for l in (pack / "gen.jsonl").read_text().splitlines()]
    assert len(rows) == 12 * 2 * 7
    assert len({(r["q"], r["rep"], r["arm"]) for r in rows}) == len(rows)  # no duplicates
    assert len(json.loads((pack / "RUN.json").read_text())["resumes"]) == 1


def test_resume_refuses_a_different_adapter_and_a_missing_run(pack):
    lr.cmd_lock(ns(dir=str(pack)))
    with pytest.raises(SystemExit, match="no gen.jsonl"):
        lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="", resume=True))
    lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="", resume=False))
    with pytest.raises(SystemExit, match="adapter differs"):
        lr.cmd_run(ns(dir=str(pack), adapter="other", note="", resume=True))


def test_claude_adapter_with_fake_cli(tmp_path):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    fake = bindir / "claude"
    fake.write_text('#!/bin/sh\ncat >/dev/null\nprintf \'{"result":"thinking=%s","usage":{"output_tokens":5,"output_tokens_details":{"thinking_tokens":0}},"modelUsage":{"fake-model":{}},"total_cost_usd":0.0}\' "$MAX_THINKING_TOKENS"\n')
    fake.chmod(0o755)
    log = tmp_path / "adp.log"
    env = {**os.environ, "PATH": f"{bindir}:{os.environ['PATH']}", "CLAUDE_ADAPTER_LOG": str(log), "CLAUDE_MODEL": "haiku"}
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "claude_adapter.py")], input="a prompt of some length", capture_output=True,
                       text=True, env=env, timeout=30)
    assert r.returncode == 0
    assert r.stdout.strip() == "thinking=0"          # extended thinking is disabled
    assert "MODEL=fake-model" in r.stderr and r.stderr.strip().endswith("TOKENS_OUT=5")
    assert json.loads(log.read_text())["models"] == ["fake-model"]


def test_claude_adapter_fails_closed_when_the_cli_keeps_failing(tmp_path, monkeypatch):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    fake = bindir / "claude"
    fake.write_text("#!/bin/sh\ncat >/dev/null\necho boom >&2\nexit 1\n")
    fake.chmod(0o755)
    src = (SKILL / "scripts" / "claude_adapter.py").read_text().replace("time.sleep(2 * (attempt + 1))", "pass")
    script = tmp_path / "adapter.py"
    script.write_text(src)
    env = {**os.environ, "PATH": f"{bindir}:{os.environ['PATH']}"}
    r = subprocess.run([sys.executable, str(script)], input="x", capture_output=True, text=True, env=env, timeout=60)
    assert r.returncode != 0 and "failed after retries" in r.stderr


def test_candidate_labels_go_beyond_26_and_parse_back():
    labels = lr.candidate_labels(80)
    assert labels[0] == "A" and labels[25] == "Z" and labels[26] == "AA" and labels[27] == "AB" and len(set(labels)) == 80
    assert lr.parse_choice("The best is AB.", labels) == 27
    assert lr.parse_choice("(C)", labels) == 2
    assert lr.parse_choice("no label here", labels) == 0


def test_resume_survives_a_crash_in_the_baseline_phase(pack):
    """A real run crashed after all single-pass arms were done; --resume must reuse them and finish the baselines."""
    lr.cmd_lock(ns(dir=str(pack)))
    lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="", resume=False))
    lines = (pack / "gen.jsonl").read_text().splitlines()
    single = [l for l in lines if not json.loads(l)["arm"].endswith("-bon")]
    (pack / "gen.jsonl").write_text("\n".join(single) + "\n")
    lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="", resume=True))
    rows = [json.loads(l) for l in (pack / "gen.jsonl").read_text().splitlines()]
    assert len(rows) == 12 * 2 * 7 and sum(r["arm"].endswith("-bon") for r in rows) == 12 * 2 * 3


def test_max_n_caps_baselines_and_records_the_deviation(pack):
    lr.cmd_lock(ns(dir=str(pack)))
    lr.cmd_run(ns(dir=str(pack), adapter="fakegen", note="", resume=False, max_n=1, deviation_reason="test"))
    plan = json.loads((pack / "plan.json").read_text())
    assert all(v["n"] == 1 and v["n_uncapped"] >= 1 for v in plan.values())
    meta = json.loads((pack / "RUN.json").read_text())
    assert meta["deviation"]["max_n"] == 1 and meta["deviation"]["reason"] == "test"
