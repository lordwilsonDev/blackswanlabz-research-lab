import http.server
import importlib.util
import json
import os
import subprocess
import sys
import threading
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parent.parent / ".claude" / "skills" / "lab-verify"
spec = importlib.util.spec_from_file_location("lab_harness", SKILL / "scripts" / "lab_harness.py")
lh = importlib.util.module_from_spec(spec)
sys.modules["lab_harness"] = lh
spec.loader.exec_module(lh)


def task(i, hidden_extra=True):
    return {"id": f"t{i}", "function": "inc", "prompt": "Write `inc(x)` returning x + 1.",
            "visible": "assert inc(1) == 2",
            "hidden": "assert inc(5) == 6" if hidden_extra else "assert inc(1) == 2",
            "ref": "def inc(x):\n    return x + 1"}


def make_exp(tmp_path, n=5, hidden_extra=True, margin=0.1):
    d = tmp_path / "exp"
    d.mkdir()
    prereg = json.loads((SKILL / "templates" / "prereg.template.json").read_text())
    prereg.update(question="q", hypothesis="h", falsification="f", limits=["l"], stopping_rule="s",
                  seeds=[0], margin=margin, bootstrap_resamples=200)
    (d / "prereg.json").write_text(json.dumps(prereg))
    (d / "tasks.json").write_text(json.dumps([task(i, hidden_extra) for i in range(n)]))
    return d


def ns(**kw):
    import argparse
    return argparse.Namespace(**kw)


def test_template_is_incomplete_until_filled():
    p = json.loads((SKILL / "templates" / "prereg.template.json").read_text())
    assert lh.validate_prereg(p) == []  # FILL markers are non-empty text; completeness is a human check
    p["limits"] = []
    assert any("limits" in e for e in lh.validate_prereg(p))
    p["standard_level"] = "rubric_other_model"
    assert any("only standard_level 'executable'" in e for e in lh.validate_prereg(p))


def test_lock_rejects_too_few_tasks(tmp_path):
    d = make_exp(tmp_path, n=3)
    with pytest.raises(SystemExit, match="fewer than 5 tasks"):
        lh.cmd_lock(ns(dir=str(d)))


def test_auto_cheat_passes_visible_and_fails_hidden():
    t = task(0)
    cheat = lh.auto_cheat(t)
    assert lh.run_tests(cheat, t["visible"], 5)[0] is True
    assert lh.run_tests(cheat, t["visible"] + "\n" + t["hidden"], 5)[0] is False


def test_selfcheck_flags_hidden_tests_that_add_nothing(tmp_path):
    d = make_exp(tmp_path, hidden_extra=False)
    lh.cmd_lock(ns(dir=str(d)))
    errs, _ = lh.selfcheck(d)
    assert any("hidden adds nothing" in e for e in errs)


def test_full_pipeline_with_fake_adapter_is_marked_not_evidence(tmp_path, capsys):
    d = make_exp(tmp_path)
    lh.cmd_lock(ns(dir=str(d)))
    lh.cmd_selfcheck(ns(dir=str(d)))
    lh.cmd_run(ns(dir=str(d), adapter="fake:0.5", note="test"))
    lh.cmd_analyze(ns(dir=str(d)))
    out = capsys.readouterr().out
    assert "NOT EVIDENCE" in out and "n/a (fake adapter)" in out
    res = json.loads((d / "ANALYSIS.json").read_text())
    assert res["evidence"] is False
    lh.cmd_report(ns(dir=str(d)))
    assert "NOT EVIDENCE" in (d / "REPORT.md").read_text()


def test_run_refuses_after_prereg_is_edited(tmp_path):
    d = make_exp(tmp_path)
    lh.cmd_lock(ns(dir=str(d)))
    lh.cmd_selfcheck(ns(dir=str(d)))
    p = json.loads((d / "prereg.json").read_text())
    p["margin"] = 0.0
    (d / "prereg.json").write_text(json.dumps(p))
    with pytest.raises(SystemExit, match="goalposts moved"):
        lh.cmd_run(ns(dir=str(d), adapter="fake:0.5", note=""))


def test_second_run_is_refused(tmp_path):
    d = make_exp(tmp_path)
    lh.cmd_lock(ns(dir=str(d)))
    lh.cmd_selfcheck(ns(dir=str(d)))
    lh.cmd_run(ns(dir=str(d), adapter="fake:0.5", note=""))
    with pytest.raises(SystemExit, match="already exists"):
        lh.cmd_run(ns(dir=str(d), adapter="fake:0.5", note=""))


def test_decision_rule_supported_and_not(tmp_path):
    d = make_exp(tmp_path)
    prereg = json.loads((d / "prereg.json").read_text())
    (d / "RUN.json").write_text(json.dumps({"evidence": True, "adapter": "x", "platform": "p", "instrument": "i"}))
    rows = []
    for i in range(5):
        for arm, ok in (("B", False), ("B-n", i < 2), ("C", True)):
            rows.append(dict(task=f"t{i}", seed=0, arm=arm, hidden_pass=ok, visible_pass=ok, false_pass=False,
                             attempts=1, tokens_out=10, seconds=1.0))
    (d / "results.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
    res = lh.analyze(d)
    assert res["decision"] == "SUPPORTED" and res["diff"] == pytest.approx(0.6)
    prereg["margin"] = 0.9
    (d / "prereg.json").write_text(json.dumps(prereg))
    assert lh.analyze(d)["decision"] == "NOT SUPPORTED"


def test_ollama_adapter_against_fake_server():
    seen = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            seen.update(body)
            out = json.dumps({"message": {"content": "<think>x</think>```python\nprint(1)\n```"}, "eval_count": 7}).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(out)
        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    env = {**os.environ, "OLLAMA_HOST": f"http://127.0.0.1:{srv.server_port}", "HARNESS_SEED": "42", "OLLAMA_MODEL": "m"}
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "ollama_adapter.py")], input="hello",
                       capture_output=True, text=True, env=env, timeout=30)
    srv.shutdown()
    assert r.returncode == 0 and "```python" in r.stdout and "<think>" not in r.stdout
    assert r.stderr.strip().endswith("TOKENS_OUT=7")
    assert seen["options"]["seed"] == 42 and seen["model"] == "m" and seen["stream"] is False
