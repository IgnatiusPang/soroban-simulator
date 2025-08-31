# Soroban Simulator: Requirements

This document outlines the functional and technical requirements for the Soroban Abacus Simulator application.

## 1. Functional Requirements

The application must provide the following capabilities to the end-user:
* Here I am labeling rods 1 - 13 from right to left, rod 1 with smallest value (e.g. 1's) and rod 13 largest value (e.g. 1 x 10^12). 

*   **Equation Input:** The user must be able to input a mathematical expression as a string.
    *   Initial scope includes positive integers, addition (+), and subtraction (-).
    *   The input must support nested parentheses () for defining the order of operations.
*   **Visual Soroban:** The application must display a graphical representation of a Japanese soroban abacus.
*   **Step-by-Step Simulation:** The calculation must be broken down into a sequence of individual steps.
    *   A "step" is defined as a single, granular bead movement on the soroban.
    *   The simulation must accurately reflect the techniques used on a real soroban (e.g., using complements for addition/subtraction).
*   **Navigation:** The user must be able to navigate through the calculation steps.
    *   A "Next" button to advance to the next bead movement.
    *   A "Previous" button to revert to the prior bead movement.
*   **State Display:** At every step, the application must clearly display:
    *   A text description of the specific action being performed (e.g., "Units rod: Carry over 1").
    *   The current numerical value represented on the soroban.

## 2. Technical Requirements

The application must adhere to the following technical specifications:
*   **Framework:** The Graphical User Interface (GUI) must be built using the PySide6 framework.
*   **Architecture:** The application must have a modular design, strictly separating the core calculation logic from the GUI presentation layer.
*   **Testability:** The core logic must have near-complete or complete unit test coverage to ensure accuracy and reliability.
*   **Extensibility:** The codebase must be designed to be easily expandable in the future to include:
    *   Multiplication and division operations.
    *   Decimal (floating-point) calculations.
    *   Handling of negative values.
    *   Modular arithmetic.
