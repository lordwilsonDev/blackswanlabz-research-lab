import json
import subprocess
from datetime import date
from pathlib import Path

import pytest

import memory_validator as mv

TODAY = date(2026, 10, 3)
GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@t"]


class Ws:
    """A throwaway workspace: git repo, one committed source file, ledger, notes."""

    def __init__(self, root: Path):
        self.root = root
        for d in ("03_COMPLETED", "42_PERMANENT_MEMORY", "state"):
            (root / d).mkdir()
        (root / "src.txt").write_text("evidence\n")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run([*GIT, "commit", "-qm", "init"], cwd=root, check=True)
        self.commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        self.ids: list[str] = []

    def ledger(self, *ids):
        self.ids += [i for i in ids if i not in self.ids]
        (self.root / "state" / "ids.lock").write_text("\n".join(self.ids) + "\n")

    def completed(self, cid, disposition="KEEP_COMPLETED", extra="", body="Body text.", **d):
        self.ledger(cid)
        fields = {"decided_at": "2026-10-03", "decided_by": "alice", **d}
        disp = "\n".join(f"  {k}: {v}" for k, v in fields.items())
        text = (f"---\nid: {cid}\nstatus: COMPLETED\ndisposition:\n  value: {disposition}\n{disp}\n"
                f"sources:\n  - path: src.txt\n    commit: {self.commit}\n"
                f"    content_hash: {mv.file_hash(self.root / 'src.txt')}\n{extra}---\n{body}\n")
        (self.root / "03_COMPLETED" / f"{cid}.md").write_text(text)

    def memory(self, mid, sources=("CAND-2026-10-03-001",), status="ACTIVE", extra="", **over):
        self.ledger(mid)
        f = {"last_verified": "2026-10-03", "verify_by": "2026-11-03", "verify_interval_days": 31, **over}
        src = ""
        for cid in sources:
            body = (self.root / "03_COMPLETED" / f"{cid}.md").read_text().split("---\n", 2)[2]
            src += f"  - id: {cid}\n    commit: {self.commit}\n    content_hash: {mv.body_hash(body)}\n"
        text = (f"---\nid: {mid}\nstatus: {status}\ncategory: workflow\ncreated_at: 2026-10-03\n"
                f"last_verified: {f['last_verified']}\nverify_by: {f['verify_by']}\n"
                f"verify_interval_days: {f['verify_interval_days']}\nowner: alice\nsources:\n{src}{extra}---\nMemory.\n")
        (self.root / "42_PERMANENT_MEMORY" / f"{mid}.md").write_text(text)

    def finish(self):
        self.ledger()
        (self.root / "CHANGELOG.md").write_text("# Changelog\n\n## 2026-10-03\n- init\n")
        rep, _ = mv.validate(self.root, TODAY)
        (self.root / "42_PERMANENT_MEMORY" / "INDEX.md").write_text(mv.render_index(rep))
        (self.root / "STATS.md").write_text(mv.render_stats(rep, "t"))

    def run(self):
        _, result = mv.validate(self.root, TODAY)
        return result

    def codes(self):
        return {f["code"] for f in self.run()["failures"]}


@pytest.fixture
def ws(tmp_path):
    return Ws(tmp_path)


C1, C2 = "CAND-2026-10-03-001", "CAND-2026-10-03-002"


def test_empty_corpus_passes(ws):
    ws.finish()
    assert ws.run()["exit_code"] == 0


def test_keep_completed_and_promote_pass(ws):
    ws.completed(C1, "PROMOTE")
    ws.completed(C2, "KEEP_COMPLETED")
    ws.memory("MEM-0001")
    ws.finish()
    r = ws.run()
    assert r["exit_code"] == 0, r["failures"]
    assert r["counts"]["dispositions"]["PROMOTE"] == 1


def test_missing_ledger_is_id_failure(ws):
    ws.completed(C1)
    ws.finish()
    (ws.root / "state" / "ids.lock").unlink()
    assert 2 in ws.codes()


