from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt
from gam.constants import BASE_DIR
from gam.levels.platforms import Platform
from gam.levels.player import Player
import os


class LevelOne(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 600)
        self.background = QPixmap(os.path.join(BASE_DIR, "assets/background/level1.png"))


        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        self.platforms = []

        # Платформы
        platform1 = Platform(10, 500, 100, 40, "assets/for game/platform.png", parent=self)
        platform1.show()
        self.platforms.append(platform1)

        platform2 = Platform(110, 450, 80, 40, "assets/for game/platform.png", parent=self)
        platform2.show()
        self.platforms.append(platform2)

        platform2 = Platform(190, 350, 80, 40, "assets/for game/platform.png", parent=self)
        platform2.show()
        self.platforms.append(platform2)

        # Игрок (выше платформы, чтобы не застревал)
        self.player = Player(20, 400, 50, 50, "assets/for game/sprite1.png", parent=self)
        self.player.set_platforms(self.platforms)
        self.player.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.player.move_left()
        elif event.key() == Qt.Key.Key_Right:
            self.player.move_right()
        elif event.key() == Qt.Key.Key_Space:
            self.player.jump()

    def keyReleaseEvent(self, event):
        if event.key() in (Qt.Key.Key_Left, Qt.Key.Key_Right):
            self.player.stop_movement()
