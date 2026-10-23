"""Adversarial probes from the AIL/MoIE review (see evals/inversion-review.md).

Each test states a prediction made by inverting an assumption of the validator. A test that
fails against an earlier version means the anomaly was real."""
import copy
import itertools
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_contract as vc  # noqa: E402

BASE = json.loads((ROOT / "examples" / "contract.json").read_text())
NOW = datetime(2026, 10, 25, tzinfo=timezone.utc)


def good_receipt(doc, **over):
    r = {"contract_hash": vc.contract_hash(doc), "executed_at": "2026-10-24T10:00:00Z", "executed_by": "the owner's account",
         "environment": "script project", "mode": "live", "deployed_version": doc.get("deployed_version", "v7"),
         "trigger_fired": True, "observed_outcome": "one draft created",
         "checks": [{"name": t, "status": "PASS", "evidence": "execution log line 12"} for t in doc["tests"]]}
    r.update(over)
    return r


class Probe(unittest.TestCase):
    def setUp(self):
        self.d = copy.deepcopy(BASE)

    def has(self, text, doc=None, **kw):
        problems = vc.validate(self.d if doc is None else doc, **kw)
        self.assertTrue(any(text in p for p in problems), (text, problems))

    def verified(self, receipt, name="receipt.json", version="v7"):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = Path(tmp.name)
        self.d.update(status="VERIFIED_IN_SCOPE", deployment_authorized=True, execution_receipt=name, deployed_version=version)
        if receipt is not None:
            (base / name).write_text(receipt if isinstance(receipt, str) else json.dumps(receipt))
        return base


class A1_NonEmptyMeansInformative(Probe):
    def test_placeholders_and_invisible_text_are_rejected(self):
        for value in ("TODO", "todo: later", "TBD", "tbd", "n/a", "N/A", "?", "??", "fixme", "xxx", "​", "​ ​", "-", "..."):
            d = copy.deepcopy(BASE)
            d["quota"] = value
            self.has("quota must be non-empty text", d)

    def test_real_short_answers_are_accepted(self):
        d = copy.deepcopy(BASE)
        d["data_retention"] = "none kept"
        d["quota"] = "1 read per run"
        self.assertEqual(vc.validate(d), [])


class A2_NamesAreUnique(Probe):
    def test_duplicate_check_names_cannot_hide_a_failure(self):
        r = good_receipt(self.d)
        r["checks"].insert(0, {"name": self.d["tests"][0], "status": "FAIL", "evidence": "x"})
        base = self.verified(r)
        self.has("duplicate", base_dir=base, now=NOW)

    def test_duplicate_or_malformed_contract_tests_are_problems_not_crashes(self):
        for tests, text in ((["a", "a"], "tests must be unique"), ([["a"]], "tests must be non-empty text"),
                            ([5], "tests must be non-empty text"), ([""], "tests must be non-empty text"),
                            ([{"a": 1}], "tests must be non-empty text")):
            d = copy.deepcopy(BASE)
            d["tests"] = tests
            self.has(text, d)

    def test_duplicate_test_results_in_local_tested(self):
        self.d["status"] = "LOCAL_TESTED"
        t = self.d["tests"][0]
        self.d["test_results"] = [{"name": x, "status": "PASS"} for x in self.d["tests"]] + [{"name": t, "status": "FAIL"}]
        self.has("duplicate")


class A3_ExactMatchIsEnough(Probe):
    def test_scope_spelling_variants_still_count_as_broad(self):
        for scope in ("https://mail.google.com", " https://mail.google.com/ ", "HTTPS://MAIL.GOOGLE.COM/",
                      "https://www.googleapis.com/auth/drive/", "https://www.googleapis.com/auth/GMAIL.MODIFY"):
            d = copy.deepcopy(BASE)
            d["permissions"] = [scope]
            self.has("needs a scope_justification", d)

    def test_narrow_scopes_are_not_flagged(self):
        for scope in ("https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets.readonly",
                      "https://www.googleapis.com/auth/gmail.compose"):
            d = copy.deepcopy(BASE)
            d["permissions"] = [scope]
            self.assertEqual(vc.validate(d), [], scope)

    def test_sending_is_recognised_however_the_action_is_spelled(self):
        for action in ("Send_Email", " send_email ", "email_send", "draft_and_send", "SEND", "post_to_slack", "publish_report"):
            d = copy.deepcopy(BASE)
            d["action"] = action
            self.has("consent_policy and a rate_limit", d)

    def test_non_sending_actions_do_not_need_consent_rules(self):
        for action in ("create_draft", "append_row", "update_cell", "copy_file"):
            d = copy.deepcopy(BASE)
            d["action"] = action
            self.assertEqual(vc.validate(d), [], action)

    def test_destructive_or_external_actions_are_flagged_when_deployed_unauthorized(self):
        for action in ("Delete_Rows", "purchase_item", "share_file", "modify_external"):
            d = copy.deepcopy(BASE)
            d.update(action=action, status="DEPLOYED_UNVERIFIED", deployed_version="v1", deployment_authorized=False)
            self.has("external side effect deployed without authorization", d)


