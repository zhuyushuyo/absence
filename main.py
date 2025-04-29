import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from PyQt6.QtWidgets import QApplication
from app.gui.main_window import AbsenceWindow

def main():
    app = QApplication(sys.argv)
    window = AbsenceWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()