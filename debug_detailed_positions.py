#!/usr/bin/env python3
"""
Debug script to see detailed positions during calculation.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from soroban_simulator.soroban.calculator import Calculator

def debug_detailed_positions():
    """Debug detailed positions during 23 * 15 calculation."""
    calculator = Calculator()
    equation = "23 * 15"
    
    print(f"Calculating: {equation}")
    steps = calculator.calculate(equation)
    
    print(f"\nTotal steps: {len(steps)}")
    
    # Look at all steps with non-zero states
    for i, step in enumerate(steps):
        non_zero_positions = []
        for rod_idx, value in enumerate(step.soroban_state):
            if value != 0:
                rod_number = 13 - rod_idx  # Convert to rod number (1-based, rightmost)
                non_zero_positions.append((rod_number, value))
        
        if non_zero_positions:
            print(f"\nStep {i}: {step.step_description}")
            print(f"Non-zero positions (rod_number, value): {non_zero_positions}")
            
            # Try to identify what these positions represent
            if "Set multiplier" in step.step_description:
                print("  ^ This is where the MULTIPLIER (15) is placed")
            elif "Set multiplicand" in step.step_description:
                print("  ^ This is where the MULTIPLICAND (23) is placed")
            elif "Final result" in step.step_description:
                print("  ^ This is the FINAL RESULT (345)")

if __name__ == '__main__':
    debug_detailed_positions()
