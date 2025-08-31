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

    def _get_interim_value(self) -> int:
        """Gets the value from the rods, ignoring leading/trailing zeros."""
        first = -1
        last = -1
        for i, r in enumerate(self.rods):
            if r != 0:
                if first == -1:
                    first = i
                last = i

        if first == -1:
            return 0

        result_rods = self.rods[first:last+1]
        value = 0
        for rod in result_rods:
            value = value * 10 + rod
        return value

    def _get_partial_products_value(self) -> int:
        """Gets the value from the partial products area (right side of soroban)."""
        # For multiplication, the partial products are typically in the right portion
        # This method is similar to _get_interim_value but focuses on the result area
        return self._get_interim_value()

    def _add_to_rods(self, start_rod_index: int, number: int) -> list[CalculationStep]:
        """Helper to add a number to a set of rods, handling carries."""
        steps = []
        number_str = str(number)  # Use natural string representation
        
        for i, digit_char in enumerate(reversed(number_str)):
            rod_index = start_rod_index + len(number_str) - 1 - i
            digit = int(digit_char)
            if rod_index >= 0:
                steps.extend(self.add_to_rod(rod_index, digit))
                
        return steps

    def multiply(self, multiplier: int) -> list[CalculationStep]:
        """Multiplies the current value by a number using the Modern Standard Method."""
        steps = []
        multiplicand = self.get_value()
        
        # Clear the soroban for the multiplication setup
        steps.extend(self.clear())

        multiplier_str = str(multiplier)
        multiplicand_str = str(multiplicand)

        # Setup on soroban (e.g., multiplier on C, multiplicand on FG for 13 rods)
        multiplier_rod_start = 2
        multiplicand_rod_start = 5

        # Set multiplier
        multiplier_markers = [(multiplier_rod_start, multiplier_rod_start + len(multiplier_str) - 1, "M1", "blue")]
        steps.append(CalculationStep(f"Set multiplier {multiplier}", self.get_state(), self.get_value(), multiplier_markers))
        for i, digit_char in enumerate(multiplier_str):
            steps.extend(self._set_rod_value(multiplier_rod_start + i, int(digit_char)))

        # Set multiplicand
        multiplicand_markers = [(multiplicand_rod_start, multiplicand_rod_start + len(multiplicand_str) - 1, "M2", "green")]
        steps.append(CalculationStep(f"Set multiplicand {multiplicand}", self.get_state(), self.get_value(), multiplicand_markers))
        for i, digit_char in enumerate(multiplicand_str):
            steps.extend(self._set_rod_value(multiplicand_rod_start + i, int(digit_char)))

        # Multiplication - place partial products in the rightmost area for final result
        # Calculate expected result length to position it correctly
        expected_result = multiplicand * multiplier
        result_length = len(str(expected_result))
        
        # Place result starting from the rightmost rods
        result_start_rod = self.num_rods - result_length
        
        for i, mc_digit_char in enumerate(reversed(multiplicand_str)):
            mc_digit = int(mc_digit_char)
            mc_rod_index = multiplicand_rod_start + len(multiplicand_str) - 1 - i

            for j, mp_digit_char in enumerate(multiplier_str):
                mp_digit = int(mp_digit_char)
                
                partial_product = mc_digit * mp_digit
                
                # Place partial product with correct place value in the result area
                # Position based on the digit positions to ensure correct place value
                pp_rod_start = result_start_rod + (len(multiplicand_str) - 1 - i) + j

                steps.append(CalculationStep(f"Multiply {mc_digit} x {mp_digit} = {partial_product}", self.get_state(), self.get_value()))
                
                if partial_product > 0:  # Only add non-zero partial products
                    steps.extend(self._add_to_rods(pp_rod_start, partial_product))

            # Clear multiplicand digit
            steps.append(CalculationStep(f"Clear multiplicand digit {mc_digit}", self.get_state(), self.get_value()))
            steps.extend(self._set_rod_value(mc_rod_index, 0))

        # Clear multiplier
        steps.append(CalculationStep(f"Clear multiplier {multiplier}", self.get_state(), self.get_value()))
        for i in range(len(multiplier_str)):
            steps.extend(self._set_rod_value(multiplier_rod_start + i, 0))

        # Final result - the product is already on the soroban in the correct position
        final_product = self.get_value()
        steps.append(CalculationStep(f"Final result: {final_product}", self.get_state(), final_product))
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
