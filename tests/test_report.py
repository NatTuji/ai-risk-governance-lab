"""Report text must remain readable without permitting display manipulation."""

import unittest

from ai_risk_lab.model import ValidationError, validate_use_case
from ai_risk_lab.report import escape
from tests.cases import basic_case


class DisplayTests(unittest.TestCase):
    def test_plain_quotes_stay_readable_while_html_is_escaped(self):
        text = escape('Owner\'s "review" <script>')
        self.assertIn('Owner\'s "review"', text)
        self.assertIn('&lt;script&gt;', text)

    def test_direction_overrides_isolates_and_terminal_controls_are_rejected(self):
        for character in ('\u202e', '\u202d', '\u202a', '\u202b', '\u202c', '\u2066', '\u2067', '\u2068', '\u2069', '\x7f', '\x9b'):
            with self.subTest(codepoint=ord(character)):
                case = basic_case()
                case['name'] = 'Synthetic ' + character + 'declaration'
                with self.assertRaises(ValidationError):
                    validate_use_case(case)

    def test_normal_non_ascii_text_is_preserved(self):
        case = basic_case()
        case['name'] = 'Évaluation نموذج'
        self.assertEqual(validate_use_case(case)['name'], case['name'])
