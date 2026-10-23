import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_contract as vc  # noqa: E402

BASE = json.loads((ROOT / "examples" / "contract.json").read_text())
NOW = datetime(2026, 10, 24, tzinfo=timezone.utc)


def receipt_for(doc, **over):
    r = {"contract_hash": vc.contract_hash(doc), "executed_at": "2026-10-23T10:00:00Z", "executed_by": "owner@example.invalid",
         "environment": "script project v7", "trigger_fired": True, "observed_outcome": "one draft created",
         "checks": [{"name": t, "status": "PASS", "evidence": "execution log"} for t in doc["tests"]]}
    r.update(over)
    return r


class Base(unittest.TestCase):
    def setUp(self):
        self.d = copy.deepcopy(BASE)

    def problems(self, **kw):
        return vc.validate(self.d, **kw)

    def has(self, text, **kw):
        self.assertTrue(any(text in p for p in self.problems(**kw)), (text, self.problems(**kw)))


class ContractShape(Base):
    def test_example_is_valid(self):
        self.assertEqual(self.problems(), [])

    def test_every_required_text_field_is_enforced(self):
        for key in vc.REQUIRED_TEXT:
            d = copy.deepcopy(BASE)
            d.pop(key)
            self.assertIn(f"missing {key}", vc.validate(d), key)
            d[key] = "   "
            self.assertIn(f"{key} must be non-empty text", vc.validate(d), key)
            d[key] = 5
            self.assertIn(f"{key} must be non-empty text", vc.validate(d), key)

    def test_every_required_list_is_enforced(self):
        for key in vc.REQUIRED_LISTS:
            d = copy.deepcopy(BASE)
            d.pop(key)
            self.assertIn(f"missing {key}", vc.validate(d), key)
            d[key] = "not a list"
            self.assertIn(f"{key} must be a list", vc.validate(d), key)

    def test_permissions_and_tests_may_not_be_empty_but_exclusions_may(self):
        self.d["permissions"] = []
        self.has("permissions must not be empty")
        self.d["permissions"] = ["spreadsheets.readonly"]
        self.d["tests"] = []
        self.has("tests must not be empty")
        self.d["tests"] = ["one"]
        self.d["exclusions"] = []
        self.d["missing_critical_facts"] = []
        self.assertEqual(self.problems(), [])

    def test_dry_run_must_be_exactly_true(self):
        for bad in (False, "true", 1, None):
            self.d["dry_run"] = bad
            self.has("dry_run must default true")
        del self.d["dry_run"]
        self.has("dry_run must default true")

    def test_status_must_be_known(self):
        self.d["status"] = "DONE"
        self.has("invalid status")
        del self.d["status"]
        self.has("invalid status")

    def test_non_object_contract(self):
        self.assertEqual(vc.validate([]), ["contract must be a JSON object"])


class Authority(Base):
    def test_broad_scope_needs_justification(self):
        for scope in vc.BROAD_SCOPES:
            self.d["permissions"] = [scope]
            self.has("needs a scope_justification")
            self.d["scope_justification"] = "must read every message"
            self.assertEqual(self.problems(), [], scope)
            del self.d["scope_justification"]
        self.d["permissions"] = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        self.assertEqual(self.problems(), [])

    def test_sending_needs_consent_policy_and_rate_limit(self):
        self.d["action"] = "send_email"
        self.has("consent_policy and a rate_limit")
        self.d["consent_policy"] = "only recipients who opted in; suppression list checked"
        self.has("consent_policy and a rate_limit")                      # still missing the rate limit
        self.d["rate_limit"] = "20 per run"
        self.assertEqual(self.problems(), [])
        self.d["action"] = "create_draft"
        del self.d["consent_policy"], self.d["rate_limit"]
        self.assertEqual(self.problems(), [])                              # drafts do not need them

    def test_deployed_statuses_need_authorization_and_a_version(self):
        for status in ("DEPLOYED_UNVERIFIED", "VERIFIED_IN_SCOPE"):
            self.d.update(status=status, deployment_authorized=False, deployed_version="v1")
            self.has("requires deployment_authorized: true")
        self.d.update(status="DEPLOYED_UNVERIFIED", deployment_authorized=True)
        self.d.pop("deployed_version")
        self.has("requires deployed_version")
        self.d["deployed_version"] = "v1"
        self.assertEqual(self.problems(), [])

    def test_external_side_effect_without_authorization_is_called_out(self):
        for action in vc.EXTERNAL_ACTIONS:
            self.d.update(action=action, status="DEPLOYED_UNVERIFIED", deployed_version="v1", consent_policy="c", rate_limit="r")
            self.has("external side effect deployed without authorization")
        self.d["action"] = "create_draft"
        self.has("requires deployment_authorized: true")
        self.assertFalse(any("external side effect" in p for p in self.problems()))

    def test_designed_does_not_need_authorization(self):
        self.d["deployment_authorized"] = False
        self.assertEqual(self.problems(), [])


