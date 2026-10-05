#!/usr/bin/env python3
"""lab_rubric: pre-registered, compute-matched, blind-judged comparison of generation methods. Standard library only.

For claims that cannot be checked by running code (for example "this method produces more novel hypotheses"), the standard is
a rubric fixed in advance and applied blind by a judge that is not the generator. This is a weaker standard than an executable
oracle and every report says so.

  lab_rubric.py lock DIR                 validate prereg.json, hash prereg.json + questions.json + prompts.json into LOCK.json
  lab_rubric.py run DIR --adapter CMD    generate every arm, compute-match best-of-n baselines, write gen.jsonl and plan.json
  lab_rubric.py blind DIR                shuffle final texts into blind_items.json (+ .csv for human raters) and a private key
  lab_rubric.py judge DIR --adapter CMD --judge-id J1     rate every blind item on the registered rubric
  lab_rubric.py import-ratings DIR FILE.csv --judge-id H1  import human ratings from the exported csv
  lab_rubric.py analyze DIR              registered decision: paired sign-flip test, Holm, Hedges g, TOST, Krippendorff alpha
  lab_rubric.py report DIR               REPORT.md, decision first
  lab_rubric.py controls [--sims N]      validate the analysis on synthetic null and planted-effect data (no model needed)

Adapter protocol: the command receives the prompt on stdin and prints the reply; it may print `TOKENS_IN=a TOKENS_OUT=b` as the
last line of stderr; HARNESS_SEED is set. Built-in adapters `fakegen` and `fakejudge:effect=1:noise=1` test the plumbing only and
mark results NOT EVIDENCE.
"""
from __future__ import annotations

import argparse, csv, datetime, hashlib, itertools, json, math, os, random, re, shlex, statistics, subprocess, sys, time, zlib
from pathlib import Path

VERSION = "lab-rubric-0.2"
FILES = ("prereg.json", "questions.json", "prompts.json")
REQUIRED = ("question", "standard_level", "hypothesis", "arms", "bon_of", "comparison", "reps", "max_words", "judges",
            "primary", "coherence_margin", "min_alpha", "falsification", "limits", "stopping_rule", "instrument_version")


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p: Path):
    return json.loads(p.read_text())


def seed_for(*parts) -> int:
    return zlib.crc32("|".join(str(x) for x in parts).encode()) % 2_000_000_000


# ---------- registration ----------
def validate(p: dict, qs: list, prompts: dict) -> list[str]:
    errs = [f"missing or empty field: {k}" for k in REQUIRED if p.get(k) in (None, "", [], {})]
    if p.get("standard_level") != "rubric_other_model":
        errs.append("standard_level must be 'rubric_other_model' for this engine")
    ids = [a.get("id") for a in p.get("arms", [])]
    for b in p.get("bon_of", []):
        if b not in ids:
            errs.append(f"bon_of names unknown arm {b}")
    cmp_ = p.get("comparison", {})
    if cmp_.get("treatment") not in ids:
        errs.append("comparison.treatment must be a registered arm id")
    for c in cmp_.get("controls", []):
        if c.removesuffix("-bon") not in ids:
            errs.append(f"comparison control {c} does not correspond to an arm")
    if len(p.get("judges", [])) < 1:
        errs.append("at least one judge must be registered")
    if len(qs) < 8:
        errs.append("fewer than 8 questions: a result would be an anecdote")
    need = {"selector", "judge"}
    builtin = {"fewshot": {"fewshot"}, "cot": {"cot"}, "tot": {"tot_branch", "tot_evaluate", "tot_final"},
               "ail_moie": {f"moie_{i}" for i in range(1, 6)}}
    for arm in p.get("arms", []):
        kind = arm.get("kind")
        if kind in builtin:
            need |= builtin[kind]
        elif kind == "prompt" and arm.get("prompt"):
            need.add(arm["prompt"])
        elif kind == "chain" and arm.get("stages"):
            need |= set(arm["stages"])
        else:
            errs.append(f"arm {arm.get('id')}: unknown kind or missing prompt/stages (kinds: {sorted(builtin) + ['prompt', 'chain']})")
    for k in sorted(need):
        if k not in prompts:
            errs.append(f"prompts.json missing '{k}'")
    return errs


