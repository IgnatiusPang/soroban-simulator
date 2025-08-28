
import unittest
from soroban_simulator.soroban.parser import Parser

class TestParser(unittest.TestCase):
    """Tests for the Parser class."""

    def test_simple_expression(self):
        """Tests a simple expression without parentheses."""
        parser = Parser()
        rpn = parser.generate_rpn("1 + 2")
        self.assertEqual(rpn, [1, 2, '+'])

    def test_expression_with_parentheses(self):
        """Tests an expression with parentheses."""
        parser = Parser()
        rpn = parser.generate_rpn("(1 + 2) * 3")
        self.assertEqual(rpn, [1, 2, '+', 3, '*'])

    def test_operator_precedence(self):
        """Tests an expression with different operator precedence."""
        parser = Parser()
        rpn = parser.generate_rpn("1 + 2 * 3")
        self.assertEqual(rpn, [1, 2, 3, '*', '+'])

    def test_mismatched_parentheses(self):
        """Tests that mismatched parentheses raise an error."""
        parser = Parser()
        with self.assertRaises(ValueError):
            parser.generate_rpn("(1 + 2")

if __name__ == '__main__':
    unittest.main()
