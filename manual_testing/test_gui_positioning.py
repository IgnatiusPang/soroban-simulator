#!/usr/bin/env python3
"""
Test script to verify GUI positioning of rod numbers and markers.
"""

import sys
from PySide6.QtWidgets import QApplication
from soroban_simulator.gui.main_window import MainWindow

def test_gui_positioning():
    """Test the GUI positioning by running a multiplication."""
    app = QApplication(sys.argv)
    
    # Create the main window
    window = MainWindow()
    window.show()
    
    # Set up a test multiplication
    window.equation_input.setText("23 * 15")
    window.calculate()
    
    print("GUI test started. Check the following:")
    print("1. Rod numbers 1-13 should be displayed at the top")
    print("   - Rod 1 should be on the rightmost position")
    print("   - Rod 13 should be on the leftmost position")
    print("2. M1, M2, PP labels should align with the correct rod numbers")
    print("3. The markers should be positioned correctly under the numbers")
    print("\nPress Ctrl+C to exit when done testing.")
    
    try:
        app.exec()
    except KeyboardInterrupt:
        print("\nTest completed.")
        sys.exit(0)

if __name__ == "__main__":
    test_gui_positioning()