class A4_AReceiptMeansItRanForReal(Probe):
    def test_a_dry_run_cannot_verify_a_live_automation(self):
        for mode in ("dry_run", "DRY_RUN", None, "", "preview"):
            base = self.verified(good_receipt(self.d, mode=mode))
            self.has("mode must be 'live'", base_dir=base, now=NOW)

    def test_a_receipt_for_another_deployed_version_is_rejected(self):
        base = self.verified(good_receipt(self.d, deployed_version="v6"), version="v7")
        self.has("deployed_version does not match", base_dir=base, now=NOW)

    def test_verified_requires_a_deployed_version(self):
        base = self.verified(good_receipt(self.d, deployed_version="v7"))
        self.d.pop("deployed_version")
        self.has("VERIFIED_IN_SCOPE requires deployed_version", base_dir=base, now=NOW)


class A5_EvidenceFieldMakesPassCredible(Probe):
    def test_pass_without_evidence_is_rejected(self):
        for ev in ("", "   ", None, "TODO"):
            r = good_receipt(self.d)
            r["checks"][0]["evidence"] = ev
            base = self.verified(r)
            self.has("needs evidence", base_dir=base, now=NOW)
        r = good_receipt(self.d)
        del r["checks"][0]["evidence"]
        self.has("needs evidence", base_dir=self.verified(r), now=NOW)


