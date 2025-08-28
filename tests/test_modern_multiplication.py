import unittest
from soroban_simulator.soroban.soroban import Soroban

class TestModernMultiplication(unittest.TestCase):

    def test_57_times_6(self):
        soroban = Soroban(num_rods=13)
        # The walkthrough uses a 13-rod soroban (A-M)
        # Multiplier '6' on rod C
        # Multiplicand '57' on rods FG
        # Expected product '342' on rods GHI
        
        # This is a placeholder for the detailed steps.
        # For now, we'll just check the final value.
        
        steps = soroban.multiply(57, 6)
        self.assertEqual(soroban.get_value(), 342)

if __name__ == '__main__':
    unittest.main()
