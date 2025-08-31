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
        # Reserve more space at bottom for marker rows and top for rod numbers
        marker_space = self.height() * 0.25  # 25% for markers (increased from 15%)
        rod_number_space = self.height() * 0.08  # 8% for rod numbers at top
        rod_height = self.height() * 0.52     # Reduced to accommodate larger marker space
        top_margin = self.height() * 0.1 + rod_number_space
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

        for i in range(self.num_rods):
            # Reverse the rod order for display: rightmost rod (highest index) should be leftmost on screen
            display_rod_index = self.num_rods - 1 - i
            rod_x = (i + 1) * rod_width
            
            # Draw rod number at the top (rod 1 is rightmost, rod 13 is leftmost)
            rod_number = display_rod_index + 1
            font_metrics = painter.fontMetrics()
            text_width = font_metrics.horizontalAdvance(str(rod_number))
            text_x = rod_x - text_width / 2
            text_y = self.height() * 0.05
            painter.drawText(int(text_x), int(text_y), str(rod_number))
            
            # Draw the rod
            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(rod_x, top_margin, rod_x, top_margin + rod_height)

            start_positions = self._get_bead_y_positions(self._start_state[display_rod_index], rod_height, top_margin, bar_y, bar_height, bead_radius)
            end_positions = self._get_bead_y_positions(self._target_state[display_rod_index], rod_height, top_margin, bar_y, bar_height, bead_radius)

            # Heaven bead
            start_y = start_positions[4]
            end_y = end_positions[4]
            current_y = start_y + (end_y - start_y) * self._animation_progress
            painter.setBrush(Qt.blue if self._target_state[display_rod_index] >= 5 else Qt.gray)
            painter.drawEllipse(rod_x - bead_radius, current_y, bead_radius * 2, bead_radius * 2)

            # Earth beads
            for j in range(4):
                start_y = start_positions[j]
                end_y = end_positions[j]
                current_y = start_y + (end_y - start_y) * self._animation_progress
                painter.setBrush(Qt.blue if j < self._target_state[display_rod_index] % 5 else Qt.gray)
                painter.drawEllipse(rod_x - bead_radius, current_y, bead_radius * 2, bead_radius * 2)

        # Draw markers with different vertical positions and color-blind safe colors
        if self.markers:
            font = painter.font()
            font.setPointSize(10)
            painter.setFont(font)
            
            # Color-blind safe colors: Blue, Orange, Green
            marker_colors = [
                QColor(0, 114, 178),    # Blue for M1 (multiplier)
                QColor(230, 159, 0),    # Orange for M2 (multiplicand) 
                QColor(0, 158, 115)     # Green for PP (partial products)
            ]
            
            # Stack markers vertically to avoid overlap
            marker_row_height = 25
            base_y = top_margin + rod_height + 10
            
            for i, (start_rod, end_rod, label) in enumerate(self.markers):
                # The markers use 0-based rod indices where:
                # - Rod index 0 = Rod number 1 (rightmost rod)
                # - Rod index 12 = Rod number 13 (leftmost rod)
                # 
                # The display uses reversed indexing:
                # - display_rod_index = self.num_rods - 1 - loop_i
                # - rod_x = (loop_i + 1) * rod_width
                # 
                # To find the correct x position for a rod index N:
                # We need loop_i such that display_rod_index = N
                # N = self.num_rods - 1 - loop_i
                # loop_i = self.num_rods - 1 - N
                
                start_loop_i = self.num_rods - 1 - start_rod
                end_loop_i = self.num_rods - 1 - end_rod
                
                start_x = (start_loop_i + 1) * rod_width
                end_x = (end_loop_i + 1) * rod_width
                
                # Ensure start_x is always to the left of end_x for proper line drawing
                if start_x > end_x:
                    start_x, end_x = end_x, start_x
                
                line_y = base_y + i * marker_row_height
                
                # Use different color for each marker type
                color = marker_colors[i % len(marker_colors)]
                painter.setPen(QPen(color, 2))

                # Draw the line
                painter.drawLine(int(start_x), int(line_y), int(end_x), int(line_y))

                # Draw the label
                font_metrics = painter.fontMetrics()
                text_width = font_metrics.horizontalAdvance(label)
                text_x = start_x + (end_x - start_x) / 2 - text_width / 2
                text_y = line_y + 15
                painter.drawText(int(text_x), int(text_y), label)
