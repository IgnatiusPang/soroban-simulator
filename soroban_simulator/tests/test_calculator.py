from decimal import Decimal

import unittest
from soroban_simulator.soroban.calculator import Calculator

class TestCalculator(unittest.TestCase):
    """Tests for the Calculator class."""

    def test_simple_calculation(self):
        """Tests a simple calculation."""
        calculator = Calculator()
        steps = calculator.calculate("10 + 5")
        final_value = steps[-1].current_value
        self.assertEqual(final_value, 15)

    def test_multiplication(self):
        """Tests a simple multiplication."""
        calculator = Calculator()
        steps = calculator.calculate("10 * 5")
        final_value = steps[-1].current_value
        self.assertEqual(final_value, 50)

    def test_invalid_expression_not_enough_operands(self):
        """Tests that an invalid expression with not enough operands raises a ValueError."""
        calculator = Calculator()
        with self.assertRaises(ValueError):
            calculator.calculate("1 +")

    def test_invalid_expression_final_stack_not_one(self):
        """Tests that an invalid expression with too many numbers raises a ValueError."""
        calculator = Calculator()
        with self.assertRaises(ValueError):
            calculator.calculate("1 2")

    def test_division(self):
        """Tests a simple division."""
        calculator = Calculator()
        steps = calculator.calculate("15 / 3")
        final_value = steps[-1].current_value
        self.assertEqual(final_value, 5)

    def test_division_with_remainder(self):
        """Tests division that results in a remainder."""
        calculator = Calculator()
        steps = calculator.calculate("17 / 3")
        final_value = steps[-1].current_value
        self.assertEqual(final_value, 5)  # 17 ÷ 3 = 5 remainder 2, but we expect quotient

    def test_division_in_complex_expression(self):
        """Tests division within a complex expression."""
        calculator = Calculator()
        steps = calculator.calculate("20 + 15 / 3 - 2")
        final_value = steps[-1].current_value
        self.assertEqual(final_value, 23)  # 20 + (15/3) - 2 = 20 + 5 - 2 = 23

    def test_division_by_zero_error(self):
        """Tests that division by zero raises a ValueError."""
        calculator = Calculator()
        with self.assertRaises(ValueError):
            calculator.calculate("10 / 0")

    def test_unsupported_token(self):
        """Tests that an unsupported token raises a ValueError."""
        calculator = Calculator()
        with self.assertRaises(ValueError):
            calculator.calculate("1 % 2")

if __name__ == '__main__':
    unittest.main()
