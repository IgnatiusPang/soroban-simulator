import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from soroban.soroban import Soroban

class TestModernMultiplication(unittest.TestCase):
    def test_multiply_57_by_6(self):
        soroban = Soroban(13, unit_rod_index=0)
        steps = soroban.set_number(57)
        steps.extend(soroban.multiply(6))
        self.assertEqual(soroban.get_value(), 342)

    def test_multiply_43_by_21(self):
        soroban = Soroban(13, unit_rod_index=0)
        steps = soroban.set_number(43)
        steps.extend(soroban.multiply(21))
        self.assertEqual(soroban.get_value(), 903)

    def test_multiply_4_by_5(self):
        """Test 4*5 = 20 with expected result: 0 in ones place and 2 in tens place."""
        soroban = Soroban(13, unit_rod_index=0)
        steps = soroban.set_number(4)
        steps.extend(soroban.multiply(5))
        
        # The multiplication algorithm now correctly calculates 4*5 = 20
        self.assertEqual(soroban.get_value(), 20, "4 * 5 should equal 20")
        
        # With the corrected positioning logic, the result should have:
        # - 0 in the ones place (rod 1, index 0)
        # - 2 in the tens place (rod 2, index 1)
        expected_state = [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(soroban.get_state(), expected_state, "Should have 0 in ones place (index 0), 2 in tens place (index 1)")

if __name__ == '__main__':
    unittest.main()
