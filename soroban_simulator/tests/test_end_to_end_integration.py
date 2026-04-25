"""
End-to-End Integration Tests for Soroban Division

This module contains comprehensive integration tests that verify the complete
division functionality works correctly from input parsing through final result
calculation, including integration with other operations.

Requirements covered: 5.1, 5.2, 5.3
"""

import unittest
import time
from soroban_simulator.soroban.calculator import Calculator
from soroban_simulator.soroban.parser import Parser
from soroban_simulator.soroban.soroban import Soroban


class TestEndToEndDivisionIntegration(unittest.TestCase):
    """End-to-end integration tests for division functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.calculator = Calculator()
        self.parser = Parser()
        self.soroban = Soroban(13)

    def test_complete_division_expression_951_by_3(self):
        """Test complete division expression: 951/3 = 317.
        
        This test verifies the entire pipeline from string input to final result:
        - Parser recognises and converts "951/3" to RPN
        - Calculator processes the RPN correctly
        - Soroban division method produces correct result
        - All steps are generated with proper descriptions
        
        Requirements: 5.1, 5.2, 5.3
        """
        expression = "951/3"
        expected_result = 317
        
        # Test the complete pipeline
        steps = self.calculator.calculate(expression)
        
        # Verify we got steps
        self.assertIsInstance(steps, list, "Should return list of calculation steps")
        self.assertGreater(len(steps), 0, "Should generate calculation steps")
        
        # Verify final result
        final_step = steps[-1]
        self.assertEqual(final_step.current_value, expected_result,
                        f"951/3 should equal {expected_result}")
        
        # Verify step descriptions are present and meaningful
        for step in steps:
            self.assertIsInstance(step.step_description, str,
                                "Each step should have a description")
            self.assertGreater(len(step.step_description), 0,
                             "Step descriptions should not be empty")
        
        # Verify division-specific steps are present
        all_descriptions = " ".join([step.step_description for step in steps]).lower()
        self.assertIn("division", all_descriptions,
                     "Should mention division in step descriptions")
        self.assertIn("951", all_descriptions,
                     "Should mention dividend in step descriptions")
        self.assertIn("3", all_descriptions,
                     "Should mention divisor in step descriptions")

    def test_complete_division_expression_100_by_7(self):
        """Test complete division expression: 100/7 = 14 (with remainder).
        
        This test verifies division with remainder handling:
        - Correct quotient calculation (14)
        - Proper remainder handling (remainder 2)
        - Complete step generation for remainder scenarios
        
        Requirements: 5.1, 5.2, 5.3
        """
        expression = "100/7"
        expected_result = 14  # 100 ÷ 7 = 14 remainder 2
        
        # Test the complete pipeline
        steps = self.calculator.calculate(expression)
        
        # Verify we got steps
        self.assertIsInstance(steps, list, "Should return list of calculation steps")
        self.assertGreater(len(steps), 0, "Should generate calculation steps")
        
        # Verify final result (quotient)
        final_step = steps[-1]
        self.assertEqual(final_step.current_value, expected_result,
                        f"100/7 should equal {expected_result} (quotient)")
        
        # Verify remainder handling is mentioned in descriptions
        all_descriptions = " ".join([step.step_description for step in steps]).lower()
        self.assertIn("remainder", all_descriptions,
                     "Should mention remainder in step descriptions")

    def test_complete_division_expression_3869_by_53(self):
        """Test complete division expression with multi-digit divisor: 3869/53 = 73.
        
        This test verifies multi-digit divisor handling:
        - Proper multi-stage multiplication
        - Multi-stage subtraction
        - Correct final result
        
        Requirements: 5.1, 5.2, 5.3
        """
        expression = "3869/53"
        expected_result = 73  # 3869 ÷ 53 = 73
        
        # Test the complete pipeline
        steps = self.calculator.calculate(expression)
        
        # Verify we got steps
        self.assertIsInstance(steps, list, "Should return list of calculation steps")
        self.assertGreater(len(steps), 0, "Should generate calculation steps")
        
        # Verify final result
        final_step = steps[-1]
        self.assertEqual(final_step.current_value, expected_result,
                        f"3869/53 should equal {expected_result}")
        
        # Verify multi-digit divisor handling is present
        all_descriptions = " ".join([step.step_description for step in steps]).lower()
        self.assertIn("53", all_descriptions,
                     "Should mention multi-digit divisor in descriptions")

    def test_division_in_complex_expression_precedence(self):
        """Test division within complex expression: 20 + 15 / 3 - 2 = 23.
        
        This test verifies:
        - Correct operator precedence (division before addition/subtraction)
        - Proper RPN conversion and evaluation
        - Integration with addition and subtraction operations
        
        Requirements: 5.1, 5.2, 5.3
        """
        expression = "20 + 15 / 3 - 2"
        expected_result = 23  # 20 + (15/3) - 2 = 20 + 5 - 2 = 23
        
        # First verify parser handles precedence correctly
        rpn = self.parser.generate_rpn(expression)
        expected_rpn = [20, 15, 3, '/', '+', 2, '-']
        self.assertEqual(rpn, expected_rpn,
                        "Parser should handle division precedence correctly")
        
        # Test the complete pipeline
        steps = self.calculator.calculate(expression)
        
        # Verify final result
        final_step = steps[-1]
        self.assertEqual(final_step.current_value, expected_result,
                        f"{expression} should equal {expected_result}")
        
        # Verify all operations are present in descriptions
        all_descriptions = " ".join([step.step_description for step in steps]).lower()
        self.assertIn("division", all_descriptions,
                     "Should mention division operation")
        # Check for addition operation (may be described as "adding")
        addition_found = "addition" in all_descriptions or "adding" in all_descriptions
        self.assertTrue(addition_found,
                       "Should mention addition operation")
        # Check for subtraction operation (may be described as "subtracting")
        subtraction_found = "subtraction" in all_descriptions or "subtracting" in all_descriptions
        self.assertTrue(subtraction_found,
                       "Should mention subtraction operation")

    def test_division_with_multiplication_mixed_operations(self):
        """Test division mixed with multiplication: 100 / 4 * 3 = 75.
        
        This test verifies:
        - Left-to-right evaluation of same-precedence operators
        - Proper integration between division and multiplication
        - Correct sequential operation handling
        
        Requirements: 5.1, 5.2, 5.3
        """
        expression = "100 / 4 * 3"
        expected_result = 75  # (100/4) * 3 = 25 * 3 = 75
        
        # Verify parser handles left-to-right associativity
        rpn = self.parser.generate_rpn(expression)
        expected_rpn = [100, 4, '/', 3, '*']
        self.assertEqual(rpn, expected_rpn,
                        "Parser should handle left-to-right associativity")
        
        # Test the complete pipeline
        steps = self.calculator.calculate(expression)
        
        # Verify final result
        final_step = steps[-1]
        self.assertEqual(final_step.current_value, expected_result,
                        f"{expression} should equal {expected_result}")

    def test_nested_division_with_parentheses(self):
        """Test division with parentheses: (100 + 50) / (10 - 5) = 30.
        
        This test verifies:
        - Proper parentheses handling in division expressions
        - Correct sub-expression evaluation before division
        - Integration with grouped operations
        
        Requirements: 5.1, 5.2, 5.3
        """
        expression = "(100 + 50) / (10 - 5)"
        expected_result = 30  # (150) / (5) = 30
        
        # Verify parser handles parentheses correctly
        rpn = self.parser.generate_rpn(expression)
        expected_rpn = [100, 50, '+', 10, 5, '-', '/']
        self.assertEqual(rpn, expected_rpn,
                        "Parser should handle parentheses in division expressions")
        
        # Test the complete pipeline
        steps = self.calculator.calculate(expression)
        
        # Verify final result
        final_step = steps[-1]
        self.assertEqual(final_step.current_value, expected_result,
                        f"{expression} should equal {expected_result}")

    def test_multiple_divisions_in_sequence(self):
        """Test multiple divisions in sequence: 1000 / 10 / 5 = 20.
        
        This test verifies:
        - Left-to-right evaluation of multiple divisions
        - Proper sequential division handling
        - Correct intermediate result management
        
        Requirements: 5.1, 5.2, 5.3
        """
        expression = "1000 / 10 / 5"
        expected_result = 20  # (1000/10) / 5 = 100 / 5 = 20
        
        # Verify parser handles multiple divisions correctly
        rpn = self.parser.generate_rpn(expression)
        expected_rpn = [1000, 10, '/', 5, '/']
        self.assertEqual(rpn, expected_rpn,
                        "Parser should handle multiple divisions left-to-right")
        
        # Test the complete pipeline
        steps = self.calculator.calculate(expression)
        
        # Verify final result
        final_step = steps[-1]
        self.assertEqual(final_step.current_value, expected_result,
                        f"{expression} should equal {expected_result}")

    def test_division_integration_with_all_operations(self):
        """Test division integrated with all operations: 100 + 50 * 2 / 5 - 10 = 110.
        
        This test verifies:
        - Correct precedence with all four operations
        - Proper integration across the entire operation set
        - Complex expression evaluation accuracy
        
        Requirements: 5.1, 5.2, 5.3
        """
        expression = "100 + 50 * 2 / 5 - 10"
        expected_result = 110  # 100 + ((50*2)/5) - 10 = 100 + (100/5) - 10 = 100 + 20 - 10 = 110
        
        # Verify parser handles complex precedence correctly
        rpn = self.parser.generate_rpn(expression)
        expected_rpn = [100, 50, 2, '*', 5, '/', '+', 10, '-']
        self.assertEqual(rpn, expected_rpn,
                        "Parser should handle complex precedence correctly")
        
        # Test the complete pipeline
        steps = self.calculator.calculate(expression)
        
        # Verify final result
        final_step = steps[-1]
        self.assertEqual(final_step.current_value, expected_result,
                        f"{expression} should equal {expected_result}")

    def test_division_error_handling_integration(self):
        """Test division error handling in complete pipeline.
        
        This test verifies:
        - Division by zero error propagation through calculator
        - Proper error messages in integrated context
        - Error handling doesn't break the pipeline
        
        Requirements: 5.1, 5.2, 5.3
        """
        # Test division by zero
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("100 / 0")
        
        error_message = str(context.exception)
        self.assertIn("Division by zero", error_message,
                     "Should propagate division by zero error")
        
        # Test division by zero in complex expression
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate("50 + 100 / 0 - 25")
        
        error_message = str(context.exception)
        self.assertIn("Division by zero", error_message,
                     "Should propagate division by zero error in complex expressions")

    def test_division_with_edge_case_numbers(self):
        """Test division with edge case numbers.
        
        This test verifies:
        - Single digit divisions work correctly
        - Large number divisions are handled properly
        - Edge cases integrate properly with the pipeline
        
        Requirements: 5.1, 5.2, 5.3
        """
        edge_cases = [
            ("9 / 3", 3),      # Single digits
            ("1 / 1", 1),      # Division by one
            ("0 / 5", 0),      # Zero dividend
            ("999 / 1", 999),  # Division by one with large number
            ("144 / 12", 12),  # Perfect division
        ]
        
        for expression, expected_result in edge_cases:
            with self.subTest(expression=expression):
                steps = self.calculator.calculate(expression)
                final_step = steps[-1]
                self.assertEqual(final_step.current_value, expected_result,
                               f"{expression} should equal {expected_result}")


class TestDivisionPerformanceIntegration(unittest.TestCase):
    """Performance tests for division step generation efficiency."""

    def setUp(self):
        """Set up test fixtures."""
        self.calculator = Calculator()

    def test_division_step_generation_performance(self):
        """Test that division step generation is reasonably efficient.
        
        This test verifies:
        - Division calculations complete within reasonable time
        - Step generation doesn't create excessive steps
        - Performance is acceptable for typical use cases
        
        Requirements: 5.1, 5.2, 5.3
        """
        test_cases = [
            ("951 / 3", 317),
            ("100 / 7", 14),
            ("3869 / 53", 73),
            ("1000 / 25", 40),
            ("9999 / 99", 101),
        ]
        
        for expression, expected_result in test_cases:
            with self.subTest(expression=expression):
                # Measure execution time
                start_time = time.time()
                steps = self.calculator.calculate(expression)
                end_time = time.time()
                
                execution_time = end_time - start_time
                
                # Verify result is correct
                final_step = steps[-1]
                self.assertEqual(final_step.current_value, expected_result,
                               f"{expression} should equal {expected_result}")
                
                # Verify performance is reasonable (should complete in under 1 second)
                self.assertLess(execution_time, 1.0,
                              f"Division {expression} should complete in under 1 second, took {execution_time:.3f}s")
                
                # Verify step count is reasonable (not excessive)
                self.assertLess(len(steps), 200,
                              f"Division {expression} should not generate excessive steps, got {len(steps)}")
                self.assertGreater(len(steps), 5,
                                 f"Division {expression} should generate meaningful steps, got {len(steps)}")

    def test_complex_expression_performance(self):
        """Test performance of complex expressions involving division.
        
        This test verifies:
        - Complex expressions with division perform adequately
        - Multiple operations don't cause performance degradation
        - Step generation remains efficient in complex scenarios
        
        Requirements: 5.1, 5.2, 5.3
        """
        complex_expressions = [
            ("20 + 15 / 3 - 2", 23),
            ("100 / 4 * 3 + 25", 100),
            ("(100 + 50) / (10 - 5) * 2", 60),
            ("1000 / 10 / 5 + 100", 120),
            ("500 - 200 / 4 + 300 / 6", 500),
        ]
        
        for expression, expected_result in complex_expressions:
            with self.subTest(expression=expression):
                # Measure execution time
                start_time = time.time()
                steps = self.calculator.calculate(expression)
                end_time = time.time()
                
                execution_time = end_time - start_time
                
                # Verify result is correct
                final_step = steps[-1]
                self.assertEqual(final_step.current_value, expected_result,
                               f"{expression} should equal {expected_result}")
                
                # Verify performance is reasonable
                self.assertLess(execution_time, 2.0,
                              f"Complex expression {expression} should complete in under 2 seconds, took {execution_time:.3f}s")
                
                # Verify step count is reasonable
                self.assertLess(len(steps), 500,
                              f"Complex expression {expression} should not generate excessive steps, got {len(steps)}")

    def test_step_description_quality_performance(self):
        """Test that step descriptions are generated efficiently without impacting performance.
        
        This test verifies:
        - Step description generation doesn't significantly impact performance
        - All steps have meaningful descriptions
        - Description quality is maintained under performance constraints
        
        Requirements: 5.1, 5.2, 5.3
        """
        expression = "951 / 3"
        expected_result = 317
        
        # Measure execution time
        start_time = time.time()
        steps = self.calculator.calculate(expression)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Verify result is correct
        final_step = steps[-1]
        self.assertEqual(final_step.current_value, expected_result,
                        f"{expression} should equal {expected_result}")
        
        # Verify all steps have quality descriptions
        for i, step in enumerate(steps):
            self.assertIsInstance(step.step_description, str,
                                f"Step {i} should have string description")
            self.assertGreater(len(step.step_description), 10,
                             f"Step {i} description should be meaningful, got: '{step.step_description}'")
            
            # Verify description doesn't contain placeholder text
            description_lower = step.step_description.lower()
            self.assertNotIn("todo", description_lower,
                           f"Step {i} should not contain TODO placeholders")
            self.assertNotIn("placeholder", description_lower,
                           f"Step {i} should not contain placeholder text")
        
        # Verify performance with description generation is still reasonable
        self.assertLess(execution_time, 1.0,
                      f"Division with description generation should complete in under 1 second, took {execution_time:.3f}s")


class TestDivisionRegressionIntegration(unittest.TestCase):
    """Regression tests to ensure division doesn't break existing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.calculator = Calculator()

    def test_existing_operations_still_work_with_division_available(self):
        """Test that existing operations continue to work correctly with division available.
        
        This test verifies:
        - Addition still works correctly
        - Subtraction still works correctly  
        - Multiplication still works correctly
        - Mixed operations without division work correctly
        
        Requirements: 5.1, 5.2, 5.3
        """
        # Test basic operations still work
        basic_operations = [
            ("10 + 5", 15),
            ("20 - 8", 12),
            ("6 * 7", 42),
            ("100 + 50 - 25", 125),
            ("5 * 4 + 10", 30),
            ("100 - 20 * 2", 60),
        ]
        
        for expression, expected_result in basic_operations:
            with self.subTest(expression=expression):
                steps = self.calculator.calculate(expression)
                final_step = steps[-1]
                self.assertEqual(final_step.current_value, expected_result,
                               f"{expression} should equal {expected_result}")

    def test_parser_precedence_unchanged_for_existing_operations(self):
        """Test that parser precedence rules remain unchanged for existing operations.
        
        This test verifies:
        - Addition/subtraction precedence unchanged
        - Multiplication precedence unchanged
        - Parentheses handling unchanged
        - Left-to-right associativity unchanged
        
        Requirements: 5.1
        """
        parser = Parser()
        
        # Test existing precedence rules
        precedence_tests = [
            ("1 + 2 * 3", [1, 2, 3, '*', '+']),
            ("10 - 4 + 2", [10, 4, '-', 2, '+']),
            ("2 * 3 * 4", [2, 3, '*', 4, '*']),
            ("(1 + 2) * 3", [1, 2, '+', 3, '*']),
            ("10 + 5 - 3", [10, 5, '+', 3, '-']),
        ]
        
        for expression, expected_rpn in precedence_tests:
            with self.subTest(expression=expression):
                rpn = parser.generate_rpn(expression)
                self.assertEqual(rpn, expected_rpn,
                               f"Parser precedence should be unchanged for {expression}")

    def test_calculator_error_handling_unchanged(self):
        """Test that calculator error handling remains unchanged for existing operations.
        
        This test verifies:
        - Invalid expression handling unchanged
        - Malformed input handling unchanged
        - Error messages remain consistent
        
        Requirements: 5.2, 5.3
        """
        # Test existing error conditions still work
        error_cases = [
            "1 +",           # Missing operand
            "1 2",           # Too many operands
            "1 % 2",         # Unsupported operator
            "(1 + 2",        # Mismatched parentheses
        ]
        
        for expression in error_cases:
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError,
                                     msg=f"Should raise ValueError for invalid expression: {expression}"):
                    self.calculator.calculate(expression)


if __name__ == '__main__':
    unittest.main()