def lock_errors(d: Path) -> list[str]:
    lk = d / "LOCK.json"
    if not lk.exists():
        return ["not locked: run `lock` first"]
    rec = load(lk)["files"]
    return [f"{n} changed after lock (goalposts moved)" for n in FILES if sha(d / n) != rec.get(n)]


def cmd_lock(a):
    d = Path(a.dir)
    if (d / "LOCK.json").exists():
        sys.exit("already locked. Create a new experiment directory to change the standard; do not edit a locked one.")
    errs = validate(load(d / "prereg.json"), load(d / "questions.json"), load(d / "prompts.json"))
    if errs:
        sys.exit("PRE-REGISTRATION INCOMPLETE:\n  " + "\n  ".join(errs))
    r = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    rec = {"locked_at": now(), "git_commit": r.stdout.strip() if r.returncode == 0 else "no-git", "instrument": VERSION,
           "files": {n: sha(d / n) for n in FILES}}
    (d / "LOCK.json").write_text(json.dumps(rec, indent=1) + "\n")
    print("LOCKED", json.dumps(rec["files"]))


# ---------- adapters ----------
def est_tokens(s: str) -> int:
    return max(1, len(s) // 4)


def call(adapter: str, prompt: str, seed: int):
    t0 = time.time()
    if adapter == "fakegen":
        word = "NOVELMARK " if "Prediction Generator" in prompt else ""
        out = (f"Reasoning text {seed % 97}. " * 6) + f"\nFINAL HYPOTHESIS: {word}the effect arises from mechanism {seed % 13} and would be falsified if measure {seed % 7} stays flat."
        return out, est_tokens(prompt), est_tokens(out), time.time() - t0
    if adapter.startswith("fakejudge"):
        kv = dict(x.split("=") for x in adapter.split(":")[1:])
        rnd = random.Random(zlib.crc32(prompt.encode()))
        nov = 3.0 + float(kv.get("effect", 0)) * ("NOVELMARK" in prompt) + rnd.gauss(0, float(kv.get("noise", 1)))
        coh = 4.0 + rnd.gauss(0, float(kv.get("noise", 1)))
        clamp = lambda x: max(1, min(7, round(x)))
        return json.dumps({"novelty": clamp(nov), "coherence": clamp(coh)}), est_tokens(prompt), 8, time.time() - t0
    r = subprocess.run(shlex.split(adapter), input=prompt, capture_output=True, text=True, timeout=1800,
                       env={**os.environ, "HARNESS_SEED": str(seed)})
    if r.returncode != 0:
        raise SystemExit(f"adapter failed ({r.returncode}): {r.stderr[-300:]}")
    ti = re.search(r"TOKENS_IN=(\d+)", r.stderr)
    to = re.search(r"TOKENS_OUT=(\d+)\s*$", r.stderr)
    return r.stdout, int(ti.group(1)) if ti else est_tokens(prompt), int(to.group(1)) if to else est_tokens(r.stdout), time.time() - t0


# ---------- generation arms ----------
def fmt(tpl: str, **kw) -> str:
    return tpl.format(**{k: v for k, v in kw.items()})


def extract_final(text: str, max_words: int):
    m = re.search(r"FINAL HYPOTHESIS:?\s*(.*)", text, re.S | re.I)
    body, ok = (m.group(1).strip(), True) if m else (text.strip().split("\n\n")[-1].strip(), False)
    words = body.split()
    truncated = len(words) > max_words
    return " ".join(words[:max_words]), ok, truncated


def run_pipeline(arm: dict, q: dict, prompts: dict, adapter: str, tag: str, mw: int):
    """Returns (final_text, calls). calls = list of (tin, tout, seconds). arm is the registered arm dict."""
    kind = arm["kind"]
    calls, ctx = [], {"q": q["text"], "mw": mw}

    def step(tpl_key, i=0, **extra):
        prompt = fmt(prompts[tpl_key], **ctx, **extra)
        out, ti, to, sec = call(adapter, prompt, seed_for(tag, kind, tpl_key, i))
        calls.append((ti, to, sec))
        return out

    def chain(keys):
        prev, out = "", ""
        for i, key in enumerate(keys, 1):
            out = step(key, prev=prev)
            prev = (prev + f"\n\n--- Stage {i} output ---\n" + out).strip()
        return out

    if kind == "fewshot":
        out = step("fewshot")
    elif kind == "cot":
        out = step("cot")
    elif kind == "tot":
        branches = step("tot_branch")
        evaluation = step("tot_evaluate", branches=branches)
        out = step("tot_final", branches=branches, evaluation=evaluation)
    elif kind == "ail_moie":
        out = chain([f"moie_{i}" for i in range(1, 6)])
    elif kind == "prompt":
        out = step(arm["prompt"])
    elif kind == "chain":
        out = chain(arm["stages"])
    else:
        raise SystemExit(f"unknown arm kind {kind}")
    return out, calls


def total(calls):
    return sum(c[0] + c[1] for c in calls)


def candidate_labels(n: int) -> list[str]:
    """A, B, ... Z, AA, AB, ...: enough labels for any number of candidates (the first version stopped at 26)."""
    import string
    out, letters = [], string.ascii_uppercase
    for i in range(n):
        k, label = i, ""
        while True:
            label = letters[k % 26] + label
            k = k // 26 - 1
            if k < 0:
                break
        out.append(label)
    return out


def parse_choice(reply: str, labels: list[str]) -> int:
    """Index of the first whole-word label found in the reply; 0 if none (recorded as the first candidate)."""
    pos = {lab: i for i, lab in enumerate(labels)}
    for m in re.finditer(r"\b([A-Z]{1,2})\b", reply.strip().upper()):
        if m.group(1) in pos:
            return pos[m.group(1)]
    return 0


def cmd_run(a):
    d = Path(a.dir)
    errs = lock_errors(d)
    exists = (d / "gen.jsonl").exists()
    if exists and not a.resume:
        errs.append("gen.jsonl already exists: runs are registered once; use --resume to continue an interrupted run, or move it aside and note why")
    if a.resume and not exists:
        errs.append("--resume given but there is no gen.jsonl to resume")
    if errs:
        sys.exit("REFUSING TO RUN:\n  " + "\n  ".join(errs))
    p, qs, prompts = load(d / "prereg.json"), load(d / "questions.json"), load(d / "prompts.json")
    mw, reps = p["max_words"], p["reps"]
    arms_by_id = {x["id"]: x for x in p["arms"]}
    if a.resume:
        meta = load(d / "RUN.json")
        if meta["adapter"] != a.adapter:
            sys.exit("REFUSING TO RESUME: the adapter differs from the original run's; outputs from two different models must not be mixed")
        meta.setdefault("resumes", []).append(now())
        if getattr(a, "max_n", 0):
            meta["deviation"] = {"max_n": a.max_n, "reason": getattr(a, "deviation_reason", ""), "declared": now(), "note": "declared before any baseline output existed; outcome-independent"}
        rows = [json.loads(l) for l in (d / "gen.jsonl").read_text().splitlines() if l.strip()]
    else:
        meta = {"adapter": a.adapter, "note": a.note, "started": now(), "instrument": VERSION, "evidence": a.adapter != "fakegen"}
        if getattr(a, "max_n", 0):
            meta["deviation"] = {"max_n": a.max_n, "reason": getattr(a, "deviation_reason", ""), "declared": now(), "note": "declared before any baseline output existed; outcome-independent"}
        rows = []
    done = {(r["q"], r["rep"], r["arm"]) for r in rows}
    (d / "RUN.json").write_text(json.dumps(meta, indent=1) + "\n")

    def emit(row, f):
        rows.append(row)
        f.write(json.dumps(row) + "\n"); f.flush()

    with open(d / "gen.jsonl", "a" if a.resume else "w") as f:
        for q in qs:  # phase A: every registered arm, single pass
            for rep in range(reps):
                for arm in p["arms"]:
                    if (q["id"], rep, arm["id"]) in done:
                        continue
                    text, calls = run_pipeline(arm, q, prompts, a.adapter, f"{q['id']}|{rep}", mw)
                    final, ok, trunc = extract_final(text, mw)
                    emit({"q": q["id"], "rep": rep, "arm": arm["id"], "final": final, "extracted": ok, "truncated": trunc,
                          "tokens": total(calls), "calls": len(calls), "seconds": round(sum(c[2] for c in calls), 2)}, f)
            print("generated", q["id"], flush=True)
        plan = {}  # phase B: compute matching, from the single-pass rows
        treat = p["comparison"]["treatment"]
        single = [r for r in rows if not r["arm"].endswith("-bon")]
        for q in qs:
            B = statistics.fmean(r["tokens"] for r in single if r["q"] == q["id"] and r["arm"] == treat)
            qtok = est_tokens(q["text"])
            for base in p["bon_of"]:
                mine = [r for r in single if r["q"] == q["id"] and r["arm"] == base]
                s_ = statistics.fmean(r["tokens"] for r in mine)
                h = statistics.fmean(est_tokens(r["final"]) for r in mine)
                n_full = max(1, math.floor((B - qtok - 40) / (s_ + h)))
                n = min(n_full, a.max_n) if getattr(a, "max_n", 0) else n_full
                plan[f"{q['id']}|{base}"] = {"budget": round(B), "single_pass_tokens": round(s_), "final_tokens": round(h), "n": n, "n_uncapped": n_full}
        (d / "plan.json").write_text(json.dumps(plan, indent=1) + "\n")
        for q in qs:  # phase C: best-of-n baselines, selector charged to the baseline's own budget
            for rep in range(reps):
                for base in p["bon_of"]:
                    if (q["id"], rep, base + "-bon") in done:
                        continue
                    n = plan[f"{q['id']}|{base}"]["n"]
                    cands, calls = [], []
                    for j in range(n):
                        text, c = run_pipeline(arms_by_id[base], q, prompts, a.adapter, f"{q['id']}|{rep}|bon{j}", mw)
                        cands.append(extract_final(text, mw)[0]); calls += c
                    labels = candidate_labels(len(cands))
                    listing = "\n\n".join(f"({labels[i]}) {t}" for i, t in enumerate(cands))
                    pick, ti, to, sec = call(a.adapter, fmt(prompts["selector"], q=q["text"], candidates=listing),
                                             seed_for(q["id"], rep, base, "sel"))
                    calls.append((ti, to, sec))
                    idx = parse_choice(pick, labels)
                    emit({"q": q["id"], "rep": rep, "arm": base + "-bon", "final": cands[idx], "extracted": True, "truncated": False,
                          "tokens": total(calls), "calls": len(calls), "n": n, "seconds": round(sum(c[2] for c in calls), 2)}, f)
            print("bon", q["id"], flush=True)
    meta["finished"] = now()
    (d / "RUN.json").write_text(json.dumps(meta, indent=1) + "\n")
    print("GENERATION COMPLETE: next, `blind`, then `judge` with a judge that is not the generator")


# ---------- blinding and judging ----------
def cmd_blind(a):
    d = Path(a.dir)
    rows = [json.loads(l) for l in (d / "gen.jsonl").read_text().splitlines() if l.strip()]
    qtext = {q["id"]: q["text"] for q in load(d / "questions.json")}
    rnd = random.Random(sha(d / "LOCK.json"))  # reproducible from the lock
    order = list(range(len(rows)))
    rnd.shuffle(order)
    items, key = [], {}
    for n, i in enumerate(order):
        iid = f"item-{n:04d}"
        r = rows[i]
        items.append({"item_id": iid, "question": qtext[r["q"]], "hypothesis": r["final"]})
        key[iid] = {"q": r["q"], "rep": r["rep"], "arm": r["arm"]}
    (d / "blind_items.json").write_text(json.dumps(items, indent=1) + "\n")
    (d / "blind_key.json").write_text(json.dumps(key, indent=1) + "\n")
    with open(d / "blind_items.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["item_id", "question", "hypothesis", "novelty_1to7", "coherence_1to7"])
        for it in items:
            w.writerow([it["item_id"], it["question"], it["hypothesis"], "", ""])
    print(f"blinded {len(items)} items; judges must never see blind_key.json")


def parse_rating(text: str):
    m = re.search(r"\{.*?\}", text, re.S)
    if not m:
        return None
    try:
        j = json.loads(m.group(0))
        n, c = float(j["novelty"]), float(j["coherence"])
        return (n, c) if 1 <= n <= 7 and 1 <= c <= 7 else None
    except (ValueError, KeyError, TypeError):
        return None


def cmd_judge(a):
    d = Path(a.dir)
    p, prompts = load(d / "prereg.json"), load(d / "prompts.json")
    items = load(d / "blind_items.json")
    out = d / "ratings.jsonl"
    done = {(json.loads(l)["judge"], json.loads(l)["item_id"]) for l in out.read_text().splitlines() if l.strip()} if out.exists() else set()
    gen_adapter = load(d / "RUN.json")["adapter"]
    with open(out, "a") as f:
        for it in items:
            if (a.judge_id, it["item_id"]) in done:
                continue
            rating = None
            for attempt in range(3):
                txt, *_ = call(a.adapter, fmt(prompts["judge"], q=it["question"], h=it["hypothesis"]), seed_for(a.judge_id, it["item_id"], attempt))
                rating = parse_rating(txt)
                if rating:
                    break
            row = {"judge": a.judge_id, "item_id": it["item_id"], "novelty": rating[0] if rating else None,
                   "coherence": rating[1] if rating else None, "judge_adapter": a.adapter,
                   "same_as_generator": a.adapter == gen_adapter}
            f.write(json.dumps(row) + "\n"); f.flush()
    print(f"judge {a.judge_id} done")


def cmd_import(a):
    d = Path(a.dir)
    with open(a.file, newline="") as fh, open(d / "ratings.jsonl", "a") as out:
        for r in csv.DictReader(fh):
            try:
                n, c = float(r["novelty_1to7"]), float(r["coherence_1to7"])
            except (ValueError, KeyError):
                continue
            out.write(json.dumps({"judge": a.judge_id, "item_id": r["item_id"], "novelty": n, "coherence": c,
                                  "judge_adapter": "human", "same_as_generator": False}) + "\n")
    print("imported")


# ---------- statistics ----------
def signflip_p(diffs: list[float], rng: random.Random, mc: int = 200_000) -> float:
    """One-sided paired sign-flip permutation test that mean(diffs) > 0."""
    obs = sum(diffs)
    n = len(diffs)
    eps = 1e-12
    if n <= 16:
        ge = tot = 0
        for signs in itertools.product((1, -1), repeat=n):
            tot += 1
            ge += sum(s * x for s, x in zip(signs, diffs)) >= obs - eps
        return ge / tot
    ge = sum(sum(rng.choice((1, -1)) * x for x in diffs) >= obs - eps for _ in range(mc))
    return (ge + 1) / (mc + 1)


def holm(ps: list[float]) -> list[float]:
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i])
    adj, run = [0.0] * m, 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (m - rank) * ps[i]))
        adj[i] = run
    return adj


