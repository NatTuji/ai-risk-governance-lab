"""Scenario baselines are expectations, not copies of engine output."""

import copy
from pathlib import Path
import unittest

from ai_risk_lab.engine import assess
from ai_risk_lab.model import load_use_case, validate_use_case
from tests.cases import add_component, add_flow, basic_case


def run_assessment(case):
    return assess(validate_use_case(case))


def finding_ids(report):
    return {finding["id"] for finding in report["findings"]}


class BaselineTests(unittest.TestCase):
    def test_committed_support_assistant_has_manually_reviewed_expected_categories(self):
        example = Path(__file__).resolve().parents[1] / "examples" / "support-assistant.json"
        report = assess(load_use_case(example))
        self.assertEqual(
            finding_ids(report),
            {"ARGL-001", "ARGL-002", "ARGL-003", "ARGL-004"},
        )
        self.assertEqual(
            {(b["source"], b["target"], b["data_classification"]) for b in report["trust_boundaries"]},
            {
                ("customer", "portal", "personal"),
                ("portal", "model", "personal"),
                ("model", "portal", "internal"),
            },
        )
        self.assertTrue(report["review_required"])

    def test_basic_model_requires_output_evaluation_only(self):
        report = run_assessment(basic_case())
        self.assertEqual(finding_ids(report), {"ARGL-004"})
        self.assertEqual(report["trust_boundaries"], [])

    def test_sensitive_untrusted_agent_has_five_candidate_categories(self):
        case = basic_case()
        add_component(case, "documents", "data_store", "external")
        add_component(case, "ticket_tool", "tool")
        add_flow(case, "documents", "app", "personal", True)
        add_flow(case, "model", "ticket_tool")
        case["consequential_decisions"] = True
        report = run_assessment(case)
        self.assertEqual(
            finding_ids(report),
            {"ARGL-001", "ARGL-002", "ARGL-003", "ARGL-004", "ARGL-005"},
        )
        self.assertEqual(len(report["trust_boundaries"]), 1)
        boundary = report["trust_boundaries"][0]
        self.assertEqual((boundary["source"], boundary["target"]), ("documents", "app"))
        self.assertEqual((boundary["source_zone"], boundary["target_zone"]), ("external", "internal"))

    def test_empty_findings_do_not_mean_deployment_approval(self):
        case = basic_case()
        case["components"] = case["components"][:1]
        case["data_flows"] = []
        report = run_assessment(case)
        self.assertEqual(report["findings"], [])
        self.assertTrue(report["review_required"])
        self.assertEqual(report["decision"], "human_review_required")
        self.assertTrue(report["limitations"])
        self.assertTrue(report["evidence_gates"])
        self.assertTrue(report["inaction_review"])

    def test_consequential_nonmodel_workflow_still_requires_accountability(self):
        case = basic_case()
        case["components"] = case["components"][:1]
        case["data_flows"] = []
        case["consequential_decisions"] = True
        self.assertEqual(finding_ids(run_assessment(case)), {"ARGL-005"})

    def test_declared_controls_do_not_lower_priority_or_accept_risk(self):
        case = basic_case()
        case["data_flows"][0]["untrusted"] = True
        before = run_assessment(case)
        case["controls"] = [
            {"id": control_id, "status": "implemented", "evidence": "Synthetic unverified claim"}
            for control_id in (
                "human_review", "access_control", "data_minimization", "output_validation",
                "monitoring", "incident_response", "supplier_review",
            )
        ]
        after = run_assessment(case)
        self.assertEqual(finding_ids(before), finding_ids(after))
        self.assertEqual(
            {f["id"]: f["priority"] for f in before["findings"]},
            {f["id"]: f["priority"] for f in after["findings"]},
        )
        self.assertTrue(after["review_required"])
        for finding in after["findings"]:
            self.assertEqual(finding["residual_risk"], "not_assessed")

    def test_candidate_scenarios_include_traceable_basis_and_limits(self):
        case = basic_case()
        case["data_flows"][0]["untrusted"] = True
        for finding in run_assessment(case)["findings"]:
            with self.subTest(finding=finding["id"]):
                self.assertEqual(finding["scenario_status"], "hypothesis")
                self.assertEqual(finding["residual_risk"], "not_assessed")
                self.assertIn(finding["priority"], {"high", "medium"})
                for field in (
                    "priority_rationale", "scenario", "trigger_facts", "framework_references",
                    "recommended_controls", "evidence_required",
                ):
                    self.assertTrue(finding[field], field)
                for reference in finding["framework_references"]:
                    self.assertTrue(reference["framework"])
                    self.assertTrue(reference["reference"])
                    self.assertTrue(reference["url"].startswith("https://"))

    def test_assessment_is_reproducible_and_does_not_mutate_input(self):
        case = validate_use_case(basic_case())
        original = copy.deepcopy(case)
        self.assertEqual(assess(case), assess(case))
        self.assertEqual(case, original)