class A6_JsonIsUnambiguous(Probe):
    def test_duplicate_keys_are_refused(self):
        with self.assertRaises(ValueError):
            vc.load_json('{"status": "DESIGNED", "status": "VERIFIED_IN_SCOPE"}')
        with self.assertRaises(ValueError):
            vc.load_json('{"a": {"b": 1, "b": 2}}')
        self.assertEqual(vc.load_json('{"a": 1, "b": [1, 2]}'), {"a": 1, "b": [1, 2]})

    def test_cli_refuses_a_contract_with_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "c.json"
            p.write_text('{"status": "DESIGNED", "status": "BLOCKED"}')
            self.assertEqual(vc.main([str(p)]), 2)

    def test_hash_of_a_non_object_is_a_clean_failure(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "c.json"
            p.write_text("[1, 2]")
            self.assertEqual(vc.main(["--hash", str(p)]), 2)


class A7_TheContractCoversThePromises(Probe):
    def test_rollback_and_success_measure_are_required(self):
        for key in ("rollback", "success_measure"):
            d = copy.deepcopy(BASE)
            d.pop(key, None)
            self.has(f"missing {key}", d)


class A8_NeverCrashOnHostileShapes(Probe):
    VALUES = (None, 0, 1, -1, 1.5, True, False, "", " ", "x", [], {}, [[]], [{}], ["x"], [None], {"a": 1}, "x" * 3000)

    def under_status(self, status):
        """A contract in the given status, with a good receipt on disk, so every code path is reachable."""
        d = copy.deepcopy(BASE)
        d.update(status=status, deployment_authorized=True, deployed_version="v7",
                 test_results=[{"name": t, "status": "PASS"} for t in BASE["tests"]], reason="because",
                 execution_receipt="receipt.json")
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        (Path(tmp.name) / "receipt.json").write_text(json.dumps(good_receipt(d)))
        return d, Path(tmp.name)

    def test_every_contract_field_with_every_wrong_type_returns_problems_in_every_status(self):
        for status in vc.STATUSES:
            for key in list(BASE) + ["test_results", "reason", "deployed_version", "execution_receipt", "scope_justification"]:
                for v in self.VALUES:
                    d, base = self.under_status(status)
                    d[key] = v
                    try:
                        out = vc.validate(d, base_dir=base, now=NOW)
                    except Exception as e:                      # the whole point: never raise
                        self.fail(f"{status}/{key}={v!r} raised {type(e).__name__}: {e}")
                    self.assertIsInstance(out, list)

    def test_hostile_list_members_in_every_status(self):
        weird = ([["a"]], [5], [None], [{}], [{"a": 1}], ["a", ["b"]])
        for status in vc.STATUSES:
            for key in ("tests", "permissions", "exclusions", "missing_critical_facts", "test_results"):
                for v in weird:
                    d, base = self.under_status(status)
                    d[key] = v
                    try:
                        self.assertIsInstance(vc.validate(d, base_dir=base, now=NOW), list)
                    except Exception as e:
                        self.fail(f"{status}/{key}={v!r} raised {type(e).__name__}: {e}")

    def test_every_receipt_field_with_every_wrong_type_returns_problems(self):
        for key in list(good_receipt(BASE)):
            for v in self.VALUES:
                base = self.verified(good_receipt(BASE, **{key: v}))
                self.assertIsInstance(vc.validate(self.d, base_dir=base, now=NOW), list, (key, v))
                self.d = copy.deepcopy(BASE)

    def test_hostile_check_entries(self):
        for item in (None, 5, "x", [], {}, {"name": []}, {"name": "t", "status": []}, {"name": {}, "status": "PASS"}):
            r = good_receipt(BASE)
            r["checks"].append(item)
            base = self.verified(r)
            self.assertIsInstance(vc.validate(self.d, base_dir=base, now=NOW), list)
            self.d = copy.deepcopy(BASE)

    def test_non_dict_inputs(self):
        for doc in (None, 5, "x", [], [1], True):
            self.assertEqual(vc.validate(doc), ["contract must be a JSON object"])


class A10_ReceiptPathIsContained(Probe):
    def test_absolute_symlink_directory_and_self_references_are_rejected(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = Path(tmp.name)
        outside = Path(tmp.name + "-outside.json")
        outside.write_text(json.dumps(good_receipt(BASE)))
        self.addCleanup(outside.unlink)
        os.symlink(outside, base / "link.json")
        (base / "adir").mkdir()
        self.d.update(status="VERIFIED_IN_SCOPE", deployment_authorized=True, deployed_version="v7")
        for ref in (str(outside), "link.json", "adir", "../x.json", "contract.json", "."):
            self.d["execution_receipt"] = ref
            self.assertTrue(vc.validate(self.d, base_dir=base, now=NOW), ref)


class RedTeamOfTheFixes(Probe):
    """Attacks on the first round of fixes, found by trying to get bad input past them."""

    def test_fullwidth_letters_do_not_dodge_the_placeholder_check(self):
        for value in ("\uff34\uff2f\uff24\uff2f", "\uff54\uff42\uff44"):          # fullwidth "TODO" and "tbd"
            d = copy.deepcopy(BASE)
            d["quota"] = value
            self.has("quota must be non-empty text", d)

    def test_sending_actions_with_unlisted_names_are_still_caught(self):
        for action in ("dispatch_mail", "email_everyone", "message_team", "Text_SMS_Customers", "tweet_update", "DM_followers"):
            d = copy.deepcopy(BASE)
            d["action"] = action
            self.has("consent_policy and a rate_limit", d)

    def test_drafting_an_email_is_not_sending_it(self):
        for action in ("create_email_draft", "draft_message", "save_mail_draft"):
            d = copy.deepcopy(BASE)
            d["action"] = action
            self.assertEqual(vc.validate(d), [], action)
        d = copy.deepcopy(BASE)
        d["action"] = "draft_and_send_email"
        self.has("consent_policy and a rate_limit", d)

    def test_full_calendar_and_contacts_scopes_are_broad(self):
        for scope in ("https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/contacts"):
            d = copy.deepcopy(BASE)
            d["permissions"] = [scope]
            self.has("needs a scope_justification", d)
        d = copy.deepcopy(BASE)
        d["permissions"] = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/calendar.events"]
        self.assertEqual(vc.validate(d), [])

    def test_known_limits_are_real_limits(self):
        """Documented gaps: the validator cannot judge meaning or truth. If one of these starts failing,
        update references/contract-schema.md and the review record."""
        d = copy.deepcopy(BASE)
        d["quota"] = "asdf"
        self.assertEqual(vc.validate(d), [])                   # gibberish is still text
        d["quota"] = "to do later"
        self.assertEqual(vc.validate(d), [])                   # a paraphrased placeholder is still text
        r = good_receipt(BASE, executed_by="x1")
        r["checks"] = [{"name": t, "status": "PASS", "evidence": "see log"} for t in BASE["tests"]]
        d = copy.deepcopy(BASE)
        d.update(status="VERIFIED_IN_SCOPE", deployment_authorized=True, execution_receipt="r.json", deployed_version="v7")
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "r.json").write_text(json.dumps(r))
            self.assertEqual(vc.validate(d, base_dir=Path(t), now=NOW), [])   # a hand-written receipt passes


if __name__ == "__main__":
    unittest.main()
