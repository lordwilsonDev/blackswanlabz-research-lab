#!/usr/bin/env python3
"""forge: scaffold, check and package a pre-registered experiment so that "run NAME" is one sentence. Standard library only.

  forge.py new NAME --type executable|rubric --claim "..." [--root 05-experiments] [--repo .] [--no-index] [--no-ledger]
  forge.py skill NAME [--root 05-experiments] [--repo .]     write .claude/skills/run-NAME/SKILL.md for an existing pack
  forge.py check NAME [--root 05-experiments] [--repo .]     completeness gate before the owner locks the pack
  forge.py process                                            print the stages this tool encodes
"""
from __future__ import annotations

import argparse, datetime, importlib.util, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent.parent / "lab-verify" / "scripts"
STAGES = [
    ("1 claim", "State what you think is true in one sentence that can fail. If it cannot fail, rewrite it."),
    ("2 standard", "Pick the strongest checkable standard: an executable check, then a measurement, then a rubric judged blind by another model, then a dated prediction. Say which and why a stronger one is impossible."),
    ("3 instrument", "Build the smallest thing that can answer the question: tasks with visible and hidden tests, or questions with prompts and a rubric."),
    ("4 pre-registration", "Write the hypothesis, arms, compared pair, metric, margin, falsification condition (a tie fails), limits and stopping rule before any run."),
    ("5 instrument controls", "Prove the instrument works on cases with known answers: reference passes, stub fails, a visible-only cheat is caught; or a null dataset rarely passes and a planted effect usually does. Record the power."),
    ("6 validity traps", "Look for ways the run can be silently wrong: a truncated context window, a hard-coded system prompt, a judge that shares the generator's family, tests the generator can see, bytes that change after the lock. Make the harness fail closed."),
    ("7 lock", "Hash the registration and inputs. After this, any edit makes the run refuse. The owner locks; the builder does not."),
    ("8 run once", "Run on the real model on the real machine. A second run is refused. A fake adapter proves plumbing only and is stamped NOT EVIDENCE."),
    ("9 report", "Registered decision first, descriptive numbers second, limits third. Results against the hypothesis get the same prominence."),
    ("10 ledger", "Add the claim as pending with a way to re-check it. It becomes verified only after someone other than the run's author reproduces it."),
    ("11 package", "Write the run sheet and a run-NAME skill so that a stranger can say one sentence and get the same process. Index the page so readers and models can find it."),
]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def read(p: Path):
    return json.loads(p.read_text())


def kind_of(d: Path) -> str:
    return "rubric" if read(d / "prereg.json").get("standard_level") == "rubric_other_model" else "executable"


def next_claim_id(claims: str) -> str:
    ids = [int(m) for m in re.findall(r"^\| C-(\d{3}) \|", claims, re.M)]
    return f"C-{max(ids, default=0) + 1:03d}"


def run_sheet_commands(name: str, rel: str, kind: str, adapter: str = "ollama") -> str:
    h = ".claude/skills/lab-verify/scripts"
    gen_env, judge_env = ("OLLAMA_MODEL=GENERATOR", "OLLAMA_MODEL=JUDGE") if adapter == "ollama" else ("CLAUDE_MODEL=haiku", "CLAUDE_MODEL=sonnet")
    script = "ollama_adapter.py" if adapter == "ollama" else "claude_adapter.py"
    if kind == "executable":
        return f"""```bash
H={h}
python3 $H/lab_harness.py selfcheck {rel}      # after you lock; must say SELF-CHECK OK
python3 $H/lab_harness.py lock      {rel}      # freezes prereg.json and tasks.json (the owner does this)
python3 $H/lab_harness.py selfcheck {rel}
{gen_env} python3 $H/lab_harness.py run {rel} --adapter "python3 $H/{script}" --note "HARDWARE and MODEL"
python3 $H/lab_harness.py analyze {rel}
python3 $H/lab_harness.py report  {rel}
```
(Run `selfcheck` once before locking to catch bad tasks, and again after.)"""
    return f"""```bash
H={h}
D={rel}
python3 $H/lab_rubric.py controls --out $D/controls.json   # validates the decision rule on synthetic data
python3 $H/lab_rubric.py lock  $D                            # freezes prereg.json, questions.json, prompts.json (the owner does this)
{gen_env} python3 $H/lab_rubric.py run $D --adapter "python3 $H/{script}" --note "HARDWARE and GENERATOR"   # add --resume to continue an interrupted run
python3 $H/lab_rubric.py blind $D                            # never show judges blind_key.json
{judge_env} python3 $H/lab_rubric.py judge $D --adapter "python3 $H/{script}" --judge-id J1   # a different family if you can
# second judge J2: another family, or a human via: lab_rubric.py import-ratings $D filled.csv --judge-id J2
python3 $H/lab_rubric.py analyze $D
python3 $H/lab_rubric.py report  $D
```
{'Set `OLLAMA_SYSTEM`, `OLLAMA_NUM_PREDICT` and `OLLAMA_NUM_CTX` for the experiment; the adapter fails closed if a prompt would overflow the context window.' if adapter == 'ollama' else 'The claude adapter disables extended thinking, runs in an empty directory, and cannot set a seed or temperature; register those facts as limits.'}"""


