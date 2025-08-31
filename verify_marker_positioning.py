#!/usr/bin/env python3
"""
Script to verify the marker positioning logic is correct.
"""

def test_marker_positioning():
    """Test the marker positioning calculation logic."""
    num_rods = 13
    
    # Test case: 23 * 15
    # According to the main_window.py logic:
    # multiplicand = 23, multiplier = 15
    # multiplier_len = 2, multiplicand_len = 2
    # multiplier_rod_start = 2 (rod C, index 2)
    # multiplicand_rod_start = 2 + 2 + 2 = 6
    # product_rod_start = 6 + 2 = 8
    # product_len = 2 + 2 = 4
    
    multiplier_rod_start = 2
    multiplier_len = 2
    multiplicand_rod_start = multiplier_rod_start + multiplier_len + 2  # = 6
    multiplicand_len = 2
    product_rod_start = multiplicand_rod_start + multiplicand_len  # = 8
    product_len = multiplicand_len + multiplier_len  # = 4
    
    markers = [
        (multiplier_rod_start, multiplier_rod_start + multiplier_len - 1, "M1"),  # (2, 3, "M1")
        (multiplicand_rod_start, multiplicand_rod_start + multiplicand_len - 1, "M2"),  # (6, 7, "M2")
        (product_rod_start, product_rod_start + product_len - 1, "PP")  # (8, 11, "PP")
    ]
    
    print("Marker positions for 23 * 15:")
    print(f"M1 (multiplier): rods {markers[0][0]} to {markers[0][1]} (rod numbers {13-markers[0][1]} to {13-markers[0][0]})")
    print(f"M2 (multiplicand): rods {markers[1][0]} to {markers[1][1]} (rod numbers {13-markers[1][1]} to {13-markers[1][0]})")
    print(f"PP (product): rods {markers[2][0]} to {markers[2][1]} (rod numbers {13-markers[2][1]} to {13-markers[2][0]})")
    
    # Test the positioning calculation from soroban_widget.py
    print("\nDisplay positioning calculation:")
    for i, (start_rod, end_rod, label) in enumerate(markers):
        start_loop_i = num_rods - 1 - start_rod
        end_loop_i = num_rods - 1 - end_rod
        
        print(f"{label}: start_rod={start_rod} -> start_loop_i={start_loop_i}")
        print(f"{label}: end_rod={end_rod} -> end_loop_i={end_loop_i}")
        
        # Rod positions (1-based for display)
        start_display_pos = start_loop_i + 1
        end_display_pos = end_loop_i + 1
        print(f"{label}: display positions {start_display_pos} to {end_display_pos}")
        print()

if __name__ == '__main__':
    test_marker_positioning()
