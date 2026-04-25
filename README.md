# Soroban Simulator

A desktop application that simulates a Japanese soroban (abacus). It performs all four basic arithmetic operations (addition, subtraction, multiplication, and division) and demonstrates granular bead movements using traditional Japanese methods.

## Features

*   Visual representation of a soroban with 13 rods.
*   Step-by-step simulation of calculations with detailed bead movements.
*   **Educational Narratives**: Rich textual descriptions including reasoning, emojis, and process indicators (REVISE, COMPENSATION, ESTIMATE).
*   **Addition**: Full support with carry operations and granular bead movement steps.
*   **Subtraction**: Full support with borrow operations and granular bead movement steps.
*   **Multiplication**: Modern Standard Method implementation with proper rod positioning and partial product calculations.
*   **Division**: Comprehensive **Modern Division Method (shojohou)** implementation with estimation-multiply-subtract-revise cycle, upward/downward revisions, and Kojima rules.
*   Supports expressions with parentheses.
*   Shows textual description of each step with correct rod numbering.
*   Rod positioning follows traditional soroban convention: Rod 1 (rightmost) = ones place, Rod 2 = tens place, etc.

## Supported Operations

- ✅ **Addition** (`+`): Complete implementation with detailed steps
- ✅ **Subtraction** (`-`): Complete implementation with detailed steps  
- ✅ **Multiplication** (`*`): Modern Standard Method with optimized step descriptions
- ✅ **Division** (`/`): Modern Division Method (shojohou) with estimation-multiply-subtract-revise cycle

## Calculation Examples

### Addition: `123 + 456`
Shows detailed bead movements for setting the initial number and adding each digit.

### Subtraction: `789 - 234` 
Shows detailed bead movements including borrow operations when needed.

### Multiplication: `123 * 456`
Uses the Modern Standard Method with:
- Multiplier positioning on rods 10-11
- Multiplicand positioning on rods 7-8  
- Result calculation in rods 1-5
- Optimized steps that skip unnecessary initial number setting details

### Division: `951 / 3`
Uses the Modern Division Method (shojohou) with:
- Divisor positioning on leftmost rods (Kojima Rule I/II)
- Dividend positioning on rightmost rods
- Quotient calculation using **Estimation-Multiply-Subtract-Revise** cycle
- Educational reasoning steps explaining the quotient digit selection
- Verification step: `Dividend = Quotient × Divisor + Remainder`
## Methodology: Shojohou (Modern Division)

The simulator implements the *shojohou* method, which is the standard modern approach for soroban division. It features:
- **Conservative Estimation**: Initial quotient digits are estimated conservatively to prevent early subtraction errors.
- **Upward/Downward Revision**: Step-by-step correction of quotient estimates using the *revise_up* and *revise_down* cycles.
- **Kojima Positioning**: Traditional rules for placing the divisor and dividend to ensure the quotient appears on the intuitive rod.

## Release Notes

### v1.0.0 (Stable Release)
- **Complete Basic Ops**: Addition, Subtraction, Multiplication, and Division fully implemented.
- **Pedagogical Polish**: Emojis, reasoning steps, and process indicators added to all operations.
- **100% Test Coverage**: All 167 functional and pedagogical tests passing.
- **Stable GUI**: Refined PySide6 interface with accurate rod highlighting.

## Prerequisites

*   Python 3.x
*   PySide6

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/soroban-simulator.git
    cd soroban-simulator
    ```

2.  Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install the required dependencies:
    ```bash
    pip install PySide6
    ```

## How to Run

To start the application, run the following command from the root directory of the project:

```bash
python3 -m soroban_simulator.main
```

## How to Run Tests

To run the unit tests, run the following command:

```bash
python3 -m unittest discover soroban_simulator/tests
```

### Files Kept for Manual Testing
- **test_different_multiplication.py** - GUI test for 7×38 multiplication
- **test_gui_positioning_fixed.py** - GUI test for marker positioning fixes
- **test_gui_positioning.py** - GUI test for rod numbers and markers
- **test_rod_order.py** - Educational rod ordering demonstration
- **simple_multiply_test.py** - Educational breakdown of 51×3 multiplication
- **debug_4x5_detailed.py** - Detailed 4×5 step tracking (converted to unit test)
- **debug_4x5.py** - Simple 4×5 test (converted to unit test)
- **debug_interim_value.py** - Interim value testing (converted to unit test)
- **debug_marker_calculation.py** - Marker calculation logic (converted to unit test)
- **debug_multiplication_logic.py** - 51×3 algorithm analysis (educational value)
