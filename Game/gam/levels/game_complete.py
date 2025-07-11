from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QLinearGradient, QColor, QBrush

DIALOG_STYLE = """
    QDialog {
        color: white;
        font-family: Arial, sans-serif;
    }
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
"""

class GameCompletedDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Game Completed")
        self.setFixedSize(500, 350)

        # Градиентный фон через палитру
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(70, 20, 100))
        gradient.setColorAt(1.0, QColor(30, 5, 60))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setStyleSheet(DIALOG_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Текст поздравления
        self.text_label = QLabel("Congratulations!\nYou escaped the dream!")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #e0c3ff;")
        layout.addWidget(self.text_label)

        # Кнопка возврата в меню
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        self.menu_button = QPushButton("Back to Menu")
        button_layout.addWidget(self.menu_button)

        layout.addLayout(button_layout)

        self.menu_button.clicked.connect(self.accept)
