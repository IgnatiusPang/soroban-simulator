from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QPropertyAnimation, Property, QEasingCurve

class SorobanWidget(QWidget):
    """A widget that displays a soroban with animated bead movements."""

    def __init__(self, num_rods: int = 13):
        """Initialises the soroban widget."""
        super().__init__()
        self.num_rods = num_rods
        self.soroban_state = [0] * num_rods
        self._start_state = list(self.soroban_state)
        self._target_state = list(self.soroban_state)
        self._animation_progress = 0.0
        self.markers = []

        self._animation = QPropertyAnimation(self, b"animation_progress")
        self._animation.setDuration(400)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)

    def _get_animation_progress(self):
        return self._animation_progress

    def _set_animation_progress(self, value):
        self._animation_progress = value
        self.update()

    animation_progress = Property(float, _get_animation_progress, _set_animation_progress)

    def set_markers(self, markers):
        """Sets the markers to display on the soroban."""
        self.markers = markers
        self.update()

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
        """Calculates the y-positions of all beads on a rod for a given value using functional dictionary comprehension."""
        # Heaven bead (index 4)
        heaven_active_y = bar_y - bar_height / 2 - bead_radius * 2
        heaven_inactive_y = top_margin
        
        # Earth beads (indices 0-3) - use dictionary comprehension to avoid for loop
        num_active = value % 5
        earth_bead_diameter = bead_radius * 2
        earth_bead_spacing = earth_bead_diameter + bead_radius / 2

        # Create the positions dictionary functionally
        positions = {
            4: heaven_active_y if value >= 5 else heaven_inactive_y
        }
        # Update with earth beads using dictionary comprehension
        positions.update({
            i: (bar_y + bar_height / 2 + i * earth_bead_spacing) if i < num_active
            else (top_margin + rod_height - (4 - i) * earth_bead_spacing)
            for i in range(4)
        })

        return positions

    def paintEvent(self, event):
        """Draws the soroban using absolute functional patterns."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.white)

        rod_width = self.width() / (self.num_rods + 1)
        self.height() * 0.25
        rod_number_space = self.height() * 0.12
        rod_height = self.height() * 0.48
        top_margin = self.height() * 0.15 + rod_number_space
        bar_height = 4
        bar_y = top_margin + rod_height * 0.3
        bead_radius = rod_width / 4

        painter.setPen(QPen(Qt.black, bar_height))
        painter.drawLine(0, bar_y, self.width(), bar_y)

        # Draw rod numbers at the top
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QPen(Qt.black, 1))

        def draw_rod(i):
            display_rod_index = self.num_rods - 1 - i
            rod_x = (i + 1) * rod_width
            
            # Draw rod number
            rod_number = display_rod_index + 1
            font_metrics = painter.fontMetrics()
            text_width = font_metrics.horizontalAdvance(str(rod_number))
            painter.drawText(int(rod_x - text_width / 2), int(self.height() * 0.05), str(rod_number))
            
            # Draw the rod
            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(int(rod_x), int(top_margin), int(rod_x), int(top_margin + rod_height))

            # Draw orienting dots
            if (display_rod_index + 1) in [1, 4, 7, 10, 13]:
                painter.setBrush(Qt.black)
                painter.drawEllipse(int(rod_x - 3), int(bar_y - bar_height / 2 - 3), 6, 6)

            start_p = self._get_bead_y_positions(self._start_state[display_rod_index], rod_height, top_margin, bar_y, bar_height, bead_radius)
            end_p = self._get_bead_y_positions(self._target_state[display_rod_index], rod_height, top_margin, bar_y, bar_height, bead_radius)

            # Draw heaven bead
            painter.setBrush(Qt.blue if self._target_state[display_rod_index] >= 5 else Qt.gray)
            painter.drawEllipse(int(rod_x - bead_radius), int(start_p[4] + (end_p[4] - start_p[4]) * self._animation_progress), int(bead_radius * 2), int(bead_radius * 2))

            # Draw earth beads using list comprehension
            [painter.setBrush(Qt.blue if j < self._target_state[display_rod_index] % 5 else Qt.gray) or
             painter.drawEllipse(int(rod_x - bead_radius), int(start_p[j] + (end_p[j] - start_p[j]) * self._animation_progress), int(bead_radius * 2), int(bead_radius * 2))
             for j in range(4)]

        # Execute rod drawing for all rods
        [draw_rod(i) for i in range(self.num_rods)]

        # Draw markers with functional mapping
        if self.markers:
            marker_row_height = 25
            base_y = top_margin + rod_height + 10
            marker_colours = [QColor(0, 114, 178), QColor(230, 159, 0), QColor(0, 158, 115)]
            colour_map = {'blue': QColor(0, 114, 178), 'green': QColor(0, 158, 115), 'red': QColor(213, 94, 0), 'orange': QColor(230, 159, 0)}

            def draw_marker(idx_marker):
                i, marker = idx_marker
                if len(marker) < 3:
                    return
                
                start_rod, end_rod, label = marker[:3]
                colour_name = marker[3] if len(marker) > 3 else None
                
                # Correct rod-to-x conversion logic
                start_x = (self.num_rods - start_rod) * rod_width
                end_x = (self.num_rods - end_rod) * rod_width
                if start_x > end_x:
                    start_x, end_x = end_x, start_x
                
                line_y = base_y + i * marker_row_height
                colour = colour_map.get(colour_name.lower() if colour_name else "", marker_colours[i % len(marker_colours)])
                
                painter.setPen(QPen(colour, 2))
                painter.drawLine(int(start_x), int(line_y), int(end_x), int(line_y))
                
                # Draw label
                font_metrics = painter.fontMetrics()
                text_width = font_metrics.horizontalAdvance(label)
                painter.drawText(int(start_x + (end_x - start_x) / 2 - text_width / 2), int(line_y + 15), label)

            [draw_marker(item) for item in enumerate(self.markers)]
