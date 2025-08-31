from .calculation_step import CalculationStep

class Soroban:
    """Represents the state of the abacus and generates granular bead movements."""

    def __init__(self, num_rods: int = 13):
        """Initializes the abacus."""
        self.num_rods = num_rods
        self.rods = [0] * num_rods

    def get_value(self) -> int:
        """Returns the current integer value.
        
        Rod positioning (1-indexed from left to right):
        - Rod 1 (index 0) = 1's place
        - Rod 2 (index 1) = 10's place
        - Rod 3 (index 2) = 100's place
        - etc.
        """
        value = 0
        for i, rod in enumerate(self.rods):
            if rod != 0:
                value += rod * (10 ** i)
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
        """Sets a number on the abacus, digit by digit, with granular steps.
        
        With the new rod positioning:
        - Rod 1 (index 0) = 1's place
        - Rod 2 (index 1) = 10's place
        - etc.
        """
        steps = self.clear()
        number_str = str(number)

        steps.append(
            CalculationStep(
                step_description=f"Setting number: {number}",
                soroban_state=self.get_state(),
                current_value=self.get_value(),
            )
        )

        # Place digits starting from rod 1 (index 0) for 1's place
        for i, digit_char in enumerate(reversed(number_str)):
            rod_index = i  # Start from index 0 for 1's place
            if rod_index >= self.num_rods:
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
        """Adds a number to the abacus with granular steps.
        
        With the new rod positioning:
        - Rod 1 (index 0) = 1's place
        - Rod 2 (index 1) = 10's place
        - etc.
        """
        steps = [
            CalculationStep(
                step_description=f"Adding: {number}",
                soroban_state=self.get_state(),
                current_value=self.get_value(),
            )
        ]
        number_str = str(number)
        
        # Add digits starting from rod 1 (index 0) for 1's place
        for i, digit_char in enumerate(reversed(number_str)):
            rod_index = i  # Start from index 0 for 1's place
            if rod_index >= self.num_rods:
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
        """Helper to add a value to a rod, handling carries.
        
        With the new rod positioning:
        - Rod 1 (index 0) = 1's place
        - Rod 2 (index 1) = 10's place
        - Carries go to higher place values (higher indices)
        """
        steps = []
        current_rod_value = self.rods[rod_index]
        new_rod_value = current_rod_value + value

        if new_rod_value < 10:
            steps.extend(self._set_rod_value(rod_index, new_rod_value))
        else:
            complement = 10 - value
            steps.extend(self._set_rod_value(rod_index, self.rods[rod_index] - complement))
            
            # Carry to the next higher place value (higher index)
            carry_rod_index = rod_index + 1
            if carry_rod_index < self.num_rods:
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
            if rod_index >= 0 and rod_index < self.num_rods:
                steps.extend(self.add_to_rod(rod_index, digit))
                
        return steps

    def _add_to_rods_left_aligned(self, start_rod_index: int, number: int) -> list[CalculationStep]:
        """Helper to add a number to rods starting from the leftmost position (for result area).
        
        This method places numbers left-aligned in the result area, where:
        - Rod 1 (index 0) = rightmost = 1's place
        - The number is placed so its rightmost digit aligns with the specified position
        """
        steps = []
        number_str = str(number)
        
        # Place digits from right to left, with rightmost digit at start_rod_index
        for i, digit_char in enumerate(reversed(number_str)):
            rod_index = start_rod_index + i  # Move right for higher-order digits
            digit = int(digit_char)
            if rod_index >= 0 and rod_index < self.num_rods:
                steps.extend(self.add_to_rod(rod_index, digit))
                
        return steps

    def multiply(self, multiplier: int) -> list[CalculationStep]:
        """Multiplies the current value by a number using the Modern Standard Method.
        
        Rod positioning (1-indexed from left to right):
        - Rod 1 = rightmost = 1's place = index 0
        - Rod 13 = leftmost = 10^12 place = index 12
        
        For 5 × 15 = 75:
        - M1 (multiplier 15) should be on rods 10-11 (indices 9-10)
        - M2 (multiplicand 5) should be on rod 8 (index 7)
        - PP (result 75) should be on rods 1-2 (indices 0-1)
        
        For 37 × 7 = 259:
        - M1 (multiplier 7) should be on rod 11 (index 10)
        - M2 (multiplicand 37) should be on rod 7 (index 6)
        - PP (result 259) should be on rods 1-3 (indices 0-2)
        """
        steps = []
        multiplicand = self.get_value()
        
        # Clear the soroban for the multiplication setup
        steps.extend(self.clear())

        multiplier_str = str(multiplier)
        multiplicand_str = str(multiplicand)

        # Setup positioning according to requirements:
        # For 5 × 15: M1=15 on rods 10-11, M2=5 on rod 8
        # For 37 × 7: M1=7 on rod 11, M2=37 on rod 7
        
        # M1 (multiplier) positioning - place on rods 10-11 for multi-digit, rod 11 for single digit
        if len(multiplier_str) == 1:
            # Single digit multiplier goes on rod 11 (index 10)
            multiplier_rod_start = 10
        else:
            # Multi-digit multiplier starts on rod 10 (index 9)
            multiplier_rod_start = 9
        
        # M2 (multiplicand) positioning
        if len(multiplicand_str) == 1:
            # Single digit multiplicand goes on rod 8 (index 7)
            multiplicand_rod_start = 7
        else:
            # Multi-digit multiplicand starts on rod 7 (index 6)
            multiplicand_rod_start = 6

        # Set multiplier (M1)
        multiplier_markers = [(multiplier_rod_start, multiplier_rod_start + len(multiplier_str) - 1, "M1", "blue")]
        steps.append(CalculationStep(f"Set multiplier {multiplier}", self.get_state(), self.get_value(), multiplier_markers))
        for i, digit_char in enumerate(multiplier_str):
            steps.extend(self._set_rod_value(multiplier_rod_start + i, int(digit_char)))

        # Set multiplicand (M2)
        multiplicand_markers = [(multiplicand_rod_start, multiplicand_rod_start + len(multiplicand_str) - 1, "M2", "green")]
        steps.append(CalculationStep(f"Set multiplicand {multiplicand}", self.get_state(), self.get_value(), multiplicand_markers))
        for i, digit_char in enumerate(multiplicand_str):
            steps.extend(self._set_rod_value(multiplicand_rod_start + i, int(digit_char)))

        # Multiplication - place partial products in the leftmost area (rods 1-N) for final result
        # The result should appear on rods 1-N (indices 0 to N-1)
        expected_result = multiplicand * multiplier
        result_length = len(str(expected_result))
        
        # Place result starting from rod 1 (index 0) - leftmost position in result area
        result_start_rod = 0
        
        # Process multiplicand digits from left to right (most significant to least significant)
        for i, mc_digit_char in enumerate(multiplicand_str):
            mc_digit = int(mc_digit_char)
            mc_rod_index = multiplicand_rod_start + i

            for j, mp_digit_char in enumerate(multiplier_str):
                mp_digit = int(mp_digit_char)
                
                partial_product = mc_digit * mp_digit
                
                # Calculate the correct position for this partial product
                # The key insight: we want the final result to appear starting at rod 1 (index 0)
                
                # Calculate the decimal place of this partial product in the final result
                multiplicand_place = len(multiplicand_str) - 1 - i  # 0 for ones, 1 for tens, etc.
                multiplier_place = len(multiplier_str) - 1 - j
                combined_place = multiplicand_place + multiplier_place
                
                # For the partial product placement in the result area (starting at index 0):
                # - The rightmost digit of the partial product should align with the correct decimal place
                # - For combined_place=0 (ones), rightmost digit goes to index 0 (rod 1)
                # - For combined_place=1 (tens), rightmost digit goes to index 1 (rod 2)
                # - We place the partial product so its rightmost digit is at combined_place
                pp_rod_start = combined_place

                steps.append(CalculationStep(f"Multiply {mc_digit} x {mp_digit} = {partial_product}", self.get_state(), self.get_value()))
                
                if partial_product > 0:  # Only add non-zero partial products
                    steps.extend(self._add_to_rods_left_aligned(pp_rod_start, partial_product))

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
        """Subtracts a number from the abacus with granular steps.
        
        With the new rod positioning:
        - Rod 1 (index 0) = 1's place
        - Rod 2 (index 1) = 10's place
        - etc.
        """
        steps = [
            CalculationStep(
                step_description=f"Subtracting: {number}",
                soroban_state=self.get_state(),
                current_value=self.get_value(),
            )
        ]
        number_str = str(number)

        # Subtract digits starting from rod 1 (index 0) for 1's place
        for i, digit_char in enumerate(reversed(number_str)):
            rod_index = i  # Start from index 0 for 1's place
            if rod_index >= self.num_rods:
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
        """Helper to subtract a value from a rod, handling borrows.
        
        With the new rod positioning:
        - Rod 1 (index 0) = 1's place
        - Rod 2 (index 1) = 10's place
        - Borrows come from higher place values (higher indices)
        """
        steps = []
        current_rod_value = self.rods[rod_index]

        if current_rod_value >= value:
            steps.extend(self._set_rod_value(rod_index, current_rod_value - value))
        else:
            complement = 10 - value
            steps.extend(self._set_rod_value(rod_index, self.rods[rod_index] + complement))

            # Borrow from the next higher place value (higher index)
            borrow_rod_index = rod_index + 1
            if borrow_rod_index < self.num_rods:
                steps.extend(self.subtract_from_rod(borrow_rod_index, 1))
        
        return steps
