"""The collaborative design: a firm baseline, situational fields decided with the user, and a
record in which the AI recommends and only the user decides."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_contract as vc  # noqa: E402

EXAMPLES = sorted((ROOT / "examples").glob("*.json"))
DRAFTER = json.loads((ROOT / "examples" / "contract.json").read_text())
INTERNAL = json.loads((ROOT / "examples" / "contract-internal-copy.json").read_text())
DEPLOY = {"topic": "deployment", "choice": "deploy to the owner's account", "reason": "tested and ready",
          "decided_by": "user", "quote": "Yes, deploy it."}


class Examples(unittest.TestCase):
    def test_every_example_is_valid(self):
        self.assertGreaterEqual(len(EXAMPLES), 2)
        for path in EXAMPLES:
            self.assertEqual(vc.validate(json.loads(path.read_text())), [], path.name)

    def test_the_internal_example_shows_fields_that_do_not_apply(self):
        waived = [k for k in vc.SITUATIONAL_TEXT if vc.is_waiver(INTERNAL[k])]
        self.assertGreaterEqual(len(waived), 4)
        self.assertEqual([k for k in vc.SITUATIONAL_TEXT if vc.is_waiver(DRAFTER[k])], [])


class Baseline(unittest.TestCase):
    def test_baseline_fields_cannot_be_waived(self):
        for key in vc.BASELINE_TEXT:
            d = copy.deepcopy(INTERNAL)
            d[key] = {"not_applicable": "it does not apply in my case"}
            self.assertIn(f"{key} must be non-empty text", vc.validate(d), key)

    def test_baseline_and_situational_sets_do_not_overlap_and_cover_the_core(self):
        self.assertFalse(set(vc.BASELINE_TEXT) & set(vc.SITUATIONAL_TEXT))
        for key in ("source_utterance", "identity", "rollback", "disable", "failure_policy", "success_measure"):
            self.assertIn(key, vc.BASELINE_TEXT)
        for key in ("idempotency", "audit_log", "quota", "data_retention", "predicate", "transformation"):
            self.assertIn(key, vc.SITUATIONAL_TEXT)


class Situational(unittest.TestCase):
    def test_a_missing_situational_field_says_how_to_resolve_it(self):
        d = copy.deepcopy(INTERNAL)
        del d["quota"]
        problems = vc.validate(d)
        self.assertEqual(len(problems), 1)
        self.assertTrue(problems[0].startswith("missing quota: give a value, or mark it"))
        self.assertIn("not_applicable", problems[0])

    def test_a_value_or_a_reasoned_waiver_both_satisfy_a_situational_field(self):
        for key in vc.SITUATIONAL_TEXT:
            d = copy.deepcopy(INTERNAL)
            d[key] = "a real answer worked out with the user"
            self.assertEqual(vc.validate(d), [], key)
            d[key] = {"not_applicable": "does not apply because nothing leaves the sheet"}
            self.assertEqual(vc.validate(d), [], key)

    def test_a_waiver_needs_a_real_reason_and_the_exact_shape(self):
        bad = ({"not_applicable": ""}, {"not_applicable": "TODO"}, {"not_applicable": "n/a"}, {"not_applicable": 5},
               {"not_applicable": "ok reason", "extra": 1}, {}, {"na": "reason"}, {"Not_Applicable": "reason"})
        for waiver in bad:
            d = copy.deepcopy(INTERNAL)
            d["quota"] = waiver
            self.assertTrue(any(p.startswith("quota waiver must be exactly") for p in vc.validate(d)), waiver)
        for notdict in (5, None, ["n/a"], "", "n/a", True):
            d = copy.deepcopy(INTERNAL)
            d["quota"] = notdict
            self.assertIn("quota must be non-empty text", vc.validate(d), notdict)

    def test_idempotency_and_audit_log_cannot_be_waived_once_the_action_reaches_outward(self):
        for action in ("send_email", "delete_rows", "modify_external", "share_file", "post_update", "email_everyone"):
            for key in vc.NOT_WAIVED_WHEN_ACTING:
                d = copy.deepcopy(DRAFTER)
                d["action"] = action
                d["consent_policy"], d["rate_limit"] = "opted-in recipients only", "20 per run"
                d[key] = {"not_applicable": "a reason that sounds fine"}
                self.assertTrue(any(f"{key} cannot be marked not_applicable" in p for p in vc.validate(d)), (action, key))

    def test_inward_actions_and_other_fields_may_still_be_waived(self):
        for action in ("append_rows", "update_cell", "create_draft", "copy_file"):
            d = copy.deepcopy(INTERNAL)
            d["action"] = action
            self.assertEqual(vc.validate(d), [], action)
        d = copy.deepcopy(DRAFTER)
        d["action"] = "send_email"
        d["consent_policy"], d["rate_limit"] = "opted-in only", "20 per run"
        d["quota"] = {"not_applicable": "twenty emails a week is far below the limit"}
        self.assertEqual(vc.validate(d), [])                   # quota may be waived even when sending


class Decisions(unittest.TestCase):
    def test_decisions_are_required_and_must_be_a_non_empty_list(self):
        d = copy.deepcopy(INTERNAL)
        del d["decisions"]
        self.assertIn("missing decisions", vc.validate(d))
        for bad in ([], "x", {}, None, 5):
            d["decisions"] = bad
            self.assertIn("decisions must be a non-empty list: record each choice made with the user", vc.validate(d), bad)

    def test_each_decision_needs_topic_choice_and_reason(self):
        good = INTERNAL["decisions"][0]
        for drop in ("topic", "choice", "reason"):
            d = copy.deepcopy(INTERNAL)
            item = dict(good)
            del item[drop]
            d["decisions"] = [item]
            self.assertIn("decisions[0] needs topic, choice and reason as real text", vc.validate(d), drop)
        for item in ("text", 5, None, []):
            d = copy.deepcopy(INTERNAL)
            d["decisions"] = [item]
            self.assertIn("decisions[0] needs topic, choice and reason as real text", vc.validate(d))
        d = copy.deepcopy(INTERNAL)
        d["decisions"] = [dict(good, reason="TODO")]
        self.assertIn("decisions[0] needs topic, choice and reason as real text", vc.validate(d))

    def test_the_ai_recommends_and_only_the_user_decides(self):
        for who in ("ai", "assistant", "claude", "", None, 5, "User", "owner"):
            d = copy.deepcopy(INTERNAL)
            d["decisions"] = [dict(INTERNAL["decisions"][0], decided_by=who)]
            self.assertTrue(any("decided_by must be 'user' or 'user_after_ai_recommendation'" in p for p in vc.validate(d)), who)
        for who in vc.DECIDERS:
            d = copy.deepcopy(INTERNAL)
            d["decisions"] = [dict(INTERNAL["decisions"][0], decided_by=who)]
            self.assertEqual(vc.validate(d), [], who)

    def test_a_bad_decision_reports_the_right_index(self):
        d = copy.deepcopy(INTERNAL)
        d["decisions"] = [INTERNAL["decisions"][0], dict(INTERNAL["decisions"][1], decided_by="ai")]
        problems = vc.validate(d)
        self.assertTrue(any("decisions[1] decided_by" in p for p in problems))
        self.assertFalse(any("decisions[0]" in p for p in problems))


class DeploymentIsTheUsersDecision(unittest.TestCase):
    def deployed(self, status="DEPLOYED_UNVERIFIED", decisions=None):
        d = copy.deepcopy(INTERNAL)
        d.update(status=status, deployment_authorized=True, deployed_version="v1")
        d["decisions"] = INTERNAL["decisions"] + ([DEPLOY] if decisions is None else decisions)
        return d

    def test_a_deployed_status_needs_a_user_deployment_decision_with_a_quote(self):
        self.assertEqual(vc.validate(self.deployed()), [])
        msg = "a deployed status requires a decision with topic 'deployment' made by the user, with a quote of their words"
        d = self.deployed(decisions=[])
        self.assertIn(msg, vc.validate(d))
        for bad in (dict(DEPLOY, decided_by="ai"), dict(DEPLOY, quote=""), dict(DEPLOY, quote="TODO"),
                    {k: v for k, v in DEPLOY.items() if k != "quote"}, dict(DEPLOY, topic="routing"),
                    dict(DEPLOY, decided_by=None)):
            self.assertIn(msg, vc.validate(self.deployed(decisions=[bad])), bad)

    def test_the_topic_match_ignores_case_and_spacing_only(self):
        for topic in ("Deployment", "  DEPLOYMENT  ", "deployment"):
            self.assertEqual(vc.validate(self.deployed(decisions=[dict(DEPLOY, topic=topic)])), [], topic)
        self.assertIn("a deployed status requires", " ".join(vc.validate(self.deployed(decisions=[dict(DEPLOY, topic="deploy")]))))

    def test_both_deployed_statuses_need_it_and_designed_does_not(self):
        for status in ("DEPLOYED_UNVERIFIED", "VERIFIED_IN_SCOPE"):
            d = self.deployed(status=status, decisions=[])
            self.assertTrue(any("a deployed status requires a decision" in p for p in vc.validate(d)), status)
        self.assertEqual(vc.validate(INTERNAL), [])

    def test_the_decision_record_does_not_change_the_receipt_hash(self):
        before = vc.contract_hash(INTERNAL)
        d = copy.deepcopy(INTERNAL)
        d["decisions"] = d["decisions"] + [DEPLOY]
        self.assertEqual(vc.contract_hash(d), before)


if __name__ == "__main__":
    unittest.main()


class WorkingMode(unittest.TestCase):
    """Careful or fast is the user's switch. Fast needs a shown warning and their words, and it
    relaxes nothing else the validator checks."""

    def doc(self, *modes):
        d = copy.deepcopy(DRAFTER)
        d["decisions"] = [x for x in d["decisions"] if x["topic"] != "working_mode"] + list(modes)
        return d

    def fast(self, **over):
        m = {"topic": "working_mode", "choice": "fast", "reason": "I want a draft quickly", "decided_by": "user",
             "warning_shown": True, "quote": "I understand, fast please."}
        m.update(over)
        return m

    def test_missing_mode_is_rejected(self):
        self.assertTrue(any("working_mode" in p for p in vc.validate(self.doc())))

    def test_two_modes_are_rejected(self):
        d = self.doc(self.fast(), {**self.fast(), "choice": "careful"})
        self.assertTrue(any("exactly one working_mode" in p for p in vc.validate(d)))

    def test_unknown_mode_is_rejected(self):
        d = self.doc({**self.fast(), "choice": "yolo"})
        self.assertTrue(any("'careful' or 'fast'" in p for p in vc.validate(d)))

    def test_fast_with_warning_and_quote_is_valid(self):
        self.assertEqual(vc.validate(self.doc(self.fast())), [])

    def test_fast_without_a_quote_is_rejected(self):
        m = self.fast()
        del m["quote"]
        self.assertTrue(any("warning" in p for p in vc.validate(self.doc(m))))

    def test_fast_without_warning_shown_is_rejected(self):
        self.assertTrue(any("warning" in p for p in vc.validate(self.doc(self.fast(warning_shown=False)))))

    def test_ai_cannot_choose_the_mode(self):
        self.assertTrue(any("decided_by" in p for p in vc.validate(self.doc(self.fast(decided_by="ai")))))

    def test_fast_does_not_relax_the_safety_checks(self):
        d = self.doc(self.fast())
        d["dry_run"] = False
        d["status"] = "DEPLOYED_UNVERIFIED"
        d["deployed_version"] = "1"
        d["deployment_authorized"] = True
        problems = vc.validate(d)
        self.assertTrue(any("dry_run" in p for p in problems))
        self.assertTrue(any("'deployment'" in p for p in problems))

    def test_choice_is_case_insensitive(self):
        self.assertEqual(vc.validate(self.doc(self.fast(choice="FAST"))), [])