def hedges_g(diffs: list[float]) -> float:
    n = len(diffs)
    if n < 2:
        return 0.0
    sd = statistics.stdev(diffs)
    mean = statistics.fmean(diffs)
    if sd == 0:
        return 999.0 if mean > 0 else 0.0
    return (mean / sd) * (1 - 3 / (4 * (n - 1) - 1))


def krippendorff_alpha(units: list[list[float]]) -> float | None:
    """Interval-metric alpha. units = list of lists of ratings (one list per item, one value per rater who rated it)."""
    units = [u for u in units if len(u) >= 2]
    n = sum(len(u) for u in units)
    if n < 2:
        return None
    do = sum(sum((x - y) ** 2 for i, x in enumerate(u) for j, y in enumerate(u) if i != j) / (len(u) - 1) for u in units) / n
    vals = [x for u in units for x in u]
    s1, s2 = sum(vals), sum(v * v for v in vals)
    de = (2 * n * s2 - 2 * s1 * s1) / (n * (n - 1))
    return None if de == 0 else 1 - do / de


def boot_ci(diffs: list[float], rnd: random.Random, level: float, n: int = 5000):
    means = sorted(statistics.fmean(rnd.choice(diffs) for _ in diffs) for _ in range(n))
    lo, hi = (1 - level) / 2, (1 + level) / 2
    return means[int(lo * n)], means[int(hi * n) - 1]


