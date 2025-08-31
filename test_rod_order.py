#!/usr/bin/env python3
"""
Test script to verify that the soroban rod order has been correctly reversed.
This will test by setting a simple number and checking the visual representation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from soroban_simulator.soroban.soroban import Soroban

def test_rod_order():
    """Test that demonstrates the rod ordering."""
    soroban = Soroban(13)
    
    # Test with number 123
    print("Testing with number 123:")
    print("Expected: 1 should be in 1's place (rightmost), 2 in 10's place, 3 in 100's place (leftmost)")
    
    steps = soroban.set_number(123)
    state = soroban.get_state()
    
    print(f"Soroban state: {state}")
    print(f"Value: {soroban.get_value()}")
    
    # Check the positions
    print("\nRod positions (index -> value):")
    for i, value in enumerate(state):
        if value != 0:
            place_value = 10 ** i
            print(f"  Rod index {i} (10^{i} = {place_value}'s place): {value}")
    
    print("\nIn the GUI display (after reversal):")
    print("- Leftmost rod should show 3 (100's place)")
    print("- Middle rod should show 2 (10's place)")  
    print("- Rightmost rod should show 1 (1's place)")
    
    return state

if __name__ == "__main__":
    test_rod_order()
