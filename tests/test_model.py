"""Validate declarations before they influence risk rules."""

import copy
import unittest

from ai_risk_lab.model import ValidationError, validate_use_case
from tests.cases import basic_case


class ModelTests(unittest.TestCase):
    def assert_invalid(self, case):
        with self.assertRaises(ValidationError):
            validate_use_case(case)

    def test_valid_case(self):
        case = basic_case()
        self.assertEqual(validate_use_case(case), case)

    def test_validation_returns_independent_copy(self):
        case = basic_case()
        result = validate_use_case(case)
        result["components"][0]["name"] = "Changed after validation"
        self.assertEqual(case["components"][0]["name"], "Assistant")

    def test_required_top_level_fields(self):
        for field in basic_case():
            with self.subTest(field=field):
                case = basic_case()
                del case[field]
                self.assert_invalid(case)

    def test_unknown_fields_at_all_levels(self):
        for level in ("root", "component", "flow", "control"):
            with self.subTest(level=level):
                case = basic_case()
                case["controls"] = [{"id": "human_review", "status": "planned"}]
                target = {
                    "root": case,
                    "component": case["components"][0],
                    "flow": case["data_flows"][0],
                    "control": case["controls"][0],
                }[level]
                target["unexpected"] = "silently ignoring this could change meaning"
                self.assert_invalid(case)

    def test_root_must_be_object(self):
        for value in (None, [], "case", 1, True):
            with self.subTest(value=value):
                self.assert_invalid(value)

    def test_schema_version_is_explicit(self):
        for version in ("2.0", 1.0, None):
            with self.subTest(version=version):
                case = basic_case()
                case["schema_version"] = version
                self.assert_invalid(case)

    def test_text_fields_are_nonempty_strings(self):
        for field in ("name", "purpose", "business_value", "owner"):
            for invalid in ("", " \n\t", None, 0, True, "x" * 4001):
                with self.subTest(field=field, value=repr(invalid)[:30]):
                    case = basic_case()
                    case[field] = invalid
                    self.assert_invalid(case)

    def test_boolean_flags_reject_numbers_and_strings(self):
        for invalid in (0, 1, "false", None):
            for field in ("consequential_decisions", "untrusted"):
                with self.subTest(field=field, value=invalid):
                    case = basic_case()
                    target = case if field == "consequential_decisions" else case["data_flows"][0]
                    target[field] = invalid
                    self.assert_invalid(case)

    def test_invalid_unicode_surrogates_and_terminal_escape_are_rejected(self):
        for invalid in ("bad\ud800text", "bad\udffftext", "\x1b[31mfalse evidence"):
            with self.subTest(value=repr(invalid)):
                case = basic_case()
                case["name"] = invalid
                self.assert_invalid(case)

    def test_components_are_nonempty_and_bounded(self):
        case = basic_case()
        case["components"] = []
        self.assert_invalid(case)
        case = basic_case()
        case["components"] = [
            {"id": f"c{i}", "name": f"Component {i}", "kind": "application", "trust_zone": "internal"}
            for i in range(51)
        ]
        self.assert_invalid(case)

    def test_component_ids_are_unique_and_constrained(self):
        case = basic_case()
        case["components"].append(copy.deepcopy(case["components"][0]))
        self.assert_invalid(case)
        for component_id in ("", "Model", "a b", "../app", "a" * 65):
            with self.subTest(component_id=component_id):
                case = basic_case()
                case["components"][0]["id"] = component_id
                self.assert_invalid(case)

    def test_component_kind_and_zone_are_validated(self):
        for field, invalid in (("kind", "database"), ("trust_zone", " "), ("name", 4)):
            with self.subTest(field=field):
                case = basic_case()
                case["components"][0][field] = invalid
                self.assert_invalid(case)

    def test_flow_endpoints_must_exist(self):
        for field in ("source", "target"):
            with self.subTest(field=field):
                case = basic_case()
                case["data_flows"][0][field] = "missing"
                self.assert_invalid(case)

    def test_flow_classification_is_not_free_text(self):
        case = basic_case()
        case["data_flows"][0]["data_classification"] = "probably safe"
        self.assert_invalid(case)

    def test_flow_count_is_bounded(self):
        case = basic_case()
        case["data_flows"] *= 201
        self.assert_invalid(case)

    def test_controls_require_supported_unique_ids_and_statuses(self):
        for controls in (
            [{"id": "unknown", "status": "planned"}],
            [{"id": "human_review", "status": "verified"}],
            [{"id": "human_review", "status": "implemented", "evidence": 42}],
            [{"id": "human_review", "status": "planned"}] * 2,
        ):
            with self.subTest(controls=controls):
                case = basic_case()
                case["controls"] = controls
                self.assert_invalid(case)

    def test_optional_control_evidence_defaults_to_empty_text(self):
        case = basic_case()
        case["controls"] = [{"id": "human_review", "status": "planned"}]
        result = validate_use_case(case)
        self.assertEqual(result["controls"][0]["evidence"], "")


if __name__ == "__main__":
    unittest.main()