def decide(scores: dict, p: dict, rnd: random.Random):
    """scores[arm][question] -> (novelty, coherence). Returns decision dict. Pure function of the ratings."""
    treat = p["comparison"]["treatment"]
    controls = p["comparison"]["controls"]
    qs = sorted(scores[treat])
    contrasts, raw = {}, []
    for c in controls:
        dn = [scores[treat][q][0] - scores[c][q][0] for q in qs]
        dc = [scores[treat][q][1] - scores[c][q][1] for q in qs]
        pv = signflip_p(dn, rnd)
        lo, hi = boot_ci(dc, rnd, 0.90)
        contrasts[c] = {"mean_novelty_diff": round(statistics.fmean(dn), 4), "p_raw": pv, "hedges_g": round(hedges_g(dn), 4),
                        "coherence_diff": round(statistics.fmean(dc), 4), "coherence_ci90": [round(lo, 4), round(hi, 4)],
                        "coherence_noninferior": lo > -p["coherence_margin"]}
        raw.append(pv)
    for c, adj in zip(controls, holm(raw)):
        contrasts[c]["p_holm"] = adj
    pr = p["primary"]
    ok = all(v["p_holm"] < pr["alpha"] and v["hedges_g"] > pr["min_g"] for v in contrasts.values())
    return {"contrasts": contrasts, "h1c_supported": ok, "n_questions": len(qs)}


