from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

DIALOG_STYLE = """
    QDialog {
        background-color: #2e1a47;
        color: white;
        font-family: Arial, sans-serif;
    }
"""

class GameOverDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Game Over")
        self.setFixedSize(500, 350)
        
        self.setStyleSheet(DIALOG_STYLE + """
            QPushButton {
                background-color: rgba(40, 10, 60, 180);
                border: 2px solid #9a3a7a;
                border-radius: 5px;
                padding: 8px 20px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(60, 30, 90, 220);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Картинка
        self.image_label = QLabel()
        pixmap = QPixmap("assets/buttons/game_over.png")
        if pixmap.isNull():
            print("Warning: game_over.png not found")
        else:
            self.image_label.setPixmap(pixmap.scaled(300, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        # Кнопка "Back to Menu"
        self.menu_button = QPushButton("Back to Menu")
        self.menu_button.clicked.connect(self.accept)  # <--- Важно!
        layout.addWidget(self.menu_button, alignment=Qt.AlignmentFlag.AlignCenter)
