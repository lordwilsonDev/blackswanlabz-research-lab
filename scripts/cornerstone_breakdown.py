"""Line breakdown of the cornerstone repo at a pinned commit (claim C-002).

Run (streams GitHub's tarball, nothing is written to disk but the JSON):

  gh api repos/lordwilsonDev/GITHUB_AI_PROJECTS_PACKAGE/tarball/b26ccc4a3445ff8ebc1513cf04c4a561b32cbb1b | python scripts/cornerstone_breakdown.py > breakdown.json

Stdlib only. Output should match 01-cornerstone/evidence/line-breakdown.json exactly.
"""
import json, sys, tarfile
from collections import defaultdict
from pathlib import PurePosixPath

VENDOR_DIRS = {"node_modules", "site-packages", ".venv", "venv", "env", "vendor", "dist", "build",
               "__pycache__", ".git", "third_party", "external", ".tox", "target", ".next", "bower_components"}
DATA_EXT = {".json", ".jsonl", ".csv", ".tsv", ".txt", ".log", ".xml", ".ndjson", ".parquet", ".pkl", ".npy"}
LOCKFILES = {"package-lock.json", "yarn.lock", "poetry.lock", "Pipfile.lock", "Cargo.lock", "pnpm-lock.yaml", "uv.lock"}
SOURCE_EXT = {".py", ".sh", ".js", ".ts", ".tsx", ".jsx", ".rs", ".go", ".swift", ".java", ".c", ".h", ".cpp",
              ".hpp", ".rb", ".html", ".css", ".scss", ".sql", ".mk", ".toml", ".cfg", ".ini", ".ejs", ".d", ".hcl", ".tf"}
DOC_EXT = {".md", ".rst", ".adoc"}
CONFIG_EXT = {".yaml", ".yml"}

def classify(path: str) -> str:
    p = PurePosixPath(path)
    parts = set(p.parts[1:-1])  # drop tarball's top-level dir and filename
    if parts & VENDOR_DIRS or any(x.endswith(".egg-info") or x.endswith(".dist-info") for x in parts):
        return "vendored_or_build"
    if p.name in LOCKFILES:
        return "lockfile"
    if p.name.endswith((".min.js", ".min.css", ".map")):
        return "minified"
    ext = p.suffix.lower()
    if p.name in ("Makefile", "Dockerfile") or ext in SOURCE_EXT:
        return "source"
    if ext in DOC_EXT:
        return "docs"
    if ext in CONFIG_EXT:
        return "config"
    if ext in DATA_EXT:
        return "data"
    return "other_text"

def main() -> int:
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:] or sys.stdin.isatty():
        print(__doc__)
        return 0
    lines = defaultdict(int); files = defaultdict(int); by_ext = defaultdict(int)
    binary_files = 0; top = defaultdict(int); dup_names = defaultdict(int)
    with tarfile.open(fileobj=sys.stdin.buffer, mode="r|gz") as tar:
        for m in tar:
            if not m.isfile():
                continue
            data = tar.extractfile(m).read()
            if b"\x00" in data[:8192]:
                binary_files += 1
                continue
            n = data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)
            c = classify(m.name)
            lines[c] += n; files[c] += 1
            if c == "source":
                by_ext[PurePosixPath(m.name).suffix.lower() or PurePosixPath(m.name).name] += n
            parts = PurePosixPath(m.name).parts
            if len(parts) > 2:
                top[parts[1]] += n
    json.dump({"lines": lines, "files": files, "source_lines_by_ext": dict(sorted(by_ext.items(), key=lambda kv: -kv[1])),
               "binary_files_skipped": binary_files, "lines_by_category_folder": dict(sorted(top.items(), key=lambda kv: -kv[1])),
               "total_text_lines": sum(lines.values())}, sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
