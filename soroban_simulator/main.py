
import sys
from PySide6.QtWidgets import QApplication
from soroban_simulator.gui.main_window import MainWindow

def main():
    """The main entry point of the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
