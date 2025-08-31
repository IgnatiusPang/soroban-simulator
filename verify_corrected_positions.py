#!/usr/bin/env python3
"""
Verify the corrected marker positions.
"""

def verify_corrected_positions():
    """Verify the corrected marker positioning for 23 * 15."""
    # For 23 * 15:
    multiplicand, multiplier = 23, 15
    multiplier_len = len(str(multiplier))  # 2
    multiplicand_len = len(str(multiplicand))  # 2
    
    print(f"Testing: {multiplicand} * {multiplier}")
    print(f"Multiplier length: {multiplier_len}, Multiplicand length: {multiplicand_len}")
    
    # New calculation based on observed positions:
    # Multiplier 15 goes to rods 3-4 (rod indices 9-10)
    multiplier_rod_start = 13 - multiplier_len - 1  # 13 - 2 - 1 = 10
    multiplier_rod_end = 13 - 2  # 13 - 2 = 11
    
    # Multiplicand 23 goes to rods 6-7 (rod indices 6-7)  
    multiplicand_rod_start = 13 - multiplicand_len - 5  # 13 - 2 - 5 = 6
    multiplicand_rod_end = 13 - 6  # 13 - 6 = 7
    
    # Product 345 appears on rods 11-13 (rod indices 0-2)
    product_len = multiplicand_len + multiplier_len  # 4
    product_rod_start = 0
    product_rod_end = product_len - 1  # 3
    
    markers = [
        (multiplier_rod_start, multiplier_rod_end, "M1"),
        (multiplicand_rod_start, multiplicand_rod_end, "M2"),
        (product_rod_start, product_rod_end, "PP")
    ]
    
    print(f"\nCalculated markers (rod indices):")
    for start_rod, end_rod, label in markers:
        print(f"  {label}: rod indices {start_rod} to {end_rod}")
    
    print(f"\nConverted to rod numbers (1=rightmost, 13=leftmost):")
    for start_rod, end_rod, label in markers:
        start_rod_num = 13 - start_rod
        end_rod_num = 13 - end_rod
        print(f"  {label}: rod numbers {end_rod_num} to {start_rod_num}")
    
    print(f"\nExpected positions based on actual calculation:")
    print(f"  M1 (multiplier 15): should be on rods 3-4")
    print(f"  M2 (multiplicand 23): should be on rods 6-7") 
    print(f"  PP (product 345): should be on rods 11-13")

if __name__ == '__main__':
    verify_corrected_positions()
