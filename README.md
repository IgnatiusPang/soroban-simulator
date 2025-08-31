# Soroban Simulator

A desktop application that simulates a Japanese soroban (abacus). It can perform arithmetic operations (addition, subtraction, and multiplication) and shows the granular steps of bead movements using traditional soroban calculation methods.

## Features

*   Visual representation of a soroban with 13 rods.
*   Step-by-step simulation of calculations with detailed bead movements.
*   **Addition**: Full support with carry operations and granular bead movement steps.
*   **Subtraction**: Full support with borrow operations and granular bead movement steps.
*   **Multiplication**: Modern Standard Method implementation with proper rod positioning and partial product calculations.
*   Supports expressions with parentheses.
*   Shows textual description of each step with correct rod numbering.
*   Rod positioning follows traditional soroban convention: Rod 1 (rightmost) = ones place, Rod 2 = tens place, etc.

## Supported Operations

- ✅ **Addition** (`+`): Complete implementation with detailed steps
- ✅ **Subtraction** (`-`): Complete implementation with detailed steps  
- ✅ **Multiplication** (`*`): Modern Standard Method with optimized step descriptions
- ❌ **Division** (`/`): Not yet implemented

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
