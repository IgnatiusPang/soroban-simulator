
import functools
from decimal import Decimal
from .soroban import Soroban
from .parser import Parser
from .calculation_step import CalculationStep
import logging

logging.basicConfig(level=logging.INFO)

class Calculator:
    """Orchestrates the calculation by evaluating the RPN queue using functional patterns."""

    def __init__(self, num_rods: int = 13, unit_rod_index: int = 0):
        """Initialises the calculator."""
        self.soroban = Soroban(num_rods, unit_rod_index)
        self.parser = Parser()

    def calculate(self, equation_string: str) -> list[CalculationStep]:
        """Calculates the result of an equation string using absolute functional patterns."""
        rpn_queue = self.parser.generate_rpn(equation_string)
        logging.info(f"RPN queue: {rpn_queue}")

        operations = {
            '+': self.soroban.add,
            '-': self.soroban.subtract,
            '*': self.soroban.multiply,
            '/': self.soroban.divide,
        }

        def process_token(state, token):
            steps, result_stack, is_first_number = state
            logging.info(f"Processing token: {token}")

            if isinstance(token, (int, Decimal)):
                return (steps, result_stack + [token], is_first_number)
            
            if token in operations:
                if len(result_stack) < 2:
                    raise ValueError("Invalid expression: not enough operands for operator.")
                
                num1, num2 = result_stack[-2:]
                new_stack = result_stack[:-2]
                
                op_steps = []
                current_is_first = is_first_number

                # Operation-specific description
                op_desc_map = {'+': "addition operation", '-': "subtraction operation", '*': "multiplication operation", '/': "division operation"}
                op_desc = op_desc_map.get(token, "operation")

                if token == '*':
                    if current_is_first:
                        op_steps.extend(self.soroban.clear())
                        current_is_first = False
                    op_steps.extend(self.soroban.multiply_with_setup(num2, num1))
                elif token == '/':
                    if current_is_first:
                        op_steps.extend(self.soroban.clear())
                        current_is_first = False
                    op_steps.extend(self.soroban.divide(num1, num2))
                else:
                    if current_is_first:
                        op_steps.extend(self.soroban.set_number(num1))
                        current_is_first = False
                    elif self.soroban.get_value() != num1:
                        logging.warning(f"Soroban value {self.soroban.get_value()} mismatch {num1}. Resetting.")
                        op_steps.extend(self.soroban.set_number(num1))
                    
                    op_steps.extend(operations[token](num2))

                new_result = self.soroban.get_value()
                op_steps.append(CalculationStep(f"Complete {token} operation ({op_desc})", self.soroban.get_state(), new_result))
                return (steps + op_steps, new_stack + [new_result], current_is_first)
            
            raise ValueError(f"Unsupported token: {token}")

        # Reduce the RPN queue to the final calculation state
        initial_state = ([], [], True)
        final_steps, final_result_stack, _ = functools.reduce(process_token, rpn_queue, initial_state)

        if len(final_result_stack) != 1:
            raise ValueError("Invalid expression: the final stack should have one number.")

        return final_steps
