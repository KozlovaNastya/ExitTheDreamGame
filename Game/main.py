import sys
from PyQt6.QtWidgets import QApplication
from gam.levels.level1 import LevelOne

if __name__ == "__main__":
    app = QApplication(sys.argv)

    level = LevelOne()
    level.setWindowTitle("Gravity - Level 1")
    level.show()

    sys.exit(app.exec())
