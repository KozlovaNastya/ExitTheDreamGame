from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt
import os
from gam.constants import BASE_DIR
from gam.levels.platforms import Platform, MovingPlatform, DisappearingPlatform, create_platform_from_data
from gam.levels.player import Player
from gam.levels.spikes import Spikes
from gam.levels.health import HeartsWidget
import logging

class BaseLevel(QWidget):
    def __init__(self, background_path, platforms_data, player_start, finish_line_x, parent=None, game=None):
        super().__init__(parent)
        self.game = game
        self.setFixedSize(800, 600)
        
        try:
            self.background = QPixmap(os.path.join(BASE_DIR, background_path))
            if self.background.isNull():
                raise FileNotFoundError
        except Exception as e:
            logging.error(f"Failed to load background: {e}")
            self.background = QPixmap(800, 600)
            self.background.fill(Qt.GlobalColor.darkGray)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        self.platforms = []
        self.finish_line_x = finish_line_x
        self.player = None
        self.audio_manager = getattr(game, 'audio_manager', None)

        try:
            for data in platforms_data:
                platform = create_platform_from_data(data, parent=self)
                if platform:
                    platform.show()
                    self.platforms.append(platform)
        except Exception as e:
            logging.error(f"Platform creation error: {e}")

        try:
            self.player = Player(*player_start, "assets/for game/sprite_stand.png", parent=self, game=game)
            self.player.set_platforms(self.platforms)
            self.player.set_level(self)
            self.player.show()
        except Exception as e:
            logging.error(f"Player creation error: {e}")
            raise

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

    def keyPressEvent(self, event):
        if not hasattr(self, 'player') or self.player is None:
            return

        scheme = getattr(self.audio_manager, 'control_scheme', 'Arrow Keys') if self.audio_manager else 'Arrow Keys'
        
        controls = {
            'Arrow Keys': {
                'left': Qt.Key.Key_Left,
                'right': Qt.Key.Key_Right,
                'up': Qt.Key.Key_Up,
                'down': Qt.Key.Key_Down
            },
            'WASD': {
                'left': Qt.Key.Key_A,
                'right': Qt.Key.Key_D,
                'up': Qt.Key.Key_W,
                'down': Qt.Key.Key_S
            }
        }.get(scheme, {
            'left': Qt.Key.Key_Left,
            'right': Qt.Key.Key_Right,
            'up': Qt.Key.Key_Up,
            'down': Qt.Key.Key_Down
        })

        gx, gy = self.player.gravity_x, self.player.gravity_y

        try:
            if gy != 0: 
                if event.key() == controls['left']:
                    self.player.move_left()
                elif event.key() == controls['right']:
                    self.player.move_right()
                elif event.key() == Qt.Key.Key_Space or event.key() == controls['up']:
                    self.player.jump()

            elif gx != 0:
                if event.key() == controls['up']:
                    self.player.vy = -5
                elif event.key() == controls['down']:
                    self.player.vy = 5
                elif event.key() == Qt.Key.Key_Space:
                    self.player.jump()

            current_level = getattr(getattr(self, 'game', None), 'current_level_index', 0) + 1
            
            if current_level == 2:
                if event.key() == Qt.Key.Key_1:
                    self.player.set_gravity_down()
                elif event.key() == Qt.Key.Key_2:
                    self.player.set_gravity_up()
            
            elif current_level >= 3:
                if event.key() == Qt.Key.Key_1:
                    self.player.set_gravity_down()
                elif event.key() == Qt.Key.Key_2:
                    self.player.set_gravity_up()
                elif event.key() == Qt.Key.Key_3:
                    self.player.set_gravity_left()
                elif event.key() == Qt.Key.Key_4:
                    self.player.set_gravity_right()

        except Exception as e:
            logging.error(f"Key press handling error: {e}")

    def keyReleaseEvent(self, event):
        if not hasattr(self, 'player') or self.player is None:
            return

        scheme = getattr(self.audio_manager, 'control_scheme', 'Arrow Keys') if self.audio_manager else 'Arrow Keys'
        controls = {
            'Arrow Keys': {
                'left': Qt.Key.Key_Left,
                'right': Qt.Key.Key_Right,
                'up': Qt.Key.Key_Up,
                'down': Qt.Key.Key_Down
            },
            'WASD': {
                'left': Qt.Key.Key_A,
                'right': Qt.Key.Key_D,
                'up': Qt.Key.Key_W,
                'down': Qt.Key.Key_S
            }
        }.get(scheme, {
            'left': Qt.Key.Key_Left,
            'right': Qt.Key.Key_Right,
            'up': Qt.Key.Key_Up,
            'down': Qt.Key.Key_Down
        })

        gx, gy = self.player.gravity_x, self.player.gravity_y

        try:
            if gy != 0:
                if event.key() in (controls['left'], controls['right']):
                    self.player.stop_movement()
            elif gx != 0:
                if event.key() in (controls['up'], controls['down']):
                    self.player.vy = 0
        except Exception as e:
            logging.error(f"Key release handling error: {e}")

    def check_level_complete(self):
        if hasattr(self, 'player') and self.player and hasattr(self, 'finish_line_x'):
            if self.player.x() >= self.finish_line_x:
                if hasattr(self, 'game') and self.game:
                    try:
                        self.game.load_next_level()
                    except Exception as e:
                        logging.error(f"Level completion error: {e}")

    def cleanup(self):
        try:
            if hasattr(self, 'platforms'):
                for platform in self.platforms[:]:
                    try:
                        if isinstance(platform, (MovingPlatform, DisappearingPlatform)):
                            platform.timer.stop()
                        if hasattr(platform, 'disappear_timer'):
                            platform.disappear_timer.stop()
                        platform.hide()
                        platform.deleteLater()
                    except Exception as e:
                        logging.error(f"Platform cleanup error: {e}")
                    finally:
                        if platform in self.platforms:
                            self.platforms.remove(platform)

            if hasattr(self, 'player') and self.player:
                try:
                    self.player.hide()
                    self.player.deleteLater()
                except Exception as e:
                    logging.error(f"Player cleanup error: {e}")
                finally:
                    self.player = None
        except Exception as e:
            logging.error(f"General cleanup error: {e}")