def build_scores(d: Path, judged_by: set | None = None):
    key = load(d / "blind_key.json")
    ratings = [json.loads(l) for l in (d / "ratings.jsonl").read_text().splitlines() if l.strip()]
    ratings = [r for r in ratings if r["novelty"] is not None and (judged_by is None or r["judge"] in judged_by)]
    per_item = {}
    for r in ratings:
        per_item.setdefault(r["item_id"], []).append((r["novelty"], r["coherence"]))
    cell = {}
    for iid, vals in per_item.items():
        k = key[iid]
        cell.setdefault((k["arm"], k["q"]), []).append((statistics.fmean(v[0] for v in vals), statistics.fmean(v[1] for v in vals)))
    scores = {}
    for (arm, q), v in cell.items():
        scores.setdefault(arm, {})[q] = (statistics.fmean(x[0] for x in v), statistics.fmean(x[1] for x in v))
    return scores, ratings, per_item


def cmd_analyze(a):
    d = Path(a.dir)
    p = load(d / "prereg.json")
    meta = load(d / "RUN.json")
    scores, ratings, per_item = build_scores(d)
    arms_needed = [p["comparison"]["treatment"]] + p["comparison"]["controls"]
    qs_needed = {q["id"] for q in load(d / "questions.json")}
    missing = [(a_, q_) for a_ in arms_needed for q_ in sorted(qs_needed) if q_ not in scores.get(a_, {})]
    if missing:
        sys.exit(f"INCOMPLETE RATINGS: {len(missing)} arm/question cells have no rating (first: {missing[0]}); finish judging before analyzing")
    rnd = random.Random(12345)
    res = decide(scores, p, rnd)
    key = load(d / "blind_key.json")
    judges = sorted({r["judge"] for r in ratings})
    by_item_judge = {}
    for r in ratings:
        by_item_judge.setdefault(r["item_id"], {})[r["judge"]] = r["novelty"]
    alpha = krippendorff_alpha([list(v.values()) for v in by_item_judge.values()]) if len(judges) >= 2 else None
    gen = [json.loads(l) for l in (d / "gen.jsonl").read_text().splitlines() if l.strip()]
    arms = sorted({g["arm"] for g in gen})
    desc = {arm: {"tokens": round(statistics.fmean(g["tokens"] for g in gen if g["arm"] == arm)),
                  "words": round(statistics.fmean(len(g["final"].split()) for g in gen if g["arm"] == arm), 1),
                  "extraction_failures": sum(not g["extracted"] for g in gen if g["arm"] == arm)} for arm in arms}
    ratio = {c: round(desc[c]["tokens"] / desc[p["comparison"]["treatment"]]["tokens"], 3) for c in p["comparison"]["controls"]}
    flags = []
    if not meta["evidence"]:
        flags.append("FAKE GENERATOR: harness test, NOT EVIDENCE")
    if any(r["same_as_generator"] for r in ratings):
        flags.append("JUDGE NOT INDEPENDENT: a judge used the same adapter as the generator (self-preference risk)")
    if len(judges) < 2:
        flags.append("ONE JUDGE: inter-rater reliability cannot be computed")
    if meta.get("deviation"):
        flags.append(f"DEVIATION: best-of-n capped at {meta['deviation']['max_n']} samples ({meta['deviation']['reason']}); baselines get less compute than registered, which favours the treatment")
    if any(not (0.85 <= v <= 1.15) for v in ratio.values()):
        flags.append("COMPUTE MATCH OUTSIDE 0.85-1.15 of the treatment's budget")
    t_words = desc[p["comparison"]["treatment"]]["words"]
    if any(abs(desc[c]["words"] - t_words) / max(t_words, 1) > 0.3 for c in p["comparison"]["controls"]):
        flags.append("LENGTH DIFFERS MORE THAN 30 PERCENT between treatment and a control")
    if alpha is not None and alpha < p["min_alpha"]:
        decision = "INCONCLUSIVE (judge reliability below the registered minimum)"
    else:
        decision = "SUPPORTED" if res["h1c_supported"] else "NOT SUPPORTED"
    if not meta["evidence"]:
        decision = "n/a (fake generator)"
    out = {"decision": decision, "flags": flags, "alpha_novelty": None if alpha is None else round(alpha, 3), "judges": judges,
           "n_ratings": len(ratings), "arms": desc, "cost_ratio_vs_treatment": ratio, **res, "run": meta}
    (d / "ANALYSIS.json").write_text(json.dumps(out, indent=1) + "\n")
    for fl in flags:
        print("***", fl, "***")
    print(f"{'arm':10}{'tokens':>8}{'words':>7}{'noextract':>10}")
    for arm, m in desc.items():
        print(f"{arm:10}{m['tokens']:8d}{m['words']:7.0f}{m['extraction_failures']:10d}")
    print(f"\nalpha(novelty) = {out['alpha_novelty']}  judges = {judges}")
    for c, v in res["contrasts"].items():
        print(f"{p['comparison']['treatment']} vs {c}: dNovelty {v['mean_novelty_diff']:+.3f}  g {v['hedges_g']:+.2f}  p_holm {v['p_holm']:.4f}  coherence non-inferior {v['coherence_noninferior']}")
    print("REGISTERED DECISION (H1c):", decision)


