from .soroban import Soroban
from .parser import Parser
from .calculation_step import CalculationStep
import logging

logging.basicConfig(level=logging.INFO)

class Calculator:
    """Orchestrates the calculation by evaluating the RPN queue."""

    def __init__(self, num_rods: int = 13):
        """Initializes the calculator."""
        self.soroban = Soroban(num_rods)
        self.parser = Parser()

    def calculate(self, equation_string: str) -> list[CalculationStep]:
        """Calculates the result of an equation string."""
        rpn_queue = self.parser.generate_rpn(equation_string)
        logging.info(f"RPN queue: {rpn_queue}")
        steps = []
        result_stack = []
        is_first_number = True

        operations = {
            '+': self.soroban.add,
            '-': self.soroban.subtract,
            '*': self.soroban.multiply,
        }

        for token in rpn_queue:
            logging.info(f"Processing token: {token}")
            if isinstance(token, int):
                result_stack.append(token)
                logging.info(f"Pushed {token} to result stack: {result_stack}")
            elif token in operations:
                if len(result_stack) < 2:
                    raise ValueError("Invalid expression: not enough operands for operator.")
                
                num2 = result_stack.pop()
                num1 = result_stack.pop()
                logging.info(f"Popped {num1} and {num2} from result stack.")

                if is_first_number:
                    steps.extend(self.soroban.set_number(num1))
                    is_first_number = False
                
                # Check if the value on soroban is already num1
                elif self.soroban.get_value() != num1:
                    logging.warning(f"Soroban value {self.soroban.get_value()} does not match expected value {num1}. This might indicate an issue.")
                    # Decide on a recovery strategy: maybe set the number anyway?
                    # For now, we will log a warning and proceed. A more robust solution might be needed.
                    steps.extend(self.soroban.set_number(num1))


                steps.extend(operations[token](num2))
                
                new_result = self.soroban.get_value()
                result_stack.append(new_result)
                logging.info(f"Pushed {new_result} to result stack: {result_stack}")
            else:
                raise ValueError(f"Unsupported token: {token}")

        if len(result_stack) != 1:
            raise ValueError("Invalid expression: the final stack should have one number.")

        logging.info(f"Final steps: {[step.step_description for step in steps]}")
        return steps
