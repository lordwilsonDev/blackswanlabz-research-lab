#!/usr/bin/env python3
"""lab_harness: pre-register, lock, self-check, run, analyze and report an executable-oracle experiment.

Standard library only. The model is any shell command (the "adapter"): it receives the prompt on stdin,
prints the answer on stdout, and may print TOKENS_OUT=<n> as the last line of stderr. HARNESS_SEED is set in its environment.

  lab_harness.py new NAME [--root 05-experiments]   scaffold NAME/ with prereg.json and tasks.json
  lab_harness.py lock DIR                           validate the pre-registration, hash it with the tasks, write LOCK.json
  lab_harness.py selfcheck DIR                      reference passes, stub fails, auto-cheat is caught by hidden tests
  lab_harness.py run DIR --adapter CMD [--note T]   run the registered arms (refuses if anything changed after lock)
  lab_harness.py analyze DIR                        paired bootstrap and the registered decision
  lab_harness.py report DIR                         REPORT.md with the decision first and a PENDING claim row
  lab_harness.py status [ROOT]                      where each experiment stands
"""
from __future__ import annotations

import argparse, ast, datetime, hashlib, json, os, platform, random, re, shlex, statistics, subprocess, sys, tempfile, time
from pathlib import Path

VERSION = "lab-harness-0.1"
LEVELS = ("executable", "measurement", "rubric_other_model", "dated_prediction")
ARM_KINDS = ("single", "resample", "feedback")
REQUIRED = ("question", "standard_level", "hypothesis", "arms", "comparison", "metric", "margin", "attempts",
            "seeds", "falsification", "limits", "stopping_rule", "instrument_version")


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


def git_commit() -> str:
    r = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else "no-git"


# ---------- pre-registration ----------
def validate_prereg(p: dict) -> list[str]:
    errs = [f"missing or empty field: {k}" for k in REQUIRED if p.get(k) in (None, "", [], {})]
    if p.get("standard_level") not in LEVELS:
        errs.append(f"standard_level must be one of {LEVELS}")
    elif p["standard_level"] != "executable":
        errs.append("this harness runs only standard_level 'executable'; use a manual protocol for the others and label them weaker")
    arms = p.get("arms") or []
    ids = [a.get("id") for a in arms]
    if len(set(ids)) != len(ids):
        errs.append("arm ids must be unique")
    for a in arms:
        if a.get("kind") not in ARM_KINDS:
            errs.append(f"arm {a.get('id')}: kind must be one of {ARM_KINDS}")
    cmp_ = p.get("comparison") or {}
    for side in ("a", "b"):
        if cmp_.get(side) not in ids:
            errs.append(f"comparison.{side} must name a registered arm id")
    if not isinstance(p.get("margin"), (int, float)) or p.get("margin", -1) < 0:
        errs.append("margin must be a number >= 0")
    if p.get("metric") != "hidden_pass":
        errs.append("metric must be 'hidden_pass' (judged on hidden tests)")
    return errs


def lock_errors(d: Path) -> list[str]:
    lk = d / "LOCK.json"
    if not lk.exists():
        return ["not locked: run `lock` first"]
    rec = load(lk)["files"]
    return [f"{n} changed after lock (goalposts moved)" for n in ("prereg.json", "tasks.json")
            if not (d / n).exists() or sha(d / n) != rec.get(n)]


def cmd_new(a):
    d = Path(a.root) / a.name
    d.mkdir(parents=True, exist_ok=True)
    tpl = Path(__file__).resolve().parent.parent / "templates" / "prereg.template.json"
    for name, src in (("prereg.json", tpl.read_text()), ("tasks.json", "[]\n")):
        if not (d / name).exists():
            (d / name).write_text(src)
    print(f"created {d}; fill prereg.json and tasks.json, then run: lock {d}")


def cmd_lock(a):
    d = Path(a.dir)
    if (d / "LOCK.json").exists():
        sys.exit("already locked. Create a new experiment directory to change the standard; do not edit a locked one.")
    errs = validate_prereg(load(d / "prereg.json"))
    tasks = load(d / "tasks.json")
    if len(tasks) < 5:
        errs.append("fewer than 5 tasks: a result would be an anecdote")
    if errs:
        sys.exit("PRE-REGISTRATION INCOMPLETE:\n  " + "\n  ".join(errs))
    rec = {"locked_at": now(), "git_commit": git_commit(), "instrument": VERSION,
           "files": {n: sha(d / n) for n in ("prereg.json", "tasks.json")}}
    (d / "LOCK.json").write_text(json.dumps(rec, indent=1) + "\n")
    print("LOCKED", json.dumps(rec["files"]))


