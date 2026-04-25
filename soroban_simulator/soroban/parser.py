
import re
import functools
from decimal import Decimal

class Parser:
    """Parses the input string into a format that respects the order of operations."""

    def generate_rpn(self, equation_string: str) -> list:
        """Converts an infix equation string to a Reverse Polish Notation (RPN) queue using functional patterns."""
        # Add spaces around operators and parentheses
        equation_string = re.sub(r'([+\-*/()])', r' \1 ', equation_string)
        tokens = equation_string.split()
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        def process_token(state, token):
            output_queue, operator_stack = state

            if re.match(r'^\d+(\.\d+)?$', token):
                return (output_queue + [Decimal(token)], operator_stack)
            
            if token in precedence:
                # Helper for while-loop logic (pop higher precedence operators)
                def pop_ops(q, s):
                    if s and s[-1] != '(' and precedence.get(s[-1], 0) >= precedence.get(token, 0):
                        return pop_ops(q + [s[-1]], s[:-1])
                    return q, s
                
                new_q, new_s = pop_ops(output_queue, operator_stack)
                return (new_q, new_s + [token])
            
            if token == '(':
                return (output_queue, operator_stack + [token])
            
            if token == ')':
                # Helper for while-loop logic (pop until open parenthesis)
                def pop_to_bracket(q, s):
                    if not s:
                        raise ValueError("Mismatched parentheses")
                    if s[-1] == '(':
                        return q, s[:-1]
                    return pop_to_bracket(q + [s[-1]], s[:-1])
                
                return pop_to_bracket(output_queue, operator_stack)
            
            raise ValueError(f"Unsupported token: {token}")

        # Process all tokens using reduce
        initial_state = ([], [])
        final_q, final_s = functools.reduce(process_token, tokens, initial_state)

        # Helper to drain the remaining operator stack
        def drain_stack(q, s):
            if not s:
                return q
            if s[-1] == '(':
                raise ValueError("Mismatched parentheses")
            return drain_stack(q + [s[-1]], s[:-1])

        return drain_stack(final_q, final_s)
