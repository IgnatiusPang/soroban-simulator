
from .soroban import Soroban
from .parser import Parser
from .calculation_step import CalculationStep

class Calculator:
    """Orchestrates the calculation by evaluating the RPN queue."""

    def __init__(self, num_rods: int = 13):
        """Initializes the calculator."""
        self.soroban = Soroban(num_rods)
        self.parser = Parser()

    def calculate(self, equation_string: str) -> list[CalculationStep]:
        """Calculates the result of an equation string."""
        rpn_queue = self.parser.generate_rpn(equation_string)
        steps = []
        result_stack = []

        operations = {
            '+': self.soroban.add,
            '-': self.soroban.subtract,
        }

        for token in rpn_queue:
            if isinstance(token, int):
                result_stack.append(token)
            elif token in operations:
                if len(result_stack) < 2:
                    raise ValueError("Invalid expression: not enough operands for operator.")
                num2 = result_stack.pop()
                num1 = result_stack.pop()

                # Set the first number on the soroban
                steps.extend(self.soroban.set_number(num1))

                # Perform the operation
                steps.extend(operations[token](num2))
                
                # Push the result back to the stack
                result_stack.append(self.soroban.get_value())
            else:
                raise ValueError(f"Unsupported token: {token}")

        if len(result_stack) != 1:
            raise ValueError("Invalid expression: the final stack should have one number.")

        return steps
