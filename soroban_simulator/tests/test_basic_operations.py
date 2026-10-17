import unittest
from soroban_simulator.soroban.soroban import Soroban


class TestBasicOperations(unittest.TestCase):
    """Tests for basic soroban operations including number setting and rod ordering."""

    def setUp(self):
        """Set up test fixtures."""
        self.soroban = Soroban(13, unit_rod_index=0)

    def test_4_times_5_detailed(self):
        """Test 4×5 multiplication with detailed step tracking."""
        # Set the number 4
        self.soroban.set_number(4)
        self.assertEqual(self.soroban.get_value(), 4)
        
        # Multiply by 5 and track each step
        multiply_steps = self.soroban.multiply(5)
        
        # Verify we have steps
        self.assertGreater(len(multiply_steps), 0, "Multiplication should produce steps")
        
        # Verify final result
        self.assertEqual(self.soroban.get_value(), 20, "4 × 5 should equal 20")
        
        # Verify each step has required attributes
        for step in multiply_steps:
            self.assertIsNotNone(step.step_description, "Each step should have a description")
            self.assertIsNotNone(step.soroban_state, "Each step should have a state")
            self.assertIsNotNone(step.current_value, "Each step should have a current value")

    def test_4_times_5_simple(self):
        """Test simple 4×5 multiplication."""
        steps = self.soroban.set_number(4)
        self.assertEqual(self.soroban.get_value(), 4)
        
        steps.extend(self.soroban.multiply(5))
        self.assertEqual(self.soroban.get_value(), 20)

    def test_rod_ordering_with_123(self):
        """Test soroban rod ordering with number 123.
        
        This test verifies that:
        - Rod 1 (rightmost, index 0) contains the 1's place
        - Rod 2 (index 1) contains the 10's place  
        - Rod 3 (index 2) contains the 100's place
        """
        self.soroban.set_number(123)
        state = self.soroban.get_state()
        value = self.soroban.get_value()
        
        self.assertEqual(value, 123, "Value should be 123")
        
        # Check the positions - 123 should have:
        # - 3 in 1's place (index 0)
        # - 2 in 10's place (index 1)
        # - 1 in 100's place (index 2)
        self.assertEqual(state[0], 3, "Rod 1 (index 0, rightmost) should contain 3 (1's place)")
        self.assertEqual(state[1], 2, "Rod 2 (index 1) should contain 2 (10's place)")
        self.assertEqual(state[2], 1, "Rod 3 (index 2) should contain 1 (100's place)")
        
        # Verify other positions are zero
        for i in range(3, 13):
            self.assertEqual(state[i], 0, f"Rod {i+1} (index {i}) should be zero")

    def test_rod_numbering_system(self):
        """Test the rod numbering system understanding."""
        # Test with a simple number to verify rod positions
        self.soroban.set_number(5)
        state = self.soroban.get_state()
        
        # 5 should be in the 1's place (index 0, rod 1)
        self.assertEqual(state[0], 5, "Single digit 5 should be in rod 1 (index 0)")
        
        # Test with 50
        self.soroban.clear()
        self.soroban.set_number(50)
        state = self.soroban.get_state()
        
        # 50 should have 5 in the 10's place (index 1, rod 2)
        self.assertEqual(state[1], 5, "50 should have 5 in rod 2 (index 1, 10's place)")
        self.assertEqual(state[0], 0, "50 should have 0 in rod 1 (index 0, 1's place)")

    def test_clear_operation(self):
        """Test clearing the soroban."""
        self.soroban.set_number(123)
        self.assertEqual(self.soroban.get_value(), 123)
        
        self.soroban.clear()
        self.assertEqual(self.soroban.get_value(), 0)
        
        # All rods should be zero
        state = self.soroban.get_state()
        for i, value in enumerate(state):
            self.assertEqual(value, 0, f"Rod {i+1} should be zero after clear")

    def test_negative_guards(self):
        """Test that negative numbers are rejected on Soroban."""
        with self.assertRaises(ValueError):
            self.soroban.set_number(-5)

        with self.assertRaises(ValueError):
            self.soroban.add(-5)

        with self.assertRaises(ValueError):
            self.soroban.subtract(-5)

    def test_capacity_guards(self):
        """Test capacity limits for addition and multiplication."""
        from soroban_simulator.soroban.soroban import Soroban
        small = Soroban(3)
        small.set_number(999)
        with self.assertRaises(ValueError):
            small.add(1)

        with self.assertRaises(ValueError):
            small.add(1000)

        # Test small soroban multiplication succeeds within capacity
        s7 = Soroban(7)
        s7.multiply(3, 2)
        self.assertEqual(s7.get_value(), 6)

        # Test small soroban multiplication exceeds capacity
        with self.assertRaises(ValueError):
            s7.multiply(12345, 67890)

    def test_initialization_bounds(self):
        """Test validation of num_rods and unit_rod_index."""
        from soroban_simulator.soroban.soroban import Soroban
        with self.assertRaises(ValueError):
            Soroban(num_rods=0)
        with self.assertRaises(ValueError):
            Soroban(num_rods=-5)
        with self.assertRaises(ValueError):
            Soroban(num_rods=5, unit_rod_index=-1)
        with self.assertRaises(ValueError):
            Soroban(num_rods=5, unit_rod_index=5)

    def test_get_value_empty_rods(self):
        """Test get_value handles empty rods without AttributeError."""
        from decimal import Decimal
        from soroban_simulator.soroban.soroban import Soroban
        s = Soroban(1)
        s.rods = []
        self.assertEqual(s.get_value(), Decimal(0))


if __name__ == '__main__':
    unittest.main()

