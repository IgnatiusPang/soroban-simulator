#!/usr/bin/env python3

def analyze_multiplication():
    """Analyze how 51 * 3 should work step by step."""
    print("=== Analyzing 51 * 3 ===")
    
    # Standard multiplication
    # 51 * 3 = (50 + 1) * 3 = 50*3 + 1*3 = 150 + 3 = 153
    
    multiplicand = "51"
    multiplier = "3"
    
    print(f"Multiplicand: {multiplicand}")
    print(f"Multiplier: {multiplier}")
    print()
    
    # For a 3-digit result (153), we need rods 10, 11, 12 (0-indexed)
    # Rod 10 = hundreds place
    # Rod 11 = tens place  
    # Rod 12 = ones place
    
    print("Expected partial products:")
    print("5 (tens digit) * 3 = 15")
    print("  - 1 goes to hundreds place (rod 10)")
    print("  - 5 goes to tens place (rod 11)")
    print("1 (ones digit) * 3 = 3")
    print("  - 3 goes to ones place (rod 12)")
    print()
    print("Final result: rod 10=1, rod 11=5, rod 12=3 -> 153")
    print()
    
    # Let's trace what the current algorithm is doing wrong
    print("=== Current Algorithm Analysis ===")
    result_length = 3
    num_rods = 13
    result_start_rod = num_rods - result_length  # = 10
    
    print(f"Result should start at rod: {result_start_rod}")
    
    # Current algorithm iterates through multiplicand = "51"
    for i, mc_digit_char in enumerate(multiplicand):
        mc_digit = int(mc_digit_char)
        print(f"Multiplicand digit {i}: {mc_digit} ('{mc_digit_char}')")
        
        for j, mp_digit_char in enumerate(multiplier):
            mp_digit = int(mp_digit_char)
            partial_product = mc_digit * mp_digit
            pp_rod_start = result_start_rod + i + j
            
            print(f"  {mc_digit} x {mp_digit} = {partial_product}")
            print(f"  Current algorithm places at rod: {pp_rod_start}")
            
            # What should happen:
            if i == 0:  # First digit (5 - tens place)
                correct_rod = result_start_rod  # Should start at rod 10 for 15
                print(f"  SHOULD place at rod: {correct_rod} (for tens place)")
            else:  # Second digit (1 - ones place)  
                correct_rod = result_start_rod + 1  # Should start at rod 11 for 3
                print(f"  SHOULD place at rod: {correct_rod} (for ones place)")
            print()

if __name__ == "__main__":
    analyze_multiplication()