def cmd_report(a):
    d = Path(a.dir)
    p, r = load(d / "prereg.json"), load(d / "ANALYSIS.json")
    banner = "\n".join(f"**{x}**\n" for x in r["flags"])
    rows = "\n".join(f"| {k} | {v['tokens']} | {v['words']} | {v['extraction_failures']} |" for k, v in r["arms"].items())
    con = "\n".join(f"| {c} | {v['mean_novelty_diff']:+.3f} | {v['hedges_g']:+.2f} | {v['p_holm']:.4f} | {v['coherence_diff']:+.3f} | {v['coherence_noninferior']} |"
                    for c, v in r["contrasts"].items())
    text = f"""# {d.name}: report

{banner}
**Registered decision (H1c): {r['decision']}.** Standard level: rubric applied blind by a judge, which is weaker than an executable check.

## Question and falsification (fixed before the run)

{p['question']}

Falsification: {p['falsification']}

## Contrasts: {p['comparison']['treatment']} against each compute-matched control, {r['n_questions']} questions

| control | novelty difference | Hedges g | Holm p | coherence difference | coherence non-inferior |
|---|---|---|---|---|---|
{con}

Judges: {', '.join(r['judges'])}; Krippendorff alpha (novelty) {r['alpha_novelty']}; ratings {r['n_ratings']}.

## Compute and length per arm

| arm | mean tokens | mean words | extraction failures |
|---|---|---|---|
{rows}

Control cost as a fraction of the treatment's: {r['cost_ratio_vs_treatment']}.

## Limits, as registered

""" + "\n".join(f"- {x}" for x in p["limits"]) + f"""

## Suggested ledger row (add to CLAIMS.md only after checking this report)

`| C-??? | {p['hypothesis']} Result under the registered rule: {r['decision']} | {d.as_posix()}/REPORT.md | re-run the commands in the run sheet with the same adapters | pending | {datetime.date.today()} |`

Status stays **pending** until someone other than the run's author has re-run it.
"""
    (d / "REPORT.md").write_text(text)
    print("wrote", d / "REPORT.md")


