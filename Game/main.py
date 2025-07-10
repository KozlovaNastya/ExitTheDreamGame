import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from gam.levels.levels import LevelOne, LevelTwo, LevelThree, LevelFour, LevelFive
from gam.levels.health import HeartsWidget
from gam.levels.game_over import GameOverDialog
from gam.levels.game_complete import GameCompletedDialog



class Game(QMainWindow):
    back_to_menu_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exit the Dream")
        self.levels = [LevelOne, LevelTwo, LevelThree, LevelFour, LevelFive]
        self.current_level_index = 0

        # 1) Центральный контейнер и его grid‑layout
        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.grid = QGridLayout(self.container)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

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

                # 2) Инициализируем пустой уровень
        self.level_widget = None
        self.load_level(self.current_level_index)


    def load_level(self, index):
        if self.level_widget is not None:
            self.level_widget.setParent(None)
            self.level_widget.deleteLater()
            self.level_widget = None
            
        # Если уровней больше нет — завершаем игру
        if index >= len(self.levels): 
            dialog = GameCompletedDialog(self)
            result = dialog.exec()
            if result == QDialog.DialogCode.Accepted.value:
                self.back_to_menu_signal.emit()
            else:
                # Если хочешь, можно сделать что-то еще или просто закрыть игру
                self.close()
            return


        # Создаём и добавляем новый уровень в layout
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

            if result == QDialog.DialogCode.Accepted:
                self.back_to_menu_signal.emit()

            return  # Всегда выходи после обработки диалога

        # Если ещё остались жизни
        self.load_level(self.current_level_index)

