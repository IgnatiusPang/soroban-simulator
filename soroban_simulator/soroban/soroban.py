
from .calculation_step import CalculationStep

class Soroban:
    """Represents the state of the abacus and generates granular bead movements."""

    def __init__(self, num_rods: int = 13):
        """Initializes the abacus."""
        self.num_rods = num_rods
        self.rods = [0] * num_rods

    def get_value(self) -> int:
        """Returns the current integer value."""
        value = 0
        for rod in self.rods:
            value = value * 10 + rod
        return value

    def get_state(self) -> list[int]:
        """Returns a data structure representing bead positions for rendering."""
        return list(self.rods)

    def clear(self) -> list[CalculationStep]:
        """Resets all rods to 0."""
        steps = []
        if any(rod != 0 for rod in self.rods):
            # Create a temporary state for clearing to have a start and end
            start_state = self.get_state()
            self.rods = [0] * self.num_rods
            end_state = self.get_state()
            
            steps.append(
                CalculationStep(
                    step_description="Clear the soroban",
                    soroban_state=end_state,
                    current_value=0,
                )
            )
        else:
            steps.append(
                CalculationStep(
                    step_description="Soroban is already clear",
                    soroban_state=self.get_state(),
                    current_value=self.get_value(),
                )
            )
        return steps

    def _set_rod_value(self, rod_index: int, digit: int) -> list[CalculationStep]:
        """Sets a single rod to a specific digit, generating a single step with a detailed description."""
        steps = []
        current_digit = self.rods[rod_index]

        if current_digit == digit:
            return steps

        descriptions = []
        
        # Heaven bead movement
        if current_digit >= 5 and digit < 5:
            descriptions.append("1 heaven bead up")
        elif current_digit < 5 and digit >= 5:
            descriptions.append("1 heaven bead down")

        # Earth beads movement
        current_earth_beads = current_digit % 5
        target_earth_beads = digit % 5
        diff = target_earth_beads - current_earth_beads

        if diff != 0:
            bead_word = "bead" if abs(diff) == 1 else "beads"
            direction = "up" if diff > 0 else "down"
            descriptions.append(f"{abs(diff)} earth {bead_word} {direction}")

        if not descriptions:
            return steps

        full_description = f"Move {' and '.join(descriptions)} on rod {self.num_rods - rod_index}"
        
        self.rods[rod_index] = digit
        steps.append(
            CalculationStep(
                step_description=full_description,
                soroban_state=self.get_state(),
                current_value=self.get_value(),
            )
        )
        return steps

    def set_number(self, number: int) -> list[CalculationStep]:
        """Sets a number on the abacus, digit by digit, with granular steps."""
        steps = self.clear()
        number_str = str(number)

        steps.append(
            CalculationStep(
                step_description=f"Setting number: {number}",
                soroban_state=self.get_state(),
                current_value=self.get_value(),
            )
        )

        for i, digit_char in enumerate(reversed(number_str)):
            rod_index = self.num_rods - 1 - i
            if rod_index < 0:
                break
            digit = int(digit_char)
            steps.extend(self._set_rod_value(rod_index, digit))
        
        steps.append(
            CalculationStep(
                step_description=f"Finished setting {number}",
                soroban_state=self.get_state(),
                current_value=self.get_value(),
            )
        )
        return steps

    def add(self, number: int) -> list[CalculationStep]:
        """Adds a number to the abacus with granular steps."""
        steps = [
            CalculationStep(
                step_description=f"Adding: {number}",
                soroban_state=self.get_state(),
                current_value=self.get_value(),
            )
        ]
        number_str = str(number)
        
        for i, digit_char in enumerate(reversed(number_str)):
            rod_index = self.num_rods - 1 - i
            if rod_index < 0:
                break
            
            digit = int(digit_char)
            steps.extend(self.add_to_rod(rod_index, digit))

        steps.append(
            CalculationStep(
                step_description=f"Finished adding {number}",
                soroban_state=self.get_state(),
                current_value=self.get_value(),
            )
        )
        return steps

    def add_to_rod(self, rod_index: int, value: int) -> list[CalculationStep]:
        """Helper to add a value to a rod, handling carries."""
        steps = []
        current_rod_value = self.rods[rod_index]
        new_rod_value = current_rod_value + value

        if new_rod_value < 10:
            steps.extend(self._set_rod_value(rod_index, new_rod_value))
        else:
            complement = 10 - value
            steps.extend(self._set_rod_value(rod_index, self.rods[rod_index] - complement))
            
            carry_rod_index = rod_index - 1
            if carry_rod_index >= 0:
                steps.extend(self.add_to_rod(carry_rod_index, 1))
        
        return steps

    def subtract(self, number: int) -> list[CalculationStep]:
        """Subtracts a number from the abacus with granular steps."""
        steps = [
            CalculationStep(
                step_description=f"Subtracting: {number}",
                soroban_state=self.get_state(),
                current_value=self.get_value(),
            )
        ]
        number_str = str(number)

        for i, digit_char in enumerate(reversed(number_str)):
            rod_index = self.num_rods - 1 - i
            if rod_index < 0:
                break
            
            digit = int(digit_char)
            steps.extend(self.subtract_from_rod(rod_index, digit))

        steps.append(
            CalculationStep(
                step_description=f"Finished subtracting {number}",
                soroban_state=self.get_state(),
                current_value=self.get_value(),
            )
        )
        return steps

    def subtract_from_rod(self, rod_index: int, value: int) -> list[CalculationStep]:
        """Helper to subtract a value from a rod, handling borrows."""
        steps = []
        current_rod_value = self.rods[rod_index]

        if current_rod_value >= value:
            steps.extend(self._set_rod_value(rod_index, current_rod_value - value))
        else:
            complement = 10 - value
            steps.extend(self._set_rod_value(rod_index, self.rods[rod_index] + complement))

            borrow_rod_index = rod_index - 1
            if borrow_rod_index >= 0:
                steps.extend(self.subtract_from_rod(borrow_rod_index, 1))
        
        return steps
