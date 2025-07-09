from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
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

        self.image_label = QLabel()
        pixmap = QPixmap("assets/buttons/game_over.png")
        if pixmap.isNull():
            print("Warning: game_over.png not found")
        else:
            self.image_label.setPixmap(pixmap.scaled(300, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        self.text_label = QLabel("Game Over")
        self.text_label.setStyleSheet("color: #e0c3ff; font-size: 24px; font-weight: bold;")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_label)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        self.retry_button = QPushButton("Retry")
        self.menu_button = QPushButton("Back to Menu")
        button_layout.addWidget(self.retry_button)
        button_layout.addWidget(self.menu_button)
        layout.addLayout(button_layout)

        self.retry_button.clicked.connect(self.accept)
        self.menu_button.clicked.connect(self.reject)
