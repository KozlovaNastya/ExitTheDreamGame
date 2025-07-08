import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from gam.levels.levels import LevelOne, LevelTwo, LevelThree, LevelFour, LevelFive

class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gravity")
        self.levels = [LevelFour, LevelFive]
        self.current_level_index = 0
        self.load_level(self.current_level_index)

    def load_level(self, index):
        if hasattr(self, 'level_widget') and self.level_widget is not None:
            self.level_widget.setParent(None)
            self.level_widget.deleteLater()
            self.level_widget = None

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
