from decimal import Decimal
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

    def test_51_times_3(self):
        """Tests 51 * 3 = 153.
        
        Note: This test currently fails due to a bug in the soroban multiplication
        algorithm. The calculator returns 180 instead of the correct answer 153.
        This test documents the expected behavior and should pass once the bug is fixed.
        """
        calculator = Calculator()
        steps = calculator.calculate("51 * 3")
        final_value = steps[-1].current_value
        # TODO: Fix multiplication bug - currently returns 180 instead of 153
        self.assertEqual(final_value, 153, 
                        f"Expected 153 but got {final_value}. "
                        f"There appears to be a bug in the soroban multiplication algorithm.")