# ---------- analysis controls ----------
def cmd_controls(a):
    """Validate decide() on synthetic data: null (no effect) must rarely pass; a planted effect must usually pass."""
    p = {"comparison": {"treatment": "T", "controls": ["A", "B", "C"]}, "coherence_margin": 0.5,
         "primary": {"alpha": 0.05, "min_g": 0.5}}
    nq = a.questions

    def sim(effect, rnd):
        scores = {arm: {q: (rnd.gauss(4 + (effect if arm == "T" else 0), 1.0), rnd.gauss(4, 1.0)) for q in range(nq)} for arm in "TABC"}
        return decide(scores, p, rnd)

    res = {}
    for name, eff in (("null", 0.0), ("planted_effect_1.0", 1.0), ("planted_effect_2.0", 2.0)):
        rnd = random.Random(zlib.crc32(name.encode()))
        wins = sum(sim(eff, rnd)["h1c_supported"] for _ in range(a.sims))
        res[name] = {"effect_in_rating_points": eff, "sims": a.sims, "questions": nq, "supported": wins, "rate": round(wins / a.sims, 4)}
        print(f"{name:20} supported {wins}/{a.sims} = {wins / a.sims:.3f}")
    # alpha sanity: perfect agreement -> 1, independent noise -> near 0
    rnd = random.Random(7)
    perfect = krippendorff_alpha([[v, v] for v in [rnd.randint(1, 7) for _ in range(200)]])
    noise = krippendorff_alpha([[rnd.randint(1, 7), rnd.randint(1, 7)] for _ in range(2000)])
    res["alpha_perfect"], res["alpha_independent"] = round(perfect, 3), round(noise, 3)
    print(f"alpha perfect agreement {perfect:.3f}; independent ratings {noise:.3f}")
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1) + "\n")
    ok = res["null"]["rate"] <= 0.05 and res["planted_effect_2.0"]["rate"] >= 0.8 and perfect > 0.99 and abs(noise) < 0.1
    print("CONTROLS", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n, f in (("lock", cmd_lock), ("blind", cmd_blind), ("analyze", cmd_analyze), ("report", cmd_report)):
        s = sub.add_parser(n); s.add_argument("dir"); s.set_defaults(f=f)
    s = sub.add_parser("run"); s.add_argument("dir"); s.add_argument("--adapter", required=True); s.add_argument("--note", default=""); s.add_argument("--resume", action="store_true", help="continue an interrupted run with the same adapter, keeping finished outputs"); s.add_argument("--max-n", type=int, default=0, help="cap best-of-n samples per baseline (a declared deviation from compute matching; recorded in RUN.json and flagged in the report)"); s.add_argument("--deviation-reason", default=""); s.set_defaults(f=cmd_run)
    s = sub.add_parser("judge"); s.add_argument("dir"); s.add_argument("--adapter", required=True); s.add_argument("--judge-id", required=True); s.set_defaults(f=cmd_judge)
    s = sub.add_parser("import-ratings"); s.add_argument("dir"); s.add_argument("file"); s.add_argument("--judge-id", required=True); s.set_defaults(f=cmd_import)
    s = sub.add_parser("controls"); s.add_argument("--sims", type=int, default=300); s.add_argument("--questions", type=int, default=12); s.add_argument("--out"); s.set_defaults(f=cmd_controls)
    args = ap.parse_args(argv)
    return args.f(args) or 0


if __name__ == "__main__":
    sys.exit(main())
