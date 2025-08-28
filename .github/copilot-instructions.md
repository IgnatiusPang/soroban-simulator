# Soroban Simulator AI Coding Agent Instructions

## Project Context
The Soroban Simulator is a desktop application designed to visually represent a Japanese soroban abacus. It simulates, step-by-step, the process of solving mathematical expressions involving addition and subtraction of positive integers, including handling nested parentheses. The application is built with Python and the PySide6 GUI framework.

## General Rules
*   When the plan changes, update the `specs/tasks.md` document.
*   When the context window or cache is getting full and tokens are running out, summarize the work done so far in a handover document.
*   At the start of every session, please read `specs/tasks.md` and any session handover document. Then continue to do the activity you've been asked to do. At each checkpoint, update `specs/tasks.md` to check off completed items and add any new tasks.

## Architecture Overview

### Core Structure
The application follows a modular design that strictly separates the core calculation logic from the GUI presentation layer.
- **`soroban_simulator/`**: Main application package.
  - **`soroban/`**: The core calculation engine, containing the logic for the abacus, parsing, and calculation steps.
    - `soroban.py`: Represents the state and mechanics of the abacus.
    - `calculator.py`: Orchestrates the calculation process.
    - `calculation_step.py`: A data class for a single simulation step.
    - `parser.py`: Handles parsing of the input expression.
  - **`gui/`**: The PySide6 user interface layer.
    - `main_window.py`: The main application window.
    - `soroban_widget.py`: The custom widget for drawing the soroban.
  - **`tests/`**: Unit tests for the core logic.
    - `test_soroban.py`
    - `test_parser.py`
    - `test_calculator.py`
  - **`main.py`**: The main entry point of the application.

### Key Architectural Patterns
- **Model-View-Controller (MVC) like pattern**: The core logic in `soroban/` acts as the model, containing the application's data and business logic. The GUI in `gui/` acts as the view and controller, presenting the model's data to the user and handling user input.
- **Separation of Concerns**: The calculation logic is completely independent of the GUI, which allows for easier testing and maintenance.

## Development Workflows

### Essential Commands
```bash
# Setup (always use venv for dependency isolation)
python -m venv venv && source venv/bin/activate
pip install PySide6
# It is recommended to create a requirements.txt file
pip freeze > requirements.txt

# Run application
python soroban_simulator/main.py

# Testing
python -m unittest discover tests
```

### Project State Management
- **Always read first**: `specs/tasks.md` at the session start.
- **Update progress**: Check off completed items in `specs/tasks.md`.

## Code Quality Standards

### Type Safety & Style
- **Type hints required**: All new functions must have complete type annotations.
- **Tools**: `ruff` and `black` for static analysis and formatting.
- **Line length**: 88 characters (Black formatter standard).
- **Import order**: stdlib, third-party, local application imports.

### Logging
Use the `logging` module for debugging and tracking events.
```python
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def my_function():
    logging.info("Starting my_function.")
    try:
        # ... function logic ...
        logging.debug("Intermediate step successful.")
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
    logging.info("Finished my_function.")
```

### Error Handling
- Use specific exceptions, not bare `except:`.
- The GUI should display user-friendly error messages.

## Testing Patterns

### Core Logic Tests
Tests for the core logic should be pure, deterministic, and not rely on the GUI.
```python
# tests/test_soroban.py
import unittest
from soroban_simulator.soroban import Soroban

class TestSoroban(unittest.TestCase):
    def test_addition(self):
        soroban = Soroban()
        steps = soroban.add(5)
        self.assertEqual(soroban.get_value(), 5)
        # Further assertions on the steps...
```

## Domain-Specific Knowledge

### Core Classes
- **`Soroban`**: Manages the state of the abacus rods and provides methods like `add`, `subtract`, `set_number`, etc., which return a list of `CalculationStep` objects.
- **`CalculationStep`**: A simple data class that holds the description of a single bead movement, the state of the soroban after the movement, and the current value.
- **`Parser`**: Implements the Shunting-yard algorithm to convert the user's input string into Reverse Polish Notation (RPN).
- **`Calculator`**: Takes an RPN queue from the `Parser` and uses the `Soroban` instance to calculate the result, generating a complete list of `CalculationStep` objects for the entire simulation.

### Common Pitfalls
- **GUI Threading**: All GUI updates must happen on the main thread. Use `QTimer.singleShot(0, callback)` for deferred execution if needed.
- **State Management**: Ensure the state of the soroban is only modified through the methods of the `Soroban` class to maintain consistency.

## Essential Files to Understand
- `specs/requirements.md`: The functional and technical requirements.
- `specs/design.md`: The technical design and architecture.
- `specs/tasks.md`: The development plan and priorities.
- `soroban_simulator/soroban/soroban.py`: The core abacus logic.
- `soroban_simulator/soroban/calculator.py`: The main calculation orchestrator.