import sys
from PyQt6.QtWidgets import QApplication
from gam.main_menu import MainMenu
from main import Game

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MainMenu()

    def handle_start(level, name):
        game = Game()
        game.resize(800, 600)
        game.show()
        menu.hide()

    menu.start_game_signal.connect(handle_start)
    menu.show()
    sys.exit(app.exec())
