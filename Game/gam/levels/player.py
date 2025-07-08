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
            self.vx -= self.gravity_x * self.jump_strength
            self.vy -= self.gravity_y * self.jump_strength
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

        # Предварительное перемещение
        self.move(new_x, new_y)
        self.on_ground = False

        player_rect = self.geometry()

        for platform in self.platforms:
            platform_rect = platform.geometry()

            if player_rect.intersects(platform_rect):
                # Гравитация вниз
                if self.gravity_y > 0 and self.vy > 0 and player_rect.bottom() - self.vy <= platform_rect.top():
                    self.move(self.x(), platform.y() - self.height())
                    self.vy = 0
                    self.on_ground = True
                # Гравитация вверх
                elif self.gravity_y < 0 and self.vy < 0 and player_rect.top() - self.vy >= platform_rect.bottom():
                    self.move(self.x(), platform.y() + platform.height())
                    self.vy = 0
                    self.on_ground = True
                # Гравитация вправо
                elif self.gravity_x > 0 and self.vx > 0 and player_rect.right() - self.vx <= platform_rect.left():
                    self.move(platform.x() - self.width(), self.y())
                    self.vx = 0
                    self.on_ground = True
                # Гравитация влево
                elif self.gravity_x < 0 and self.vx < 0 and player_rect.left() - self.vx >= platform_rect.right():
                    self.move(platform.x() + platform.width(), self.y())
                    self.vx = 0
                    self.on_ground = True



       # Выход за нижнюю границу — перезапуск
        if self.y() > self.parent().height() or self.y() + self.height() < 0:
           from PyQt6.QtWidgets import QApplication
           QApplication.quit()
           return

       # Ограниичения по бокам
        if self.x() < 0:
            self.move(0, self.y())
        elif self.x() + self.width() > self.parent().width():
            self.move(self.parent().width() - self.width(), self.y())

        # Проверка прохождения уровня
        if hasattr(self.parent(), "check_level_complete"):
            self.parent().check_level_complete()


