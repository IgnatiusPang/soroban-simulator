
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QListWidget
from PySide6.QtCore import Qt
from .soroban_widget import SorobanWidget
from soroban_simulator.soroban.calculator import Calculator
from soroban_simulator.soroban.calculation_step import CalculationStep

class MainWindow(QMainWindow):
    """The main window of the Soroban Simulator."""

    def __init__(self):
        """Initializes the main window."""
        super().__init__()

        self.setWindowTitle("Soroban Simulator")

        self.calculator = Calculator()
        self.steps: list[CalculationStep] = []
        self.display_steps: list[CalculationStep] = []
        self.step_map: list[int] = []
        self.current_step = 0

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
        self.completion_label.setAlignment(Qt.AlignCenter)

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
        self.refresh_button.clicked.connect(self.refresh)
        self.previous_button.clicked.connect(self.previous_step)
        self.next_button.clicked.connect(self.next_step)
        self.steps_list_widget.currentRowChanged.connect(self.go_to_step)
        self.soroban_widget._animation.finished.connect(self.on_animation_finished)

        self.refresh()

    def calculate(self):
        """Calculates the equation and displays the first step."""
        equation = self.equation_input.text()
        if not equation:
            return

        self.soroban_widget.set_markers([]) # Clear existing markers

        try:
            # Set markers for multiplication, following the Modern Standard Method.
            if "*" in equation:
                parts = self.calculator.parser.generate_rpn(equation)
                operands = [p for p in parts if isinstance(p, int)]
                if len(operands) == 2:
                    # In RPN, the operands are pushed onto the stack first,
                    # so the first operand is the multiplicand and the second is the multiplier.
                    multiplicand, multiplier = operands[0], operands[1]
                    
                    multiplier_len = len(str(multiplier))
                    multiplicand_len = len(str(multiplicand))

                    # Position the multiplier on the far left (rod C, index 2).
                    multiplier_rod_start = 2

                    # Leave a gap of 2 rods after the multiplier.
                    multiplicand_rod_start = multiplier_rod_start + multiplier_len + 2
                    
                    # The product is formed to the right of the multiplicand.
                    product_rod_start = multiplicand_rod_start + multiplicand_len 
                    product_len = multiplicand_len + multiplier_len

                    markers = [
                        (multiplier_rod_start, multiplier_rod_start + multiplier_len - 1, "Multiplier"),
                        (multiplicand_rod_start, multiplicand_rod_start + multiplicand_len - 1, "Multiplicand"),
                        (product_rod_start, product_rod_start + product_len - 1, "Partial Product")
                    ]
                    self.soroban_widget.set_markers(markers)

            self.steps = self.calculator.calculate(equation)
            self.result = self.steps[-1].current_value if self.steps else 0
            self.current_step = 0
            
            self.steps_list_widget.clear()
            self.display_steps = []
            self.step_map = []
            
            for i, step in enumerate(self.steps):
                if step.step_description:
                    self.step_map.append(i)
                    self.display_steps.append(step)
                    self.steps_list_widget.addItem(step.step_description)

            self.update_step_display(animated=False)
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def previous_step(self):
        """Displays the previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step_display()

    def next_step(self):
        """Displays the next step."""
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
            return

        step = self.steps[self.current_step]
        if animated:
            self.previous_button.setEnabled(False)
            self.next_button.setEnabled(False)
            self.steps_list_widget.setEnabled(False)
            self.soroban_widget.animate_to_state(step.soroban_state)
        else:
            self.soroban_widget.set_state(step.soroban_state)
            self.on_animation_finished() # Manually call to update UI state

        self.step_description_label.setText(f"Step description: {step.step_description}")
        self.current_value_label.setText(f"Current value: {step.current_value}")
        
        # Update list widget selection
        display_row = -1
        for i, step_index in enumerate(self.step_map):
            if step_index >= self.current_step:
                if step_index == self.current_step:
                    display_row = i
                else:
                    display_row = i -1
                break
        
        if display_row != -1:
            self.steps_list_widget.setCurrentRow(display_row)

    def on_animation_finished(self):
        """Called when the soroban animation finishes."""
        self.previous_button.setEnabled(self.current_step > 0)
        self.next_button.setEnabled(self.current_step < len(self.steps) - 1)
        self.steps_list_widget.setEnabled(True)

        if self.current_step == len(self.steps) - 1:
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
        self.calculator.soroban.clear()
        self.soroban_widget.set_markers([])
        self.soroban_widget.set_state(self.calculator.soroban.get_state())
        self.step_description_label.setText("Step description:")
        self.current_value_label.setText("Current value:")
        self.steps_list_widget.clear()
        self.update_step_display(animated=False)