class StatusLadder(Base):
    def test_failed_and_blocked_need_a_reason(self):
        for status in ("FAILED", "BLOCKED"):
            self.d["status"] = status
            self.has(f"{status} requires a reason")
            self.d["reason"] = "permission revoked"
            self.assertEqual(self.problems(), [])
            del self.d["reason"]

    def test_local_tested_needs_a_pass_for_every_test(self):
        self.d["status"] = "LOCAL_TESTED"
        self.has("test_results must be a non-empty list")
        self.d["test_results"] = [{"name": t, "status": "PASS"} for t in self.d["tests"]]
        self.assertEqual(self.problems(), [])
        self.d["test_results"][0]["status"] = "FAIL"
        self.has(f"LOCAL_TESTED needs a PASS test result for {self.d['tests'][0]!r}")
        self.d["test_results"][0]["status"] = "NOT_RUN"
        self.has("LOCAL_TESTED needs a PASS test result")
        self.d["test_results"] = self.d["test_results"][1:]
        self.has("LOCAL_TESTED needs a PASS test result")
        self.d["test_results"] = [{"name": "x", "status": "MAYBE"}]
        self.has("needs a name and a status")


class Receipts(Base):
    def verified(self, receipt, name="receipt.json"):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.d.update(status="VERIFIED_IN_SCOPE", deployment_authorized=True, execution_receipt=name)
        if receipt is not None:
            (base / name).write_text(receipt if isinstance(receipt, str) else json.dumps(receipt))
        return base

    def test_a_good_receipt_passes_and_a_bare_string_no_longer_does(self):
        base = self.verified(receipt_for(self.d))
        self.assertEqual(self.problems(base_dir=base, now=NOW), [])
        self.d["execution_receipt"] = "example_receipt"
        self.has("does not exist", base_dir=base, now=NOW)                # the old placebo input

    def test_receipt_needs_a_path_and_a_directory_to_resolve_against(self):
        self.verified(None)
        for bad in ("", "  ", None, 5):
            self.d["execution_receipt"] = bad
            self.has("requires execution_receipt")
        self.d["execution_receipt"] = "r.json"
        self.has("cannot resolve execution_receipt")

    def test_receipt_must_stay_inside_the_contract_directory(self):
        base = self.verified(receipt_for(self.d))
        self.d["execution_receipt"] = "../escape.json"
        self.has("inside the contract's directory", base_dir=base, now=NOW)

    def test_unreadable_or_non_object_receipt(self):
        base = self.verified("{not json")
        self.has("not readable JSON", base_dir=base, now=NOW)
        base = self.verified("[1, 2]")
        self.has("receipt missing executed_by", base_dir=base, now=NOW)

    def test_receipt_bound_to_a_different_contract_is_rejected(self):
        base = self.verified(receipt_for(self.d))
        self.d["intent"] = "something else entirely"
        self.has("contract_hash does not match", base_dir=base, now=NOW)

    def test_status_and_evidence_changes_do_not_change_the_hash(self):
        before = vc.contract_hash(self.d)
        self.d.update(status="VERIFIED_IN_SCOPE", deployment_authorized=True, execution_receipt="r.json",
                      test_results=[], deployed_version="v1", reason="x", contract_hash="whatever")
        self.assertEqual(vc.contract_hash(self.d), before)
        self.d["trigger"] = "different"
        self.assertNotEqual(vc.contract_hash(self.d), before)

    def test_hash_ignores_key_order_but_not_content(self):
        reordered = dict(reversed(list(self.d.items())))
        self.assertEqual(vc.contract_hash(reordered), vc.contract_hash(self.d))
        self.d["tests"] = list(reversed(self.d["tests"]))
        self.assertNotEqual(vc.contract_hash(self.d), vc.contract_hash(BASE))      # list order is content

    def test_example_flag_and_missing_fields_and_untriggered_runs_are_rejected(self):
        for over, text in (({"example": True}, "marked as an example"), ({"executed_by": ""}, "missing executed_by"),
                           ({"environment": ""}, "missing environment"), ({"observed_outcome": ""}, "missing observed_outcome"),
                           ({"trigger_fired": False}, "trigger_fired: true"), ({"trigger_fired": "yes"}, "trigger_fired: true")):
            base = self.verified(receipt_for(self.d, **over))
            self.has(text, base_dir=base, now=NOW)

    def test_receipt_time_must_be_iso_zoned_and_not_future(self):
        for value, text in (("yesterday", "not an ISO 8601"), ("2026-10-23T10:00:00", "needs a timezone"),
                            ("2030-01-01T00:00:00Z", "in the future"), (None, "not an ISO 8601")):
            base = self.verified(receipt_for(self.d, executed_at=value))
            self.has(text, base_dir=base, now=NOW)
        base = self.verified(receipt_for(self.d, executed_at="2026-10-23T10:00:00+02:00"))
        self.assertEqual(self.problems(base_dir=base, now=NOW), [])

    def test_every_contract_test_needs_a_passing_check(self):
        r = receipt_for(self.d)
        r["checks"] = r["checks"][1:]
        base = self.verified(r)
        self.has(f"no check for contract test {self.d['tests'][0]!r}", base_dir=base, now=NOW)
        for state in ("FAIL", "NOT_RUN"):
            r = receipt_for(self.d)
            r["checks"][0]["status"] = state
            base = self.verified(r)
            self.has(f"is {state}", base_dir=base, now=NOW)
        base = self.verified(receipt_for(self.d, checks=[]))
        self.has("receipt checks must be a non-empty list", base_dir=base, now=NOW)
        r = receipt_for(self.d)
        r["checks"].append({"name": "extra", "status": "FAIL"})
        base = self.verified(r)
        self.has("receipt check 'extra' is FAIL", base_dir=base, now=NOW)