class GraphTests(unittest.TestCase):
    def test_untrusted_source_reaches_model_through_application(self):
        case = basic_case()
        add_component(case, "documents", "data_store", "external")
        add_flow(case, "documents", "app", untrusted=True)
        report = run_assessment(case)
        finding = next(f for f in report["findings"] if f["id"] == "ARGL-001")
        self.assertEqual(finding["attack_path"], ["documents", "app", "model"])

    def test_disconnected_untrusted_flow_does_not_reach_model(self):
        case = basic_case()
        add_component(case, "archive", "data_store")
        add_component(case, "reader", "application")
        add_flow(case, "archive", "reader", untrusted=True)
        self.assertNotIn("ARGL-001", finding_ids(run_assessment(case)))

    def test_cycle_with_model_path_terminates_and_finds_reachability(self):
        case = basic_case()
        add_component(case, "retriever", "application")
        add_component(case, "documents", "data_store")
        add_flow(case, "documents", "retriever", untrusted=True)
        add_flow(case, "retriever", "documents")
        add_flow(case, "retriever", "app")
        self.assertIn("ARGL-001", finding_ids(run_assessment(case)))

    def test_cycle_without_model_path_does_not_invent_reachability(self):
        case = basic_case()
        add_component(case, "archive", "data_store")
        add_component(case, "reader", "application")
        add_flow(case, "archive", "reader", untrusted=True)
        add_flow(case, "reader", "archive")
        self.assertNotIn("ARGL-001", finding_ids(run_assessment(case)))

    def test_disconnected_tool_does_not_imply_model_authority(self):
        case = basic_case()
        add_component(case, "ticket_tool", "tool")
        self.assertNotIn("ARGL-003", finding_ids(run_assessment(case)))

    def test_tool_path_can_pass_through_application(self):
        case = basic_case()
        add_component(case, "executor", "application")
        add_component(case, "ticket_tool", "tool")
        add_flow(case, "model", "executor")
        add_flow(case, "executor", "ticket_tool")
        report = run_assessment(case)
        finding = next(f for f in report["findings"] if f["id"] == "ARGL-003")
        self.assertEqual(finding["attack_path"], ["model", "executor", "ticket_tool"])

    def test_sensitive_internal_flow_and_public_boundary_do_not_trigger_sensitive_rule(self):
        for classification, zone in (("personal", "internal"), ("public", "external")):
            with self.subTest(classification=classification, zone=zone):
                case = basic_case()
                case["data_flows"][0]["data_classification"] = classification
                case["components"][1]["trust_zone"] = zone
                self.assertNotIn("ARGL-002", finding_ids(run_assessment(case)))

    def test_confidential_and_personal_boundaries_require_review(self):
        for classification in ("confidential", "personal"):
            with self.subTest(classification=classification):
                case = basic_case()
                case["data_flows"][0]["data_classification"] = classification
                case["components"][1]["trust_zone"] = "vendor"
                self.assertIn("ARGL-002", finding_ids(run_assessment(case)))


if __name__ == "__main__":
    unittest.main()
