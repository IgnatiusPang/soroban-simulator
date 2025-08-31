
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

    def test_unsupported_token(self):
        """Tests that an unsupported token raises a ValueError."""
        calculator = Calculator()
        with self.assertRaises(ValueError):
            calculator.calculate("1 / 2")

if __name__ == '__main__':
    unittest.main()