# ---------- oracle ----------
def run_tests(code: str, tests: str, timeout: float) -> tuple[bool, str]:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code + "\n\n" + tests + "\n")
        path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, (r.stderr or r.stdout).strip()[-600:]
    except subprocess.TimeoutExpired:
        return False, f"timeout after {timeout}s"
    finally:
        os.unlink(path)


def auto_cheat(task: dict) -> str | None:
    """Code that passes the visible tests by lookup alone. Hidden tests must reject it."""
    fn, table = task["function"], {}
    try:
        body = ast.parse(task["visible"]).body
    except SyntaxError:
        return None
    for node in body:
        t = getattr(node, "test", None)
        if isinstance(node, ast.Assert) and isinstance(t, ast.Compare) and len(t.ops) == 1 \
                and isinstance(t.ops[0], (ast.Eq, ast.Is)) and isinstance(t.left, ast.Call) \
                and getattr(t.left.func, "id", None) == fn:
            try:
                table[repr(tuple(ast.literal_eval(x) for x in t.left.args))] = ast.literal_eval(t.comparators[0])
            except (ValueError, SyntaxError):
                continue
    return f"_T = {table!r}\ndef {fn}(*a):\n    return _T.get(repr(a))\n" if table else None


def selfcheck(d: Path, timeout: float = 10) -> tuple[list[str], list[str]]:
    errs, warns = [], []
    tasks = load(d / "tasks.json")
    ids = [t["id"] for t in tasks]
    if len(set(ids)) != len(ids):
        errs.append("duplicate task ids")
    covered = 0
    for t in tasks:
        ok_v, m1 = run_tests(t["ref"], t["visible"], timeout)
        ok_h, m2 = run_tests(t["ref"], t["hidden"], timeout)
        if not (ok_v and ok_h):
            errs.append(f"{t['id']}: reference fails its own tests: {m1 or m2}")
        stub, _ = run_tests(f"def {t['function']}(*a, **k):\n    return None", t["visible"], timeout)
        if stub:
            errs.append(f"{t['id']}: a stub passes the visible tests")
        cheat = t.get("cheat") or auto_cheat(t)
        if cheat:
            cv, _ = run_tests(cheat, t["visible"], timeout)
            if cv:
                ch, _ = run_tests(cheat, t["visible"] + "\n" + t["hidden"], timeout)
                if ch:
                    errs.append(f"{t['id']}: visible-only cheat also passes hidden tests (hidden adds nothing)")
                else:
                    covered += 1
            else:
                warns.append(f"{t['id']}: no working cheat could be built (false-pass detection unproven)")
        else:
            warns.append(f"{t['id']}: no cheat possible")
    print(f"cheat caught by hidden tests on {covered}/{len(tasks)} tasks")
    return errs, warns


def cmd_selfcheck(a):
    d = Path(a.dir)
    e = lock_errors(d)
    if e:
        sys.exit("; ".join(e))
    errs, warns = selfcheck(d)
    for w in warns:
        print("WARN", w)
    if errs:
        sys.exit("SELF-CHECK FAILED:\n  " + "\n  ".join(errs))
    (d / "SELFCHECK.json").write_text(json.dumps({"ok": True, "at": now(), "tasks_sha256": sha(d / "tasks.json")}) + "\n")
    print(f"SELF-CHECK OK ({len(load(d / 'tasks.json'))} tasks, {len(warns)} warnings)")


# ---------- model adapter ----------
def first_prompt(t: dict) -> str:
    return (f"{t['prompt']}\n\nIt will be checked with tests like these (more cases exist that you cannot see):\n"
            f"```python\n{t['visible']}\n```\nReply with exactly one ```python code block defining `{t['function']}`; "
            f"no tests, no prints, no explanations.\n[task:{t['id']}]")


def feedback_prompt(t: dict, code: str, failure: str) -> str:
    return (first_prompt(t) + f"\n\nYour previous attempt:\n```python\n{code}\n```\nIt failed with:\n```\n{failure}\n```\n"
            "Fix the function. Think about cases the visible tests do not cover. Reply with the full corrected code block.")


def extract_code(text: str) -> str:
    m = re.findall(r"```(?:python)?\n(.*?)```", text, re.S)
    return (m[-1] if m else text).strip()


def call_adapter(adapter: str, prompt: str, seed: int, tasks: dict) -> tuple[str, int, float]:
    t0 = time.time()
    if adapter.startswith("fake"):  # harness self-test only; results are flagged as NOT EVIDENCE
        p = float(adapter.split(":")[1]) if ":" in adapter else 0.5
        t = tasks[re.search(r"\[task:([^\]]+)\]", prompt).group(1)]
        good = random.Random(f"{seed}|{prompt}").random() < p
        code = t["ref"] if good else f"def {t['function']}(*a, **k):\n    return None"
        return f"```python\n{code}\n```", len(code) // 4, time.time() - t0
    r = subprocess.run(shlex.split(adapter), input=prompt, capture_output=True, text=True, timeout=900,
                       env={**os.environ, "HARNESS_SEED": str(seed)})
    if r.returncode != 0:
        raise SystemExit(f"adapter failed ({r.returncode}): {r.stderr[-300:]}")
    m = re.search(r"TOKENS_OUT=(\d+)\s*$", r.stderr)
    return r.stdout, int(m.group(1)) if m else len(r.stdout) // 4, time.time() - t0


