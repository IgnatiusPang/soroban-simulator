from soroban_simulator.soroban.soroban import Soroban

# Test the _get_interim_value method
soroban = Soroban(13)

# Manually set the state that should represent 20
# Based on the debug output, after multiplication we have: [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]
soroban.rods = [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]

print("Manual state (should be 20):", soroban.rods)
print("get_value():", soroban.get_value())
print("_get_interim_value():", soroban._get_interim_value())

# Let's also test what 20 should look like
soroban2 = Soroban(13)
soroban2.set_number(20)
print("\nCorrect representation of 20:")
print("State:", soroban2.get_state())
print("Value:", soroban2.get_value())
