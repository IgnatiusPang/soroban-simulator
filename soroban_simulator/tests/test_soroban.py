
import unittest
from soroban_simulator.soroban.soroban import Soroban

class TestSoroban(unittest.TestCase):
    """Tests for the Soroban class."""

    def test_set_number(self):
        """Tests that the set_number method correctly sets a number."""
        soroban = Soroban()
        soroban.set_number(123)
        self.assertEqual(soroban.get_value(), 123)

    def test_add(self):
        """Tests that the add method correctly adds two numbers."""
        soroban = Soroban()
        soroban.set_number(123)
        soroban.add(456)
        self.assertEqual(soroban.get_value(), 579)

    def test_subtract(self):
        """Tests that the subtract method correctly subtracts two numbers."""
        soroban = Soroban()
        soroban.set_number(579)
        soroban.subtract(456)
        self.assertEqual(soroban.get_value(), 123)

    def test_subtract_with_borrow(self):
        """Tests that the subtract method correctly subtracts with borrowing."""
        soroban = Soroban()
        soroban.set_number(521)
        soroban.subtract(132)
        self.assertEqual(soroban.get_value(), 389)

if __name__ == '__main__':
    unittest.main()
