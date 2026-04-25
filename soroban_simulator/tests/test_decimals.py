import unittest
from decimal import Decimal
from soroban_simulator.soroban.soroban import Soroban
from soroban_simulator.soroban.calculator import Calculator

class TestDecimals(unittest.TestCase):
    def setUp(self):
        # Using default 13 rods, unit rod at index 3 (Rod 4)
        self.soroban = Soroban(13, unit_rod_index=3)
        self.calculator = Calculator(13)
        # Ensure calculator's soroban also has the same unit_rod_index
        self.calculator.soroban.unit_rod_index = 3

    def test_decimal_addition(self):
        # 1.2 + 3.45 = 4.65
        steps = self.calculator.calculate("1.2 + 3.45")
        self.assertEqual(steps[-1].current_value, Decimal("4.65"))
        
        # Check rod states: 1.2 -> Rod 4=1, Rod 3=2. 3.45 -> Rod 4=3, Rod 3=4, Rod 2=5.
        # Total: Rod 4=4, Rod 3=6, Rod 2=5.
        expected_rods = [0, 5, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(steps[-1].soroban_state, expected_rods)

    def test_decimal_subtraction(self):
        # 10.5 - 4.75 = 5.75
        steps = self.calculator.calculate("10.5 - 4.75")
        self.assertEqual(steps[-1].current_value, Decimal("5.75"))
        
        # 10.5: Rod 5=1, Rod 4=0, Rod 3=5.
        # 4.75: Rod 4=4, Rod 3=7, Rod 2=5.
        # 10.50 - 4.75 = 5.75
        # 5.75: Rod 4=5, Rod 3=7, Rod 2=5.
        expected_rods = [0, 5, 7, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(steps[-1].soroban_state, expected_rods)

    def test_integer_still_works_with_unit_rod(self):
        # 123 + 456 = 579
        # 123: Rod 6=1, Rod 5=2, Rod 4=3.
        # 456: Rod 6=4, Rod 5=5, Rod 4=6.
        # 579: Rod 6=5, Rod 5=7, Rod 4=9.
        steps = self.calculator.calculate("123 + 456")
        self.assertEqual(steps[-1].current_value, Decimal("579"))
        expected_rods = [0, 0, 0, 9, 7, 5, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(steps[-1].soroban_state, expected_rods)

    def test_decimal_multiplication(self):
        # 1.2 * 3.4 = 4.08
        # 1.2 scaled: Rod 4=1, Rod 3=2.
        # 3.4 scaled: Rod 4=3, Rod 3=4.
        # Result 4.08: Rod 4=4, Rod 3=0, Rod 2=8.
        steps = self.calculator.calculate("1.2 * 3.4")
        self.assertEqual(steps[-1].current_value, Decimal("4.08"))
        
        # 4.08: Rod 4=4, Rod 3=0, Rod 2=8.
        expected_rods = [0, 8, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(steps[-1].soroban_state, expected_rods)

if __name__ == '__main__':
    unittest.main()
