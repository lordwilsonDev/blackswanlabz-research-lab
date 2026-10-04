#!/usr/bin/env python3
"""Meta-test: test the tests. Standard library only (Python 3.11+), pytest as the runner.

A passing suite proves little unless it fails when the code is wrong. For each suite in
meta-test.toml this tool:

  1. runs the suite and requires it to be green (a red baseline makes everything else moot);
  2. traces which target lines the suite actually executes (a test that never reaches the
     target is TEST_NOT_EVIDENCE, however green);
  3. generates mutants of the target (flipped comparisons, swapped and/or, removed
     branches, changed returns and constants) on the executed lines, runs the suite against
     each in an isolated copy, and counts the ones it fails to notice (survivors);
  4. audits the test files for tests with no assertions, tautologies, and test files that
     do not import their target.

    meta_test.py run   --root . [--config meta-test.toml] [--suite NAME] [--max-mutants N]
                       [--seed S] [--jobs J] [--min-score F] [--out DIR]
    meta_test.py audit --root . [--config meta-test.toml]

A survivor is a lead, not a verdict: some mutants are equivalent (the change cannot alter
behavior). Triage them; do not chase a score of 100 percent.
Exit codes: 0 ok, 1 below threshold or audit findings, 2 baseline red or could not run.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import queue
import random
import shutil
import subprocess
import sys
import tempfile
import threading
import tomllib
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

COPY_IGNORE = shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", ".meta-test", "node_modules")


def copy_ignore(scratch: Path):
    """COPY_IGNORE plus the scratch directory itself, in case it sits inside the project."""
    scratch = scratch.resolve()

    def ignore(directory: str, names: list[str]) -> set[str]:
        skip = set(COPY_IGNORE(directory, names))
        skip |= {n for n in names if (Path(directory) / n).resolve() == scratch}
        return skip
    return ignore
CMP_SWAP = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.GtE, ast.GtE: ast.Lt, ast.Gt: ast.LtE,
            ast.LtE: ast.Gt, ast.Is: ast.IsNot, ast.IsNot: ast.Is, ast.In: ast.NotIn, ast.NotIn: ast.In}


# --------------------------------------------------------------------------
# Executable lines and tracing
# --------------------------------------------------------------------------
def executable_lines(tree: ast.AST) -> set[int]:
    lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.stmt):
            is_doc = (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
                      and isinstance(node.value.value, str))
            if not is_doc:
                lines.add(node.lineno)
    return lines


def trace_run(targets: list[str], pytest_args: list[str], out_json: str) -> int:
    """Run pytest in this process with a line tracer limited to the target files."""
    import pytest
    wanted = {os.path.realpath(t) for t in targets}
    executed: dict[str, set[int]] = {w: set() for w in wanted}

    def tracer(frame, event, arg):
        fn = os.path.realpath(frame.f_code.co_filename)
        if fn not in wanted:
            return None
        executed[fn].add(frame.f_lineno)

        def local(frame, event, arg):
            if event == "line":
                executed[fn].add(frame.f_lineno)
            return local
        return local

    sys.settrace(tracer)
    threading.settrace(tracer)
    try:
        rc = int(pytest.main(pytest_args))
    finally:
        sys.settrace(None)
        threading.settrace(None)
    Path(out_json).write_text(json.dumps({k: sorted(v) for k, v in executed.items()}))
    return rc


# --------------------------------------------------------------------------
# Mutation
# --------------------------------------------------------------------------
class Mutator(ast.NodeTransformer):
    """Enumerates mutation sites (target=-1) or applies the k-th one."""

    def __init__(self, target: int = -1, allowed_lines: set[int] | None = None):
        self.target, self.n, self.sites = target, 0, []
        self.allowed = allowed_lines
        self.applied = False
        self._skip = 0

    def _hit(self, node, desc: str) -> bool:
        if self._skip or (self.allowed is not None and getattr(node, "lineno", 0) not in self.allowed):
            return False
        idx = self.n
        self.n += 1
        self.sites.append((idx, node.lineno, desc))
        if idx == self.target:
            self.applied = True
            return True
        return False

    def visit_If(self, node: ast.If):
        if (isinstance(node.test, ast.Compare) and isinstance(node.test.left, ast.Name)
                and node.test.left.id == "__name__"):
            return node                                   # never mutate the __main__ guard
        self.generic_visit(node)
        if not isinstance(node.test, ast.Constant):
            if self._hit(node, "if-condition -> False (branch removed)"):
                node.test = ast.Constant(False)
            elif self._hit(node, "if-condition -> True (branch forced)"):
                node.test = ast.Constant(True)
        return node

    def visit_While(self, node: ast.While):
        self.generic_visit(node)
        return node

    def visit_Compare(self, node: ast.Compare):
        self.generic_visit(node)
        if len(node.ops) == 1 and type(node.ops[0]) in CMP_SWAP:
            old = type(node.ops[0]).__name__
            if self._hit(node, f"comparison {old} -> {CMP_SWAP[type(node.ops[0])].__name__}"):
                node.ops[0] = CMP_SWAP[type(node.ops[0])]()
        return node

    def visit_BoolOp(self, node: ast.BoolOp):
        self.generic_visit(node)
        new = ast.Or if isinstance(node.op, ast.And) else ast.And
        if self._hit(node, f"{type(node.op).__name__} -> {new.__name__}"):
            node.op = new()
        return node

    def visit_UnaryOp(self, node: ast.UnaryOp):
        self.generic_visit(node)
        if isinstance(node.op, ast.Not) and self._hit(node, "'not' removed"):
            return node.operand
        return node

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, bool) and self._hit(node, f"{node.value} -> {not node.value}"):
            return ast.copy_location(ast.Constant(not node.value), node)
        if (isinstance(node.value, int) and not isinstance(node.value, bool) and node.value not in (0, 1)
                and self._hit(node, f"{node.value} -> {node.value + 1}")):
            return ast.copy_location(ast.Constant(node.value + 1), node)
        return node

    def visit_JoinedStr(self, node: ast.JoinedStr):
        return node                                       # leave f-strings alone

    def visit_Return(self, node: ast.Return):
        self.generic_visit(node)
        if node.value is not None and not (isinstance(node.value, ast.Constant) and node.value.value is None):
            if self._hit(node, "return value -> None"):
                node.value = ast.Constant(None)
        return node


def enumerate_sites(source: str, allowed_lines: set[int] | None) -> list[tuple[int, int, str]]:
    m = Mutator(-1, allowed_lines)
    m.visit(ast.parse(source))
    return m.sites


def apply_mutant(source: str, index: int, allowed_lines: set[int] | None) -> str:
    m = Mutator(index, allowed_lines)
    tree = m.visit(ast.parse(source))
    if not m.applied:
        raise ValueError(f"mutation site {index} not found")
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


# --------------------------------------------------------------------------
# Test audit
# --------------------------------------------------------------------------
def audit_test_file(path: Path, target_modules: set[str]) -> list[str]:
    findings: list[str] = []
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    if target_modules and not (imported & target_modules):
        findings.append(f"{path.name}: imports none of its targets {sorted(target_modules)} (TEST_NOT_EVIDENCE)")
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test")]:
        asserts = [n for n in ast.walk(fn) if isinstance(n, ast.Assert)]
        raises = [n for n in ast.walk(fn) if isinstance(n, ast.Call)
                  and getattr(n.func, "attr", getattr(n.func, "id", "")) in {"raises", "fail", "warns"}]
        delegated = [n for n in ast.walk(fn) if isinstance(n, ast.Call)
                     and getattr(n.func, "id", "").startswith(("assert_", "check_", "verify_"))]
        if not (asserts or raises or delegated):
            findings.append(f"{path.name}::{fn.name}: no assertion")
        for a in asserts:
            t = a.test
            if isinstance(t, ast.Constant) and t.value in (True, 1):
                findings.append(f"{path.name}::{fn.name}:{a.lineno}: assert always true")
            elif (isinstance(t, ast.Compare) and len(t.ops) == 1 and isinstance(t.ops[0], ast.Eq)
                  and ast.dump(t.left) == ast.dump(t.comparators[0])):
                findings.append(f"{path.name}::{fn.name}:{a.lineno}: compares a value with itself")
    return findings


# --------------------------------------------------------------------------
# Suites and the run
# --------------------------------------------------------------------------
@dataclass
class Suite:
    name: str
    targets: list[str]
    tests: list[str]
    timeout: float = 120.0


@dataclass
class MutantResult:
    target: str
    line: int
    desc: str
    outcome: str          # KILLED | SURVIVED | TIMEOUT | NOT_EXERCISED


@dataclass
class SuiteReport:
    name: str
    baseline_ok: bool = True
    coverage: dict[str, tuple[int, int]] = field(default_factory=dict)   # target -> (executed, executable)
    results: list[MutantResult] = field(default_factory=list)
    audit: list[str] = field(default_factory=list)

    @property
    def score(self) -> float | None:
        killed = sum(r.outcome in ("KILLED", "TIMEOUT") for r in self.results)
        surv = sum(r.outcome == "SURVIVED" for r in self.results)
        return killed / (killed + surv) if killed + surv else None


def load_suites(root: Path, config: Path) -> list[Suite]:
    cfg = tomllib.loads(config.read_text(encoding="utf-8"))
    suites = [Suite(s["name"], s["targets"], s["tests"], float(s.get("timeout", 120))) for s in cfg.get("suite", [])]
    for s in suites:
        for p in s.targets + s.tests:
            if not (root / p).is_file():
                raise FileNotFoundError(f"{s.name}: {p} does not exist")
    return suites


def pytest_cmd(tests: list[str], fail_fast: bool) -> list[str]:
    return [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *(["-x"] if fail_fast else []), *tests]


def run_suite(root: Path, s: Suite, max_mutants: int, seed: int, jobs: int, scratch: Path) -> SuiteReport:
    rep = SuiteReport(s.name)
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    base = subprocess.run(pytest_cmd(s.tests, False), cwd=root, capture_output=True, text=True, env=env, timeout=s.timeout * 3)
    if base.returncode != 0:
        rep.baseline_ok = False
        rep.audit.append("baseline suite is RED:\n" + base.stdout[-800:])
        return rep

    cov_file = scratch / f"{s.name}.cov.json"
    subprocess.run([sys.executable, __file__, "_trace", "--out", str(cov_file), "--targets", *s.targets,
                    "--", *pytest_cmd(s.tests, False)[3:]], cwd=root, capture_output=True, text=True, env=env,
                   timeout=s.timeout * 6)
    executed = json.loads(cov_file.read_text()) if cov_file.is_file() else {}

    all_sites: list[tuple[str, int, int, str, set[int]]] = []
    for t in s.targets:
        src = (root / t).read_text(encoding="utf-8")
        ex = set(executed.get(os.path.realpath(root / t), []))
        stmts = executable_lines(ast.parse(src))
        rep.coverage[t] = (len(ex & stmts), len(stmts))
        for idx, line, desc in enumerate_sites(src, None):
            if line in ex:
                all_sites.append((t, idx, line, desc, ex))
            else:
                rep.results.append(MutantResult(t, line, desc, "NOT_EXERCISED"))

    random.Random(seed).shuffle(all_sites)
    chosen = all_sites[:max_mutants] if max_mutants else all_sites

    pool: queue.Queue[Path] = queue.Queue()
    for i in range(jobs):
        d = scratch / f"{s.name}-w{i}"
        shutil.copytree(root, d, ignore=copy_ignore(scratch))
        pool.put(d)

    def one(site) -> MutantResult:
        t, idx, line, desc, _ = site
        work = pool.get()
        try:
            f = work / t
            original = (root / t).read_text(encoding="utf-8")
            f.write_text(apply_mutant(original, idx, None), encoding="utf-8")
            try:
                r = subprocess.run(pytest_cmd(s.tests, True), cwd=work, capture_output=True, text=True,
                                   env=env, timeout=s.timeout)
                outcome = "KILLED" if r.returncode != 0 else "SURVIVED"
            except subprocess.TimeoutExpired:
                outcome = "TIMEOUT"
            finally:
                f.write_text(original, encoding="utf-8")
            return MutantResult(t, line, desc, outcome)
        finally:
            pool.put(work)

    with ThreadPoolExecutor(max_workers=jobs) as ex:
        rep.results += list(ex.map(one, chosen))
    return rep


def audit_suite(root: Path, s: Suite) -> list[str]:
    mods = {Path(t).stem for t in s.targets}
    out: list[str] = []
    for t in s.tests:
        out += audit_test_file(root / t, mods)
    return out


def render_markdown(reports: list[SuiteReport], seed: int, max_mutants: int) -> str:
    lines = ["# Meta-test report", "", f"Mutants sampled per suite: up to {max_mutants or 'all'} (seed {seed}). "
             "A survivor is a lead to triage, not a verdict.", ""]
    for r in reports:
        lines += [f"## {r.name}", ""]
        if not r.baseline_ok:
            lines += ["**Baseline RED: nothing else was run.**", ""] + [f"    {x}" for x in r.audit] + [""]
            continue
        for t, (e, n) in r.coverage.items():
            lines.append(f"- `{t}`: {e}/{n} statements executed by the suite ({e / n:.0%})" if n else f"- `{t}`: no statements")
        counts = {k: sum(x.outcome == k for x in r.results) for k in ("KILLED", "TIMEOUT", "SURVIVED", "NOT_EXERCISED")}
        sc = r.score
        lines += [f"- mutation score: {sc:.0%} ({counts['KILLED'] + counts['TIMEOUT']} caught, {counts['SURVIVED']} survived)"
                  if sc is not None else "- mutation score: n/a",
                  f"- mutation sites on lines no test executes: {counts['NOT_EXERCISED']}", ""]
        surv = sorted((x for x in r.results if x.outcome == "SURVIVED"), key=lambda x: (x.target, x.line))
        if surv:
            lines += ["Survivors (a test should have failed):", ""] + [f"- `{x.target}:{x.line}` {x.desc}" for x in surv] + [""]
        if r.audit:
            lines += ["Test audit:", ""] + [f"- {a}" for a in r.audit] + [""]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("run", "audit"):
        p = sub.add_parser(name)
        p.add_argument("--root", type=Path, default=Path("."))
        p.add_argument("--config", type=Path, default=None)
        p.add_argument("--suite", action="append")
        if name == "run":
            p.add_argument("--max-mutants", type=int, default=120)
            p.add_argument("--seed", type=int, default=1)
            p.add_argument("--jobs", type=int, default=min(4, os.cpu_count() or 1))
            p.add_argument("--min-score", type=float, default=0.0)
            p.add_argument("--out", type=Path, default=None)
    t = sub.add_parser("_trace")
    t.add_argument("--out", required=True)
    t.add_argument("--targets", nargs="+", required=True)
    t.add_argument("pytest_args", nargs=argparse.REMAINDER)
    a = ap.parse_args(argv)

    if a.cmd == "_trace":
        args = [x for x in a.pytest_args if x != "--"]
        return trace_run(a.targets, args, a.out)

    root = a.root.resolve()
    config = (a.config or root / "meta-test.toml")
    try:
        suites = [s for s in load_suites(root, config) if not a.suite or s.name in a.suite]
    except (OSError, KeyError, tomllib.TOMLDecodeError) as e:
        print(f"cannot load config: {e}", file=sys.stderr)
        return 2
    if not suites:
        print("no suites selected", file=sys.stderr)
        return 2

    if a.cmd == "audit":
        findings = [f for s in suites for f in audit_suite(root, s)]
        for f in findings:
            print(f"AUDIT {f}")
        print("audit clean" if not findings else f"{len(findings)} audit findings")
        return 1 if findings else 0

    out = (a.out or root / ".meta-test").resolve()
    out.mkdir(parents=True, exist_ok=True)
    reports: list[SuiteReport] = []
    with tempfile.TemporaryDirectory(prefix="meta-test-") as tmp:
        for s in suites:
            print(f"== {s.name}", flush=True)
            r = run_suite(root, s, a.max_mutants, a.seed, a.jobs, Path(tmp))
            if r.baseline_ok:
                r.audit += audit_suite(root, s)
            reports.append(r)
            sc = r.score
            print(f"   baseline {'ok' if r.baseline_ok else 'RED'}; score {'n/a' if sc is None else f'{sc:.0%}'}", flush=True)
    (out / "meta-test-report.md").write_text(render_markdown(reports, a.seed, a.max_mutants), encoding="utf-8")
    (out / "meta-test-report.json").write_text(json.dumps([{
        "suite": r.name, "baseline_ok": r.baseline_ok, "score": r.score, "coverage": r.coverage,
        "audit": r.audit, "results": [x.__dict__ for x in r.results]} for r in reports], indent=2))
    print(f"report: {out / 'meta-test-report.md'}")
    if any(not r.baseline_ok for r in reports):
        return 2
    low = [r for r in reports if r.score is not None and r.score < a.min_score]
    return 1 if low or any(r.audit for r in reports) else 0


if __name__ == "__main__":
    sys.exit(main())
