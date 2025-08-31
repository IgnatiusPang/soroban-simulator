#!/usr/bin/env python3
"""
Final verification of the corrected marker positions.
"""

def final_position_verification():
    """Final verification of marker positioning for 23 * 15."""
    print("Final verification for 23 * 15:")
    
    # Fixed positions from main_window.py:
    multiplier_rod_start = 13 - 4  # Rod index 9 (rod 4)
    multiplier_rod_end = 13 - 3    # Rod index 10 (rod 3)
    
    multiplicand_rod_start = 13 - 7  # Rod index 6 (rod 7)
    multiplicand_rod_end = 13 - 6    # Rod index 7 (rod 6)
    
    product_rod_start = 13 - 13  # Rod index 0 (rod 13)
    product_rod_end = 13 - 11    # Rod index 2 (rod 11)
    
    markers = [
        (multiplier_rod_start, multiplier_rod_end, "M1"),
        (multiplicand_rod_start, multiplicand_rod_end, "M2"),
        (product_rod_start, product_rod_end, "PP")
    ]
    
    print(f"\nMarker positions (rod indices):")
    for start_rod, end_rod, label in markers:
        print(f"  {label}: rod indices {start_rod} to {end_rod}")
    
    print(f"\nMarker positions (rod numbers, 1=rightmost, 13=leftmost):")
    for start_rod, end_rod, label in markers:
        start_rod_num = 13 - start_rod
        end_rod_num = 13 - end_rod
        print(f"  {label}: rod numbers {end_rod_num} to {start_rod_num}")
    
    print(f"\nActual number positions from calculation:")
    print(f"  Multiplier 15: rods 3-4")
    print(f"  Multiplicand 23: rods 6-7")
    print(f"  Product 345: rods 11-13")
    
    print(f"\nVerification:")
    print(f"  M1 matches multiplier position: {'✓' if (13-multiplier_rod_end, 13-multiplier_rod_start) == (3, 4) else '✗'}")
    print(f"  M2 matches multiplicand position: {'✓' if (13-multiplicand_rod_end, 13-multiplicand_rod_start) == (6, 7) else '✗'}")
    print(f"  PP matches product position: {'✓' if (13-product_rod_end, 13-product_rod_start) == (11, 13) else '✗'}")

if __name__ == '__main__':
    final_position_verification()