def write_readme(d: Path, name: str, rel: str, kind: str, claim: str, adapter: str = "ollama"):
    text = f"""---
source: pre-registration and run sheet scaffolded by lab-forge on {datetime.date.today()}
captured: {datetime.date.today()}
status: pending
---

# {name}: run sheet and pre-registration

**Not run.** Nothing on this page is a result. It fixes what will be run and how it will be judged.

## The claim

{claim}

## Run it

{run_sheet_commands(name, rel, kind, adapter)}

Or in Claude Code or claude.ai, say: **use the run-{name} skill**.

## Registered decision, design and limits

See `prereg.json` in this folder. Fill every `FILL` marker before locking; after locking the harness refuses to run if anything changed.

## Status

Pending until a real run exists and someone other than its author has reproduced it.
"""
    (d / "README.md").write_text(text)


def write_skill(repo: Path, name: str, rel: str, kind: str, claim: str, adapter: str = "ollama"):
    sk = repo / ".claude" / "skills" / f"run-{name}"
    sk.mkdir(parents=True, exist_ok=True)
    one = " ".join(claim.split()).rstrip(".").replace('"', "'")
    short = one if len(one) <= 140 else one[:140].rsplit(" ", 1)[0] + " ..."
    text = f"""---
name: run-{name}
description: "Run the {name} experiment ({short}). Use when the user says run {name}, use the run-{name} skill, or asks to reproduce this test. Follows the registered pre-registration exactly and never edits it."
---

# run-{name}

This skill runs one registered experiment, `{rel}`. First read `.claude/skills/lab-verify/SKILL.md` for the rules. Then follow this sheet.

## Rules that apply

- Never describe a result as peer reviewed, externally validated or independently confirmed.
- Never edit `prereg.json`, `{'tasks.json' if kind == 'executable' else 'questions.json` or `prompts.json'}` after the lock, and never edit result files. The harness refuses to run if they changed.
- The owner locks. If the pack is not locked yet, show the owner the pre-registration and ask them to run `lock`.
- A fake adapter is a harness test: say it is not evidence and do not quote its numbers.
- Report the registered decision first, then the numbers, then the limits. Results against the hypothesis get the same prominence.

## Ask the user first

1. The adapter command for the model under test (`ollama_adapter.py` with `OLLAMA_MODEL`, or `claude_adapter.py` with `CLAUDE_MODEL`).
{'2. A judge model of a different family from the generator, and a second judge (another family or a human).' + chr(10) + '3. A run note: the hardware and the models. Do not guess them.' if kind == 'rubric' else '2. A run note: the hardware and the model. Do not guess them.'}

## Steps

{run_sheet_commands(name, rel, kind, adapter)}

## Return to the user

What was run and its output; the registered decision; the suggested ledger row (add it to `CLAIMS.md` as `pending`); what could not be verified. Add nothing as `verified` until someone else has reproduced it.
"""
    (sk / "SKILL.md").write_text(text)
    return sk / "SKILL.md"


def add_index(repo: Path, root: str, name: str, claim: str, claim_id: str | None):
    rel = f"{root}/{name}/README.md"
    llms = repo / "llms.txt"
    if llms.exists():
        t = llms.read_text()
        line = f"- [{name} run sheet]({rel}): scaffolded experiment; not run, no result. {claim.strip().rstrip('.')[:120]}."
        if rel not in t:
            m = re.search(r"^## Experiments\n(?:- .*\n)+", t, re.M)
            t = t[:m.end()] + line + "\n" + t[m.end():] if m else t.rstrip("\n") + "\n" + line + "\n"
            llms.write_text(t)
    idx = repo / root / "README.md"
    if idx.exists():
        ref = f" | [{claim_id}](../CLAIMS.md) pending |" if claim_id else " | none yet |"
        row = f"| [{name}]({name}/README.md) | Scaffolded; not run, no result |{ref}\n"
        t = idx.read_text()
        if f"({name}/README.md)" not in t:
            idx.write_text(t.rstrip("\n") + "\n" + row)


