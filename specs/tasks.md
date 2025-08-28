# Soroban Simulator: Development Tasks

This document outlines the development tasks for building the Soroban Abacus Simulator.

## Phase 1: Core Logic Implementation

- [x] **Task 1.1: Implement `CalculationStep` Class**
  - Create `soroban/calculation_step.py`.
  - Define attributes: `step_description`, `soroban_state`, `current_value`.

- [x] **Task 1.2: Implement `Soroban` Class**
  - Create `soroban/soroban.py`.
  - Implement `__init__`, `get_value`, `get_state`, `clear`.
  - Implement `set_number` method.
  - Implement `add` method with complement logic.
  - Implement `subtract` method with borrow logic.

- [x] **Task 1.3: Implement `Parser` Class**
  - Create `soroban/parser.py`.
  - Implement Shunting-yard algorithm in `generate_rpn`.

- [x] **Task 1.4: Implement `Calculator` Class**
  - Create `soroban/calculator.py`.
  - Implement `calculate` method to orchestrate RPN evaluation.

## Phase 2: Unit Testing

- [x] **Task 2.1: Write Tests for `Soroban` Class**
  - Create `tests/test_soroban.py`.
  - Test `set_number`, `add`, and `subtract` methods for various cases.

- [x] **Task 2.2: Write Tests for `Parser` Class**
  - Create `tests/test_parser.py`.
  - Test RPN conversion with different equations.

- [x] **Task 2.3: Write Tests for `Calculator` Class**
  - Create `tests/test_calculator.py`.
  - Test full calculation workflow.

## Phase 3: GUI Development

- [x] **Task 3.1: Implement `SorobanWidget`**
  - Create `gui/soroban_widget.py`.
  - Implement `paintEvent` to draw the abacus from state.

- [x] **Task 3.2: Implement `MainWindow`**
  - Create `gui/main_window.py`.
  - Add input field, buttons, and labels.
  - Integrate `SorobanWidget`.
  - Connect GUI signals to calculator logic.

- [x] **Task 3.3: Create Main Application Entry Point**
  - Create `main.py`.
  - Initialize and show the `MainWindow`.

## Phase 4: Integration and Refinement

- [x] **Task 4.1: End-to-End Testing**
  - Manually test the full application.
- [ ] **Task 4.2: Code Review and Refactoring**
  - Review codebase for clarity, consistency, and adherence to design.
- [ ] **Task 4.3: Documentation**
  - Write a `README.md` with instructions on how to run the application.

## Phase 5: GUI Polish

- [ ] **Task 5.1: Implement Bead Movement Animation**
  - The four beads that represents 1's 10's 100's etc... are not moving. they are only turning blue
  - Animate granular steps from `CalculationStep` objects, such as carrying over, to show the bead movements. The `paintEvent` in `soroban_widget.py` is currently static and only redraws the final state of a calculation.
- [ ] **Task 5.2: Add Step Notation Viewer**
  - Display a sequential list of all calculation steps, similar to chess notation.
- [ ] **Task 5.3: Indicate Calculation Completion**
  - Display a "Calculation Complete" message when the last step is reached.

## Bug Fixes

- [ ] **Task 6.1: Correct Bead Positioning**
  - The top beads should not overlap with the horizontal line, only touch it.
  - The bottom beads are not touching the horizontal line; they should touch it but not overlap.
- [ ] **Task 6.2: Fix Bead Coloring Issue**
  - During the calculation `5 + 13`, the result `18` is correctly represented, but one of the beads representing the value '1' (in the tens column) is not colored blue as it should be.