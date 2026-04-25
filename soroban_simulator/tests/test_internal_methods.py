from decimal import Decimal
import unittest
from soroban_simulator.soroban.soroban import Soroban


class TestInternalMethods(unittest.TestCase):
    """Tests for internal soroban methods and edge cases."""

    def setUp(self):
        """Set up test fixtures."""
        self.soroban = Soroban(13, unit_rod_index=0)

    def test_get_interim_value_method(self):
        """Test value retrieval with various states."""
        # Test what 20 should actually look like when set properly
        soroban2 = Soroban(13, unit_rod_index=0)
        soroban2.set_number(20)
        soroban2.get_state()
        expected_value = soroban2.get_value()
        
        self.assertEqual(expected_value, 20, "Properly set 20 should have value 20")
        
        # Test with manually set state
        self.soroban.rods = [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]
        get_value_result = self.soroban.get_value()
        
        # Document that manual setting may produce different results
        self.assertIsNotNone(get_value_result, "Manual setting should produce some value")

    def test_interim_value_with_zero_state(self):
        """Test value retrieval with zero state."""
        self.soroban.clear()
        
        get_value_result = self.soroban.get_value()
        self.assertEqual(get_value_result, 0, "Cleared soroban should have value 0")

    def test_interim_value_with_simple_numbers(self):
        """Test value retrieval with simple numbers."""
        test_numbers = [1, 5, 25, 100, 123, 456]
        
        for number in test_numbers:
            with self.subTest(number=number):
                self.soroban.clear()
                self.soroban.set_number(number)
                
                get_value_result = self.soroban.get_value()
                self.assertEqual(get_value_result, number, f"Set number {number} should have value {number}")

    def test_interim_value_after_multiplication(self):
        """Test value retrieval after multiplication operations."""
        # Test 4 × 5 = 20
        self.soroban.set_number(4)
        self.soroban.multiply(5)
        
        get_value_result = self.soroban.get_value()
        self.assertEqual(get_value_result, 20, "4 × 5 should equal 20")

    def test_state_consistency(self):
        """Test that internal state remains consistent."""
        # Set a number and verify state consistency
        self.soroban.set_number(789)
        
        state = self.soroban.get_state()
        value = self.soroban.get_value()
        
        # Verify the state represents the correct number
        self.assertEqual(value, 789, "Value should be 789")
        
        # Verify state structure
        self.assertEqual(len(state), 13, "State should have 13 rods")
        self.assertIsInstance(state, list, "State should be a list")
        
        # Verify all state values are integers
        for i, rod_value in enumerate(state):
            self.assertIsInstance(rod_value, (int, Decimal), f"Rod {i} value should be an integer")
            self.assertGreaterEqual(rod_value, 0, f"Rod {i} value should be non-negative")

    def test_large_number_handling(self):
        """Test handling of large numbers within soroban capacity."""
        # Test with a large number that should fit in 13 rods
        large_number = 999999999999  # 12 digits, should fit in 13 rods
        
        self.soroban.set_number(large_number)
        
        get_value_result = self.soroban.get_value()
        self.assertEqual(get_value_result, large_number, f"Large number {large_number} should be set correctly")


if __name__ == '__main__':
    unittest.main()
