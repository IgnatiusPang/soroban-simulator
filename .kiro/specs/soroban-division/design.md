# Design Document

## Overview

The division implementation follows the Modern Division Method (shojohou), which treats division as iterative subtraction. The design integrates seamlessly with the existing soroban simulator architecture, extending the `Soroban` class with division capabilities and updating the `Calculator` class to handle the "/" operator.

The shojohou method operates on a four-step cycle:
1. **Estimate**: Determine a provisional quotient digit by mental estimation
2. **Multiply**: Calculate the product of the estimated digit and the divisor
3. **Subtract**: Remove the product from the current dividend fragment
4. **Revise**: Adjust the quotient digit if the estimate was incorrect

## Architecture

### Core Components

The division functionality extends the existing architecture without breaking changes:

```
Soroban Class (Extended)
├── divide(dividend: int, divisor: int) -> List[CalculationStep]
├── _estimate_quotient_digit(dividend_fragment: int, divisor: int) -> int
├── _apply_kojima_placement_rules(dividend: int, divisor: int) -> int
└── _setup_division_workspace(dividend: int, divisor: int) -> List[CalculationStep]

Calculator Class (Extended)
└── Updated to handle "/" operator in RPN evaluation

Parser Class (Extended)
└── Updated to recognize "/" with appropriate operator precedence
```

## Components and Interfaces

### 1. Soroban Class Extensions

#### Primary Method: `divide(dividend: int, divisor: int) -> List[CalculationStep]`

**Purpose**: Orchestrates the complete division process using shojohou method

**Algorithm Flow**:
1. Clear the soroban and set up workspace with visual markers
2. Position divisor on leftmost rods, dividend on rightmost rods
3. Apply Kojima's placement rules to determine quotient starting position
4. Execute the estimate-multiply-subtract-revise cycle for each quotient digit
5. Handle remainders and finalize the result

**Rod Positioning Strategy**:
- Divisor: Leftmost rods (indices 10-12 for typical cases)
- Dividend: Rightmost rods (indices 0-4 for typical cases)  
- Quotient workspace: Middle rods (indices 5-9)
- Buffer zones: Minimum 1 rod between each section

#### Helper Method: `_estimate_quotient_digit(dividend_fragment: int, divisor: int) -> int`

**Purpose**: Implements the mental estimation logic central to shojohou

**Estimation Strategy**:
- For single-digit divisors: Direct division of dividend fragment by divisor
- For multi-digit divisors: Approximate by dividing first 1-2 digits of dividend fragment by first digit of divisor
- Apply bounds checking to ensure estimate doesn't exceed 9
- Use conservative estimation to minimize revision frequency

#### Helper Method: `_apply_kojima_placement_rules(dividend: int, divisor: int) -> int`

**Purpose**: Determines correct starting rod for quotient based on Kojima's rules

**Rule Implementation**:
- Rule I: If first digit of divisor ≤ first digit of dividend → quotient starts 2 rods left of dividend
- Rule II: If first digit of divisor > first digit of dividend → quotient starts 1 rod left of dividend
- Returns the rod index where the first quotient digit should be placed

#### Helper Method: `_setup_division_workspace(dividend: int, divisor: int) -> List[CalculationStep]`

**Purpose**: Prepares the soroban with proper number placement and visual markers

**Setup Process**:
1. Clear all rods
2. Calculate optimal positioning based on number sizes
3. Place divisor on designated leftmost rods
4. Place dividend on designated rightmost rods
5. Add visual markers for D (Divisor), DV (Dividend), Q (Quotient) areas
6. Return setup steps with descriptive text

### 2. Calculator Class Integration

#### Updated Method: `calculate(equation_string: str) -> List[CalculationStep]`

**Division Integration**:
- Extend RPN token processing to handle "/" operator
- When "/" is encountered, pop two operands and call `soroban.divide(num1, num2)`
- Maintain existing error handling for invalid expressions
- Ensure division by zero throws appropriate exception

### 3. Parser Class Integration

#### Updated Method: `generate_rpn(equation_string: str) -> List`

**Operator Precedence**:
- Division "/" has same precedence as multiplication "*"
- Left-to-right associativity for same-precedence operators
- Proper handling in Shunting-yard algorithm implementation

## Data Models

### CalculationStep Extensions

The existing `CalculationStep` class supports the division implementation without modifications:

