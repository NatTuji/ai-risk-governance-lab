"""Exercise real process boundaries, JSON parsing, and file safety."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tests.cases import basic_case


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.input = self.directory / "case.json"
        self.input.write_text(json.dumps(basic_case()), encoding="utf-8")

    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, "-m", "ai_risk_lab", *map(str, arguments)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

    def test_json_report_round_trip(self):
        result = self.run_cli("assess", self.input, "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["decision"], "human_review_required")
        self.assertEqual({f["id"] for f in report["findings"]}, {"ARGL-004"})
        self.assertEqual(result.stderr, "")

    def test_default_report_is_readable_markdown(self):
        result = self.run_cli("assess", self.input)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Synthetic document assistant", result.stdout)
        self.assertIn("ARGL-004", result.stdout)
        self.assertIn("#", result.stdout)

    def test_committed_sample_report_matches_cli_output(self):
        input_path = PROJECT_ROOT / "examples" / "support-assistant.json"
        sample_path = PROJECT_ROOT / "examples" / "support-assistant.assessment.md"
        result = self.run_cli("assess", input_path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, sample_path.read_text(encoding="utf-8"))

    def test_can_write_new_report_file(self):
        output = self.directory / "report.json"
        result = self.run_cli("assess", self.input, "--format", "json", "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(output.read_text(encoding="utf-8"))
        self.assertTrue(report["review_required"])

    def test_existing_file_is_preserved(self):
        output = self.directory / "report.md"
        output.write_text("existing assessment", encoding="utf-8")
        result = self.run_cli("assess", self.input, "--output", output)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(output.read_text(encoding="utf-8"), "existing assessment")
        self.assertNotIn("Traceback", result.stderr)

    def test_input_file_cannot_be_overwritten(self):
        original = self.input.read_bytes()
        result = self.run_cli("assess", self.input, "--output", self.input)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.input.read_bytes(), original)

    def test_missing_input_has_actionable_error_without_traceback(self):
        result = self.run_cli("assess", self.directory / "missing.json")
        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stderr.strip())
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_invalid_utf8_is_reported_cleanly(self):
        self.input.write_bytes(b"\xff\xfe invalid JSON")
        result = self.run_cli("assess", self.input)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_unknown_field_diagnostic_does_not_emit_terminal_escape(self):
        case = basic_case()
        case["\x1b[31mspoofed"] = True
        self.input.write_text(json.dumps(case), encoding="utf-8")
        result = self.run_cli("assess", self.input)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("\x1b", result.stderr)
        self.assertIn("unknown fields", result.stderr)

    def test_json_syntax_and_schema_errors_fail_before_report(self):
        invalid_documents = (
            "{",
            "[]",
            '{"schema_version":"1.0"}',
            json.dumps({**basic_case(), "consequential_decisions": 1}),
        )
        for raw in invalid_documents:
            with self.subTest(raw=raw[:60]):
                self.input.write_text(raw, encoding="utf-8")
                result = self.run_cli("assess", self.input)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_json_fields_are_rejected(self):
        raw = json.dumps(basic_case())
        raw = raw[:-1] + ', "consequential_decisions": true}'
        self.input.write_text(raw, encoding="utf-8")
        result = self.run_cli("assess", self.input)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")

    def test_nested_duplicate_component_field_is_rejected(self):
        raw = json.dumps(basic_case()).replace('"id": "app"', '"id": "app", "id": "model"', 1)
        self.input.write_text(raw, encoding="utf-8")
        result = self.run_cli("assess", self.input)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)

    def test_nonstandard_json_constants_are_rejected(self):
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                raw = json.dumps(basic_case()).replace('"Synthetic review team"', constant)
                self.input.write_text(raw, encoding="utf-8")
                result = self.run_cli("assess", self.input)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("Traceback", result.stderr)

    def test_large_input_is_rejected_before_parsing(self):
        self.input.write_bytes(b" " * (1024 * 1024 + 1))
        result = self.run_cli("assess", self.input)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_escaped_unpaired_surrogate_is_reported_cleanly(self):
        case = basic_case()
        case["name"] = "bad\ud800text"
        self.input.write_text(json.dumps(case), encoding="utf-8")
        result = self.run_cli("assess", self.input)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_unknown_output_format_is_rejected(self):
        result = self.run_cli("assess", self.input, "--format", "html")
        self.assertEqual(result.returncode, 2)

    def test_untrusted_html_is_not_emitted_as_active_markup(self):
        case = basic_case()
        case["name"] = '<img src="x" onerror="alert(1)">'
        self.input.write_text(json.dumps(case), encoding="utf-8")
        result = self.run_cli("assess", self.input)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("<img", result.stdout)
        self.assertIn("&lt;img", result.stdout)

    def test_untrusted_markdown_cannot_add_heading_or_remote_image(self):
        case = basic_case()
        case["purpose"] = "Declared purpose\n\n## Deployment approved\n![tracker](https://example.invalid/pixel)"
        self.input.write_text(json.dumps(case), encoding="utf-8")
        result = self.run_cli("assess", self.input)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("\n## Deployment approved\n", result.stdout)
        self.assertNotIn("![tracker](", result.stdout)


if __name__ == "__main__":
    unittest.main()
