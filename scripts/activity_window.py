#!/usr/bin/env python3
"""Commit activity across repos in a date window, de-duplicated by commit hash. Stdlib only; needs git and network.

  python3 scripts/activity_window.py --start 2026-07-05 --end 2026-10-03 \
      --owner "lordwilson,lord wilson" --repos a,b,c --out result.json

Clones each repo bare and blobless (history only) into a temp directory. A commit that appears in several repos
(mirrors, forks of the same history) is counted once. Counts commits, not lines of code or effort.
"""
import argparse, collections, datetime as dt, glob, json, os, subprocess, sys, tempfile


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True); ap.add_argument("--end", required=True)
    ap.add_argument("--owner", required=True, help="comma-separated author names that count as the owner")
    ap.add_argument("--repos", required=True, help="comma-separated repo names")
    ap.add_argument("--github-user", default="lordwilsonDev")
    ap.add_argument("--base-url", default="https://github.com", help="where repos are cloned from (tests use file://)")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    start, end = dt.date.fromisoformat(a.start), dt.date.fromisoformat(a.end)
    owners = {n.strip().lower().replace(" ", "") for n in a.owner.split(",")}
    seen, repos_of, failed = {}, collections.defaultdict(set), []
    with tempfile.TemporaryDirectory() as tmp:
        for repo in [r.strip() for r in a.repos.split(",") if r.strip()]:
            path = os.path.join(tmp, repo + ".git")
            r = subprocess.run(["git", "clone", "-q", "--bare", "--filter=blob:none",
                                f"{a.base_url}/{a.github_user}/{repo}.git", path], capture_output=True, text=True)
            if r.returncode != 0:
                failed.append(repo); continue
            out = subprocess.run(["git", "--git-dir", path, "log", "--all", "--format=%H%x09%ad%x09%an", "--date=short"],
                                 capture_output=True, text=True).stdout.splitlines()
            for line in out:
                h, d, who = line.split("\t", 2)
                repos_of[h].add(repo)
                seen.setdefault(h, (dt.date.fromisoformat(d), who))
    win = {h: v for h, v in seen.items() if start <= v[0] <= end}
    mine = {h: v for h, v in win.items() if v[1].lower().replace(" ", "") in owners}
    days = sorted({v[0] for v in mine.values()})
    per_day = collections.Counter(v[0] for v in mine.values())
    per_repo = collections.Counter(next(iter(sorted(repos_of[h]))) for h in mine)
    result = {
        "window": [a.start, a.end], "repos_requested": len(a.repos.split(",")), "repos_failed": failed,
        "repos_with_commits_in_window": len({r for h in win for r in repos_of[h]}),
        "unique_commits": len(win), "owner_commits": len(mine),
        "authors": dict(collections.Counter(v[1] for v in win.values()).most_common(8)),
        "commits_present_in_more_than_one_repo": sum(1 for h in win if len(repos_of[h]) > 1),
        "owner_active_days": len(days),
        "owner_longest_gap_days": max(((y - x).days for x, y in zip(days, days[1:])), default=0),
        "owner_busiest_days": [[d.isoformat(), n] for d, n in per_day.most_common(5)],
        "owner_commits_by_week": {f"wk{w}": sum(1 for v in mine.values() if (v[0] - start).days // 7 == w) for w in range(13)},
    }
    text = json.dumps(result, indent=1)
    if a.out:
        open(a.out, "w").write(text + "\n")
    print(text)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
