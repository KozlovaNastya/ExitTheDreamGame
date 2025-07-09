import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint
from gam.constants import BASE_DIR

class HeartsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lives = 3
        self.setup_ui()
        self.update_level(1)

    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # Label for level text
        self.level_label = QLabel("lvl1")
        self.level_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        self.layout.addWidget(self.level_label)

        # Hearts
        self.hearts = []
        for _ in range(3):
            heart = QLabel()
            pixmap_path = os.path.join(BASE_DIR, "assets/for game/full_heart.png")
            pixmap = QPixmap(pixmap_path)
            if pixmap.isNull():
                print(f"Failed to load image: {pixmap_path}")
            heart.setPixmap(pixmap)
            heart.setFixedSize(24, 24)
            heart.setScaledContents(True)
            self.hearts.append(heart)
            self.layout.addWidget(heart)

        self.layout.addStretch()

        self.setStyleSheet("background-color: transparent;")

        # Обновляем уровень сразу
        self.update_level(1)


    def update_level(self, level_num):
        self.level_label.setText(f"lvl{level_num}")

    def lose_life(self):
        if self.lives <= 0:
            return

        self.lives -= 1
        heart_to_lose = self.hearts[self.lives]
        
        # Animation for losing heart
        animation = QPropertyAnimation(heart_to_lose, b"pos")
        animation.setDuration(300)
        animation.setKeyValueAt(0, heart_to_lose.pos())
        animation.setKeyValueAt(0.25, heart_to_lose.pos() + QPoint(0, -5))
        animation.setKeyValueAt(0.5, heart_to_lose.pos() + QPoint(5, 0))
        animation.setKeyValueAt(0.75, heart_to_lose.pos() + QPoint(0, 5))
        animation.setKeyValueAt(1, heart_to_lose.pos())
        animation.start()
        
        # Change to empty heart after animation
        animation.finished.connect(lambda: heart_to_lose.setPixmap(
            QPixmap(os.path.join(BASE_DIR, "assets/for game/empty_heart.png"))
        ))

    def reset_lives(self):
        self.lives = 3
        for i, heart in enumerate(self.hearts):
            if i < 3:
                heart.setPixmap(QPixmap(os.path.join(BASE_DIR, "assets/for game/full_heart.png")))