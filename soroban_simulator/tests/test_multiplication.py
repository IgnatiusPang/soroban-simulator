import unittest
from soroban_simulator.soroban.calculator import Calculator

class TestMultiplication(unittest.TestCase):
    """Tests for the multiplication functionality."""

    def test_multiply_by_zero(self):
        """Tests multiplication by zero."""
        calculator = Calculator()
        steps = calculator.calculate("10 * 0")
        final_value = steps[-1].current_value
        self.assertEqual(final_value, 0)

    def test_multiply_by_one(self):
        """Tests multiplication by one."""
        calculator = Calculator()
        steps = calculator.calculate("10 * 1")
        final_value = steps[-1].current_value
        self.assertEqual(final_value, 10)

    def test_large_multiplication(self):
        """Tests a larger multiplication."""
        calculator = Calculator()
        steps = calculator.calculate("12 * 12")
        final_value = steps[-1].current_value
        self.assertEqual(final_value, 144)

    def test_complex_multiplication(self):
        """Tests a more complex multiplication problem."""
        calculator = Calculator()
        steps = calculator.calculate("43 * 21")
        final_value = steps[-1].current_value
        self.assertEqual(final_value, 903)
