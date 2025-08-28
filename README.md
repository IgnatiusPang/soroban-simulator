# Soroban Simulator

A simple desktop application that simulates a Japanese soroban (abacus). It can perform basic arithmetic operations (+, -) and shows the granular steps of bead movements.

## Features

*   Visual representation of a soroban.
*   Step-by-step simulation of calculations.
*   Supports addition and subtraction with parentheses.
*   Shows textual description of each step.

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
