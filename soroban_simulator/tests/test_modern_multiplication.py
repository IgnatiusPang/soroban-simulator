import unittest
from soroban_simulator.soroban.soroban import Soroban

class TestModernMultiplication(unittest.TestCase):
    def test_multiply_57_by_6(self):
        soroban = Soroban(13)
        steps = soroban.set_number(57)
        steps.extend(soroban.multiply(6))
        self.assertEqual(soroban.get_value(), 342)

    def test_multiply_43_by_21(self):
        soroban = Soroban(13)
        steps = soroban.set_number(43)
        steps.extend(soroban.multiply(21))
        self.assertEqual(soroban.get_value(), 903)

if __name__ == '__main__':
    unittest.main()
