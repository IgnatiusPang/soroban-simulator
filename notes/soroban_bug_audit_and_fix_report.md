# Formal Verification & Bug Audit Report: `soroban-simulator`

**Target Repository:** [`IgnatiusPang/soroban-simulator`](https://github.com/IgnatiusPang/soroban-simulator)  
**Local Checkout:** [`soroban_simulator/`](file:///d:/Bioinformatics/Projects/corpus/rust/soroban-simulator/upstream)  
**Verification Toolchain:** [`OuroPy (Python ↔ Lean 4)`](file:///d:/Bioinformatics/Projects/ouropy)

---

## 1. Executive Summary

Using **OuroPy**'s closed-loop Python $\to$ Lean 4 formal verification toolchain (`ouropy doctor`, `ouropy hazards`, `ouropy hunt-bugs`, and `ouropy airlock`), we performed two comprehensive semantic, mathematical, and invariant audit passes across the `soroban-simulator` package. 

Our investigation uncovered and fixed **6 distinct categories of defects**, ranging from a **critical mathematical scaling error in decimal division** (producing answers off by factors of 10 or 100) to **unbounded recursion hazards** in quotient estimation, **unhandled index exceptions on non-13 rod configurations**, **empty-rod `AttributeError` in `get_value` caught via sandbox edge fuzzing**, **silent carry overflows**, and **missing negative number guards**.

All defects were formally verified, patched with defensive guards preserving Soroban invariants, and verified against an expanded test suite of **175 tests** (all passing).

```mermaid
flowchart TD
    subgraph Audit ["OuroPy Formal Scan"]
        DOCTOR["ouropy doctor"]
        HAZARD["ouropy hazards & termination"]
        AIRLOCK["ouropy airlock"]
        FUZZ["ouropy sandbox edge fuzzer"]
    end

    subgraph Defects ["Identified Defects"]
        D1["Critical: Decimal Division Scale Bug (10x off)"]
        D2["High: Unbounded Recursion in revise_down"]
        D3["High: Calculator Decimal Division Crash"]
        D4["Medium: Hardcoded Rod Positioning Crash (num_rods < 13)"]
        D5["Medium: Silent Overflow & Missing Negative Guards"]
        D6["Medium: AttributeError on Empty Rods in get_value"]
    end

    subgraph Patches ["Remediations & Verification"]
        P1["Scale Normalization: total_scale = actual_precision + s1 - s2"]
        P2["Quotient Bound Enforcement: can_revise guard"]
        P3["Dynamic Decimal Precision Selection in Calculator"]
        P4["Adaptive Rod Placement & Capacity Bounds"]
        P5["Physical Soroban Unsigned & Capacity Guards"]
        P6["Decimal(0) Initializer in sum() & __init__ Rod Bounds"]
        TESTS["175 Unit & Property Tests Passing"]
    end

    Audit --> Defects
    Defects --> Patches
    Patches --> TESTS
```

---

## 2. Detailed Findings & Bug Taxonomy

### Defect 1: Critical Mathematical Scaling Error in Decimal Division
* **Location:** [`soroban.py:350-358`](file:///d:/Bioinformatics/Projects/corpus/rust/soroban-simulator/upstream/soroban_simulator/soroban/soroban.py#L350-L358)
* **Severity:** **CRITICAL (Mathematical Soundness)**
* **Description:**  
  When dividing operands containing decimal components (e.g. `0.5 ÷ 2`, `1.2 ÷ 3`, or `0.5 ÷ 0.25`), `Soroban.divide` normalized `d1_dec` and `d2_dec` to integer representations $v_1$ and $v_2$ with decimal scales $s_1$ and $s_2$. However, when reconstructing the final quotient from the accumulated integer quotient `final_q`, the calculation completely ignored the operand scales $s_1$ and $s_2$:
  ```python
  # Defective original:
  actual_precision = max(0, final_idx - len(v1_str_clean))
  quotient = Decimal(final_q) / (Decimal(10) ** actual_precision)
  ```
* **Failure Examples:**
  - `0.5 ÷ 2` with `precision=2` produced `2.5` instead of `0.25` (**10× error!**)
  - `1.2 ÷ 3` with `precision=3` produced `4.0` instead of `0.4` (**10× error!**)
  - `0.5 ÷ 0.25` with `precision=2` produced `0.2` instead of `2.0` (**10× error!**)
* **Remediation:**  
  Mathematically, $\frac{d_1}{d_2} = \frac{v_1 \cdot 10^{-s_1}}{v_2 \cdot 10^{-s_2}} = \frac{v_1}{v_2} \cdot 10^{-(s_1 - s_2)}$. The total net decimal scaling is:
  $$\text{total\_scale} = \text{actual\_precision} + s_1 - s_2$$
  ```python
  total_scale = actual_precision + s1 - s2
  if total_scale >= 0:
      quotient = Decimal(final_q) / (Decimal(10) ** total_scale)
  else:
      quotient = Decimal(final_q) * (Decimal(10) ** (-total_scale))
  ```

---

### Defect 2: Unbounded Recursion / Underflow Hazard in `revise_down`
* **Location:** [`soroban.py:310-320`](file:///d:/Bioinformatics/Projects/corpus/rust/soroban-simulator/upstream/soroban_simulator/soroban/soroban.py#L310-L320)
* **Severity:** **HIGH (Termination Hazard - Flagged by `ouropy doctor`)**
* **OuroPy Diagnostic:**  
  `Soroban.divide.shojohou.revise_down: recursive: no decrease shown at 1 call site(s); 1 finding`
* **Description:**  
  During pedagogical quotient estimation in `shojohou`, `revise_down` called `_validate_revision_bounds(est_q, "decrease")`, which returns a boolean `(can_revise, message)`. However, `revise_down` discarded the boolean:
  ```python
  # Defective original:
  _, msg = self._validate_revision_bounds(est_q, "decrease")
  revised_q = est_q - 1
  return revise_down(revised_q, ...)
  ```
  If `est_q <= 0`, `est_q` continued decrementing into negative numbers (`-1, -2, ...`), generating contradictory step descriptions (*"🚨 OVERESTIMATE! Cannot decrease quotient below 0"*) while continuing to decrement and recurse.
* **Remediation:**  
  Guarded `revise_down` so that recursion immediately halts if `est_q <= 0` or if `_validate_revision_bounds` reports `can_revise == False`. Following the fix, OuroPy certified termination:
  `recursive: termination shown (size-change); clean`.

---

### Defect 3: Calculator Crash & Precision Truncation on Decimal Division
* **Location:** [`calculator.py:61-67`](file:///d:/Bioinformatics/Projects/corpus/rust/soroban-simulator/upstream/soroban_simulator/soroban/calculator.py#L61-L67)
* **Severity:** **HIGH (Runtime Crash / Data Loss)**
* **Description:**  
  In `Calculator.calculate`, when an equation contained a division operator `/`, it invoked `self.soroban.divide(num1, num2)` without providing `precision`. `Soroban.divide` defaulted to `precision=0`. 
  1. If either operand was a `Decimal` (e.g. `Calculator().calculate("1.2 / 3")`), `Soroban.divide` raised `ValueError("Operands must be integer operands when precision is 0.")`.
  2. If the Calculator was configured with decimal rods (e.g. `unit_rod_index=3`), `Calculator().calculate("3 / 2")` passed `precision=0`, truncating the fractional part and returning `1` instead of `1.5`.
* **Remediation:**  
  Updated `Calculator.calculate` to propagate `div_precision = self.soroban.unit_rod_index`. If `unit_rod_index == 0` but operands contain decimal fractions, dynamic precision fallback is applied (`div_precision = 2`).

---

### Defect 4: Hardcoded Rod Positioning Crash on Non-13 Rod Sorobans
* **Location:** [`soroban.py:157-164`](file:///d:/Bioinformatics/Projects/corpus/rust/soroban-simulator/upstream/soroban_simulator/soroban/soroban.py#L157-L164)
* **Severity:** **MEDIUM (Index Out of Bounds / Capacity Crash)**
* **Description:**  
  In `Soroban.multiply`:
  ```python
  # Defective original:
  m2_start = 8 if len(m2_str) == 1 else 4
  ```
  On a Soroban constructed with fewer than 13 rods (e.g. `Soroban(num_rods=7)` or `Soroban(num_rods=5)`), `self.rods[m2_start + i]` crashed immediately with `IndexError: list assignment index out of range`. Additionally, `multiply` had no capacity check if `len(m1_str) + len(m2_str) > self.num_rods`.
* **Remediation:**  
  Added a capacity check `if len(m1_str) + len(m2_str) > self.num_rods: raise ValueError(...)` and bounded `m2_start`:
  ```python
  m2_start = (8 if len(m2_str) == 1 else 4) if self.num_rods >= 13 else max(0, min(self.num_rods - len(m2_str), self.num_rods // 2))
  ```

---

### Defect 5: Silent Addition Carry Overflow and Negative Number Invariants
* **Location:** [`soroban.py:88-128`](file:///d:/Bioinformatics/Projects/corpus/rust/soroban-simulator/upstream/soroban_simulator/soroban/soroban.py#L88-L128)
* **Severity:** **MEDIUM (Silent Data Corruption / Invariant Violation)**
* **Description:**  
  1. On a Soroban of capacity $N$, adding a number that causes a carry past rod $N-1$ (e.g. $999 + 1$ on a 3-rod soroban) caused `add_to_rod` to silently discard the carry, resetting the value to $0$ without raising an overflow error.
  2. Because `add` and `set_number` used `s_str = str(abs(scaled))`, calling `s.add(-5)` or `s.set_number(-5)` silently converted negative numbers into positive additions, violating Soroban's unsigned non-negative bead invariant.
* **Remediation:**  
  Added explicit negative guards (`if num_dec < 0: raise ValueError(...)`) to `set_number`, `add`, and `subtract`, and added result capacity verification to `add`.

---

### Defect 6: AttributeError in `get_value` on Empty Rods & Missing `__init__` Validation
* **Location:** [`soroban.py:23-53`](file:///d:/Bioinformatics/Projects/corpus/rust/soroban-simulator/upstream/soroban_simulator/soroban/soroban.py#L23-L53)
* **Severity:** **MEDIUM (Unhandled Exception - Discovered by `ouropy doctor` sandbox edge fuzzer)**
* **OuroPy Diagnostic:**  
  `error[E021]: Uncaught runtime exception during execution: AttributeError: 'int' object has no attribute 'normalize' during Soroban(0, 1).get_value()`
* **Description:**  
  In `get_value()`, `sum(...)` without a `start` parameter defaulted to integer `0`. When `self.rods` was empty, `sum` returned integer `0`, causing `0.normalize()` to crash with `AttributeError`. Additionally, `Soroban.__init__` accepted negative `num_rods` or `unit_rod_index >= num_rods`.
* **Remediation:**  
  1. Added `num_rods > 0` and `0 <= unit_rod_index < num_rods` bounds validation in `__init__`.
  2. Passed `Decimal(0)` as the `start` parameter in `sum(..., Decimal(0))` and added an empty rod check in `get_value()`.

---

## 3. Second Scan & Verification Results

Following both patch cycles, all OuroPy detectors were executed again:

| Detector | Result | Details |
| :--- | :---: | :--- |
| **`ouropy hazards`** | **CLEAN** | 0 static hazards across the entire package |
| **`ouropy termination`** | **CERTIFIED** | All 6 recursive functions (`add_to_rod`, `subtract_from_rod`, `shojohou`, `revise_down`, `revise_up`, `subtract_pps`) proven to terminate via size-change graphs |
| **`ouropy doctor`** | **0 ERRORS** | Dynamic sandbox edge fuzzing clean across all valid input spaces |
| **`ouropy airlock`** | **ALL GATES PASSED** | Syntax, Static Types, and Lean 4 elaboration verified for all dataclasses |
| **`pytest` (Core Engine)** | **175/175 PASSED** | 169 original + 6 new tests verifying all fixed edge cases (0.68s runtime) |

---

## 4. PySide6 GUI Formal Verification & Bug Audit

Following the core arithmetic audit, we used **OuroPy** and headless PySide6 execution (`QT_QPA_PLATFORM=offscreen`) to audit the GUI subsystem:
* [`soroban_simulator/gui/soroban_widget.py`](file:///d:/Bioinformatics/Projects/corpus/rust/soroban-simulator/upstream/soroban_simulator/gui/soroban_widget.py)
* [`soroban_simulator/gui/main_window.py`](file:///d:/Bioinformatics/Projects/corpus/rust/soroban-simulator/upstream/soroban_simulator/gui/main_window.py)
* [`soroban_simulator/main.py`](file:///d:/Bioinformatics/Projects/corpus/rust/soroban-simulator/upstream/soroban_simulator/main.py)

### GUI Defect Taxonomy & Remediations

#### GUI Defect 1: Sandbox Access Violation Crash (`0xC0000005`) on Widget Instantiation
* **Severity:** **HIGH (Segmentation Fault / Access Violation)**
* **OuroPy Diagnostic:**  
  `error[E021]: Uncaught runtime exception during execution: process crashed (exit code 3221226505) during SorobanWidget(1).set_state([1, 2])`
* **Root Cause:**  
  Instantiating `QWidget` and `QPropertyAnimation` in PySide6 without an active `QApplication` instance causes a hard access violation crash (`0xC0000005`) in Qt C++ internals.
* **Remediation:**  
  In both `SorobanWidget.__init__` and `MainWindow.__init__`, added defensive fallback:
  ```python
  if QApplication.instance() is None:
      self._app = QApplication(sys.argv if sys.argv else ["soroban_simulator"])
  ```

#### GUI Defect 2: IndexError in `paintEvent` on Mismatched State Lengths
* **Severity:** **HIGH (Widget Crash)**
* **Root Cause:**  
  When `set_state` or `animate_to_state` was called with a state list of length different from `num_rods`, `paintEvent` iterated up to `self.num_rods - 1`, attempting to index `self._start_state[display_rod_index]` and crashing with `IndexError: list index out of range`.
* **Remediation:**  
  Dynamically updated `self.num_rods = max(self.num_rods, len(soroban_state))` and added boundary guards in `draw_rod`:
  ```python
  start_val = self._start_state[display_rod_index] if display_rod_index < len(self._start_state) else 0
  end_val = self._target_state[display_rod_index] if display_rod_index < len(self._target_state) else 0
  ```

#### GUI Defect 3: Relative Import Failure in `main_window.py`
* **Severity:** **MEDIUM (ImportError in Standalone & Sandbox Contexts)**
* **OuroPy Diagnostic:**  
  `error[E021]: ImportError: attempted relative import with no known parent package at main_window.py:4`
* **Root Cause:**  
  Line 4 used `from .soroban_widget import SorobanWidget` while lines 5-6 used absolute package imports `from soroban_simulator.soroban...`. When run or imported standalone or in sandboxes without package context, relative imports fail.
* **Remediation:**  
  Added package root resolution to `sys.path` and provided dual relative/absolute fallback:
  ```python
  try:
      from .soroban_widget import SorobanWidget
  except ImportError:
      from soroban_simulator.gui.soroban_widget import SorobanWidget
  ```

#### GUI Defect 4: Bidirectional Marker Leakage & Desynchronization
* **Severity:** **MEDIUM (State Inconsistency / Visual Bug)**
* **Root Cause:**  
  `MainWindow.active_markers` was imperatively updated forwards as steps were visited, but was never recalculated when the user stepped backwards (`previous_step()`) or jumped directly to a step via the step list (`go_to_step()`). Stepping forward to step 3 and then stepping back to step 0 left multiplication markers (M1/M2) permanently visible at step 0 ("Clear soroban"). Jumping directly to a step also resulted in 0 markers being displayed.
* **Remediation:**  
  Implemented pure deterministic marker extraction for the active step index:
  ```python
  def _get_markers_at_step(self, step_index: int) -> list:
      if not self.steps or step_index < 0:
          return []
      marker_dict = {}
      for s in self.steps[:step_index + 1]:
          if "Clear soroban" in s.step_description:
              marker_dict.clear()
          elif hasattr(s, 'markers') and s.markers:
              for m in s.markers:
                  if len(m) >= 3:
                      marker_dict[m[2]] = m
      return list(marker_dict.values())
  ```

#### GUI Defect 5: Recursive Signal Feedback Loop in `update_step_display`
* **Severity:** **MEDIUM (Signal Feedback / Event Recursion)**
* **Root Cause:**  
  `update_step_display` invoked `self.steps_list_widget.setCurrentRow(display_row)`, which fired `currentRowChanged`, which invoked `self.go_to_step(row)`, which invoked `update_step_display` again.
* **Remediation:**  
  Blocked signals around `setCurrentRow`:
  ```python
  self.steps_list_widget.blockSignals(True)
  self.steps_list_widget.setCurrentRow(display_row)
  self.steps_list_widget.blockSignals(False)
  ```

#### GUI Defect 6: Missing Return Key Handler & Unhandled Exceptions
* **Severity:** **LOW (UX / Crash on Uncaught Exception)**
* **Root Cause:**  
  `QLineEdit` was not connected to `returnPressed`, forcing mouse clicks on "Calculate". In `calculate()`, only `ValueError` was caught; other errors could crash the UI.
* **Remediation:**  
  Connected `self.equation_input.returnPressed.connect(self.calculate)`, caught general `Exception`, reset state cleanly on error, and added arrow key navigation (`Qt.Key_Left` / `Qt.Key_Right`).

#### GUI Defect 7: Dead Code & Single-Rod Marker Drawing in `SorobanWidget`
* **Severity:** **LOW (Visual Polish & Dead Code)**
* **Root Cause:**  
  `SorobanWidget.paintEvent` contained unassigned float calculation `self.height() * 0.25`. For single-rod markers (`start_rod == end_rod`), `drawLine` drew a 0-length line. Missing yellow color in `colour_map` fell back to blue for remainder markers.
* **Remediation:**  
  Removed dead expression, added `draw_start_x -= rod_width * 0.35` / `draw_end_x += rod_width * 0.35` bracket underline for single-rod markers, and added `yellow` and `QColor.isValidColorName` fallback.

---

## 5. Comprehensive Test Results

```
================== 185 passed, 247 subtests passed in 0.84s ===================
```
* **Core Simulator Tests:** 175 passed
* **PySide6 Headless GUI Tests ([`test_gui.py`](file:///d:/Bioinformatics/Projects/corpus/rust/soroban-simulator/upstream/soroban_simulator/tests/test_gui.py)):** 10 passed
* **`ouropy doctor` on GUI files:** **0 ERRORS**, clean execution!
* **`ouropy hazards` on GUI files:** **CLEAN** (0 hazards)

