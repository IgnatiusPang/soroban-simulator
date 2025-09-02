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

        full_description = f"Move {' and '.join(descriptions)} on rod {rod_index + 1}"
        
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
        
        Rod positioning (1-indexed from RIGHT to LEFT as per requirements):
        - Rod 1 = rightmost = 1's place = index 0
        - Rod 13 = leftmost = 10^12 place = index 12
        
        Requirements for positioning:
        - Rods numbered 1-13 from right to left
        - Rod 1 = smallest value (1's place)
        - Rod 13 = largest value (10^12 place)
        
        Updated positioning to avoid overlap:
        - M1 and M2 positioned further left to avoid overlap with PP
        - PP (result) always starts from rod 1 (index 0)
        """
        steps = []
        multiplicand = self.get_value()
        
        # Clear the soroban for the multiplication setup
        steps.extend(self.clear())

        multiplier_str = str(multiplier)
        multiplicand_str = str(multiplicand)

        # Calculate expected result size for proper positioning
        expected_result_size = len(str(multiplicand * multiplier))
        
        # PP (Partial Products/Result) positioning - rightmost rods starting from rod 1 (index 0)
        pp_rod_start = 0  # Always start from the rightmost position
        pp_rod_end = expected_result_size - 1  # End position based on expected result size
        
        # M2 (multiplicand) positioning - position to the left of PP with safety gap
        safety_gap = 1
        multiplicand_rod_start = pp_rod_end + safety_gap + 1
        
        # M1 (multiplier) positioning - leftmost available rods
        multiplier_rod_start = self.num_rods - len(multiplier_str)

        # Place multiplier digits from right to left (least significant first)
        # This ensures proper positioning: rightmost digit goes to lower rod index
        steps.append(CalculationStep(f"Set multiplier {multiplier}", self.get_state(), self.get_value()))
        m1_actual_positions = []
        for i, digit_char in enumerate(reversed(multiplier_str)):
            rod_index = multiplier_rod_start + i
            m1_actual_positions.append(rod_index)
            steps.extend(self._set_rod_value(rod_index, int(digit_char)))

        # Calculate actual positions for all markers
        m1_actual_positions = list(range(multiplier_rod_start, multiplier_rod_start + len(multiplier_str)))
        m2_actual_positions = list(range(multiplicand_rod_start, multiplicand_rod_start + len(multiplicand_str)))
        pp_actual_positions = list(range(pp_rod_start, pp_rod_end + 1))

        # Show all markers at the very beginning before placing any numbers
        all_markers = [
            (min(m1_actual_positions), max(m1_actual_positions), "M1", "blue"),
            (min(m2_actual_positions), max(m2_actual_positions), "M2", "green"), 
            (min(pp_actual_positions), max(pp_actual_positions), "PP", "red")
        ]
        steps.append(CalculationStep("Setup multiplication areas", self.get_state(), self.get_value(), all_markers))

        # Add M1 marker after placing the digits, based on actual positions
        if m1_actual_positions:
            steps.append(CalculationStep(f"Multiplier {multiplier} positioned", self.get_state(), self.get_value()))

        # Place multiplicand digits from right to left (least significant first)
        # This ensures proper positioning: rightmost digit goes to lower rod index
        steps.append(CalculationStep(f"Set multiplicand {multiplicand}", self.get_state(), self.get_value()))
        for i, digit_char in enumerate(reversed(multiplicand_str)):
            rod_index = multiplicand_rod_start + i
            steps.extend(self._set_rod_value(rod_index, int(digit_char)))

        # Add M2 marker after placing the digits, based on actual positions
        steps.append(CalculationStep(f"Multiplicand {multiplicand} positioned", self.get_state(), self.get_value()))

        # Perform multiplication - place partial products in PP area (rightmost rods)
        # The result accumulates in the PP area starting from rod 1 (index 0)
        
        # Process multiplicand digits from right to left (least significant first for traditional method)
        for i in range(len(multiplicand_str) - 1, -1, -1):
            mc_digit = int(multiplicand_str[i])
            mc_rod_index = multiplicand_rod_start + i
            multiplicand_place_value = len(multiplicand_str) - 1 - i  # 0 for ones, 1 for tens, etc.

            # Process multiplier digits from right to left
            for j in range(len(multiplier_str) - 1, -1, -1):
                mp_digit = int(multiplier_str[j])
                multiplier_place_value = len(multiplier_str) - 1 - j  # 0 for ones, 1 for tens, etc.
                
                partial_product = mc_digit * mp_digit
                
                # Calculate the position for this partial product in the PP area
                # The combined place value determines where the rightmost digit goes
                combined_place_value = multiplicand_place_value + multiplier_place_value
                
                # Place the partial product in the PP area (rightmost rods)
                # Rod 1 (index 0) = 1's place, Rod 2 (index 1) = 10's place, etc.
                pp_position = pp_rod_start + combined_place_value

                if partial_product > 0:
                    steps.append(CalculationStep(f"Multiply {mc_digit} × {mp_digit} = {partial_product}", self.get_state(), self.get_value()))
                    steps.extend(self._add_to_rods_left_aligned(pp_position, partial_product))

            # Clear the multiplicand digit after processing
            steps.append(CalculationStep(f"Clear multiplicand digit {mc_digit}", self.get_state(), self.get_value()))
            steps.extend(self._set_rod_value(mc_rod_index, 0))

        # Clear multiplier digits
        steps.append(CalculationStep(f"Clear multiplier {multiplier}", self.get_state(), self.get_value()))
        for i in range(len(multiplier_str)):
            steps.extend(self._set_rod_value(multiplier_rod_start + i, 0))

        # Final result - the result is already in the PP area, no need to move it
        final_product = self.get_value()
        steps.append(CalculationStep(f"Final result: {final_product}", self.get_state(), final_product))
        
        return steps

    def multiply_with_setup(self, multiplicand: int, multiplier: int) -> list[CalculationStep]:
        """Multiplies two numbers using the Modern Standard Method without detailed initial setup steps.
        
        This method is specifically designed for use in calculations where we want to skip
        the granular bead movement steps for setting the initial multiplicand.
        
        Rod positioning strategy:
        - PP (Partial Products/Result) positioned on rightmost rods (starting from rod 1/index 0)
        - M2 (Multiplicand) positioned to the left of PP with safety gap
        - M1 (Multiplier) positioned on leftmost available rods
        """
        steps = []
        
        # Clear the soroban for the multiplication setup (but don't include detailed clearing steps)
        self.rods = [0] * self.num_rods

        multiplier_str = str(multiplier)
        multiplicand_str = str(multiplicand)

        # Calculate expected result size for proper positioning
        expected_result_size = len(str(multiplicand * multiplier))
        
        # PP (Partial Products/Result) positioning - rightmost rods starting from rod 1 (index 0)
        pp_rod_start = 0  # Always start from the rightmost position
        pp_rod_end = expected_result_size - 1  # End position based on expected result size
        
        # M2 (multiplicand) positioning - position to the left of PP with safety gap
        safety_gap = 1
        multiplicand_rod_start = pp_rod_end + safety_gap + 1
        
        # M1 (multiplier) positioning - leftmost available rods
        multiplier_rod_start = self.num_rods - len(multiplier_str)

        # Calculate actual positions for all markers
        m1_actual_positions = list(range(multiplier_rod_start, multiplier_rod_start + len(multiplier_str)))
        m2_actual_positions = list(range(multiplicand_rod_start, multiplicand_rod_start + len(multiplicand_str)))
        pp_actual_positions = list(range(pp_rod_start, pp_rod_end + 1))

        # Show all markers at the very beginning before placing any numbers
        all_markers = [
            (min(m1_actual_positions), max(m1_actual_positions), "M1", "blue"),
            (min(m2_actual_positions), max(m2_actual_positions), "M2", "green"), 
            (min(pp_actual_positions), max(pp_actual_positions), "PP", "red")
        ]
        steps.append(CalculationStep("Setup multiplication areas", self.get_state(), self.get_value(), all_markers))

        # Place multiplier digits from right to left (least significant first)
        steps.append(CalculationStep(f"Set multiplier {multiplier}", self.get_state(), self.get_value()))
        for i, digit_char in enumerate(reversed(multiplier_str)):
            rod_index = multiplier_rod_start + i
            self.rods[rod_index] = int(digit_char)

        steps.append(CalculationStep(f"Multiplier {multiplier} positioned", self.get_state(), self.get_value()))

        # Place multiplicand digits from right to left (least significant first)
        steps.append(CalculationStep(f"Set multiplicand {multiplicand}", self.get_state(), self.get_value()))
        for i, digit_char in enumerate(reversed(multiplicand_str)):
            rod_index = multiplicand_rod_start + i
            self.rods[rod_index] = int(digit_char)

        steps.append(CalculationStep(f"Multiplicand {multiplicand} positioned", self.get_state(), self.get_value()))

        # Perform multiplication - place partial products in PP area (rightmost rods)
        # The result accumulates in the PP area starting from rod 1 (index 0)
        
        # Process multiplicand digits from right to left (least significant first for traditional method)
        for i in range(len(multiplicand_str) - 1, -1, -1):
            mc_digit = int(multiplicand_str[i])
            mc_rod_index = multiplicand_rod_start + i
            multiplicand_place_value = len(multiplicand_str) - 1 - i  # 0 for ones, 1 for tens, etc.

            # Process multiplier digits from right to left
            for j in range(len(multiplier_str) - 1, -1, -1):
                mp_digit = int(multiplier_str[j])
                multiplier_place_value = len(multiplier_str) - 1 - j  # 0 for ones, 1 for tens, etc.
                
                partial_product = mc_digit * mp_digit
                
                # Calculate the position for this partial product in the PP area
                # The combined place value determines where the rightmost digit goes
                combined_place_value = multiplicand_place_value + multiplier_place_value
                
                # Place the partial product in the PP area (rightmost rods)
                # Rod 1 (index 0) = 1's place, Rod 2 (index 1) = 10's place, etc.
                pp_position = pp_rod_start + combined_place_value

                if partial_product > 0:
                    steps.append(CalculationStep(f"Multiply {mc_digit} × {mp_digit} = {partial_product}", self.get_state(), self.get_value()))
                    steps.extend(self._add_to_rods_left_aligned(pp_position, partial_product))

            # Clear the multiplicand digit after processing
            steps.append(CalculationStep(f"Clear multiplicand digit {mc_digit}", self.get_state(), self.get_value()))
            self.rods[mc_rod_index] = 0

        # Clear multiplier digits
        steps.append(CalculationStep(f"Clear multiplier {multiplier}", self.get_state(), self.get_value()))
        for i in range(len(multiplier_str)):
            self.rods[multiplier_rod_start + i] = 0

        # Final result - the result is already in the PP area, no need to move it
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
