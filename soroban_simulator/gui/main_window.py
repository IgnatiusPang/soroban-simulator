import os
import sys

# Ensure repository root is in sys.path for standalone or sandboxed execution
_repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox, QListWidget
)
from PySide6.QtCore import Qt, QPropertyAnimation

try:
    from .soroban_widget import SorobanWidget
except ImportError:
    from soroban_simulator.gui.soroban_widget import SorobanWidget

from soroban_simulator.soroban.calculator import Calculator
from soroban_simulator.soroban.calculation_step import CalculationStep

class MainWindow(QMainWindow):
    """The main window of the Soroban Simulator."""

    def __init__(self):
        """Initialises the main window."""
        if QApplication.instance() is None:
            self._app = QApplication(sys.argv if sys.argv else ["soroban_simulator"])
        super().__init__()

        self.setWindowTitle("Soroban Simulator")
        
        # Set minimum window size to ensure all markers (including PP) are visible
        # Height needs to accommodate: rod numbers (8%), soroban rods (52%), markers (25%), controls
        self.setMinimumSize(800, 600)
        self.resize(1000, 700)  # Set a comfortable default size

        self.calculator = Calculator(unit_rod_index=3)
        self.steps: list[CalculationStep] = []
        self.display_steps: list[CalculationStep] = []
        self.step_map: list[int] = []
        self.current_step = 0
        self.active_markers = []  # Track active markers throughout the calculation
        self.result = 0

        # Create widgets
        self.equation_input = QLineEdit()
        self.calculate_button = QPushButton("Calculate")
        self.refresh_button = QPushButton("Refresh")
        self.soroban_widget = SorobanWidget()
        self.step_description_label = QLabel("Step description:")
        self.current_value_label = QLabel("Current value:")
        self.previous_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.steps_list_widget = QListWidget()
        self.completion_label = QLabel("Calculation Complete")
        self.completion_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        central_widget = QWidget()
        content_layout = QHBoxLayout()
        soroban_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        navigation_layout = QHBoxLayout()

        input_layout.addWidget(self.equation_input)
        input_layout.addWidget(self.calculate_button)
        input_layout.addWidget(self.refresh_button)

        navigation_layout.addWidget(self.previous_button)
        navigation_layout.addWidget(self.next_button)

        soroban_layout.addLayout(input_layout)
        soroban_layout.addWidget(self.soroban_widget)
        soroban_layout.addWidget(self.step_description_label)
        soroban_layout.addWidget(self.current_value_label)
        soroban_layout.addLayout(navigation_layout)
        soroban_layout.addWidget(self.completion_label)

        content_layout.addLayout(soroban_layout)
        content_layout.addWidget(self.steps_list_widget)

        central_widget.setLayout(content_layout)
        self.setCentralWidget(central_widget)

        # Connect signals
        self.calculate_button.clicked.connect(self.calculate)
        self.equation_input.returnPressed.connect(self.calculate)
        self.refresh_button.clicked.connect(self.refresh)
        self.previous_button.clicked.connect(self.previous_step)
        self.next_button.clicked.connect(self.next_step)
        self.steps_list_widget.currentRowChanged.connect(self.go_to_step)
        self.soroban_widget._animation.finished.connect(self.on_animation_finished)

        self.refresh()

    def _get_markers_at_step(self, step_index: int) -> list:
        """Determines the active markers at a given step index deterministically."""
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

    def calculate(self):
        """Calculates the equation and displays the first step."""
        equation = self.equation_input.text().strip()
        if not equation:
            return

        self.soroban_widget.set_markers([]) # Clear existing markers

        try:
            self.steps = self.calculator.calculate(equation)
            self.result = self.steps[-1].current_value if self.steps else 0
            self.current_step = 0
            
            self.steps_list_widget.clear()
            self.display_steps = []
            self.step_map = []
            
            # Populate step mapping and list widget
            filtered_steps = [(i, s) for i, s in enumerate(self.steps) if s.step_description]
            self.step_map = [i for i, s in filtered_steps]
            self.display_steps = [s for i, s in filtered_steps]
            for s in self.display_steps:
                self.steps_list_widget.addItem(s.step_description)

            self.update_step_display(animated=False)
        except Exception as e:
            self.steps = []
            self.display_steps = []
            self.step_map = []
            self.current_step = 0
            self.steps_list_widget.clear()
            self.update_step_display(animated=False)
            QMessageBox.warning(self, "Error", str(e))

    def previous_step(self):
        """Displays the previous step."""
        if self.soroban_widget._animation.state() == QPropertyAnimation.Running:
            self.soroban_widget._animation.stop()
            self.soroban_widget.set_state(self.soroban_widget._target_state)
            self.on_animation_finished()
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step_display()

    def next_step(self):
        """Displays the next step."""
        if self.soroban_widget._animation.state() == QPropertyAnimation.Running:
            self.soroban_widget._animation.stop()
            self.soroban_widget.set_state(self.soroban_widget._target_state)
            self.on_animation_finished()
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_step_display()

    def go_to_step(self, row):
        """Goes to a specific step when the user clicks on the list."""
        if 0 <= row < len(self.display_steps):
            new_step_index = self.step_map[row]
            if self.current_step != new_step_index:
                self.current_step = new_step_index
                self.update_step_display()

    def update_step_display(self, animated=True):
        """Updates the display with the current step's information."""
        if not self.steps:
            self.completion_label.hide()
            self.previous_button.setEnabled(False)
            self.next_button.setEnabled(False)
            self.steps_list_widget.setEnabled(True)
            self.step_description_label.setText("Step description:")
            self.current_value_label.setText("Current value:")
            self.soroban_widget.set_markers([])
            return

        step = self.steps[self.current_step]
        if animated and self.soroban_widget.soroban_state != step.soroban_state:
            self.previous_button.setEnabled(False)
            self.next_button.setEnabled(False)
            self.steps_list_widget.setEnabled(False)
            self.soroban_widget.animate_to_state(step.soroban_state)
        else:
            self.soroban_widget.set_state(step.soroban_state)
            self.on_animation_finished() # Manually call to update UI state

        # Update active markers deterministically based on the current step
        self.active_markers = self._get_markers_at_step(self.current_step)
        self.soroban_widget.set_markers(self.active_markers)

        self.step_description_label.setText(f"Step description: {step.step_description}")
        self.current_value_label.setText(f"Current value: {step.current_value}")
        
        # Update list widget selection without recursive signal loop
        if self.step_map:
            display_row = next((i if step_index == self.current_step else max(0, i - 1) 
                                for i, step_index in enumerate(self.step_map) if step_index >= self.current_step),
                               len(self.display_steps) - 1)
            
            if 0 <= display_row < self.steps_list_widget.count():
                self.steps_list_widget.blockSignals(True)
                self.steps_list_widget.setCurrentRow(display_row)
                self.steps_list_widget.blockSignals(False)

    def on_animation_finished(self):
        """Called when the soroban animation finishes."""
        has_steps = bool(self.steps)
        self.previous_button.setEnabled(has_steps and self.current_step > 0)
        self.next_button.setEnabled(has_steps and self.current_step < len(self.steps) - 1)
        self.steps_list_widget.setEnabled(True)

        if has_steps and self.current_step == len(self.steps) - 1:
            self.completion_label.show()
        else:
            self.completion_label.hide()

    def refresh(self):
        """Resets the application to its initial state."""
        self.equation_input.clear()
        self.steps = []
        self.display_steps = []
        self.step_map = []
        self.current_step = 0
        self.active_markers = []  # Clear active markers
        self.result = 0
        self.calculator.soroban.clear()
        self.soroban_widget.set_markers([])
        self.soroban_widget.set_state(self.calculator.soroban.get_state())
        self.step_description_label.setText("Step description:")
        self.current_value_label.setText("Current value:")
        self.steps_list_widget.clear()
        self.update_step_display(animated=False)

    def keyPressEvent(self, event):
        """Handles arrow key navigation when input does not have focus."""
        if not self.equation_input.hasFocus():
            if event.key() == Qt.Key_Left:
                self.previous_step()
                return
            elif event.key() == Qt.Key_Right:
                self.next_step()
                return
        super().keyPressEvent(event)
