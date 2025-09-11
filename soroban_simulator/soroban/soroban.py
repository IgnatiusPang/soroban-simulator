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

    def _apply_kojima_placement_rules(self, dividend: int, divisor: int) -> int:
        """Applies Kojima's placement rules to determine quotient starting position.
        
        Rule I: If first digit of divisor ≤ first digit of dividend → quotient starts 2 rods left of dividend
        Rule II: If first digit of divisor > first digit of dividend → quotient starts 1 rod left of dividend
        
        Args:
            dividend: The dividend number
            divisor: The divisor number
            
        Returns:
            Rod index where the first quotient digit should be placed
        """
        # Get first digits
        divisor_first_digit = int(str(divisor)[0])
        dividend_first_digit = int(str(dividend)[0])
        
        # Calculate dividend's rightmost position (assuming dividend is placed on rightmost rods)
        dividend_length = len(str(dividend))
        dividend_rightmost_rod = dividend_length - 1  # 0-indexed, rightmost digit at index dividend_length-1
        
        # Apply Kojima's rules
        if divisor_first_digit <= dividend_first_digit:
            # Rule I: quotient starts 2 rods left of dividend
            quotient_start_rod = dividend_rightmost_rod + 2
        else:
            # Rule II: quotient starts 1 rod left of dividend  
            quotient_start_rod = dividend_rightmost_rod + 1
            
        return quotient_start_rod

    def _setup_division_workspace(self, dividend: int, divisor: int) -> list[CalculationStep]:
        """Sets up the soroban workspace for division using the shojohou method.
        
        This method implements optimal rod positioning with:
        - Divisor on leftmost rods (D area)
        - Dividend on rightmost rods (DV area) 
        - Quotient workspace in middle (Q area)
        - Proper spacing and visual markers
        
        Args:
            dividend: The dividend number
            divisor: The divisor number
            
        Returns:
            List of calculation steps showing the workspace setup process
        """
        steps = []
        
        # Clear the soroban first
        steps.extend(self.clear())
        
        # Calculate number lengths for positioning
        dividend_str = str(dividend)
        divisor_str = str(divisor)
        dividend_length = len(dividend_str)
        divisor_length = len(divisor_str)
        
        # Calculate optimal positioning
        # Dividend goes on rightmost rods (starting from rod 1, index 0)
        dividend_start_rod = 0
        dividend_end_rod = dividend_length - 1
        
        # Apply Kojima's placement rules to determine quotient area
        quotient_start_rod = self._apply_kojima_placement_rules(dividend, divisor)
        
        # Estimate quotient length (conservative estimate)
        estimated_quotient_length = max(1, dividend_length - divisor_length + 1)
        quotient_end_rod = quotient_start_rod + estimated_quotient_length - 1
        
        # Divisor goes on leftmost available rods with buffer from quotient area
        buffer_from_quotient = 1
        divisor_end_rod = self.num_rods - 1  # Rightmost position for divisor
        divisor_start_rod = divisor_end_rod - divisor_length + 1
        
        # Ensure divisor doesn't overlap with quotient area
        if divisor_start_rod <= quotient_end_rod + buffer_from_quotient:
            divisor_start_rod = quotient_end_rod + buffer_from_quotient + 1
            divisor_end_rod = divisor_start_rod + divisor_length - 1
        
        # Validate positioning fits within soroban
        if divisor_end_rod >= self.num_rods:
            raise ValueError(f"Numbers too large for {self.num_rods}-rod soroban")
        
        # Create visual markers for all areas
        divisor_markers = (divisor_start_rod, divisor_end_rod, "D", "blue")
        dividend_markers = (dividend_start_rod, dividend_end_rod, "DV", "green")
        quotient_markers = (quotient_start_rod, quotient_end_rod, "Q", "red")
        all_markers = [divisor_markers, dividend_markers, quotient_markers]
        
        # Show workspace layout with markers
        steps.append(CalculationStep(
            f"🏗️  WORKSPACE SETUP: Preparing soroban for {dividend} ÷ {divisor}",
            self.get_state(),
            self.get_value(),
            all_markers
        ))
        steps.append(CalculationStep(
            f"📍 Layout: D (Divisor) | Q (Quotient) | DV (Dividend) with proper spacing",
            self.get_state(),
            self.get_value(),
            all_markers
        ))
        
        # Place divisor on leftmost rods
        steps.append(CalculationStep(
            f"🔵 DIVISOR PLACEMENT: Position {divisor} on leftmost rods {divisor_start_rod + 1}-{divisor_end_rod + 1}",
            self.get_state(),
            self.get_value()
        ))
        steps.append(CalculationStep(
            f"📝 Divisor role: This number will be multiplied by each quotient digit",
            self.get_state(),
            self.get_value()
        ))
        
        # Place divisor digits from right to left (least significant first)
        for i, digit_char in enumerate(reversed(divisor_str)):
            rod_index = divisor_start_rod + i
            steps.extend(self._set_rod_value(rod_index, int(digit_char)))
        
        # Place dividend on rightmost rods  
        steps.append(CalculationStep(
            f"🟢 DIVIDEND PLACEMENT: Position {dividend} on rightmost rods {dividend_start_rod + 1}-{dividend_end_rod + 1}",
            self.get_state(),
            self.get_value()
        ))
        steps.append(CalculationStep(
            f"📝 Dividend role: This number will be divided by the divisor",
            self.get_state(),
            self.get_value()
        ))
        
        # Place dividend digits from right to left (least significant first)
        for i, digit_char in enumerate(reversed(dividend_str)):
            rod_index = dividend_start_rod + i
            steps.extend(self._set_rod_value(rod_index, int(digit_char)))
        
        # Final setup confirmation with all markers visible
        kojima_rule = "Rule I" if int(str(divisor)[0]) <= int(str(dividend)[0]) else "Rule II"
        steps.append(CalculationStep(
            f"✅ WORKSPACE READY: Applied Kojima's {kojima_rule} for quotient positioning",
            self.get_state(),
            self.get_value(),
            all_markers
        ))
        steps.append(CalculationStep(
            f"🎯 Ready for shojohou: Estimate → Multiply → Subtract → Revise cycle",
            self.get_state(),
            self.get_value(),
            all_markers
        ))
        
        return steps

    def _estimate_quotient_digit(self, dividend_fragment: int, divisor: int) -> int:
        """Estimates a single quotient digit using the shojohou method.
        
        This method implements the mental estimation logic central to the shojohou
        division method. It provides conservative estimates to minimize revision frequency.
        
        Args:
            dividend_fragment: The current portion of the dividend being processed
            divisor: The divisor number
            
        Returns:
            Estimated quotient digit (0-9)
            
        Algorithm:
        - For single-digit divisors: Direct division of dividend fragment by divisor
        - For multi-digit divisors: Approximate by dividing first 1-2 digits of 
          dividend fragment by first digit of divisor
        - Apply bounds checking to ensure estimate doesn't exceed 9
        - Use conservative estimation to minimize revision frequency
        """
        if dividend_fragment == 0:
            return 0
            
        if divisor == 0:
            raise ValueError("Cannot estimate quotient digit with divisor of 0")
        
        # First check: if dividend fragment is smaller than divisor, result is 0
        if dividend_fragment < divisor:
            return 0
            
        # Convert to strings for digit manipulation
        dividend_str = str(dividend_fragment)
        divisor_str = str(divisor)
        
        if len(divisor_str) == 1:
            # Single-digit divisor: Direct division
            estimate = dividend_fragment // divisor
        else:
            # Multi-digit divisor: Approximate using first digits with better logic
            divisor_first_digit = int(divisor_str[0])
            
            if len(dividend_str) == 1:
                # Single digit dividend fragment with multi-digit divisor
                # Since we already checked dividend_fragment < divisor above,
                # this case should not occur, but handle it safely
                estimate = 0
            else:
                # Multi-digit dividend fragment: use first 1-2 digits for approximation
                if len(dividend_str) >= 2:
                    # Use first two digits for better accuracy
                    dividend_for_estimation = int(dividend_str[:2])
                else:
                    dividend_for_estimation = dividend_fragment
                
                # Use a more sophisticated approximation that considers more digits
                # This is closer to what a human would do mentally
                
                if len(divisor_str) == 2:
                    # For 2-digit divisors, use a smarter approximation
                    divisor_approx = int(divisor_str)
                    
                    # For divisors ending in 0-2, round down to nearest 10
                    # For divisors ending in 3-7, round to nearest 5
                    # For divisors ending in 8-9, round up to next 10
                    last_digit = divisor_approx % 10
                    if last_digit <= 2:
                        divisor_mental = (divisor_approx // 10) * 10
                    elif last_digit <= 7:
                        divisor_mental = (divisor_approx // 10) * 10 + 5
                    else:
                        divisor_mental = ((divisor_approx // 10) + 1) * 10
                    
                    if divisor_mental == 0:
                        divisor_mental = 10
                    
                    # For better accuracy with larger dividend fragments, use more digits
                    if len(dividend_str) >= 3:
                        dividend_for_estimation = int(dividend_str[:3])
                    
                    rough_estimate = dividend_for_estimation // divisor_mental
                else:
                    # For 3+ digit divisors, use first two digits
                    divisor_approx = int(divisor_str[:2])
                    # Round to nearest 10 for mental math
                    divisor_mental = (divisor_approx // 10) * 10
                    if divisor_mental == 0:
                        divisor_mental = 10
                    
                    # For better accuracy with larger dividend fragments, use more digits
                    if len(dividend_str) >= 3:
                        dividend_for_estimation = int(dividend_str[:3])
                    
                    rough_estimate = dividend_for_estimation // divisor_mental
                
                # Apply final conservative adjustment BEFORE bounds checking
                # Even with better approximation, be slightly conservative
                if rough_estimate > 10:
                    estimate = max(1, int(rough_estimate * 0.1))  # Very conservative for large estimates
                elif rough_estimate > 5:
                    estimate = max(1, int(rough_estimate * 0.6))
                elif rough_estimate > 3:
                    estimate = max(1, int(rough_estimate * 0.8))
                elif rough_estimate > 1:
                    estimate = max(1, int(rough_estimate * 0.9))
                else:
                    estimate = rough_estimate
        
        # Apply bounds checking to ensure estimate doesn't exceed 9
        estimate = min(9, max(0, estimate))
        
        return estimate

    def _get_estimation_reasoning(self, dividend_fragment: int, divisor: int, estimate: int) -> str:
        """Provides detailed reasoning for quotient digit estimation.
        
        This method explains the mental process used to arrive at the quotient estimate,
        making the shojohou method more educational and transparent.
        
        Args:
            dividend_fragment: The dividend fragment being estimated
            divisor: The divisor number
            estimate: The calculated estimate
            
        Returns:
            String explaining the estimation reasoning
        """
        if dividend_fragment == 0:
            return "Dividend fragment is 0, so quotient digit is 0"
            
        if dividend_fragment < divisor:
            return f"{dividend_fragment} < {divisor}, so quotient digit is 0"
            
        divisor_str = str(divisor)
        dividend_str = str(dividend_fragment)
        
        if len(divisor_str) == 1:
            # Single-digit divisor reasoning
            exact_result = dividend_fragment // divisor
            remainder = dividend_fragment % divisor
            
            if remainder == 0:
                return f"{dividend_fragment} ÷ {divisor} = {exact_result} exactly"
            else:
                return f"{dividend_fragment} ÷ {divisor} = {exact_result} remainder {remainder}, so quotient digit is {estimate}"
        else:
            # Multi-digit divisor reasoning
            divisor_first = int(divisor_str[0])
            
            if len(dividend_str) == 1:
                return f"Single digit {dividend_fragment} < multi-digit divisor {divisor}, so quotient digit is 0"
            
            # Explain the approximation process
            if len(dividend_str) >= 2:
                dividend_approx = int(dividend_str[:2])
                rough_estimate = dividend_approx // divisor_first
                
                reasoning = f"Mental approximation: {dividend_approx} ÷ {divisor_first} ≈ {rough_estimate}"
                
                if len(divisor_str) == 2:
                    reasoning += f", then adjust for 2-digit divisor {divisor}"
                elif len(divisor_str) > 2:
                    reasoning += f", then adjust for {len(divisor_str)}-digit divisor {divisor}"
                
                if estimate != rough_estimate:
                    reasoning += f" → conservative estimate {estimate}"
                
                return reasoning
            else:
                return f"Approximate {dividend_fragment} ÷ {divisor} ≈ {estimate} (conservative estimate)"

    def _validate_revision_bounds(self, quotient: int, revision_type: str) -> tuple[bool, str]:
        """Validates revision bounds and provides explanatory messages.
        
        This method checks if a quotient digit revision is within valid bounds (0-9)
        and provides detailed explanations for boundary conditions.
        
        Args:
            quotient: The current quotient digit value
            revision_type: Type of revision ("increase" or "decrease")
            
        Returns:
            Tuple of (is_valid, explanation_message)
        """
        if revision_type == "decrease":
            if quotient <= 0:
                return False, f"Cannot decrease quotient below 0 (current: {quotient})"
            return True, f"Quotient can be decreased from {quotient} to {quotient - 1}"
        
        elif revision_type == "increase":
            if quotient >= 9:
                return False, f"Cannot increase quotient above 9 (current: {quotient})"
            return True, f"Quotient can be increased from {quotient} to {quotient + 1}"
        
        else:
            return False, f"Invalid revision type: {revision_type}"

    def _get_dividend_fragment(self, current_dividend: int, divisor: int) -> int:
        """Determines the appropriate dividend fragment for quotient digit estimation.
        
        This method implements the logic for selecting the portion of the remaining
        dividend to use for estimating the next quotient digit in multi-digit division.
        
        Args:
            current_dividend: The remaining dividend after previous subtractions
            divisor: The divisor number
            
        Returns:
            The dividend fragment to use for quotient estimation
            
        Algorithm:
        - For single-digit divisors: Use enough leftmost digits to ensure fragment >= divisor
        - For multi-digit divisors: Use divisor length + 1 digits when possible
        - Ensure fragment is large enough for meaningful estimation
        """
        if current_dividend == 0:
            return 0
            
        current_dividend_str = str(current_dividend)
        divisor_str = str(divisor)
        divisor_length = len(divisor_str)
        
        # For single-digit divisors, use minimal fragment that's >= divisor
        if divisor_length == 1:
            # Start with single digit and expand if needed
            for fragment_length in range(1, len(current_dividend_str) + 1):
                fragment = int(current_dividend_str[:fragment_length])
                if fragment >= divisor:
                    return fragment
            # If no fragment is >= divisor, return the full dividend
            return current_dividend
        
        # For multi-digit divisors, use divisor length + 1 digits when possible
        # This provides better estimation accuracy
        target_fragment_length = min(divisor_length + 1, len(current_dividend_str))
        
        # Ensure we have at least divisor_length digits for comparison
        fragment_length = max(divisor_length, target_fragment_length)
        fragment_length = min(fragment_length, len(current_dividend_str))
        
        fragment = int(current_dividend_str[:fragment_length])
        
        # If fragment is still smaller than divisor, use the full dividend
        if fragment < divisor:
            return current_dividend
            
        return fragment

    def _detect_and_display_remainder(self, remainder: int, divisor: int, quotient: int, original_dividend: int) -> list[CalculationStep]:
        """Detects remainder and provides detailed display logic with educational explanations.
        
        This method implements comprehensive remainder handling including validation,
        educational explanations, and verification steps.
        
        Args:
            remainder: The remainder value after division
            divisor: The original divisor
            quotient: The calculated quotient
            original_dividend: The original dividend for verification
            
        Returns:
            List of calculation steps explaining the remainder
            
        Requirements: 3.4, 4.4
        """
        steps = []
        
        if remainder == 0:
            # Exact division case
            steps.append(CalculationStep(
                f"🔍 REMAINDER ANALYSIS: No remainder (exact division)",
                self.get_state(),
                self.get_value()
            ))
            
            steps.append(CalculationStep(
                f"✨ PERFECT DIVISION: {original_dividend} ÷ {divisor} = {quotient} with no remainder",
                self.get_state(),
                self.get_value()
            ))
            
            steps.append(CalculationStep(
                f"📚 Educational note: {divisor} is a factor of {original_dividend}",
                self.get_state(),
                self.get_value()
            ))
            
        else:
            # Division with remainder case
            steps.append(CalculationStep(
                f"🔍 REMAINDER ANALYSIS: Remainder = {remainder}",
                self.get_state(),
                self.get_value()
            ))
            steps.append(CalculationStep(
                f"📊 Division type: Inexact division (has remainder)",
                self.get_state(),
                self.get_value()
            ))
            
            # Validate remainder is proper (less than divisor)
            if remainder >= divisor:
                steps.append(CalculationStep(
                    f"❌ VALIDATION ERROR: Remainder {remainder} ≥ divisor {divisor}",
                    self.get_state(),
                    self.get_value()
                ))
                
                steps.append(CalculationStep(
                    f"🚨 Problem detected: Division incomplete - quotient should be increased",
                    self.get_state(),
                    self.get_value()
                ))
            else:
                steps.append(CalculationStep(
                    f"✅ VALIDATION SUCCESS: Remainder {remainder} < divisor {divisor} (proper remainder)",
                    self.get_state(),
                    self.get_value()
                ))
                steps.append(CalculationStep(
                    f"📚 Rule confirmed: Remainder must always be less than divisor",
                    self.get_state(),
                    self.get_value()
                ))
            
            # Educational explanation of what the remainder means
            steps.append(CalculationStep(
                f"📚 REMAINDER MEANING: {remainder} is the amount left over after dividing {original_dividend} by {divisor}",
                self.get_state(),
                self.get_value()
            ))
            steps.append(CalculationStep(
                f"💡 Think of it as: {original_dividend} items divided into groups of {divisor}, with {remainder} items remaining",
                self.get_state(),
                self.get_value()
            ))
            
            # Show the division relationship
            product = quotient * divisor
            steps.append(CalculationStep(
                f"Division relationship: {quotient} × {divisor} = {product}",
                self.get_state(),
                self.get_value()
            ))
            
            steps.append(CalculationStep(
                f"Complete equation: {product} + {remainder} = {product + remainder} = {original_dividend}",
                self.get_state(),
                self.get_value()
            ))
            
            # Verification
            verification_result = product + remainder
            if verification_result == original_dividend:
                steps.append(CalculationStep(
                    f"Verification: ✓ {quotient} × {divisor} + {remainder} = {original_dividend}",
                    self.get_state(),
                    self.get_value()
                ))
            else:
                steps.append(CalculationStep(
                    f"Verification: ✗ {quotient} × {divisor} + {remainder} = {verification_result} ≠ {original_dividend}",
                    self.get_state(),
                    self.get_value()
                ))
        
        return steps

    def _get_dividend_fragment_for_position(self, current_dividend: int, divisor: int, position: int) -> int:
        """Gets the appropriate dividend fragment for a specific quotient position.
        
        This method determines how much of the remaining dividend to use when
        calculating each quotient digit in multi-digit division.
        
        Args:
            current_dividend: The remaining dividend
            divisor: The divisor number
            position: The current quotient digit position (0 = leftmost)
            
        Returns:
            The dividend fragment to use for this position
        """
        if current_dividend == 0:
            return 0
            
        current_dividend_str = str(current_dividend)
        divisor_length = len(str(divisor))
        
        # For the first quotient digit, use enough digits to get a meaningful estimate
        if position == 0:
            # Use divisor length + 1 digits when possible, but at least divisor length
            target_length = min(divisor_length + 1, len(current_dividend_str))
            target_length = max(divisor_length, target_length)
            fragment = int(current_dividend_str[:target_length])
            
            # If fragment is still smaller than divisor, use full dividend
            if fragment < divisor:
                return current_dividend
            return fragment
        
        # For subsequent positions, we typically work with the full remaining dividend
        # since we're continuing the division process
        return current_dividend

    def divide(self, dividend: int, divisor: int) -> list[CalculationStep]:
        """Divides two numbers using the Modern Division Method (shojohou).
        
        The shojohou method treats division as iterative subtraction, where the operator:
        1. Estimates quotient digits
        2. Multiplies by the divisor  
        3. Subtracts from the dividend
        4. Revises as needed
        
        This method implements the complete estimate-multiply-subtract-revise cycle
        for multi-digit quotient calculations, processing one quotient digit at a time.
        
        Args:
            dividend: The dividend number (must be positive integer)
            divisor: The divisor number (must be positive integer, non-zero)
            
        Returns:
            List of calculation steps showing the division process
            
        Raises:
            ValueError: If divisor is zero or if inputs are invalid
            
        Requirements: 1.1, 2.1, 2.2, 2.3, 3.4, 5.4
        """
        steps = []
        
        # Error handling for invalid input types (must be done first)
        if not isinstance(dividend, int) or not isinstance(divisor, int):
            raise ValueError("Division requires integer operands")
        
        # Error handling for division by zero
        if divisor == 0:
            raise ValueError("Division by zero is not allowed")
        
        # Error handling for negative inputs
        if dividend < 0 or divisor < 0:
            raise ValueError("Division requires positive integers")
        
        # Error handling for workspace overflow scenarios
        dividend_length = len(str(dividend))
        divisor_length = len(str(divisor))
        
        # Check if numbers are too large for the soroban workspace
        # We need space for dividend, divisor, and quotient with proper spacing
        estimated_quotient_length = max(1, dividend_length - divisor_length + 1)
        total_space_needed = dividend_length + divisor_length + estimated_quotient_length + 2  # +2 for spacing
        
        if total_space_needed > self.num_rods:
            raise ValueError(f"Numbers too large for {self.num_rods}-rod soroban: need {total_space_needed} rods but only have {self.num_rods}")
        
        # Additional check for extremely large individual numbers (conservative limits)
        if dividend_length > 10 or divisor_length > 8:
            raise ValueError(f"Numbers too large for {self.num_rods}-rod soroban: dividend has {dividend_length} digits, divisor has {divisor_length} digits")
        
        # Handle special case: dividend is 0
        if dividend == 0:
            steps.extend(self.clear())
            steps.append(CalculationStep(
                f"Division: {dividend} ÷ {divisor} = 0",
                self.get_state(),
                0
            ))
            return steps
        
        # Handle special case: divisor is 1
        if divisor == 1:
            steps.extend(self.set_number(dividend))
            steps.append(CalculationStep(
                f"Division: {dividend} ÷ 1 = {dividend}",
                self.get_state(),
                dividend
            ))
            return steps
        
        # Setup division workspace with proper positioning and markers
        steps.extend(self._setup_division_workspace(dividend, divisor))
        
        # Get workspace positioning information
        dividend_str = str(dividend)
        divisor_str = str(divisor)
        
        # Calculate positioning (matching the setup method logic)
        dividend_start_rod = 0
        dividend_length = len(dividend_str)
        
        # Get quotient starting position from Kojima's rules
        quotient_start_rod = self._apply_kojima_placement_rules(dividend, divisor)
        
        # Initialize division state for multi-digit quotients
        quotient_digits = []
        current_quotient_rod = quotient_start_rod
        
        # Work with the dividend digits from left to right (like long division)
        dividend_str = str(dividend)
        divisor_value = divisor
        
        # Initialize working dividend (starts with first few digits)
        working_dividend = 0
        dividend_index = 0
        
        steps.append(CalculationStep(
            f"🔢 Begin shojohou division: {dividend} ÷ {divisor} using estimate-multiply-subtract-revise cycle",
            self.get_state(),
            self.get_value()
        ))
        
        # Process each digit of the dividend from left to right
        while dividend_index < len(dividend_str):
            # Bring down the next digit
            next_digit = int(dividend_str[dividend_index])
            working_dividend = working_dividend * 10 + next_digit
            dividend_index += 1
            
            steps.append(CalculationStep(
                f"📥 Bring down next digit: {next_digit} → working dividend becomes {working_dividend}",
                self.get_state(),
                self.get_value()
            ))
            
            # If working dividend is still smaller than divisor, continue bringing down digits
            if working_dividend < divisor and dividend_index < len(dividend_str):
                # Add a 0 to quotient if we already have quotient digits
                if quotient_digits:
                    quotient_digits.append(0)
                    if current_quotient_rod >= 0:
                        steps.append(CalculationStep(
                            f"⚠️  Cannot divide: {working_dividend} < {divisor}, so quotient digit = 0",
                            self.get_state(),
                            self.get_value()
                        ))
                        steps.extend(self._set_rod_value(current_quotient_rod, 0))
                        current_quotient_rod -= 1
                continue
            
            # Now we can divide: working_dividend ÷ divisor
            if working_dividend >= divisor:
                # Step 1: Estimate quotient digit with detailed reasoning
                estimated_quotient = self._estimate_quotient_digit(working_dividend, divisor)
                estimation_reasoning = self._get_estimation_reasoning(working_dividend, divisor, estimated_quotient)
                steps.append(CalculationStep(
                    f"🧮 ESTIMATE: {working_dividend} ÷ {divisor} ≈ {estimated_quotient}",
                    self.get_state(),
                    self.get_value()
                ))
                steps.append(CalculationStep(
                    f"💭 Reasoning: {estimation_reasoning}",
                    self.get_state(),
                    self.get_value()
                ))
                
                # Step 2: Multiply estimated quotient by divisor (with multi-digit support)
                if len(str(divisor)) == 1:
                    # Single-digit divisor: simple multiplication
                    product = estimated_quotient * divisor
                    steps.append(CalculationStep(
                        f"✖️  MULTIPLY: {estimated_quotient} × {divisor} = {product}",
                        self.get_state(),
                        self.get_value()
                    ))
                    steps.append(CalculationStep(
                        f"📝 Mental calculation: {estimated_quotient} times {divisor} equals {product}",
                        self.get_state(),
                        self.get_value()
                    ))
                else:
                    # Multi-digit divisor: break down into partial products
                    steps.append(CalculationStep(
                        f"✖️  MULTIPLY (Multi-stage): {estimated_quotient} × {divisor}",
                        self.get_state(),
                        self.get_value()
                    ))
                    steps.append(CalculationStep(
                        f"🔧 Breaking down: Multi-digit divisor requires partial products",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    divisor_str = str(divisor)
                    partial_products = []
                    
                    # Calculate partial products for each digit of the divisor
                    for i, digit_char in enumerate(reversed(divisor_str)):
                        digit = int(digit_char)
                        place_value = 10 ** i
                        partial_product = estimated_quotient * digit * place_value
                        partial_products.append(partial_product)
                        
                        steps.append(CalculationStep(
                            f"Partial product: {estimated_quotient} × {digit} × {place_value} = {partial_product}",
                            self.get_state(),
                            self.get_value()
                        ))
                    
                    # Sum all partial products
                    product = sum(partial_products)
                    steps.append(CalculationStep(
                        f"Total product: {' + '.join(map(str, partial_products))} = {product}",
                        self.get_state(),
                        self.get_value()
                    ))
                
                # Step 3: Handle estimation corrections with enhanced revision logic
                revision_count = 0
                max_revisions = 10  # Safety limit to prevent infinite loops
                original_estimate = estimated_quotient
                
                # Enhanced overestimate detection (when subtraction is impossible)
                while product > working_dividend and estimated_quotient > 0 and revision_count < max_revisions:
                    revision_count += 1
                    
                    # Detailed overestimate detection explanation with visual cues
                    steps.append(CalculationStep(
                        f"🚨 OVERESTIMATE DETECTED: Product {product} > working dividend {working_dividend}",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    steps.append(CalculationStep(
                        f"❌ Problem: Cannot subtract {product} from {working_dividend} (impossible subtraction)",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    steps.append(CalculationStep(
                        f"🔄 Solution: Must revise quotient estimate downward",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    # Validate revision bounds before proceeding
                    can_revise, validation_msg = self._validate_revision_bounds(estimated_quotient, "decrease")
                    
                    if not can_revise:
                        steps.append(CalculationStep(
                            f"Revision boundary reached: {validation_msg}",
                            self.get_state(),
                            self.get_value()
                        ))
                        break
                    
                    # Revise quotient down with compensation explanation
                    old_quotient = estimated_quotient
                    estimated_quotient -= 1
                    old_product = product
                    product = estimated_quotient * divisor
                    
                    steps.append(CalculationStep(
                        f"⬇️  REVISION #{revision_count}: Decrease quotient {old_quotient} → {estimated_quotient}",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    steps.append(CalculationStep(
                        f"🔄 COMPENSATION: Recalculate {estimated_quotient} × {divisor} = {product}",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    steps.append(CalculationStep(
                        f"📊 Comparison: Old product {old_product} → New product {product}",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    # Verify the revision resolved the overestimate
                    if product <= working_dividend:
                        steps.append(CalculationStep(
                            f"✅ REVISION SUCCESS: {product} ≤ {working_dividend}, subtraction now possible",
                            self.get_state(),
                            self.get_value()
                        ))
                    elif estimated_quotient == 0:
                        steps.append(CalculationStep(
                            f"Quotient revised to 0 - no further reduction possible",
                            self.get_state(),
                            self.get_value()
                        ))
                
                # Step 4: Subtract product from working dividend with multi-stage support
                if estimated_quotient > 0:
                    if len(str(divisor)) == 1:
                        # Single-digit divisor: simple subtraction
                        steps.append(CalculationStep(
                            f"➖ SUBTRACT: {working_dividend} - {product}",
                            self.get_state(),
                            self.get_value()
                        ))
                        steps.append(CalculationStep(
                            f"🧮 Mental calculation: {working_dividend} minus {product}",
                            self.get_state(),
                            self.get_value()
                        ))
                        
                        # Update working dividend with remainder
                        old_working_dividend = working_dividend
                        working_dividend = working_dividend - product
                        
                        steps.append(CalculationStep(
                            f"Subtraction complete: {old_working_dividend} - {product} = {working_dividend}",
                            self.get_state(),
                            self.get_value()
                        ))
                    else:
                        # Multi-digit divisor: multi-stage subtraction
                        steps.append(CalculationStep(
                            f"Multi-stage subtraction: {working_dividend} - {product}",
                            self.get_state(),
                            self.get_value()
                        ))
                        
                        # Break down the subtraction by partial products
                        divisor_str = str(divisor)
                        current_working_dividend = working_dividend
                        
                        for i, digit_char in enumerate(reversed(divisor_str)):
                            digit = int(digit_char)
                            place_value = 10 ** i
                            partial_product = estimated_quotient * digit * place_value
                            
                            if partial_product > 0:
                                steps.append(CalculationStep(
                                    f"Subtract partial product: {current_working_dividend} - {partial_product}",
                                    self.get_state(),
                                    self.get_value()
                                ))
                                
                                old_working_dividend = current_working_dividend
                                current_working_dividend = current_working_dividend - partial_product
                                
                                steps.append(CalculationStep(
                                    f"Partial subtraction: {old_working_dividend} - {partial_product} = {current_working_dividend}",
                                    self.get_state(),
                                    self.get_value()
                                ))
                        
                        # Update working dividend with final remainder
                        working_dividend = current_working_dividend
                        
                        steps.append(CalculationStep(
                            f"Multi-stage subtraction complete: remainder = {working_dividend}",
                            self.get_state(),
                            self.get_value()
                        ))
                
                # Enhanced underestimate detection (when remainder ≥ divisor)
                underestimate_revisions = 0
                while working_dividend >= divisor and estimated_quotient < 9 and revision_count < max_revisions:
                    revision_count += 1
                    underestimate_revisions += 1
                    
                    # Detailed underestimate detection explanation with visual cues
                    steps.append(CalculationStep(
                        f"🔍 UNDERESTIMATE DETECTED: Remainder {working_dividend} ≥ divisor {divisor}",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    steps.append(CalculationStep(
                        f"💡 Analysis: Since {working_dividend} ≥ {divisor}, we can divide at least once more",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    steps.append(CalculationStep(
                        f"🔄 Solution: Must revise quotient estimate upward",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    # Validate revision bounds before proceeding
                    can_revise, validation_msg = self._validate_revision_bounds(estimated_quotient, "increase")
                    
                    if not can_revise:
                        steps.append(CalculationStep(
                            f"Revision boundary reached: {validation_msg}",
                            self.get_state(),
                            self.get_value()
                        ))
                        break
                    
                    # Revise quotient up with compensation explanation
                    old_quotient = estimated_quotient
                    estimated_quotient += 1
                    additional_product = divisor
                    
                    steps.append(CalculationStep(
                        f"⬆️  REVISION #{revision_count}: Increase quotient {old_quotient} → {estimated_quotient}",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    steps.append(CalculationStep(
                        f"🔄 COMPENSATION: Subtract additional {divisor} from remainder {working_dividend}",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    # Update working dividend with detailed tracking
                    old_remainder = working_dividend
                    working_dividend -= additional_product
                    
                    steps.append(CalculationStep(
                        f"Updated remainder: {old_remainder} - {additional_product} = {working_dividend}",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    # Verify the revision progress
                    if working_dividend < divisor:
                        steps.append(CalculationStep(
                            f"Revision successful: Remainder {working_dividend} < divisor {divisor}",
                            self.get_state(),
                            self.get_value()
                        ))
                    elif estimated_quotient == 9:
                        steps.append(CalculationStep(
                            f"Maximum quotient digit reached (9) - no further increase possible",
                            self.get_state(),
                            self.get_value()
                        ))
                
                # Summary of revision process if any occurred
                total_revisions = revision_count
                if total_revisions > 0:
                    revision_type = "overestimate" if original_estimate > estimated_quotient else "underestimate"
                    if original_estimate > estimated_quotient and underestimate_revisions > 0:
                        revision_type = "mixed (overestimate then underestimate)"
                    elif original_estimate < estimated_quotient:
                        revision_type = "underestimate"
                    
                    steps.append(CalculationStep(
                        f"Revision summary: {total_revisions} revision(s) applied ({revision_type})",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    steps.append(CalculationStep(
                        f"Final quotient digit: {original_estimate} → {estimated_quotient}, remainder: {working_dividend}",
                        self.get_state(),
                        self.get_value()
                    ))
                else:
                    # If quotient became 0 due to overestimate corrections
                    steps.append(CalculationStep(
                        f"Quotient revised to 0 due to overestimate - no subtraction performed",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    steps.append(CalculationStep(
                        f"Working dividend remains unchanged: {working_dividend}",
                        self.get_state(),
                        self.get_value()
                    ))
                
                # Update dividend area to show the remainder
                for i in range(dividend_length):
                    rod_index = dividend_start_rod + i
                    steps.extend(self._set_rod_value(rod_index, 0))
                
                # Show the current state with remaining digits
                remaining_digits = dividend_str[dividend_index:] if dividend_index < len(dividend_str) else ""
                current_display = str(working_dividend) + remaining_digits if remaining_digits else str(working_dividend)
                if int(current_display) > 0:
                    steps.extend(self._add_to_rods_left_aligned(dividend_start_rod, int(current_display)))
                
                steps.append(CalculationStep(
                    f"Final remainder for this step: {working_dividend}",
                    self.get_state(),
                    self.get_value()
                ))
                
                # Step 6: Place quotient digit in quotient area
                if current_quotient_rod >= 0:
                    steps.append(CalculationStep(
                        f"Place quotient digit {estimated_quotient} at rod {current_quotient_rod + 1}",
                        self.get_state(),
                        self.get_value()
                    ))
                    
                    steps.extend(self._set_rod_value(current_quotient_rod, estimated_quotient))
                
                # Update state for next iteration
                quotient_digits.append(estimated_quotient)
                current_quotient_rod -= 1  # Move to next quotient position (right to left)
                
                steps.append(CalculationStep(
                    f"Quotient so far: {''.join(map(str, quotient_digits))}, remainder: {working_dividend}",
                    self.get_state(),
                    self.get_value()
                ))
            else:
                # Working dividend is smaller than divisor, place 0 in quotient
                if quotient_digits:  # Only if we already started the quotient
                    quotient_digits.append(0)
                    if current_quotient_rod >= 0:
                        steps.append(CalculationStep(
                            f"Working dividend {working_dividend} < divisor {divisor}, place 0 in quotient",
                            self.get_state(),
                            self.get_value()
                        ))
                        steps.extend(self._set_rod_value(current_quotient_rod, 0))
                        current_quotient_rod -= 1
        
        # Final result processing with enhanced remainder handling
        final_quotient = int(''.join(map(str, quotient_digits))) if quotient_digits else 0
        final_remainder = working_dividend
        
        # Step 1: Remainder detection and analysis using dedicated method
        steps.extend(self._detect_and_display_remainder(final_remainder, divisor, final_quotient, dividend))
        
        # Step 2: Final quotient positioning and workspace cleanup
        steps.append(CalculationStep(
            f"Begin final result processing: quotient = {final_quotient}, remainder = {final_remainder}",
            self.get_state(),
            self.get_value()
        ))
        
        # Clear divisor area first (leftmost rods)
        divisor_length = len(str(divisor))
        divisor_start_rod = self.num_rods - divisor_length
        
        steps.append(CalculationStep(
            f"Clear divisor area (rods {divisor_start_rod + 1}-{self.num_rods})",
            self.get_state(),
            self.get_value()
        ))
        
        for i in range(divisor_length):
            rod_index = divisor_start_rod + i
            if rod_index < self.num_rods:
                steps.extend(self._set_rod_value(rod_index, 0))
        
        # Clear dividend area (rightmost rods) 
        dividend_length = len(str(dividend))
        dividend_start_rod = 0
        
        steps.append(CalculationStep(
            f"Clear dividend area (rods {dividend_start_rod + 1}-{dividend_length})",
            self.get_state(),
            self.get_value()
        ))
        
        for i in range(dividend_length):
            rod_index = dividend_start_rod + i
            steps.extend(self._set_rod_value(rod_index, 0))
        
        # Clear quotient workspace area, keeping only the final result
        quotient_start_rod = self._apply_kojima_placement_rules(dividend, divisor)
        estimated_quotient_length = max(1, len(str(dividend)) - len(str(divisor)) + 1)
        
        steps.append(CalculationStep(
            f"Clear quotient workspace area",
            self.get_state(),
            self.get_value()
        ))
        
        for i in range(estimated_quotient_length):
            rod_index = quotient_start_rod - i
            if rod_index >= 0:
                steps.extend(self._set_rod_value(rod_index, 0))
        
        # Step 3: Position final quotient in standard location (starting from rod 1)
        steps.append(CalculationStep(
            f"Position final quotient {final_quotient} in standard location",
            self.get_state(),
            self.get_value()
        ))
        
        if final_quotient > 0:
            # Place quotient starting from rightmost position (rod 1, index 0)
            quotient_str = str(final_quotient)
            for i, digit_char in enumerate(reversed(quotient_str)):
                rod_index = i  # Start from index 0 for 1's place
                if rod_index < self.num_rods:
                    steps.extend(self._set_rod_value(rod_index, int(digit_char)))
        
        # Step 4: Final result indication with clear remainder display
        if final_remainder == 0:
            steps.append(CalculationStep(
                f"🎉 DIVISION COMPLETE: {dividend} ÷ {divisor} = {final_quotient} (exact division)",
                self.get_state(),
                self.get_value()
            ))
            steps.append(CalculationStep(
                f"✨ Perfect result: No remainder - {divisor} divides evenly into {dividend}",
                self.get_state(),
                self.get_value()
            ))
        else:
            # For divisions with remainders, show both quotient and remainder clearly
            steps.append(CalculationStep(
                f"🎯 DIVISION COMPLETE: {dividend} ÷ {divisor} = {final_quotient} remainder {final_remainder}",
                self.get_state(),
                self.get_value()
            ))
            steps.append(CalculationStep(
                f"📋 Result breakdown: Quotient = {final_quotient}, Remainder = {final_remainder}",
                self.get_state(),
                self.get_value()
            ))
            
            # Add educational explanation of the remainder
            steps.append(CalculationStep(
                f"Remainder explanation: {final_quotient} × {divisor} + {final_remainder} = {final_quotient * divisor + final_remainder} = {dividend}",
                self.get_state(),
                self.get_value()
            ))
            
            # Verification step
            verification = final_quotient * divisor + final_remainder
            if verification == dividend:
                steps.append(CalculationStep(
                    f"Verification successful: quotient and remainder are correct",
                    self.get_state(),
                    self.get_value()
                ))
            else:
                steps.append(CalculationStep(
                    f"Verification failed: {verification} ≠ {dividend} - calculation error detected",
                    self.get_state(),
                    self.get_value()
                ))
        
        return steps