def judge(t: dict, code: str, timeout: float):
    v, msg = run_tests(code, t["visible"], timeout)
    h = run_tests(code, t["visible"] + "\n" + t["hidden"], timeout)[0] if v else False
    return v, h, msg


def cmd_run(a):
    d = Path(a.dir)
    errs = lock_errors(d)
    sc = d / "SELFCHECK.json"
    if not sc.exists() or load(sc).get("tasks_sha256") != sha(d / "tasks.json"):
        errs.append("self-check missing or stale: run `selfcheck` first")
    if (d / "results.jsonl").exists():
        errs.append("results.jsonl already exists: runs are registered once; move it aside and note why")
    if errs:
        sys.exit("REFUSING TO RUN:\n  " + "\n  ".join(errs))
    p = load(d / "prereg.json")
    tasks = {t["id"]: t for t in load(d / "tasks.json")}
    timeout = p.get("test_timeout_s", 5)
    meta = {"adapter": a.adapter, "note": a.note, "started": now(), "platform": platform.platform(),
            "machine": platform.machine(), "python": platform.python_version(), "instrument": VERSION,
            "evidence": not a.adapter.startswith("fake")}
    (d / "RUN.json").write_text(json.dumps(meta, indent=1) + "\n")
    with open(d / "results.jsonl", "w") as out:
        for t in tasks.values():
            for seed in p["seeds"]:
                text, tok, sec = call_adapter(a.adapter, first_prompt(t), seed * 1000, tasks)
                first = (text, tok, sec)
                for arm in p["arms"]:
                    gens, code = [first], extract_code(first[0])
                    v, h, msg = judge(t, code, timeout)
                    n = 1
                    while arm["kind"] != "single" and not v and n < p["attempts"]:
                        prompt = first_prompt(t) if arm["kind"] == "resample" else feedback_prompt(t, code, msg)
                        g = call_adapter(a.adapter, prompt, seed * 1000 + n, tasks)
                        gens.append(g); n += 1
                        code = extract_code(g[0])
                        v, h, msg = judge(t, code, timeout)
                    row = dict(task=t["id"], seed=seed, arm=arm["id"], visible_pass=v, hidden_pass=h,
                               false_pass=bool(v and not h), attempts=len(gens), tokens_out=sum(g[1] for g in gens),
                               seconds=round(sum(g[2] for g in gens), 2), adapter=a.adapter)
                    out.write(json.dumps(row) + "\n"); out.flush()
            print("done", t["id"], flush=True)
    meta["finished"] = now()
    (d / "RUN.json").write_text(json.dumps(meta, indent=1) + "\n")
    print("RUN COMPLETE: next, `analyze`")


# ---------- analysis ----------
def analyze(d: Path) -> dict:
    p = load(d / "prereg.json")
    rows = [json.loads(l) for l in (d / "results.jsonl").read_text().splitlines() if l.strip()]
    meta = load(d / "RUN.json")
    arms = [a["id"] for a in p["arms"]]
    table = {}
    for arm in arms:
        rs = [r for r in rows if r["arm"] == arm]
        table[arm] = {k: round(statistics.fmean(float(r[k]) for r in rs), 4) for k in
                      ("hidden_pass", "visible_pass", "false_pass", "attempts", "tokens_out", "seconds")} | {"n": len(rs)}
    a_id, b_id = p["comparison"]["a"], p["comparison"]["b"]
    tasks = sorted({r["task"] for r in rows})
    def tm(arm, task):
        v = [r["hidden_pass"] for r in rows if r["arm"] == arm and r["task"] == task]
        return sum(v) / len(v)
    diffs = [tm(a_id, t) - tm(b_id, t) for t in tasks]
    rnd, n = random.Random(12345), p.get("bootstrap_resamples", 5000)
    boots = sorted(statistics.fmean(rnd.choice(diffs) for _ in diffs) for _ in range(n))
    level = p.get("ci_level", 0.95)
    lo, hi = boots[int((1 - level) / 2 * n)], boots[int((1 + level) / 2 * n) - 1]
    diff = statistics.fmean(diffs)
    supported = diff >= p["margin"] and lo > 0
    return {"table": table, "comparison": f"{a_id} minus {b_id}", "diff": round(diff, 4),
            "ci": [round(lo, 4), round(hi, 4)], "ci_level": level, "margin": p["margin"], "n_tasks": len(tasks),
            "decision": "SUPPORTED" if supported else "NOT SUPPORTED", "evidence": meta["evidence"], "run": meta}


