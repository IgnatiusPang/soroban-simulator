# Soroban Simulator: Technical Design

This document provides the technical blueprint for the Soroban Abacus Simulator, detailing the classes, methods, and overall architecture.

## 1. Core Logic

The core logic is encapsulated in a dedicated module, independent of the GUI.

### 1.1. Soroban Class

Represents the state of the abacus and generates granular bead movements.

**Attributes:**

*   `rods`: A list of integers representing the value of each rod (0-9).

**Methods:**

*   `__init__(self, num_rods=13)`: Initializes the abacus.
*   `get_value(self)`: Returns the current integer value.
*   `get_state(self)`: Returns a data structure representing bead positions for rendering.
*   `clear(self)`: Resets all rods to 0.
*   `set_number(self, number)`: Returns a list of `CalculationStep` objects for setting a number on the abacus, digit by digit.
*   `add(self, number)`: Returns a list of `CalculationStep` objects detailing every bead movement (including complements and carries) required for the addition.
*   `subtract(self, number)`: Returns a list of `CalculationStep` objects detailing every bead movement (including borrows) for the subtraction.
*   `multiply(self, number)`: Returns a list of `CalculationStep` objects detailing every bead movement for the multiplication using the Modern Standard Method.

### 1.2. CalculationStep Class

A simple data class holding the state for a single step.

**Attributes:**

*   `step_description`: A detailed string describing the specific bead movement.
*   `soroban_state`: The state of the soroban after the movement.
*   `current_value`: The numerical value on the soroban at that step.

### 1.3. Parser Class

Parses the input string into a format that respects the order of operations.

**Methods:**

*   `generate_rpn(self, equation_string)`: Implements the Shunting-yard algorithm to convert an infix equation string (e.g., "10 + (5 - 2)") into a Reverse Polish Notation (RPN) queue (e.g., `[10, 5, 2, '-', '+']`).

### 1.4. Calculator Class

Orchestrates the calculation by evaluating the RPN queue.

**Attributes:**

*   `soroban`: An instance of the `Soroban` class.
*   `parser`: An instance of the `Parser` class.

**Methods:**

*   `calculate(self, equation_string)`:
    *   Generates the RPN queue using the parser.
    *   Initializes a main steps list and an intermediate results stack.
    *   Iterates through the RPN queue, performing sub-calculations for each operator.
    *   For each sub-calculation, it calls the appropriate `Soroban` methods (`set_number`, `add`, `subtract`, `multiply`) and extends the main steps list with the granular `CalculationStep` objects returned.
    *   Returns the final, complete list of all granular steps in the correct order.

## 2. Graphical User Interface (GUI)

The GUI is built with PySide6.

*   **MainWindow (QMainWindow):** The main application window containing all UI elements (`QLineEdit`, `QPushButton`, `QLabel`) and the `SorobanWidget`. It manages the application state, such as the current step index.
*   **SorobanWidget (QWidget):** A custom widget responsible for drawing the soroban. Its `paintEvent` method will render the beads and rods based on the `soroban_state` passed to it via a `set_state` method.

## 3. Unit Testing

The `unittest` framework will be used.

*   **TestSoroban:** Will verify that the `add` and `subtract` methods return the correct sequence of `CalculationStep` objects for various scenarios.
*   **TestParser:** Will verify the correct RPN output for equations with and without brackets.
*   **TestModernMultiplication:** Will verify that the `multiply` method returns the correct sequence of `CalculationStep` objects for the Modern Standard Method.
*   **TestCalculator:** Will verify that the final aggregated list of steps is correct for a complete equation.

## 4. Project Structure

```
soroban_simulator/
├── main.py
├── soroban/
│   ├── __init__.py
│   ├── soroban.py
│   ├── calculator.py
│   └── calculation_step.py
├── gui/
│   ├── __init__.py
│   ├── main_window.py
│   └── soroban_widget.py
└── tests/
    ├── __init__.py
    ├── test_soroban.py
    ├── test_parser.py
    ├── test_calculator.py
    └── test_modern_multiplication.py
```