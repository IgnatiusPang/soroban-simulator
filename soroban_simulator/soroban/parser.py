
import re

class Parser:
    """Parses the input string into a format that respects the order of operations."""

    def generate_rpn(self, equation_string: str) -> list:
        """Converts an infix equation string to a Reverse Polish Notation (RPN) queue."""
        # Add spaces around operators and parentheses
        equation_string = re.sub(r'([+\-*/()])', r' \1 ', equation_string)
        tokens = equation_string.split()

        output_queue = []
        operator_stack = []

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if token.isnumeric():
                output_queue.append(int(token))
            elif token in precedence:
                while (
                    operator_stack
                    and operator_stack[-1] != '('
                    and precedence.get(operator_stack[-1], 0) >= precedence.get(token, 0)
                ):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Discard the '('
                else:
                    raise ValueError("Mismatched parentheses")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())

        return output_queue
