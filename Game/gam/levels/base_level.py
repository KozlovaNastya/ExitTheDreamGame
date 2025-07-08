from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt
import os
from gam.constants import BASE_DIR
from gam.levels.platforms import Platform, MovingPlatform
from gam.levels.player import Player

class BaseLevel(QWidget):
    def __init__(self, background_path, platforms_data, player_start, finish_line_x, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 600)
        self.background = QPixmap(os.path.join(BASE_DIR, background_path))

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        self.platforms = []
        self.finish_line_x = finish_line_x

        for data in platforms_data:
            if len(data) == 6:
                x, y, w, h, path, rotation = data
            else:
                x, y, w, h, path = data
                rotation = 0
            platform = Platform(x, y, w, h, path, rotation, parent=self)
            platform.show()
            self.platforms.append(platform)
        self.player = Player(*player_start, "assets/for game/sprite1.png", parent=self)
        self.player.set_platforms(self.platforms)
        self.player.set_level(self)
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
        elif event.key() == Qt.Key.Key_1:
            self.player.set_gravity_down()
        elif event.key() == Qt.Key.Key_2:
            self.player.set_gravity_up()
        elif event.key() == Qt.Key.Key_3:
            self.player.set_gravity_left()
        elif event.key() == Qt.Key.Key_4:
            self.player.set_gravity_right()


    def keyReleaseEvent(self, event):
        if event.key() in (Qt.Key.Key_Left, Qt.Key.Key_Right):
            self.player.stop_movement()

    def check_level_complete(self):
        if self.player.x() >= self.finish_line_x:
            if self.parent() is not None and hasattr(self.parent(), "load_next_level"):
                self.parent().load_next_level()
