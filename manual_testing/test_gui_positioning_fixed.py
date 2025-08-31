#!/usr/bin/env python3
"""
Test script to verify the GUI positioning fixes for M1, M2, and PP labels.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from PySide6.QtWidgets import QApplication
from soroban_simulator.gui.main_window import MainWindow

def main():
    """Test the GUI with a multiplication example to verify label positioning."""
    app = QApplication(sys.argv)
    
    # Create the main window
    window = MainWindow()
    window.show()
    
    # Set a multiplication equation to test the positioning
    window.equation_input.setText("23 * 15")
    
    # Trigger the calculation to show the markers
    window.calculate()
    
    print("GUI launched with 23 * 15 multiplication.")
    print("Check that:")
    print("1. M1, M2, and PP labels are positioned correctly under their respective numbers")
    print("2. All labels (including PP) are visible without needing to resize the window")
    print("3. The bottom margin provides enough space for all three marker rows")
    
    # Run the application
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