def test_unallocated_and_duplicate_ids(ws):
    ws.completed(C1)
    (ws.root / "03_COMPLETED" / "copy.md").write_text((ws.root / "03_COMPLETED" / f"{C1}.md").read_text())
    ws.finish()
    assert any("duplicate id" in f["message"] for f in ws.run()["failures"])
    (ws.root / "state" / "ids.lock").write_text("\n")
    assert 2 in ws.codes()


def test_unknown_and_missing_disposition(ws):
    ws.completed(C1, "MAYBE")
    ws.finish()
    assert 3 in ws.codes()
    (ws.root / "03_COMPLETED" / f"{C1}.md").write_text(
        f"---\nid: {C1}\nstatus: COMPLETED\nsources:\n  - path: a\n    commit: b\n    content_hash: c\n---\nx\n")
    assert 3 in ws.codes()


def test_promote_without_memory_is_failure(ws):
    ws.completed(C1, "PROMOTE")
    ws.finish()
    assert 3 in ws.codes()


def test_silent_promotion(ws):
    ws.completed(C1, "KEEP_COMPLETED")
    ws.memory("MEM-0001")
    ws.finish()
    assert any("silent promotion" in f["message"] for f in ws.run()["failures"])


def test_reject_requires_log_entry(ws):
    ws.completed(C1, "REJECT")
    ws.finish()
    assert 3 in ws.codes()
    (ws.root / "DISPOSITION_LOG.md").write_text(
        json.dumps({"event": "DECIDED", "candidate_id": C1, "disposition": "REJECT"}) + "\n")
    assert 3 not in ws.codes()


def test_needs_review_requires_owner_and_deadline(ws):
    ws.completed(C1, "NEEDS_REVIEW")
    ws.finish()
    assert 3 in ws.codes()


def test_needs_review_expiry_fails_and_never_promotes(ws):
    ws.completed(C1, "NEEDS_REVIEW", owner="bob", review_by="2026-10-02")
    ws.finish()
    r = ws.run()
    assert 4 in {f["code"] for f in r["failures"]}
    assert r["exit_code"] == 4


def test_needs_review_in_window_passes_and_long_window_alerts(ws):
    ws.completed(C1, "NEEDS_REVIEW", owner="bob", review_by="2026-11-30")
    ws.finish()
    r = ws.run()
    assert r["exit_code"] == 0
    assert any("REVIEW_WINDOW_EXCEEDS_DEFAULT" in a for a in r["alerts"])


def test_provenance_drift_and_missing_commit(ws):
    ws.completed(C1)
    ws.finish()
    (ws.root / "src.txt").write_text("changed\n")
    assert any("PROVENANCE_DRIFT" in f["message"] for f in ws.run()["failures"])
    (ws.root / "src.txt").write_text("evidence\n")
    text = (ws.root / "03_COMPLETED" / f"{C1}.md").read_text().replace(ws.commit, "deadbeef" * 5)
    (ws.root / "03_COMPLETED" / f"{C1}.md").write_text(text)
    assert 5 in ws.codes()


def test_memory_provenance_drift_when_completed_body_edited(ws):
    ws.completed(C1, "PROMOTE")
    ws.memory("MEM-0001")
    ws.finish()
    p = ws.root / "03_COMPLETED" / f"{C1}.md"
    p.write_text(p.read_text().replace("Body text.", "Edited text."))
    assert 5 in ws.codes()


def test_frontmatter_edit_does_not_cause_drift(ws):
    ws.completed(C1, "PROMOTE")
    ws.memory("MEM-0001")
    ws.finish()
    p = ws.root / "03_COMPLETED" / f"{C1}.md"
    p.write_text(p.read_text().replace("decided_by: alice", "decided_by: carol"))
    assert 5 not in ws.codes()


def test_dangling_reference(ws):
    ws.completed(C1, "SUPERSEDED", extra="superseded_by:\n  - MEM-0099\n")
    ws.finish()
    assert 6 in ws.codes()


