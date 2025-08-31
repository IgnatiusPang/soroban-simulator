from soroban_simulator.soroban.soroban import Soroban

# Test 4*5 multiplication
soroban = Soroban(13)
print("Initial state:", soroban.get_state())
print("Initial value:", soroban.get_value())

steps = soroban.set_number(4)
print("\nAfter setting 4:")
print("State:", soroban.get_state())
print("Value:", soroban.get_value())

steps.extend(soroban.multiply(5))
print("\nAfter multiplying by 5:")
print("State:", soroban.get_state())
print("Value:", soroban.get_value())

# Let's also check the _get_interim_value method
print("Interim value:", soroban._get_interim_value())
