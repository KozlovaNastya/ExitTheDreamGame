from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt
import os
from gam.constants import BASE_DIR
from gam.levels.platforms import Platform, MovingPlatform
from gam.levels.player import Player
from gam.levels.spikes import Spikes
from gam.levels.health import HeartsWidget


class BaseLevel(QWidget):
    def __init__(self, background_path, platforms_data, player_start, finish_line_x, parent=None, game=None):
        super().__init__(parent)
        self.game = game
        print(f"[DEBUG] BaseLevel created with game: {self.game}, parent: {self.parent()}")
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
        self.player = Player(*player_start, "assets/for game/sprite1.png", parent=self, game=game)
        self.player.set_platforms(self.platforms)
        self.player.set_level(self)
        self.player.show()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

    def keyPressEvent(self, event):
        print(f"[DEBUG] key pressed: {event.key()}, player: {self.player}, game: {getattr(self, 'game', None)}")
        print(f"[DEBUG] parent: {self.parent()}")
        print(f"[DEBUG] current_level_index from game: {getattr(self.game, 'current_level_index', None)}")

        if event.key() == Qt.Key.Key_Left:
            self.player.move_left()
        elif event.key() == Qt.Key.Key_Right:
            self.player.move_right()
        elif event.key() == Qt.Key.Key_Space:
            self.player.jump()
    
        current_level = self.game.current_level_index + 1 if self.game else 1

   
        if current_level == 1:
            return
   
        elif current_level == 2:
            if event.key() == Qt.Key.Key_1:
                self.player.set_gravity_down()
            elif event.key() == Qt.Key.Key_2:
                self.player.set_gravity_up()
            return
 
        else:
            if event.key() == Qt.Key.Key_1:
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
            if self.game is not None:
                self.game.load_next_level()