def test_supersession_cycle(ws):
    ws.completed(C1, "PROMOTE")
    ws.memory("MEM-0001", status="SUPERSEDED", extra="supersedes:\n  - MEM-0002\nsuperseded_by:\n  - MEM-0002\n")
    ws.memory("MEM-0002", status="SUPERSEDED", sources=(C1,),
              extra="supersedes:\n  - MEM-0001\nsuperseded_by:\n  - MEM-0001\n")
    ws.finish()
    assert any("CYCLE" in f["message"] for f in ws.run()["failures"])


def test_valid_supersession_chain_resolves_to_head(ws):
    ws.completed(C1, "PROMOTE")
    ws.memory("MEM-0001", status="SUPERSEDED", extra="superseded_by:\n  - MEM-0002\n")
    ws.memory("MEM-0002", extra="supersedes:\n  - MEM-0001\n")
    ws.finish()
    r = ws.run()
    assert r["exit_code"] == 0, r["failures"]
    rep, _ = mv.validate(ws.root, TODAY)
    assert mv.resolve_head(rep, "MEM-0001") == "MEM-0002"
    assert [m["id"] for m in mv.retrieve(rep)] == ["MEM-0002"]


def test_asymmetric_supersession_and_fork(ws):
    ws.completed(C1, "PROMOTE")
    ws.memory("MEM-0001", status="SUPERSEDED", extra="superseded_by:\n  - MEM-0002\n  - MEM-0003\n")
    ws.memory("MEM-0002")
    ws.memory("MEM-0003")
    ws.finish()
    msgs = " ".join(f["message"] for f in ws.run()["failures"])
    assert "does not list" in msgs and "ambiguous fork" in msgs


def test_merge_requires_back_reference_and_provenance(ws):
    ws.completed(C1, "PROMOTE")
    ws.completed(C2, "MERGE", extra="merged_into:\n  - MEM-0001\n")
    ws.memory("MEM-0001")
    ws.finish()
    assert 8 in ws.codes()  # MEM-0001 does not list C2 in merged_from or sources
    ws.memory("MEM-0001", sources=(C1, C2), extra="merged_from:\n  - " + C2 + "\n")
    ws.finish()
    assert ws.run()["exit_code"] == 0, ws.run()["failures"]


def test_hidden_merge(ws):
    ws.completed(C1, "PROMOTE")
    ws.completed(C2, "KEEP_COMPLETED")
    ws.memory("MEM-0001", sources=(C1, C2), extra="merged_from:\n  - " + C2 + "\n")
    ws.finish()
    assert any("hidden merge" in f["message"] for f in ws.run()["failures"])


def test_stale_memory(ws):
    ws.completed(C1, "PROMOTE")
    ws.memory("MEM-0001", last_verified="2026-08-01", verify_by="2026-09-01")
    ws.finish()
    r = ws.run()
    assert 10 in {f["code"] for f in r["failures"]}
    assert r["counts"]["stale_memory"] == 1


def test_verify_by_beyond_interval(ws):
    ws.completed(C1, "PROMOTE")
    ws.memory("MEM-0001", verify_interval_days=7)
    ws.finish()
    assert 10 in ws.codes()


def test_demoted_requires_block_and_completed_must_not_stay_promote(ws):
    ws.completed(C1, "PROMOTE")
    ws.memory("MEM-0001", status="DEMOTED")
    ws.finish()
    assert 1 in ws.codes()  # no demotion block
    ws.memory("MEM-0001", status="DEMOTED",
              extra=f"demotion:\n  reason: wrong\n  decided_at: 2026-10-03\n  decided_by: bob\n  destination: 03_COMPLETED/{C1}.md\n")
    ws.finish()
    assert 3 in ws.codes()  # silent demotion: item still says PROMOTE


