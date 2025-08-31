#!/usr/bin/env python3
"""
Debug script to see where numbers are actually placed during calculation.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from soroban_simulator.soroban.calculator import Calculator

def debug_actual_positions():
    """Debug where numbers are actually placed during 23 * 15 calculation."""
    calculator = Calculator()
    equation = "23 * 15"
    
    print(f"Calculating: {equation}")
    steps = calculator.calculate(equation)
    
    print(f"\nTotal steps: {len(steps)}")
    
    # Look for steps that mention setting numbers
    for i, step in enumerate(steps):
        if step.step_description and ("Set multiplier" in step.step_description or 
                                     "Set multiplicand" in step.step_description or
                                     "Setting number" in step.step_description):
            print(f"\nStep {i}: {step.step_description}")
            print(f"Soroban state: {step.soroban_state}")
            
            # Find non-zero positions
            non_zero_positions = []
            for rod_idx, value in enumerate(step.soroban_state):
                if value != 0:
                    rod_number = 13 - rod_idx  # Convert to rod number (1-based, rightmost)
                    non_zero_positions.append((rod_number, value))
            
            print(f"Non-zero positions (rod_number, value): {non_zero_positions}")

if __name__ == '__main__':
    debug_actual_positions()
