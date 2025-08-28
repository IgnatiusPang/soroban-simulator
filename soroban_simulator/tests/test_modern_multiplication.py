import unittest
from soroban_simulator.soroban.soroban import Soroban

class TestModernMultiplication(unittest.TestCase):

    def test_57_times_6(self):
        soroban = Soroban(num_rods=13)
        soroban.set_number(57)
        steps = soroban.multiply(6)
        self.assertEqual(soroban.get_value(), 342)

    def test_43_times_21(self):
        soroban = Soroban(num_rods=13)
        soroban.set_number(43)
        steps = soroban.multiply(21)
        self.assertEqual(soroban.get_value(), 903)

if __name__ == '__main__':
    unittest.main()
