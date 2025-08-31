from soroban_simulator.soroban.soroban import Soroban

# Test 4*5 multiplication with detailed step tracking
soroban = Soroban(13)
print("=== Testing 4 * 5 ===")
print("Initial state:", soroban.get_state())

# Set the number 4
steps = soroban.set_number(4)
print("\nAfter setting 4:")
print("State:", soroban.get_state())
print("Value:", soroban.get_value())

# Now multiply by 5 and track each step
print("\n=== Starting multiplication by 5 ===")
multiply_steps = soroban.multiply(5)

print(f"\nTotal steps in multiplication: {len(multiply_steps)}")
for i, step in enumerate(multiply_steps):
    print(f"Step {i+1}: {step.step_description}")
    print(f"  State: {step.soroban_state}")
    print(f"  Value: {step.current_value}")
    print()

print("Final state:", soroban.get_state())
print("Final value:", soroban.get_value())
