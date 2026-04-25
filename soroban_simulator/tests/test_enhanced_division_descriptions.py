from decimal import Decimal
import unittest
from soroban_simulator.soroban.soroban import Soroban


class TestEnhancedDivisionDescriptions(unittest.TestCase):
    """Tests for enhanced step descriptions and visual feedback in division operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.soroban = Soroban(13)

    def test_enhanced_step_descriptions_basic_division(self):
        """Test that enhanced step descriptions are present in basic division.
        
        This test verifies that the enhanced step descriptions include:
        - Visual cues (emojis and symbols)
        - Educational explanations
        - Clear process indicators
        
        Requirements: 6.1, 6.2
        """
        dividend = 951
        divisor = 3
        
        steps = self.soroban.divide(dividend, divisor)
        
        # Collect all step descriptions
        descriptions = [step.step_description for step in steps]
        combined_text = " ".join(descriptions)
        
        # Test for visual cues and enhanced formatting
        visual_cues = ["🔢", "📥", "🧮", "✖️", "➖", "🎉", "✅", "🏗️", "🔵", "🟢"]
        found_visual_cues = [cue for cue in visual_cues if cue in combined_text]
        self.assertGreater(len(found_visual_cues), 5, 
                          f"Should have multiple visual cues, found: {found_visual_cues}")
        
        # Test for enhanced process indicators
        process_indicators = ["ESTIMATE", "MULTIPLY", "SUBTRACT", "WORKSPACE SETUP", "DIVISION COMPLETE"]
        found_indicators = [indicator for indicator in process_indicators if indicator in combined_text]
        self.assertGreater(len(found_indicators), 3,
                          f"Should have process indicators, found: {found_indicators}")
        
        # Test for educational content
        educational_keywords = ["reasoning", "mental", "calculation", "role", "meaning"]
        found_educational = [keyword for keyword in educational_keywords if keyword.lower() in combined_text.lower()]
        self.assertGreater(len(found_educational), 2,
                          f"Should have educational content, found: {found_educational}")

    def test_estimation_reasoning_explanations(self):
        """Test detailed explanations for estimation reasoning.
        
        This test verifies that estimation steps include detailed reasoning
        that explains the mental process used to arrive at estimates.
        
        Requirements: 6.2, 6.3
        """
        test_cases = [
            (951, 3, "single-digit divisor"),
            (3869, 53, "multi-digit divisor"),
            (100, 7, "round number"),
        ]
        
        for dividend, divisor, description in test_cases:
            with self.subTest(dividend=dividend, divisor=divisor, desc=description):
                self.soroban.clear()
                steps = self.soroban.divide(dividend, divisor)
                
                # Find estimation steps
                estimation_steps = [step for step in steps if "ESTIMATE" in step.step_description]
                reasoning_steps = [step for step in steps if "Reasoning" in step.step_description or "reasoning" in step.step_description]
                
                self.assertGreater(len(estimation_steps), 0, 
                                 f"Should have estimation steps for {description}")
                self.assertGreater(len(reasoning_steps), 0,
                                 f"Should have reasoning explanations for {description}")
                
                # Verify reasoning content quality
                for step in reasoning_steps:
                    desc = step.step_description
                    self.assertIn("💭", desc, "Reasoning should have thinking emoji")
                    # Should contain mathematical explanation
                    contains_math = any(op in desc for op in ["÷", "×", "≈", "="])
                    self.assertTrue(contains_math, f"Reasoning should contain mathematical operations: {desc}")

    def test_revision_process_visual_cues(self):
        """Test visual cues for revision processes.
        
        This test verifies that revision processes (overestimate and underestimate
        corrections) include clear visual cues and explanations.
        
        Requirements: 6.3, 6.4
        """
        # Use a case that's likely to require revisions
        dividend = 259
        divisor = 7
        
        steps = self.soroban.divide(dividend, divisor)
        descriptions = [step.step_description for step in steps]
        combined_text = " ".join(descriptions)
        
        # Look for revision indicators
        revision_indicators = ["OVERESTIMATE", "UNDERESTIMATE", "REVISION", "COMPENSATION"]
        found_revisions = [indicator for indicator in revision_indicators if indicator in combined_text]
        
        # Test revision visual cues
        revision_visual_cues = ["🚨", "❌", "🔄", "⬇️", "⬆️", "✅"]
        found_revision_cues = [cue for cue in revision_visual_cues if cue in combined_text]
        
        # If revisions occurred, verify they have proper visual cues
        if found_revisions:
            self.assertGreater(len(found_revision_cues), 0,
                             f"Revision processes should have visual cues, found revisions: {found_revisions}")
            
            # Verify revision explanations
            revision_explanations = ["Problem:", "Solution:", "Analysis:", "Comparison:"]
            found_explanations = [exp for exp in revision_explanations if exp in combined_text]
            self.assertGreater(len(found_explanations), 0,
                             f"Should have revision explanations, found: {found_explanations}")

    def test_workspace_setup_descriptions(self):
        """Test enhanced workspace setup descriptions.
        
        This test verifies that workspace setup includes clear explanations
        of rod positioning, Kojima's rules, and area purposes.
        
        Requirements: 6.1
        """
        dividend = 951
        divisor = 3
        
        steps = self.soroban.divide(dividend, divisor)
        
        # Find workspace setup steps (including role explanations)
        setup_steps = [step for step in steps if any(keyword in step.step_description for keyword in 
                      ["WORKSPACE", "PLACEMENT", "role:", "READY", "Layout"])]
        self.assertGreater(len(setup_steps), 0, "Should have workspace setup steps")
        
        setup_descriptions = [step.step_description for step in setup_steps]
        combined_setup_text = " ".join(setup_descriptions)
        
        # Test for workspace components
        workspace_components = ["DIVISOR", "DIVIDEND", "quotient", "Layout"]
        found_components = [comp for comp in workspace_components if comp in combined_setup_text]
        self.assertGreaterEqual(len(found_components), 3,
                               f"Should mention workspace components, found: {found_components}")
        
        # Test for Kojima's rules mention
        kojima_indicators = ["Kojima", "Rule I", "Rule II"]
        found_kojima = [indicator for indicator in kojima_indicators if indicator in combined_setup_text]
        self.assertGreater(len(found_kojima), 0,
                          f"Should mention Kojima's rules, found: {found_kojima}")
        
        # Test for role explanations
        role_explanations = ["role:", "will be", "purpose"]
        found_roles = [role for role in role_explanations if role in combined_setup_text.lower()]
        self.assertGreater(len(found_roles), 0,
                          f"Should explain component roles, found: {found_roles}")

    def test_final_result_descriptions(self):
        """Test enhanced final result descriptions.
        
        This test verifies that final results include celebratory language,
        clear summaries, and educational explanations.
        
        Requirements: 6.1, 6.4
        """
        test_cases = [
            (951, 3, 0, "exact division"),  # 951 ÷ 3 = 317 remainder 0
            (100, 7, 2, "division with remainder"),  # 100 ÷ 7 = 14 remainder 2
        ]
        
        for dividend, divisor, expected_remainder, description in test_cases:
            with self.subTest(dividend=dividend, divisor=divisor, desc=description):
                self.soroban.clear()
                steps = self.soroban.divide(dividend, divisor)
                
                # Find final result steps
                final_steps = [step for step in steps if "COMPLETE" in step.step_description]
                self.assertGreater(len(final_steps), 0, f"Should have completion steps for {description}")
                
                final_descriptions = [step.step_description for step in final_steps]
                combined_final_text = " ".join(final_descriptions)
                
                # Test for celebratory language
                celebratory_cues = ["🎉", "🎯", "✨", "COMPLETE"]
                found_celebratory = [cue for cue in celebratory_cues if cue in combined_final_text]
                self.assertGreater(len(found_celebratory), 0,
                                 f"Should have celebratory language for {description}")
                
                # Test for result breakdown
                if expected_remainder == 0:
                    exact_indicators = ["exact", "Perfect", "evenly"]
                    found_exact = [indicator for indicator in exact_indicators if indicator.lower() in combined_final_text.lower()]
                    self.assertGreater(len(found_exact), 0,
                                     f"Should indicate exact division for {description}")
                else:
                    remainder_indicators = ["remainder", "breakdown", "Quotient"]
                    found_remainder = [indicator for indicator in remainder_indicators if indicator in combined_final_text]
                    self.assertGreater(len(found_remainder), 0,
                                     f"Should explain remainder for {description}")

    def test_step_description_completeness(self):
        """Test that all steps have non-empty, meaningful descriptions.
        
        This test verifies that every calculation step has a proper description
        that provides educational value.
        
        Requirements: 6.1, 6.2
        """
        dividend = 951
        divisor = 3
        
        steps = self.soroban.divide(dividend, divisor)
        
        # Verify all steps have descriptions
        for i, step in enumerate(steps):
            self.assertIsNotNone(step.step_description, f"Step {i} should have a description")
            self.assertIsInstance(step.step_description, str, f"Step {i} description should be string")
            self.assertGreater(len(step.step_description.strip()), 0, f"Step {i} description should not be empty")
            
            # Verify descriptions are meaningful (not just generic)
            desc = step.step_description.strip()
            self.assertGreater(len(desc), 10, f"Step {i} description should be meaningful: '{desc}'")
            
            # Should not be just numbers
            self.assertFalse(desc.isdigit(), f"Step {i} description should not be just numbers: '{desc}'")

    def test_educational_value_indicators(self):
        """Test that steps include educational value indicators.
        
        This test verifies that the enhanced descriptions include educational
        elements that help users understand the shojohou method.
        
        Requirements: 6.2, 6.3, 6.4
        """
        dividend = 3869
        divisor = 53
        
        steps = self.soroban.divide(dividend, divisor)
        descriptions = [step.step_description for step in steps]
        combined_text = " ".join(descriptions)
        
        # Test for educational indicators
        educational_indicators = [
            "Mental", "calculation", "approximation", "conservative",
            "Analysis", "reasoning", "explanation", "meaning",
            "Rule", "method", "process", "cycle"
        ]
        
        found_educational = [indicator for indicator in educational_indicators 
                           if indicator.lower() in combined_text.lower()]
        self.assertGreater(len(found_educational), 5,
                          f"Should have educational indicators, found: {found_educational}")
        
        # Test for process explanation
        process_words = ["estimate", "multiply", "subtract", "revise"]
        found_process = [word for word in process_words if word.lower() in combined_text.lower()]
        self.assertGreaterEqual(len(found_process), 3,
                               f"Should explain the shojohou process, found: {found_process}")
        
        # Test for mathematical terminology
        math_terms = ["quotient", "dividend", "divisor", "remainder", "product"]
        found_math = [term for term in math_terms if term.lower() in combined_text.lower()]
        self.assertGreater(len(found_math), 3,
                          f"Should use proper mathematical terminology, found: {found_math}")

    def test_step_description_consistency(self):
        """Test consistency in step description formatting and style.
        
        This test verifies that enhanced descriptions follow consistent
        formatting patterns and style guidelines.
        
        Requirements: 6.1
        """
        dividend = 951
        divisor = 3
        
        steps = self.soroban.divide(dividend, divisor)
        
        # Count different types of enhanced descriptions
        process_steps = 0
        visual_cue_steps = 0
        educational_steps = 0
        
        for step in steps:
            desc = step.step_description
            
            # Count process indicators (ALL CAPS words)
            if any(word.isupper() and len(word) > 3 for word in desc.split()):
                process_steps += 1
            
            # Count visual cues (emojis)
            if any(ord(char) > 127 for char in desc):  # Unicode characters (emojis)
                visual_cue_steps += 1
            
            # Count educational content
            educational_keywords = ["reasoning", "mental", "analysis", "explanation", "meaning", "rule"]
            if any(keyword.lower() in desc.lower() for keyword in educational_keywords):
                educational_steps += 1
        
        # Verify we have a good distribution of enhanced descriptions
        total_steps = len(steps)
        self.assertGreater(process_steps, total_steps * 0.1,  # At least 10% should have process indicators
                          f"Should have process indicators in {process_steps}/{total_steps} steps")
        self.assertGreater(visual_cue_steps, total_steps * 0.2,  # At least 20% should have visual cues
                          f"Should have visual cues in {visual_cue_steps}/{total_steps} steps")
        self.assertGreater(educational_steps, 0,  # Should have some educational content
                          f"Should have educational content in {educational_steps}/{total_steps} steps")


if __name__ == '__main__':
    unittest.main()