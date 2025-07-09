# import sys
# from PyQt6.QtWidgets import QApplication
# from gam.main_menu import MainMenu
# from main import Game

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     menu = MainMenu()

#     def handle_start(level, name):
#         game = Game()
#         game.resize(800, 600)
#         game.show()
#         menu.hide()

#     menu.start_game_signal.connect(handle_start)
#     menu.show()
#     sys.exit(app.exec())
import sys
from PyQt6.QtWidgets import QApplication
from gam.main_menu import MainMenu
from main import Game

game = None  # глобальная переменная для игры

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MainMenu()

    game = None  # Глобальная переменная для окна игры

    def handle_start(level, name):
        global game
        game = Game()
        game.resize(800, 600)
        game.show()
        menu.hide()

        # Подписываемся на сигнал возврата в меню из игры
        game.back_to_menu_signal.connect(handle_back_to_menu)

    def handle_back_to_menu():
        global game
        try:
            if game:
                game.hide()          # просто скрываем окно
                game.deleteLater()   # безопасно удаляем объект (через очередь событий Qt)
                game = None
            menu.show()
        except Exception as e:
            print(f"Error in handle_back_to_menu: {e}")

    menu.start_game_signal.connect(handle_start)
    menu.show()
    sys.exit(app.exec())
