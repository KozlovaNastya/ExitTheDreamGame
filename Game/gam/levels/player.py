from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer
import os
from gam.constants import BASE_DIR

class Player(QWidget):
    def __init__(self, x, y, width, height, image_path, parent=None):
        super().__init__(parent)
        self.setGeometry(x, y, width, height)

        full_path = os.path.join(BASE_DIR, image_path)
        self.image = QPixmap(full_path)

        self.vx = 0
        self.vy = 0
        self.gravity = 1
        self.gravity_x = 0
        self.gravity_y = 1 
        self.jump_strength = 15
        self.on_ground = False
        self.platforms = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(16)

    def set_platforms(self, platforms):
        self.platforms = platforms

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.image and not self.image.isNull():
            painter.drawPixmap(self.rect(), self.image)
        else:
            painter.fillRect(self.rect(), Qt.GlobalColor.red)

    def move_left(self):
        self.vx = -5

    def move_right(self):
        self.vx = 5

    def stop_movement(self):
        self.vx = 0

    def jump(self):
        if self.on_ground:
            if self.gravity_y != 0:
                self.vy = -self.gravity_y * self.jump_strength
            else:
                self.vx = -self.gravity_x * self.jump_strength
            self.on_ground = False


    def switch_gravity(self):
        self.gravity_direction *= -1

    def set_gravity_down(self):
        self.gravity_x = 0
        self.gravity_y = 1

    def set_gravity_up(self):
        self.gravity_x = 0
        self.gravity_y = -1

    def set_gravity_left(self):
        self.gravity_x = -1
        self.gravity_y = 0

    def set_gravity_right(self):
        self.gravity_x = 1
        self.gravity_y = 0


    def set_level(self, level):
        self.level = level

    def update_position(self):
        self.vx += self.gravity_x * self.gravity
        self.vy += self.gravity_y * self.gravity

        new_x = self.x() + self.vx
        new_y = self.y() + self.vy
        player_rect = self.geometry()

        # Движение по X
        self.move(new_x, self.y())
        self.on_ground = False  # Сброс перед проверкой

        for platform in self.platforms:
            if self.geometry().intersects(platform.geometry()):
                plat_rect = platform.geometry()
                if self.vx > 0:  # Движение вправо
                    self.move(plat_rect.left() - self.width(), self.y())
                elif self.vx < 0:  # Влево
                    self.move(plat_rect.right(), self.y())
                self.vx = 0

        # Движение по Y
        self.move(self.x(), new_y)

        for platform in self.platforms:
            if self.geometry().intersects(platform.geometry()):
                plat_rect = platform.geometry()
                if self.vy > 0:  # Вниз
                    self.move(self.x(), plat_rect.top() - self.height())
                    self.on_ground = True
                elif self.vy < 0:  # Вверх
                    self.move(self.x(), plat_rect.bottom())
                self.vy = 0

        # Проверка выхода за пределы экрана
        if self.y() > self.parent().height() or self.y() + self.height() < 0:
            QApplication.quit()
            return

        if self.x() < 0:
            self.move(0, self.y())
            self.vx = 0
        elif self.x() + self.width() > self.parent().width():
            self.move(self.parent().width() - self.width(), self.y())
            self.vx = 0

        if hasattr(self.parent(), "check_level_complete"):
            self.parent().check_level_complete()


    def check_on_ground(self, player_rect, platform_rect):
        tolerance = 5

        if self.gravity_y > 0:  # Гравитация вниз
            return (
                abs(player_rect.bottom() - platform_rect.top()) <= tolerance and
                player_rect.right() > platform_rect.left() and
                player_rect.left() < platform_rect.right()
            )
        elif self.gravity_y < 0:  # Вверх
            return (
                abs(player_rect.top() - platform_rect.bottom()) <= tolerance and
                player_rect.right() > platform_rect.left() and
                player_rect.left() < platform_rect.right()
            )
        elif self.gravity_x > 0:  # Вправо
            return (
                abs(player_rect.right() - platform_rect.left()) <= tolerance and
                player_rect.bottom() > platform_rect.top() and
                player_rect.top() < platform_rect.bottom()
            )
        elif self.gravity_x < 0:  # Влево
            return (
                abs(player_rect.left() - platform_rect.right()) <= tolerance and
                player_rect.bottom() > platform_rect.top() and
                player_rect.top() < platform_rect.bottom()
            )
        return False

