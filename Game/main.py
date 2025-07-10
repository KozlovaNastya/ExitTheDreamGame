import sys


from PyQt6.QtWidgets import QApplication, QMainWindow
from gam.levels.levels import LevelOne, LevelTwo, LevelThree, LevelFour, LevelFive
<<<<<<< Updated upstream

class Game(QMainWindow):
=======
from gam.levels.health import HeartsWidget
from gam.levels.game_over import GameOverDialog

class Game(QMainWindow):
    back_to_menu_signal = pyqtSignal()
    
>>>>>>> Stashed changes
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gravity")
        self.levels = [LevelFour, LevelFive]
        self.current_level_index = 0
<<<<<<< Updated upstream
=======

        # Main container and layout        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.grid = QGridLayout(self.container)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        # Hearts widget overlay
        self.hearts_widget = HeartsWidget(self.container)
        self.hearts_widget.setFixedSize(150, 50)
        self.grid.addWidget(
            self.hearts_widget,
            0, 0,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        # Initialize empty level
        self.level_widget = None
>>>>>>> Stashed changes
        self.load_level(self.current_level_index)

    def load_level(self, index):
        if hasattr(self, 'level_widget') and self.level_widget is not None:
            self.level_widget.setParent(None)
            self.level_widget.deleteLater()
            self.level_widget = None
<<<<<<< Updated upstream

        if index >= len(self.levels):
            print("Game finished!")
            self.close()
            return

        self.level_widget = self.levels[index](parent=self)
        self.setCentralWidget(self.level_widget)
        self.level_widget.setFocus()

    def load_next_level(self):
        self.current_level_index += 1
        self.load_level(self.current_level_index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec())
=======
            
        if index >= len(self.levels): 
            self.close()
            return

        self.level_widget = self.levels[index](parent=self.container, game=self)
        self.grid.addWidget(self.level_widget, 0, 0)
        self.level_widget.setFocus()

        self.hearts_widget.raise_()
        self.hearts_widget.update_level(index + 1)

    def load_next_level(self):
        self.current_level_index += 1
        self.hearts_widget.update_level(self.current_level_index + 1)
        self.load_level(self.current_level_index)

    def player_died(self):
        self.hearts_widget.lose_life()

        if self.hearts_widget.lives <= 0:
            dialog = GameOverDialog(self)
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted.value:
                self.back_to_menu_signal.emit()
            return

        self.load_level(self.current_level_index) 
>>>>>>> Stashed changes
git add Game/main.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QDialog
from PyQt6.QtCore import pyqtSignal, Qt
from gam.levels.levels import LevelOne, LevelTwo, LevelThree, LevelFour, LevelFive
from gam.levels.health import HeartsWidget
from gam.levels.game_over import GameOverDialog

class Game(QMainWindow):
    back_to_menu_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gravity")
        self.levels = [LevelFour, LevelFive]
        self.current_level_index = 0

        # Main container and layout
        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.grid = QGridLayout(self.container)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        # Hearts widget overlay
        self.hearts_widget = HeartsWidget(self.container)
        self.hearts_widget.setFixedSize(150, 50)
        self.grid.addWidget(
            self.hearts_widget,
            0, 0,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        # Initialize empty level
        self.level_widget = None
        self.load_level(self.current_level_index)

    def load_level(self, index):
        if hasattr(self, 'level_widget') and self.level_widget is not None:
            self.level_widget.setParent(None)
            self.level_widget.deleteLater()
            self.level_widget = None

        if index >= len(self.levels):
            self.close()
            return

        self.level_widget = self.levels[index](parent=self.container, game=self)
        self.grid.addWidget(self.level_widget, 0, 0)
        self.level_widget.setFocus()
        self.hearts_widget.raise_()
        self.hearts_widget.update_level(index + 1)

    def load_next_level(self):
        self.current_level_index += 1
        self.hearts_widget.update_level(self.current_level_index + 1)
        self.load_level(self.current_level_index)

    def player_died(self):
        self.hearts_widget.lose_life()

        if self.hearts_widget.lives <= 0:
            dialog = GameOverDialog(self)
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted.value:
                self.back_to_menu_signal.emit()
            return

        self.load_level(self.current_level_index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec())