class Cli(Base):
    def run_cli(self, argv):
        import io
        from contextlib import redirect_stdout, redirect_stderr
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = vc.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_pass_fail_hash_and_unreadable(self):
        good = ROOT / "examples" / "contract.json"
        code, out, _ = self.run_cli([str(good)])
        self.assertEqual((code, out.strip()), (0, "PASS"))
        code, out, _ = self.run_cli(["--hash", str(good)])
        self.assertEqual((code, out.strip()), (0, vc.contract_hash(BASE)))
        with tempfile.TemporaryDirectory() as t:
            bad = Path(t) / "c.json"
            bad.write_text(json.dumps({**BASE, "dry_run": False}))
            code, out, _ = self.run_cli([str(bad)])
            self.assertEqual(code, 1)
            self.assertIn("ERROR: dry_run must default true", out)
            self.assertTrue(out.strip().endswith("FAIL"))
            bad.write_text("{nope")
            code, _, err = self.run_cli([str(bad)])
            self.assertEqual(code, 2)
            self.assertIn("cannot read contract", err)
            code, _, _ = self.run_cli([str(Path(t) / "missing.json")])
            self.assertEqual(code, 2)

    def test_cli_resolves_receipts_next_to_the_contract(self):
        with tempfile.TemporaryDirectory() as t:
            d = copy.deepcopy(BASE)
            d.update(status="VERIFIED_IN_SCOPE", deployment_authorized=True, execution_receipt="receipt.json")
            (Path(t) / "receipt.json").write_text(json.dumps(receipt_for(d)))
            (Path(t) / "contract.json").write_text(json.dumps(d))
            code, out, _ = self.run_cli([str(Path(t) / "contract.json")])
            self.assertEqual((code, out.strip()), (0, "PASS"))


if __name__ == "__main__":
    unittest.main()
