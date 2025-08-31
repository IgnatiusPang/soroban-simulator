#!/usr/bin/env python3
"""
Test the GUI with different multiplication examples to verify positioning works generally.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from PySide6.QtWidgets import QApplication
from soroban_simulator.gui.main_window import MainWindow

def main():
    """Test the GUI with different multiplication examples."""
    app = QApplication(sys.argv)
    
    # Create the main window
    window = MainWindow()
    window.show()
    
    # Test with a different multiplication: 7 * 38
    window.equation_input.setText("7 * 38")
    
    # Trigger the calculation to show the markers
    window.calculate()
    
    print("GUI launched with 7 * 38 multiplication.")
    print("This tests a single-digit × two-digit multiplication.")
    print("Check that M1, M2, and PP labels are positioned correctly.")
    
    # Run the application
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
