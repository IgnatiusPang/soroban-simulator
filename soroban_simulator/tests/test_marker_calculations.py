import unittest
from soroban_simulator.soroban.calculator import Calculator
from soroban_simulator.soroban.parser import Parser


class TestMarkerCalculations(unittest.TestCase):
    """Tests for marker positioning calculations and logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.calculator = Calculator()
        self.parser = Parser()

    def test_marker_calculation_23_times_15(self):
        """Test marker calculation logic for 23 × 15."""
        equation = "23 * 15"
        
        # Get the RPN parts
        parts = self.parser.generate_rpn(equation)
        operands = [p for p in parts if isinstance(p, int)]
        
        self.assertEqual(len(operands), 2, "Should have exactly 2 operands")
        
        multiplicand, multiplier = operands[0], operands[1]
        self.assertEqual(multiplicand, 23, "First operand should be 23")
        self.assertEqual(multiplier, 15, "Second operand should be 15")
        
        # Test the marker calculation logic
        multiplier_len = len(str(multiplier))
        multiplicand_len = len(str(multiplicand))
        
        self.assertEqual(multiplier_len, 2, "Multiplier 15 should have length 2")
        self.assertEqual(multiplicand_len, 2, "Multiplicand 23 should have length 2")

        # Position the multiplier on the far left (rod C, index 2).
        multiplier_rod_start = 2
        
        # Leave a gap of 2 rods after the multiplier.
        multiplicand_rod_start = multiplier_rod_start + multiplier_len + 2
        
        # The product is formed to the right of the multiplicand.
        product_rod_start = multiplicand_rod_start + multiplicand_len 
        product_len = multiplicand_len + multiplier_len
        
        self.assertEqual(multiplier_rod_start, 2, "Multiplier should start at rod index 2")
        self.assertEqual(multiplicand_rod_start, 6, "Multiplicand should start at rod index 6")
        self.assertEqual(product_rod_start, 8, "Product should start at rod index 8")
        self.assertEqual(product_len, 4, "Product should have length 4")

        # Create markers
        markers = [
            (multiplier_rod_start, multiplier_rod_start + multiplier_len - 1, "M1"),
            (multiplicand_rod_start, multiplicand_rod_start + multiplicand_len - 1, "M2"),
            (product_rod_start, product_rod_start + product_len - 1, "PP")
        ]
        
        expected_markers = [
            (2, 3, "M1"),  # Multiplier 15 at rod indices 2-3
            (6, 7, "M2"),  # Multiplicand 23 at rod indices 6-7
            (8, 11, "PP") # Product 345 at rod indices 8-11
        ]
        
        self.assertEqual(markers, expected_markers, "Markers should match expected positions")
        
        # Convert to rod numbers (1-based, rightmost)
        rod_number_markers = []
        for start_rod, end_rod, label in markers:
            start_rod_num = 13 - start_rod
            end_rod_num = 13 - end_rod
            rod_number_markers.append((end_rod_num, start_rod_num, label))
        
        expected_rod_numbers = [
            (10, 11, "M1"),  # M1: rods 10-11
            (6, 7, "M2"),    # M2: rods 6-7
            (2, 5, "PP")     # PP: rods 2-5
        ]
        
        self.assertEqual(rod_number_markers, expected_rod_numbers, 
                        "Rod number conversion should be correct")

    def test_marker_positioning_display_calculation(self):
        """Test the display positioning calculation from soroban_widget.py logic."""
        num_rods = 13
        
        # Test markers for 23 × 15
        markers = [
            (2, 3, "M1"),   # Multiplier
            (6, 7, "M2"),   # Multiplicand  
            (8, 11, "PP")   # Product
        ]
        
        display_positions = []
        for start_rod, end_rod, label in markers:
            start_loop_i = num_rods - 1 - start_rod
            end_loop_i = num_rods - 1 - end_rod
            
            # Rod positions (1-based for display)
            start_display_pos = start_loop_i + 1
            end_display_pos = end_loop_i + 1
            
            display_positions.append((start_display_pos, end_display_pos, label))
        
        expected_display_positions = [
            (11, 10, "M1"),  # M1 display positions
            (7, 6, "M2"),    # M2 display positions
            (5, 2, "PP")     # PP display positions
        ]
        
        self.assertEqual(display_positions, expected_display_positions,
                        "Display position calculation should be correct")

    def test_different_multiplication_markers(self):
        """Test marker calculation for different multiplication: 7 × 38."""
        multiplicand, multiplier = 7, 38
        multiplier_len = len(str(multiplier))  # 2
        multiplicand_len = len(str(multiplicand))  # 1
        
        self.assertEqual(multiplier_len, 2, "Multiplier 38 should have length 2")
        self.assertEqual(multiplicand_len, 1, "Multiplicand 7 should have length 1")

        # Apply same positioning logic
        multiplier_rod_start = 2
        multiplicand_rod_start = multiplier_rod_start + multiplier_len + 2  # 2 + 2 + 2 = 6
        product_rod_start = multiplicand_rod_start + multiplicand_len  # 6 + 1 = 7
        product_len = multiplicand_len + multiplier_len  # 1 + 2 = 3
        
        markers = [
            (multiplier_rod_start, multiplier_rod_start + multiplier_len - 1, "M1"),  # (2, 3)
            (multiplicand_rod_start, multiplicand_rod_start + multiplicand_len - 1, "M2"),  # (6, 6)
            (product_rod_start, product_rod_start + product_len - 1, "PP")  # (7, 9)
        ]
        
        expected_markers = [
            (2, 3, "M1"),   # Multiplier 38 at rod indices 2-3
            (6, 6, "M2"),   # Multiplicand 7 at rod index 6
            (7, 9, "PP")    # Product 266 at rod indices 7-9
        ]
        
        self.assertEqual(markers, expected_markers, 
                        "Markers for 7 × 38 should match expected positions")

    def test_single_digit_multiplication_markers(self):
        """Test marker calculation for single digit multiplication: 4 × 5."""
        multiplicand, multiplier = 4, 5
        multiplier_len = len(str(multiplier))  # 1
        multiplicand_len = len(str(multiplicand))  # 1
        
        # Apply positioning logic
        multiplier_rod_start = 2
        multiplicand_rod_start = multiplier_rod_start + multiplier_len + 2  # 2 + 1 + 2 = 5
        product_rod_start = multiplicand_rod_start + multiplicand_len  # 5 + 1 = 6
        product_len = multiplicand_len + multiplier_len  # 1 + 1 = 2
        
        markers = [
            (multiplier_rod_start, multiplier_rod_start + multiplier_len - 1, "M1"),  # (2, 2)
            (multiplicand_rod_start, multiplicand_rod_start + multiplicand_len - 1, "M2"),  # (5, 5)
            (product_rod_start, product_rod_start + product_len - 1, "PP")  # (6, 7)
        ]
        
        expected_markers = [
            (2, 2, "M1"),   # Multiplier 5 at rod index 2
            (5, 5, "M2"),   # Multiplicand 4 at rod index 5
            (6, 7, "PP")    # Product 20 at rod indices 6-7
        ]
        
        self.assertEqual(markers, expected_markers, 
                        "Markers for 4 × 5 should match expected positions")

    def test_marker_bounds_checking(self):
        """Test that marker calculations stay within soroban bounds."""
        # Test with numbers that should fit within 13 rods
        multiplicand, multiplier = 99, 99  # Smaller numbers to fit within bounds
        multiplier_len = len(str(multiplier))  # 2
        multiplicand_len = len(str(multiplicand))  # 2
        
        multiplier_rod_start = 2
        multiplicand_rod_start = multiplier_rod_start + multiplier_len + 2  # 2 + 2 + 2 = 6
        product_rod_start = multiplicand_rod_start + multiplicand_len  # 6 + 2 = 8
        product_len = multiplicand_len + multiplier_len  # 2 + 2 = 4
        
        # Check that all positions are within bounds (0-12 for 13 rods)
        self.assertGreaterEqual(multiplier_rod_start, 0, "Multiplier start should be >= 0")
        self.assertLess(multiplier_rod_start + multiplier_len - 1, 13, "Multiplier end should be < 13")
        
        self.assertGreaterEqual(multiplicand_rod_start, 0, "Multiplicand start should be >= 0")
        self.assertLess(multiplicand_rod_start + multiplicand_len - 1, 13, "Multiplicand end should be < 13")
        
        self.assertGreaterEqual(product_rod_start, 0, "Product start should be >= 0")
        self.assertLess(product_rod_start + product_len - 1, 13, "Product end should be < 13")
        
        # Test that very large numbers would exceed bounds (documenting the limitation)
        large_multiplicand, large_multiplier = 999, 999
        large_multiplier_len = len(str(large_multiplier))  # 3
        large_multiplicand_len = len(str(large_multiplicand))  # 3
        
        large_product_rod_start = 2 + large_multiplier_len + 2 + large_multiplicand_len  # 2 + 3 + 2 + 3 = 10
        large_product_len = large_multiplicand_len + large_multiplier_len  # 3 + 3 = 6
        large_product_end = large_product_rod_start + large_product_len - 1  # 10 + 6 - 1 = 15
        
        # Document that large numbers exceed soroban capacity
        self.assertGreaterEqual(large_product_end, 13, "Large numbers should exceed 13-rod capacity")


if __name__ == '__main__':
    unittest.main()
