import os
import json
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QDialog,
    QInputDialog
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
        self.player_name = "Player"
        self.score = 0

        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.grid = QGridLayout(self.container)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.hearts_widget = HeartsWidget(self.container)
        self.hearts_widget.setFixedSize(150, 50)
        self.grid.addWidget(
            self.hearts_widget,
            0, 0,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        self.level_widget = None
        self.load_level(self.current_level_index)

    def load_level(self, index):
        if self.level_widget is not None:
            self.level_widget.setParent(None)
            self.level_widget.deleteLater()
            self.level_widget = None
            
        if index >= len(self.levels): 
            self.score += (index) * self.hearts_widget.lives
            
            name, ok = QInputDialog.getText(
                self, 
                "Game Completed", 
                "Enter your name for the leaderboard:", 
                text=self.player_name
            )
            
            if ok and name:
                self.player_name = name.strip()
            
            self.save_score_to_leaderboard()
            
            dialog = GameCompletedDialog(self)
            result = dialog.exec()
            if result == QDialog.DialogCode.Accepted.value:
                self.back_to_menu_signal.emit()
            else:
                self.close()
            return

        self.level_widget = self.levels[index](parent=self.container, game=self)

        self.grid.addWidget(self.level_widget, 0, 0)
        self.level_widget.setFocus()

        self.hearts_widget.raise_()
        self.hearts_widget.update_level(index + 1)
        
        # Add score for completing previous level (1 point per level * lives)
        if index > 0:
            self.score += (index) * self.hearts_widget.lives

    def save_score_to_leaderboard(self):
        path = os.path.join(os.path.dirname(__file__), "leaderboard.json")
        data = []
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
        data.append({"player": self.player_name, "score": self.score})
        with open(path, 'w') as f:
            json.dump(data, f)

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

                return

        self.load_level(self.current_level_index)

    def set_audio_manager(self, audio_manager):
        self.audio_manager = audio_manager
        print(f"Audio manager set in game: {audio_manager.control_scheme}")

