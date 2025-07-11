import os
import json
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout,
    QDialog, QInputDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from gam.levels.levels import LevelOne, LevelTwo, LevelThree, LevelFour, LevelFive
from gam.levels.health import HeartsWidget
from gam.levels.game_over import GameOverDialog
from gam.levels.game_complete import GameCompletedDialog
from pathlib import Path

def get_leaderboard_path():
    base_dir = Path(__file__).parent
    return base_dir / "leaderboard.json"

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
        
            input_dialog = QDialog(self)
            input_dialog.setWindowTitle("Game Completed")
            input_dialog.setFixedSize(400, 200)
            input_dialog.setStyleSheet("""
                QDialog {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #2a0845, stop:1 #7a1a5a);
                    color: white;
                    font-family: 'Minecraft';
                }
                QLabel {
                    color: white;
                    font-size: 16px;
                    margin-bottom: 20px;
                }
                QLineEdit {
                    background: rgba(60, 20, 80, 220);
                    border: 2px solid #9a3a7a;
                    border-radius: 5px;
                    padding: 8px;
                    color: white;
                    font-size: 14px;
                    margin-bottom: 20px;
                }
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a2a75, stop:1 #9a3a7a);
                    color: white;
                    border: 2px solid #ba5a9a;
                    border-radius: 5px;
                    padding: 8px 16px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #6a3a85, stop:1 #aa4a8a);
                }
            """)
        
            layout = QVBoxLayout(input_dialog)
            label = QLabel("Enter your name for the leaderboard:")
            layout.addWidget(label)
        
            self.name_input = QLineEdit()
            self.name_input.setPlaceholderText("Player Name")
            self.name_input.setText(self.player_name)
            layout.addWidget(self.name_input)
        
            button_box = QHBoxLayout()
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(input_dialog.accept)
            button_box.addWidget(ok_button)
        
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(input_dialog.reject)
            button_box.addWidget(cancel_button)
        
            layout.addLayout(button_box)
        
            if input_dialog.exec() == QDialog.DialogCode.Accepted:
                name = self.name_input.text().strip()
                if name:
                    self.player_name = name
        
            self.save_score_to_leaderboard()
        
            dialog = GameCompletedDialog(self)
            result = dialog.exec()
            if result == QDialog.DialogCode.Accepted:
                self.back_to_menu_signal.emit()
            else:
                self.close()
            return

        self.level_widget = self.levels[index](parent=self.container, game=self)
        self.grid.addWidget(self.level_widget, 0, 0)
        self.level_widget.setFocus()
        self.hearts_widget.raise_()
        self.hearts_widget.update_level(index + 1)
        
        if index > 0:
            self.score += (index) * self.hearts_widget.lives

    def save_score_to_leaderboard(self):
        try:
            leaderboard_path = get_leaderboard_path()
            
            if leaderboard_path.exists():
                with open(leaderboard_path, 'r', encoding='utf-8') as f:
                    scores = json.load(f)
            else:
                scores = []

            scores.append({
                "player": self.player_name,
                "score": min(self.score, 15)
            })

            unique_scores = []
            seen = set()
            for entry in scores:
                identifier = (entry["player"], entry["score"])
                if identifier not in seen:
                    seen.add(identifier)
                    unique_scores.append(entry)

            unique_scores.sort(key=lambda x: x['score'], reverse=True)
            scores = unique_scores[:10]

            with open(leaderboard_path, 'w', encoding='utf-8') as f:
                json.dump(scores, f, indent=4, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
        
        except Exception as e:
            pass

    def load_next_level(self):
        self.score += (self.current_level_index + 1) * self.hearts_widget.lives
        self.current_level_index += 1
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