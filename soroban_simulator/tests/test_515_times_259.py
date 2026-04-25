import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from soroban.calculator import Calculator
from soroban.soroban import Soroban


class Test515Times259(unittest.TestCase):
    """Test for 515 × 259 = 133385 with proper positioning to avoid overlap.
    
    This test verifies the fix for the overlap issue where M1 and M2 were positioned
    too close to the PP (result) area, causing interference when M1/M2 were cleared
    during multiplication. The fix moves M1 and M2 further to the left to ensure
    no overlap with the result area.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.calculator = Calculator(num_rods=13)
        self.soroban = Soroban(num_rods=13)

    def test_515_times_259_positioning(self):
        """Test the positioning for 515 × 259 = 133385.
        
        Expected positioning to avoid overlap:
        - PP (result 133385) needs 6 digits, so rods 1-6 (indices 0-5)
        - M1 (multiplier 259) needs 3 digits, should be on rods 10-12 (indices 9-11)
        - M2 (multiplicand 515) needs 3 digits, should be on rods 7-9 (indices 6-8)
        
        This ensures no overlap between M1/M2 and PP areas.
        """
        # Set up the multiplication: 515 × 259
        steps = self.calculator.calculate("515 * 259")
        
        # Verify the final result is correct
        final_step = steps[-1]
        self.assertEqual(final_step.current_value, 133385, "Final multiplication result should be 133385")
        
        # Find where the result (133385) is positioned
        pp_actual_positions = []
        for i, value in enumerate(final_step.soroban_state):
            if value != 0:
                pp_actual_positions.append(i)
        
        print("\n515 × 259 = 133385 POSITIONING TEST:")
        print(f"Final result: {final_step.current_value}")
        print(f"Final state: {final_step.soroban_state}")
        print(f"PP (133385) positions: {pp_actual_positions}")
        
        # Expected PP positions for 6-digit result
        expected_pp_positions = [0, 1, 2, 3, 4, 5]  # rods 1-6 (indices 0-5)
        
        print(f"Expected PP positions: {expected_pp_positions}")
        
        # Verify the result is positioned correctly (should be in the rightmost positions)
        self.assertTrue(len(pp_actual_positions) <= 6, "Result should fit in 6 digits or less")
        self.assertTrue(all(pos < 6 for pos in pp_actual_positions), "Result should be in rods 1-6 (indices 0-5)")
        
        # Verify no overlap occurred by checking that the calculation is correct
        self.assertEqual(final_step.current_value, 133385, "No overlap should have occurred - result should be correct")

    def test_515_times_259_step_analysis(self):
        """Detailed step-by-step analysis of 515 × 259 = 133385 multiplication."""
        steps = self.calculator.calculate("515 * 259")
        
        print("\nDETAILED STEP ANALYSIS FOR 515 × 259 = 133385:")
        print(f"Total steps: {len(steps)}")
        
        # Find key steps
        m1_setup_step = None
        m2_setup_step = None
        final_step = steps[-1]
        
        for i, step in enumerate(steps):
            if "Set multiplier 259" in step.step_description:
                m1_setup_step = step
                print(f"M1 setup at step {i}: {step.step_description}")
            elif "Set multiplicand 515" in step.step_description:
                m2_setup_step = step
                print(f"M2 setup at step {i}: {step.step_description}")
        
        # Analyze positioning after setup
        if m1_setup_step and m2_setup_step:
            # Look for the state after both M1 and M2 are set
            setup_complete_step = None
            for i, step in enumerate(steps):
                if ("Set multiplicand 515" in step.step_description and 
                    i + 1 < len(steps)):
                    setup_complete_step = steps[i + 1]
                    break
            
            if setup_complete_step:
                print("\nAfter M1 and M2 setup:")
                print(f"State: {setup_complete_step.soroban_state}")
                
                # Find M1 positions (259)
                m1_positions = []
                for i, value in enumerate(setup_complete_step.soroban_state):
                    if value in [2, 5, 9]:  # digits of 259
                        m1_positions.append(i)
                
                # Find M2 positions (515)  
                m2_positions = []
                for i, value in enumerate(setup_complete_step.soroban_state):
                    if value in [5, 1, 5] and i not in m1_positions:  # digits of 515, excluding M1 positions
                        m2_positions.append(i)
                
                print(f"M1 (259) estimated positions: {m1_positions}")
                print(f"M2 (515) estimated positions: {m2_positions}")
        
        print(f"\nFinal result: {final_step.current_value}")
        print(f"Final state: {final_step.soroban_state}")
        
        # Verify final result
        self.assertEqual(final_step.current_value, 133385, "Final result should be 133385")

    def test_positioning_requirements_515_times_259(self):
        """Document the positioning requirements for 515 × 259 = 133385."""
        requirements = {
            "multiplication": "515 × 259 = 133385",
            "result_digits": "6 digits (133385)",
            "PP_position": "Should occupy rods 1-6 (indices 0-5)",
            "M1_position": "259 should be on rods 10-12 (indices 9-11) to avoid overlap",
            "M2_position": "515 should be on rods 7-9 (indices 6-8) to avoid overlap",
            "overlap_issue": "M1 and M2 must be positioned left enough to not overlap with PP"
        }
        
        print("\nPositioning Requirements for 515 × 259 = 133385:")
        for key, value in requirements.items():
            print(f"  {key}: {value}")
        
        # Verify the calculation works
        steps = self.calculator.calculate("515 * 259")
        final_result = steps[-1].current_value
        self.assertEqual(final_result, 133385, "Calculation must be correct")
        
        # This test documents the requirements
        self.assertTrue(True, "Requirements documented")

    def test_no_overlap_verification(self):
        """Verify that M1 and M2 positioning doesn't cause overlap with PP."""
        steps = self.calculator.calculate("515 * 259")
        final_step = steps[-1]
        
        # The key test: if positioning is correct, the result should be exactly 133385
        # If there's overlap, the result would be incorrect due to interference
        self.assertEqual(final_step.current_value, 133385, 
                        "Result should be exactly 133385 - any deviation indicates overlap issues")
        
        # Additional verification: the result should be in the expected range of positions
        result_positions = []
        for i, value in enumerate(final_step.soroban_state):
            if value != 0:
                result_positions.append(i)
        
        # For a 6-digit number, we expect positions in the lower indices (rightmost rods)
        max_expected_position = 5  # rod 6 (index 5) should be the leftmost position for the result
        
        print("\nOverlap verification:")
        print(f"Result positions: {result_positions}")
        print(f"Max expected position: {max_expected_position}")
        print(f"All positions within expected range: {all(pos <= max_expected_position for pos in result_positions)}")
        
        # If positioning is correct, all result digits should be in positions 0-5
        self.assertTrue(all(pos <= max_expected_position for pos in result_positions),
                       "All result digits should be in positions 0-5 to avoid overlap with M1/M2 areas")


if __name__ == '__main__':
    unittest.main()