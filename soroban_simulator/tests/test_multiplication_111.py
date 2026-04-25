from decimal import Decimal
import unittest
from soroban_simulator.soroban.soroban import Soroban

class TestMultiplication111(unittest.TestCase):
    def test_multiply_111_by_111(self):
        """Test multiplication of 111 × 111 = 12321"""
        soroban = Soroban(13)
        steps = soroban.set_number(111)
        steps.extend(soroban.multiply(111))
        # The result should be in the partial products area
        result = soroban._get_partial_products_value()
        self.assertEqual(result, 12321)
        
        # Validate that we have proper step descriptions
        step_descriptions = [step.step_description for step in steps]
        self.assertTrue(any("111" in desc for desc in step_descriptions))
        
        # Validate that markers are present in multiplication steps
        multiplication_steps = [step for step in steps if step.markers]
        self.assertTrue(len(multiplication_steps) > 0, "Should have steps with markers")
        
        # Check that markers follow the expected pattern
        for step in multiplication_steps:
            for marker in step.markers:
                start_rod, end_rod, label, color = marker
                self.assertIsInstance(start_rod, (int, Decimal))
                self.assertIsInstance(end_rod, (int, Decimal))
                self.assertIn(label, ["M1", "M2", "PP"])
                self.assertIsInstance(color, str)
                self.assertTrue(start_rod <= end_rod)

if __name__ == '__main__':
    unittest.main()