def cmd_analyze(a):
    d = Path(a.dir)
    res = analyze(d)
    (d / "ANALYSIS.json").write_text(json.dumps(res, indent=1) + "\n")
    if not res["evidence"]:
        print("*** HARNESS TEST WITH A FAKE ADAPTER: NOT EVIDENCE. Do not record, quote or claim these numbers. ***")
    print(f"{'arm':6}{'hidden':>8}{'visible':>9}{'falsepass':>10}{'attempts':>9}{'tok_out':>9}{'sec':>8}")
    for arm, m in res["table"].items():
        print(f"{arm:6}{m['hidden_pass']:8.3f}{m['visible_pass']:9.3f}{m['false_pass']:10.3f}{m['attempts']:9.2f}{m['tokens_out']:9.0f}{m['seconds']:8.1f}")
    print(f"\n{res['comparison']}: {res['diff']:+.3f}  {int(res['ci_level']*100)}% CI [{res['ci'][0]:+.3f}, {res['ci'][1]:+.3f}]  margin {res['margin']}")
    print("REGISTERED DECISION:", res["decision"] if res["evidence"] else "n/a (fake adapter)")


def cmd_report(a):
    d = Path(a.dir)
    res = analyze(d)
    p = load(d / "prereg.json")
    banner = "" if res["evidence"] else "**HARNESS TEST WITH A FAKE ADAPTER. NOT EVIDENCE.**\n\n"
    rows = "\n".join(f"| {k} | {m['hidden_pass']:.3f} | {m['visible_pass']:.3f} | {m['false_pass']:.3f} | {m['attempts']:.2f} | {m['tokens_out']:.0f} | {m['seconds']:.1f} |"
                     for k, m in res["table"].items())
    text = f"""# {d.name}: report

{banner}**Registered decision: {res['decision'] if res['evidence'] else 'n/a'}.** {res['comparison']} on hidden tests = {res['diff']:+.3f}, {int(res['ci_level']*100)}% CI [{res['ci'][0]:+.3f}, {res['ci'][1]:+.3f}], registered margin {res['margin']}, {res['n_tasks']} tasks.

## Registered question and falsification

{p['question']}

Falsification, fixed before the run: {p['falsification']}

## Results (descriptive)

| arm | hidden | visible | false pass | attempts | tokens out | seconds |
|---|---|---|---|---|---|---|
{rows}

## Run record

Adapter `{res['run']['adapter']}`; note: {res['run'].get('note') or '(none)'}; {res['run']['platform']}; instrument {res['run']['instrument']}.

## Limits, as registered

""" + "\n".join(f"- {x}" for x in p["limits"]) + f"""

## Suggested ledger row (add to CLAIMS.md only after you have checked this report)

`| C-??? | {p['hypothesis']} Result under the registered rule: {res['decision']} ({res['comparison']} {res['diff']:+.3f}, n={res['n_tasks']} tasks) | {d.as_posix()}/REPORT.md | re-run `lab_harness.py run` with the same adapter; compare ANALYSIS.json | pending | {datetime.date.today()} |`

Status stays **pending** until someone other than the run's author has re-run it, or the author states plainly that it was not independently re-run.
"""
    (d / "REPORT.md").write_text(text)
    print(f"wrote {d / 'REPORT.md'}")


def cmd_status(a):
    root = Path(a.root)
    for d in sorted(p.parent for p in root.glob("*/prereg.json")):
        st = ("analyzed" if (d / "ANALYSIS.json").exists() else "run" if (d / "results.jsonl").exists()
              else "self-checked" if (d / "SELFCHECK.json").exists() else "locked" if (d / "LOCK.json").exists() else "draft")
        bad = lock_errors(d) if (d / "LOCK.json").exists() else []
        print(f"{d.name}: {st}" + (f"  !! {'; '.join(bad)}" if bad else ""))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("new"); s.add_argument("name"); s.add_argument("--root", default="05-experiments"); s.set_defaults(f=cmd_new)
    for n, f in (("lock", cmd_lock), ("selfcheck", cmd_selfcheck), ("analyze", cmd_analyze), ("report", cmd_report)):
        s = sub.add_parser(n); s.add_argument("dir"); s.set_defaults(f=f)
    s = sub.add_parser("run"); s.add_argument("dir"); s.add_argument("--adapter", required=True); s.add_argument("--note", default=""); s.set_defaults(f=cmd_run)
    s = sub.add_parser("status"); s.add_argument("root", nargs="?", default="05-experiments"); s.set_defaults(f=cmd_status)
    args = ap.parse_args(argv)
    args.f(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