```python
@dataclass
class CalculationStep:
    step_description: str      # Detailed description of division step
    soroban_state: List[int]   # Rod values after the step
    current_value: int         # Current soroban value
    markers: List[Tuple] = None # Visual markers for D, DV, Q areas
```

### Division State Tracking

Internal state during division process:

```python
DivisionState = {
    'dividend_remaining': int,     # Current dividend fragment
    'quotient_built': str,         # Quotient digits accumulated so far
    'current_quotient_rod': int,   # Rod index for next quotient digit
    'divisor_value': int,          # Original divisor value
    'divisor_rods': List[int],     # Rod indices containing divisor
}
```

## Error Handling

### Division-Specific Error Cases

1. **Division by Zero**
   - Detection: Check if divisor equals 0 before processing
   - Response: Raise `ValueError` with descriptive message
   - User feedback: Clear error message in GUI

2. **Invalid Operands**
   - Detection: Ensure both dividend and divisor are positive integers
   - Response: Raise `ValueError` for negative numbers or non-integers
   - Future extension: Support for negative numbers and decimals

3. **Workspace Overflow**
   - Detection: Check if numbers fit within 13-rod soroban
   - Response: Raise `ValueError` if positioning is impossible
   - Mitigation: Suggest using larger numbers within reasonable bounds

### Revision Handling

The shojohou method naturally handles estimation errors through revisions:

1. **Overestimate Detection**: When subtraction is impossible (product > dividend fragment)
2. **Underestimate Detection**: When remainder ≥ divisor after subtraction
3. **Revision Process**: Adjust quotient digit up/down and recalculate

## Testing Strategy

### Unit Test Coverage

#### TestSorobanDivision Class

**Basic Division Tests**:
- `test_simple_single_digit_division()`: 951 ÷ 3 = 317
- `test_division_with_remainder()`: 259 ÷ 7 = 37 remainder 0
- `test_multi_digit_divisor()`: 3869 ÷ 53 = 73

**Edge Case Tests**:
- `test_division_by_one()`: Any number ÷ 1
- `test_division_resulting_in_zero()`: 0 ÷ any number
- `test_division_by_zero_error()`: Error handling verification

**Kojima Rule Tests**:
- `test_kojima_rule_one()`: Cases where divisor first digit ≤ dividend first digit
- `test_kojima_rule_two()`: Cases where divisor first digit > dividend first digit

**Estimation Tests**:
- `test_quotient_estimation_accuracy()`: Verify estimation algorithm
- `test_revision_handling()`: Test overestimate and underestimate corrections

#### TestCalculatorDivision Class

**Integration Tests**:
- `test_division_in_expression()`: "100 / 4" evaluation
- `test_mixed_operations()`: "20 + 15 / 3 - 2" evaluation
- `test_division_precedence()`: Operator precedence verification

#### TestParserDivision Class

**Parsing Tests**:
- `test_division_operator_recognition()`: "/" token parsing
- `test_division_precedence()`: Precedence relative to +, -, *
- `test_complex_expressions()`: Nested expressions with division

### Integration Testing

**End-to-End Scenarios**:
1. User inputs "951/3" → System produces 317 with detailed steps
2. User inputs "100/7" → System produces 14 remainder 2 with explanations
3. User inputs "3869/53" → System demonstrates multi-digit divisor handling

### Performance Considerations

**Step Generation Efficiency**:
- Minimize redundant calculations during estimation
- Optimize rod positioning algorithms
- Ensure step descriptions are generated efficiently

**Memory Usage**:
- Reasonable step count for typical division problems
- Efficient storage of intermediate states
- Proper cleanup of temporary calculations

## Visual Design Elements

### Soroban Markers

**Division Workspace Markers**:
- **D (Divisor)**: Blue markers on leftmost rods containing divisor
- **DV (Dividend)**: Green markers on rightmost rods containing dividend  
- **Q (Quotient)**: Red markers on middle rods where quotient is built

### Step Descriptions

**Descriptive Text Patterns**:
- Setup: "Position divisor 53 on rods 11-12, dividend 3869 on rods 1-4"
- Estimation: "Estimate: 38 ÷ 5 ≈ 7, place 7 in quotient"
- Multiplication: "Calculate: 7 × 53 = 371"
- Subtraction: "Subtract 371 from 386, remainder: 15"
- Revision: "Remainder 15 > divisor 7, revise quotient up by 2"

This design provides a comprehensive foundation for implementing division using the shojohou method while maintaining compatibility with the existing soroban simulator architecture.