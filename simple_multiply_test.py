#!/usr/bin/env python3

def simple_multiply_51_by_3():
    """Test the simple multiplication logic."""
    print("=== Simple Multiplication: 51 × 3 ===")
    
    # Break down 51 × 3
    # Method 1: Standard algorithm
    print("Method 1: Standard multiplication")
    print("  51")
    print("×  3")
    print("----")
    print("  3  (1 × 3)")
    print("150  (50 × 3)")
    print("----")
    print("153")
    print()
    
    # Method 2: Digit by digit with proper place values
    print("Method 2: Digit by digit")
    multiplicand = "51"
    multiplier = 3
    
    total = 0
    for i, digit_char in enumerate(multiplicand):
        digit = int(digit_char)
        place_value = 10 ** (len(multiplicand) - 1 - i)
        partial_product = digit * multiplier * place_value
        
        print(f"Digit {digit} at position {i} (place value {place_value})")
        print(f"  {digit} × {multiplier} × {place_value} = {partial_product}")
        total += partial_product
    
    print(f"Total: {total}")
    print()
    
    # Method 3: What the soroban should do
    print("Method 3: Soroban approach")
    print("1. Set up multiplicand 51 and multiplier 3")
    print("2. For each digit in multiplicand:")
    print("   - Multiply digit by multiplier")
    print("   - Add result to appropriate position in result area")
    print()
    print("For 51 × 3:")
    print("- Digit 5 (tens): 5 × 3 = 15")
    print("  Add 15 to result starting at tens position → 150")
    print("- Digit 1 (ones): 1 × 3 = 3") 
    print("  Add 3 to result starting at ones position → 3")
    print("- Final result: 150 + 3 = 153")

if __name__ == "__main__":
    simple_multiply_51_by_3()
