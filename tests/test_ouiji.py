import unittest
import conch.ouiji as ouiji

class TestDivide(unittest.TestCase):
    def assertDivide(self, expected):
        string = "\n".join("\n".join(par) for par in expected)
        divide = ouiji._divide(string)
        self.assertEqual(expected, divide)

    def test_empty_string(self):
        self.assertDivide([[""]])

    def test_single_line_whitespace(self):
        self.assertDivide([["   "]])

    def test_multiline_no_whitespace(self):
        self.assertDivide([["abc", "def", "ghi"]])

    def test_multiline_with_nonblank_whitespace_only_line(self):
        self.assertDivide([["abc", "   ", "ghi"]])

    def test_multiparagraph(self):
        self.assertDivide([["abc", ""], ["ghi"]])

    def test_two_blank_lines(self):
        self.assertDivide([["abc", "", ""], ["ghi"]])

    def test_trailing_blank_line(self):
        self.assertDivide([["abc", ""], ["ghi", ""]])

    def test_initial_blank_line(self):
        self.assertDivide([[""], ["ghi"]])


