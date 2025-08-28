from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QPropertyAnimation, Property, QEasingCurve

class SorobanWidget(QWidget):
    """A widget that displays a soroban with animated bead movements."""

    def __init__(self, num_rods: int = 13):
        """Initializes the soroban widget."""
        super().__init__()
        self.num_rods = num_rods
        self.soroban_state = [0] * num_rods
        self._start_state = list(self.soroban_state)
        self._target_state = list(self.soroban_state)
        self._animation_progress = 0.0

        self._animation = QPropertyAnimation(self, b"animation_progress")
        self._animation.setDuration(400)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)

    def _get_animation_progress(self):
        return self._animation_progress

    def _set_animation_progress(self, value):
        self._animation_progress = value
        self.update()

    animation_progress = Property(float, _get_animation_progress, _set_animation_progress)

    def set_state(self, soroban_state: list[int]):
        """Sets the state of the soroban to display without animation."""
        if self._animation.state() == QPropertyAnimation.Running:
            self._animation.stop()
        
        self.soroban_state = soroban_state
        self._start_state = list(soroban_state)
        self._target_state = list(soroban_state)
        self._animation_progress = 1.0
        self.update()

    def animate_to_state(self, new_state: list[int]):
        """Animates the soroban from its current state to a new state."""
        if self._animation.state() == QPropertyAnimation.Running:
            self._animation.stop()

        self._start_state = list(self.soroban_state)
        self._target_state = list(new_state)
        
        self._animation.setStartValue(0.0)
        self._animation.setEndValue(1.0)
        self._animation.start()

        # Update the logical state immediately
        self.soroban_state = new_state

    def _get_bead_y_positions(self, value, rod_height, top_margin, bar_y, bar_height, bead_radius):
        """Calculates the y-positions of all beads on a rod for a given value."""
        positions = {}
        
        # Heaven bead (index 4)
        heaven_active_y = bar_y - bar_height / 2 - bead_radius * 2
        heaven_inactive_y = top_margin
        positions[4] = heaven_active_y if value >= 5 else heaven_inactive_y

        # Earth beads (indices 0-3)
        num_active = value % 5
        earth_bead_diameter = bead_radius * 2
        earth_bead_spacing = earth_bead_diameter + bead_radius / 2

        for i in range(4):
            if i < num_active:
                # Active beads start from the bar and go down
                positions[i] = bar_y + bar_height / 2 + i * earth_bead_spacing
            else:
                # Inactive beads start from the bottom and go up
                positions[i] = top_margin + rod_height - (4 - i) * earth_bead_spacing

        return positions

    def paintEvent(self, event):
        """Draws the soroban."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.white)

        rod_width = self.width() / (self.num_rods + 1)
        rod_height = self.height() * 0.8
        top_margin = self.height() * 0.1
        bar_height = 4
        bar_y = top_margin + rod_height * 0.3
        bead_radius = rod_width / 4

        painter.setPen(QPen(Qt.black, bar_height))
        painter.drawLine(0, bar_y, self.width(), bar_y)

        for i in range(self.num_rods):
            print(f"Rod {i}: value={self._target_state[i]}")
            rod_x = (i + 1) * rod_width
            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(rod_x, top_margin, rod_x, top_margin + rod_height)

            start_positions = self._get_bead_y_positions(self._start_state[i], rod_height, top_margin, bar_y, bar_height, bead_radius)
            end_positions = self._get_bead_y_positions(self._target_state[i], rod_height, top_margin, bar_y, bar_height, bead_radius)

            # Heaven bead
            start_y = start_positions[4]
            end_y = end_positions[4]
            current_y = start_y + (end_y - start_y) * self._animation_progress
            painter.setBrush(Qt.blue if self._target_state[i] >= 5 else Qt.gray)
            painter.drawEllipse(rod_x - bead_radius, current_y, bead_radius * 2, bead_radius * 2)

            # Earth beads
            for j in range(4):
                start_y = start_positions[j]
                end_y = end_positions[j]
                current_y = start_y + (end_y - start_y) * self._animation_progress
                painter.setBrush(Qt.blue if j < self._target_state[i] % 5 else Qt.gray)
                painter.drawEllipse(rod_x - bead_radius, current_y, bead_radius * 2, bead_radius * 2)