def test_stale_index_stats_changelog(ws):
    ws.completed(C1, "PROMOTE")
    ws.memory("MEM-0001")
    ws.finish()
    idx = ws.root / "42_PERMANENT_MEMORY" / "INDEX.md"
    idx.write_text(idx.read_text().replace("| MEM-0001 |", "| MEM-0001 |", 1) + "| MEM-0042 | ghost | ACTIVE | x | y |\n")
    (ws.root / "STATS.md").write_text("PZS MEMORY STATISTICS\nCompleted: 99\n")
    (ws.root / "CHANGELOG.md").write_text("## 2026-01-01\n")
    r = ws.run()
    assert {f["check"] for f in r["failures"]} >= {"index", "stats", "changelog"}
    assert r["exit_code"] == 9


def test_disposition_mix_alert_is_not_a_failure(ws):
    for i in range(1, 7):
        ws.completed(f"CAND-2026-10-03-{i:03d}", "KEEP_COMPLETED")
    ws.finish()
    r = ws.run()
    assert r["exit_code"] == 0
    assert any("DISPOSITION_MIX cycle" in a for a in r["alerts"])
    assert any("reviewer alice" in a for a in r["alerts"])


def test_unparseable_note_is_structural_failure(ws):
    (ws.root / "03_COMPLETED" / "bad.md").write_text("no frontmatter here\n")
    ws.finish()
    assert ws.run()["exit_code"] == 1


def test_missing_required_directory_never_passes(ws):
    ws.finish()
    (ws.root / "42_PERMANENT_MEMORY" / "INDEX.md").unlink()
    (ws.root / "42_PERMANENT_MEMORY").rmdir()
    assert ws.run()["exit_code"] == 1


def test_non_git_root_cannot_verify_provenance(tmp_path):
    w = Ws(tmp_path)
    w.completed(C1)
    w.finish()
    import shutil
    shutil.rmtree(tmp_path / ".git")
    mv._git_cache.clear()
    assert 5 in w.codes()


def test_alloc_id_is_mechanical_and_never_reuses(tmp_path):
    (tmp_path / "state").mkdir()
    (tmp_path / "state" / "ids.lock").write_text("MEM-0007\nCAND-2026-10-03-004\n")
    assert mv.alloc_id(tmp_path, "mem", TODAY) == "MEM-0008"
    assert mv.alloc_id(tmp_path, "cand", TODAY) == "CAND-2026-10-03-005"
    assert mv.alloc_id(tmp_path, "cand", date(2026, 10, 4)) == "CAND-2026-10-04-001"
    ids = (tmp_path / "state" / "ids.lock").read_text().split()
    assert len(ids) == len(set(ids)) == 5


def test_frontmatter_parser_rejects_unsupported_yaml():
    for bad in ("---\na: |\n  x\n---\n", "---\na: 1\na: 2\n---\n", "---\na: [x\n---\n", "no fm"):
        with pytest.raises(mv.FrontmatterError):
            mv.parse_frontmatter(bad)
    meta, _ = mv.parse_frontmatter("---\nl: []\nm:\n  - id: X\n    n: 1\n  - id: Y\ns: [a, b]\n---\nbody")
    assert meta == {"l": [], "m": [{"id": "X", "n": 1}, {"id": "Y"}], "s": ["a", "b"]}


def test_cli_exit_codes_and_generate(ws, capsys):
    ws.completed(C1, "PROMOTE")
    ws.memory("MEM-0001")
    (ws.root / "CHANGELOG.md").write_text("## 2026-10-03\n")
    args = ["--root", str(ws.root), "--today", "2026-10-03"]
    assert mv.main(["validate", *args]) == 9          # INDEX/STATS not generated yet
    assert mv.main(["generate", *args]) == 0
    assert mv.main(["validate", *args]) == 0
    assert mv.main(["retrieve", *args]) == 0
    assert "MEM-0001" in capsys.readouterr().out


def test_index_text_drift_with_matching_ids_is_caught(ws):
    ws.completed(C1, "PROMOTE")
    ws.memory("MEM-0001")
    ws.finish()
    idx = ws.root / "42_PERMANENT_MEMORY" / "INDEX.md"
    idx.write_text(idx.read_text().replace("2026-11-03", "2099-01-01"))   # same IDs, stale content
    assert any(f["check"] == "index" and "out of date" in f["message"] for f in ws.run()["failures"])
