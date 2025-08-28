
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
        return self.rods

    def clear(self) -> list[CalculationStep]:
        """Resets all rods to 0."""
        self.rods = [0] * self.num_rods
        return [
            CalculationStep(
                step_description="Clear the soroban",
                soroban_state=self.get_state(),
                current_value=self.get_value(),
            )
        ]

    def set_number(self, number: int) -> list[CalculationStep]:
        """Sets a number on the abacus, digit by digit."""
        steps = self.clear()
        number_str = str(number)

        for i, digit_char in enumerate(reversed(number_str)):
            rod_index = self.num_rods - 1 - i
            if rod_index < 0:
                break
            digit = int(digit_char)
            self.rods[rod_index] = digit
            steps.append(
                CalculationStep(
                    step_description=f"Set rod {self.num_rods - i} to {digit}",
                    soroban_state=self.get_state(),
                    current_value=self.get_value(),
                )
            )
        return steps

    def add(self, number: int) -> list[CalculationStep]:
        """Adds a number to the abacus."""
        steps = []
        number_str = str(number)
        carry = 0

        for i, digit_char in enumerate(reversed(number_str)):
            rod_index = self.num_rods - 1 - i
            digit = int(digit_char)

            new_value = self.rods[rod_index] + digit + carry
            carry = 1 if new_value >= 10 else 0
            self.rods[rod_index] = new_value % 10

            steps.append(
                CalculationStep(
                    step_description=f"Add {digit} to rod {self.num_rods - i}",
                    soroban_state=self.get_state(),
                    current_value=self.get_value(),
                )
            )

            if carry > 0:
                steps.append(
                    CalculationStep(
                        step_description=f"Carry over 1 to rod {self.num_rods - i - 1}",
                        soroban_state=self.get_state(),
                        current_value=self.get_value(),
                    )
                )

        # Handle remaining carry
        i = len(number_str)
        while carry > 0 and self.num_rods - 1 - i >= 0:
            rod_index = self.num_rods - 1 - i
            new_value = self.rods[rod_index] + carry
            carry = 1 if new_value >= 10 else 0
            self.rods[rod_index] = new_value % 10
            steps.append(
                CalculationStep(
                    step_description=f"Add carry to rod {self.num_rods - i}",
                    soroban_state=self.get_state(),
                    current_value=self.get_value(),
                )
            )
            i += 1

        return steps

    def subtract(self, number: int) -> list[CalculationStep]:
        """Subtracts a number from the abacus."""
        steps = []
        number_str = str(number)
        borrow = 0

        for i, digit_char in enumerate(reversed(number_str)):
            rod_index = self.num_rods - 1 - i
            digit = int(digit_char)

            new_value = self.rods[rod_index] - digit - borrow
            
            if new_value < 0:
                borrow = 1
                self.rods[rod_index] = new_value + 10
            else:
                borrow = 0
                self.rods[rod_index] = new_value

            steps.append(
                CalculationStep(
                    step_description=f"Subtract {digit} from rod {self.num_rods - i}",
                    soroban_state=self.get_state(),
                    current_value=self.get_value(),
                )
            )

            if borrow > 0:
                steps.append(
                    CalculationStep(
                        step_description=f"Borrow 1 from rod {self.num_rods - i - 1}",
                        soroban_state=self.get_state(),
                        current_value=self.get_value(),
                    )
                )

        # Handle remaining borrow
        i = len(number_str)
        while borrow > 0 and self.num_rods - 1 - i >= 0:
            rod_index = self.num_rods - 1 - i
            new_value = self.rods[rod_index] - borrow
            
            if new_value < 0:
                borrow = 1
                self.rods[rod_index] = new_value + 10
            else:
                borrow = 0
                self.rods[rod_index] = new_value

            steps.append(
                CalculationStep(
                    step_description=f"Subtract borrow from rod {self.num_rods - i}",
                    soroban_state=self.get_state(),
                    current_value=self.get_value(),
                )
            )
            i += 1

        return steps
