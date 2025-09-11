
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

    def test_division_operator_recognition(self):
        """Tests that the division operator is recognized and parsed correctly."""
        parser = Parser()
        rpn = parser.generate_rpn("10 / 2")
        self.assertEqual(rpn, [10, 2, '/'])

    def test_division_precedence_same_as_multiplication(self):
        """Tests that division has the same precedence as multiplication."""
        parser = Parser()
        # Division and multiplication should be evaluated left-to-right
        rpn = parser.generate_rpn("12 * 3 / 4")
        self.assertEqual(rpn, [12, 3, '*', 4, '/'])
        
        rpn = parser.generate_rpn("12 / 3 * 4")
        self.assertEqual(rpn, [12, 3, '/', 4, '*'])

    def test_division_precedence_over_addition_subtraction(self):
        """Tests that division has higher precedence than addition and subtraction."""
        parser = Parser()
        rpn = parser.generate_rpn("1 + 12 / 3")
        self.assertEqual(rpn, [1, 12, 3, '/', '+'])
        
        rpn = parser.generate_rpn("20 - 15 / 3")
        self.assertEqual(rpn, [20, 15, 3, '/', '-'])

    def test_left_to_right_associativity_with_division(self):
        """Tests left-to-right associativity for same-precedence operators including division."""
        parser = Parser()
        # Multiple divisions should be evaluated left-to-right
        rpn = parser.generate_rpn("100 / 5 / 2")
        self.assertEqual(rpn, [100, 5, '/', 2, '/'])
        
        # Mixed multiplication and division should be evaluated left-to-right
        rpn = parser.generate_rpn("8 * 3 / 2 * 4")
        self.assertEqual(rpn, [8, 3, '*', 2, '/', 4, '*'])

    def test_complex_expression_with_division(self):
        """Tests complex expressions involving division with parentheses."""
        parser = Parser()
        rpn = parser.generate_rpn("(20 + 15) / 5 - 2")
        self.assertEqual(rpn, [20, 15, '+', 5, '/', 2, '-'])
        
        rpn = parser.generate_rpn("100 / (10 - 5) + 3")
        self.assertEqual(rpn, [100, 10, 5, '-', '/', 3, '+'])

    def test_division_with_spaces_and_without_spaces(self):
        """Tests that division works with and without spaces around the operator."""
        parser = Parser()
        rpn_with_spaces = parser.generate_rpn("951 / 3")
        rpn_without_spaces = parser.generate_rpn("951/3")
        self.assertEqual(rpn_with_spaces, [951, 3, '/'])
        self.assertEqual(rpn_without_spaces, [951, 3, '/'])

if __name__ == '__main__':
    unittest.main()