def cmd_new(a):
    repo, d = Path(a.repo), Path(a.repo) / a.root / a.name
    if d.exists():
        sys.exit(f"{d} already exists; forge never overwrites an experiment")
    d.mkdir(parents=True)
    rel = f"{a.root}/{a.name}"
    if a.type == "executable":
        (d / "prereg.json").write_text((LAB.parent / "templates" / "prereg.template.json").read_text())
        (d / "tasks.json").write_text("[]\n")
    else:
        (d / "prereg.json").write_text((HERE.parent / "templates" / "rubric-prereg.template.json").read_text())
        (d / "prompts.json").write_text((HERE.parent / "templates" / "rubric-prompts.template.json").read_text())
        (d / "questions.json").write_text("[]\n")
    claim_id = None
    cl = repo / "CLAIMS.md"
    if cl.exists() and not a.no_ledger:
        t = cl.read_text()
        claim_id = next_claim_id(t)
        row = f"| {claim_id} | {a.claim.strip()} (experiment {a.name}, not run) | [{a.name}/README.md]({rel}/README.md) | the run commands in that page | pending | {datetime.date.today()} |"
        cl.write_text(t.rstrip("\n") + "\n" + row + "\n")
    write_readme(d, a.name, rel, a.type, a.claim, a.adapter)
    skill = write_skill(repo, a.name, rel, a.type, a.claim, a.adapter)
    if not a.no_index:
        add_index(repo, a.root, a.name, a.claim, claim_id)
    print(f"created {d}\nrun-skill {skill}\nledger row {claim_id or '(skipped)'}")
    print("next: fill every FILL marker, add tasks or questions, run `check`, then the owner runs `lock`.")


def cmd_skill(a):
    repo, d = Path(a.repo), Path(a.repo) / a.root / a.name
    claim = read(d / "prereg.json").get("question", a.name)
    print("wrote", write_skill(repo, a.name, f"{a.root}/{a.name}", kind_of(d), claim, a.adapter))


def cmd_check(a):
    repo, d = Path(a.repo), Path(a.repo) / a.root / a.name
    problems, notes = [], []
    if not (d / "prereg.json").exists():
        sys.exit(f"no pack at {d}")
    kind = kind_of(d)
    p = read(d / "prereg.json")
    for f in ("prereg.json", "prompts.json"):
        if (d / f).exists() and "FILL" in (d / f).read_text():
            problems.append(f"{f} still has FILL markers")
    if kind == "executable":
        h = load_module(LAB / "lab_harness.py", "forge_lab_harness")
        tasks = read(d / "tasks.json")
        problems += [f"prereg: {e}" for e in h.validate_prereg(p)]
        if len(tasks) < 5:
            problems.append(f"only {len(tasks)} tasks (need at least 5)")
        elif not problems:
            errs, warns = h.selfcheck(d)
            problems += [f"selfcheck: {e}" for e in errs]
            notes += [f"selfcheck warning: {w}" for w in warns]
    else:
        r = load_module(LAB / "lab_rubric.py", "forge_lab_rubric")
        qs = read(d / "questions.json")
        prompts = read(d / "prompts.json") if (d / "prompts.json").exists() else {}
        problems += [f"prereg: {e}" for e in r.validate(p, qs, prompts)]
        if not (d / "controls.json").exists():
            problems.append("controls.json missing: run `lab_rubric.py controls --out controls.json` and record the power")
    if not (d / "README.md").exists():
        problems.append("README.md run sheet missing")
    if not (repo / ".claude" / "skills" / f"run-{a.name}" / "SKILL.md").exists():
        problems.append(f"run-{a.name} skill missing: run `forge.py skill {a.name}`")
    cl = repo / "CLAIMS.md"
    if cl.exists() and not re.search(rf"^\| C-\d{{3}} \|.*\b{re.escape(a.name)}\b", cl.read_text(), re.M):
        problems.append(f"no CLAIMS.md row mentions {a.name}: add a pending claim")
    llms = repo / "llms.txt"
    if llms.exists() and f"{a.root}/{a.name}/README.md" not in llms.read_text():
        problems.append("llms.txt does not link the run sheet")
    locked = (d / "LOCK.json").exists()
    for n in notes:
        print("NOTE", n)
    for x in problems:
        print("MISSING", x)
    state = "ALREADY LOCKED" if locked else ("READY TO LOCK (the owner runs `lock`)" if not problems else "NOT READY")
    print(f"{a.name} [{kind}]: {state}")
    return 1 if problems else 0


def cmd_process(a):
    for k, v in STAGES:
        print(f"{k:22} {v}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    common = lambda s: (s.add_argument("--root", default="05-experiments"), s.add_argument("--repo", default="."))
    s = sub.add_parser("new"); s.add_argument("name"); s.add_argument("--type", required=True, choices=["executable", "rubric"])
    s.add_argument("--claim", required=True); s.add_argument("--adapter", default="ollama", choices=["ollama", "claude"]); s.add_argument("--no-index", action="store_true"); s.add_argument("--no-ledger", action="store_true")
    common(s); s.set_defaults(f=cmd_new)
    for n, f in (("skill", cmd_skill), ("check", cmd_check)):
        s = sub.add_parser(n); s.add_argument("name"); common(s)
        if n == "skill":
            s.add_argument("--adapter", default="ollama", choices=["ollama", "claude"])
        s.set_defaults(f=f)
    s = sub.add_parser("process"); s.set_defaults(f=cmd_process)
    args = ap.parse_args(argv)
    return args.f(args) or 0


if __name__ == "__main__":
    sys.exit(main())
