import os
import unittest
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap, QKeyEvent
from PySide6.QtCore import Qt

# Force offscreen rendering for headless test execution
os.environ["QT_QPA_PLATFORM"] = "offscreen"

app = QApplication.instance() or QApplication(["test_gui"])

from soroban_simulator.gui.soroban_widget import SorobanWidget
from soroban_simulator.gui.main_window import MainWindow

class TestSorobanWidget(unittest.TestCase):
    def test_widget_creation_and_defaults(self):
        widget = SorobanWidget(13)
        self.assertEqual(widget.num_rods, 13)
        self.assertEqual(len(widget.soroban_state), 13)
        self.assertEqual(widget.animation_progress, 0.0)
        self.assertEqual(widget.markers, [])

    def test_set_state_and_animate(self):
        widget = SorobanWidget(5)
        widget.set_state([1, 2, 3, 4, 5])
        self.assertEqual(widget.soroban_state, [1, 2, 3, 4, 5])
        self.assertEqual(widget.animation_progress, 1.0)

        # Setting state with different length adjusts num_rods safely
        widget.set_state([0] * 13)
        self.assertEqual(widget.num_rods, 13)

        widget.animate_to_state([5] * 13)
        self.assertEqual(widget.soroban_state, [5] * 13)

    def test_markers_setting(self):
        widget = SorobanWidget(13)
        widget.set_markers([(2, 3, "M1", "blue"), (4, 5, "M2", "green")])
        self.assertEqual(len(widget.markers), 2)

    def test_render_paint_event(self):
        widget = SorobanWidget(13)
        widget.set_state([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2])
        widget.set_markers([
            (2, 3, "M1", "blue"),
            (4, 5, "M2", "green"),
            (8, 11, "PP", "red"),
            (0, 0, "Q", "yellow")  # Single rod marker with yellow
        ])
        widget.resize(800, 600)
        pix = QPixmap(800, 600)
        widget.render(pix)
        self.assertFalse(pix.isNull())

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.window = MainWindow()

    def test_initial_state(self):
        self.assertEqual(self.window.equation_input.text(), "")
        self.assertEqual(self.window.steps, [])
        self.assertEqual(self.window.current_step, 0)
        self.assertFalse(self.window.previous_button.isEnabled())
        self.assertFalse(self.window.next_button.isEnabled())

    def test_calculate_simple_addition(self):
        self.window.equation_input.setText("12 + 34")
        self.window.calculate()
        self.assertTrue(len(self.window.steps) > 0)
        self.assertEqual(self.window.result, 46)
        self.assertEqual(self.window.current_step, 0)

    def test_calculate_invalid_expression(self):
        from unittest.mock import patch
        with patch("PySide6.QtWidgets.QMessageBox.warning"):
            self.window.equation_input.setText("1 / 0")
            self.window.calculate()
        # On error, steps are reset cleanly
        self.assertEqual(self.window.steps, [])
        self.assertEqual(self.window.steps_list_widget.count(), 0)

    def test_navigation_and_marker_bidirectional_sync(self):
        self.window.equation_input.setText("23 * 15")
        self.window.calculate()
        self.assertTrue(len(self.window.steps) > 5)

        # Step 0: "Clear soroban" should have no markers
        self.assertEqual(len(self.window.soroban_widget.markers), 0)

        # Step forward until multipliers are set
        while self.window.current_step < 5 and self.window.current_step < len(self.window.steps) - 1:
            self.window.next_step()

        # Step 3+ should have active markers
        self.assertTrue(len(self.window.soroban_widget.markers) > 0)

        # Step back to step 0
        while self.window.current_step > 0:
            self.window.previous_step()

        self.assertEqual(self.window.current_step, 0)
        # Verify fix: stepping backwards to step 0 correctly clears active markers!
        self.assertEqual(len(self.window.soroban_widget.markers), 0)

    def test_go_to_step(self):
        self.window.equation_input.setText("5 + 5")
        self.window.calculate()
        if len(self.window.display_steps) > 1:
            self.window.go_to_step(1)
            self.assertEqual(self.window.current_step, self.window.step_map[1])

    def test_refresh(self):
        self.window.equation_input.setText("10 * 10")
        self.window.calculate()
        self.window.refresh()
        self.assertEqual(self.window.equation_input.text(), "")
        self.assertEqual(self.window.steps, [])
        self.assertEqual(self.window.current_step, 0)
        self.assertEqual(self.window.soroban_widget.markers, [])

if __name__ == "__main__":
    unittest.main()
