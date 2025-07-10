import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QObject, pyqtProperty
from gam.constants import BASE_DIR

class MarginAnimator(QObject):
    def __init__(self, label):
        super().__init__()
        self._margin = 0
        self.label = label

    def getMargin(self):
        return self._margin

    def setMargin(self, value):
        self._margin = value
        # Устанавливаем отступы через стиль
        self.label.setStyleSheet(f"margin-left: {value}px; margin-top: {value // 2}px;")

    margin = pyqtProperty(int, getMargin, setMargin)

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

        # ��������� ������� �����
        self.update_level(1)


    def update_level(self, level_num):
        self.level_label.setText(f"lvl{level_num}")

    def lose_life(self):
       if self.lives <= 0:
            return

       self.lives -= 1
       heart_to_lose = self.hearts[self.lives]

       self.animator = MarginAnimator(heart_to_lose)  # Сохраняем как атрибут, чтобы не удалился

       animation = QPropertyAnimation(self.animator, b"margin")
       animation.setDuration(400)
       animation.setKeyValueAt(0, 0)
       animation.setKeyValueAt(0.1, -3)
       animation.setKeyValueAt(0.2, 3)
       animation.setKeyValueAt(0.3, -3)
       animation.setKeyValueAt(0.4, 3)
       animation.setKeyValueAt(0.5, 0)
       animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

       def on_finished():
           empty_pixmap = QPixmap(os.path.join(BASE_DIR, "assets/for game/empty_heart.png"))
           heart_to_lose.setPixmap(empty_pixmap)
            # Сбрасываем стиль
           heart_to_lose.setStyleSheet("margin: 0px;")

       animation.finished.connect(on_finished)
       animation.start()
       self.animation = animation  # Сохраняем анимацию, чтобы не удалился


    def reset_lives(self):
        self.lives = 3
        for i, heart in enumerate(self.hearts):
            if i < 3:
                heart.setPixmap(QPixmap(os.path.join(BASE_DIR, "assets/for game/full_heart.png")))