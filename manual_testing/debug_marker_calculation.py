#!/usr/bin/env python3
"""
Debug script to understand the marker calculation issue.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from soroban_simulator.soroban.calculator import Calculator

def debug_marker_calculation():
    """Debug the marker calculation for 23 * 15."""
    calculator = Calculator()
    equation = "23 * 15"
    
    # Get the RPN parts
    parts = calculator.parser.generate_rpn(equation)
    print(f"RPN parts: {parts}")
    
    operands = [p for p in parts if isinstance(p, int)]
    print(f"Operands: {operands}")
    
    if len(operands) == 2:
        # This is what the current code does:
        multiplicand, multiplier = operands[0], operands[1]
        print(f"Current assignment: multiplicand={multiplicand}, multiplier={multiplier}")
        
        multiplier_len = len(str(multiplier))
        multiplicand_len = len(str(multiplicand))
        print(f"Lengths: multiplier_len={multiplier_len}, multiplicand_len={multiplicand_len}")

        # Position the multiplier on the far left (rod C, index 2).
        multiplier_rod_start = 2
        print(f"Multiplier rod start: {multiplier_rod_start}")

        # Leave a gap of 2 rods after the multiplier.
        multiplicand_rod_start = multiplier_rod_start + multiplier_len + 2
        print(f"Multiplicand rod start: {multiplicand_rod_start}")
        
        # The product is formed to the right of the multiplicand.
        product_rod_start = multiplicand_rod_start + multiplicand_len 
        product_len = multiplicand_len + multiplier_len
        print(f"Product rod start: {product_rod_start}, length: {product_len}")

        markers = [
            (multiplier_rod_start, multiplier_rod_start + multiplier_len - 1, "M1"),
            (multiplicand_rod_start, multiplicand_rod_start + multiplicand_len - 1, "M2"),
            (product_rod_start, product_rod_start + product_len - 1, "PP")
        ]
        
        print(f"\nMarkers:")
        for marker in markers:
            print(f"  {marker}")
            
        # Convert to rod numbers (1-based, rightmost)
        print(f"\nRod numbers (1=rightmost, 13=leftmost):")
        for start_rod, end_rod, label in markers:
            start_rod_num = 13 - start_rod
            end_rod_num = 13 - end_rod
            print(f"  {label}: rods {end_rod_num} to {start_rod_num}")

if __name__ == '__main__':
    debug_marker_calculation()
