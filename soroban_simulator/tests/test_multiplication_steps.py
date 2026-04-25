import unittest
from soroban_simulator.soroban.calculator import Calculator


class TestMultiplicationSteps(unittest.TestCase):
    """Test that multiplication steps don't include unnecessary initial number setting steps."""

    def setUp(self):
        self.calculator = Calculator()

    def test_multiplication_123_times_456_steps(self):
        """Test that 123 * 456 doesn't include initial number setting steps."""
        steps = self.calculator.calculate("123 * 456")
        step_descriptions = [step.step_description for step in steps]
        
        # Print all steps for debugging
        print("\nAll steps for 123 * 456:")
        for i, desc in enumerate(step_descriptions):
            print(f"{i+1}: {desc}")
        
        # These steps should NOT be present in multiplication
        # These are the specific initial setup steps we want to avoid
        unwanted_steps = [
            "Setting number: 123",
            "Finished setting 123"
        ]
        
        # Also check that we don't have the initial clearing step that comes with set_number
        # The "Clear the soroban" step should not appear after "Setting number: 123"
        setting_index = -1
        clear_index = -1
        for i, desc in enumerate(step_descriptions):
            if desc == "Setting number: 123":
                setting_index = i
            elif desc == "Clear the soroban" and setting_index != -1 and i > setting_index:
                clear_index = i
                break
        
        self.assertEqual(setting_index, -1, "Should not have 'Setting number: 123' step")
        self.assertEqual(clear_index, -1, "Should not have 'Clear the soroban' step after setting number")
        
        for unwanted_step in unwanted_steps:
            self.assertNotIn(unwanted_step, step_descriptions, 
                           f"Unwanted step found: '{unwanted_step}'")
        
        # These steps SHOULD be present
        expected_steps = [
            "Set multiplier 456",
            "Set multiplicand 123"
        ]
        
        for expected_step in expected_steps:
            self.assertIn(expected_step, step_descriptions,
                         f"Expected step missing: '{expected_step}'")

    def test_simple_multiplication_5_times_7_steps(self):
        """Test that 5 * 7 doesn't include initial number setting steps."""
        steps = self.calculator.calculate("5 * 7")
        step_descriptions = [step.step_description for step in steps]
        
        # Print all steps for debugging
        print("\nAll steps for 5 * 7:")
        for i, desc in enumerate(step_descriptions):
            print(f"{i+1}: {desc}")
        
        # These steps should NOT be present - focus on the initial setup steps we want to avoid
        unwanted_steps = [
            "Setting number: 5",
            "Finished setting 5"
        ]
        
        # Check that we don't have the initial clearing step that comes with set_number
        # The "Clear the soroban" step should not appear after "Setting number: 5"
        setting_index = -1
        clear_index = -1
        for i, desc in enumerate(step_descriptions):
            if desc == "Setting number: 5":
                setting_index = i
            elif desc == "Clear the soroban" and setting_index != -1 and i > setting_index:
                clear_index = i
                break
        
        self.assertEqual(setting_index, -1, "Should not have 'Setting number: 5' step")
        self.assertEqual(clear_index, -1, "Should not have 'Clear the soroban' step after setting number")
        
        for unwanted_step in unwanted_steps:
            self.assertNotIn(unwanted_step, step_descriptions,
                           f"Unwanted step found: '{unwanted_step}'")
        
        # These steps SHOULD be present
        expected_steps = [
            "Set multiplier 7",
            "Set multiplicand 5"
        ]
        
        for expected_step in expected_steps:
            self.assertIn(expected_step, step_descriptions,
                         f"Expected step missing: '{expected_step}'")

    def test_addition_still_includes_setting_steps(self):
        """Test that addition operations still include initial number setting steps."""
        steps = self.calculator.calculate("123 + 456")
        step_descriptions = [step.step_description for step in steps]
        
        # For addition, we should still have the initial setting steps
        expected_steps = [
            "Set number 123"
        ]
        
        for expected_step in expected_steps:
            self.assertIn(expected_step, step_descriptions,
                         f"Expected step missing in addition: '{expected_step}'")


if __name__ == '__main__':
    unittest.main()
