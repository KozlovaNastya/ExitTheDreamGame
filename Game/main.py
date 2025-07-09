import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
)
from PyQt6.QtCore import Qt
from gam.levels.levels import LevelOne, LevelTwo, LevelThree, LevelFour, LevelFive
from gam.levels.health import HeartsWidget


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gravity")
        self.levels = [LevelOne, LevelTwo, LevelThree, LevelFour, LevelFive]
        self.current_level_index = 0

        # 1) Центральный контейнер и его grid‑layout
        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.grid = QGridLayout(self.container)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        # 2) Инициализируем пустой уровень
        self.level_widget = None
        self.load_level(self.current_level_index)

        # 3) Создаём hearts_widget и сразу кладём его в ту же ячейку (0,0),
        #    но с выравниванием сверху‑слева — это и сделает оверлей.
        self.hearts_widget = HeartsWidget(self.container)
        self.hearts_widget.setFixedSize(150, 50)
        # фон уже внутри transparent, не надо стили переносить сюда
        self.grid.addWidget(
            self.hearts_widget,
            0, 0,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

    def load_level(self, index):
        if self.level_widget is not None:
            # Если в уровне есть игрок — удаляем его корректно (останавливаем таймер и т.п.)
            if hasattr(self.level_widget, 'player') and self.level_widget.player is not None:
                self.level_widget.player.deleteLater()

            if self.level_widget and hasattr(self.level_widget, 'player'):
                self.level_widget.player.set_gravity_down()

            # Удаляем сам виджет уровня
            self.level_widget.setParent(None)
            self.level_widget.deleteLater()
            self.level_widget = None

        # Если уровней больше нет — завершаем игру
        if index >= len(self.levels): 
            print("Game finished!")
            self.close()
            return

        # Создаём и добавляем новый уровень в layout
        self.level_widget = self.levels[index](parent=self.container, game=self)
        self.grid.addWidget(self.level_widget, 0, 0)
        self.level_widget.setFocus()


    def load_next_level(self):
        self.current_level_index += 1
        self.hearts_widget.update_level(self.current_level_index + 1)
        self.load_level(self.current_level_index)

    def player_died(self):
        self.hearts_widget.lose_life()
        if self.hearts_widget.lives <= 0:
            self.hearts_widget.reset_lives()
            self.current_level_index = 0
            self.hearts_widget.update_level(1)
        # Всегда загружаем уровень заново при смерти
        self.load_level(self.current_level_index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        game = Game()
        game.resize(800, 600)
        game.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
