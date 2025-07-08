from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer
from gam.constants import BASE_DIR
import os

class Platform(QWidget):
    def __init__(self, x, y, width, height, image_path=None, parent=None):
        super().__init__(parent)
        self.setGeometry(x, y, width, height)
        if image_path:      
            full_path = os.path.join(BASE_DIR, image_path)
            self.image = QPixmap(full_path)
        else:
            self.image = None

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.image and not self.image.isNull():
            scaled_pixmap = self.image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
        else:
            painter.fillRect(self.rect(), Qt.GlobalColor.darkGray)


class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, image_path=None, speed=2, move_range=(0, 100), parent=None):
        super().__init__(x, y, width, height, image_path, parent)

        self.speed = speed
        self.move_range = move_range
        self.direction = 1

        self.timer = QTimer()
        self.timer.timeout.connect(self.move_platform)
        self.timer.start(16)

    def move_platform(self):
        old_x = self.x()
        new_x = self.x() + self.speed * self.direction

        if new_x < self.move_range[0]:
            new_x = self.move_range[0]
            self.direction = 1
        elif new_x + self.width() > self.move_range[1]:
            new_x = self.move_range[1] - self.width()
            self.direction = -1

        dx = new_x - old_x
        self.move(new_x, self.y())

        if hasattr(self.parent(), 'player'):
            player = self.parent().player
            player_rect = player.geometry()
            platform_rect = self.geometry()

            if (
                abs(player_rect.bottom() - platform_rect.top()) <= 5 and
                player_rect.right() > platform_rect.left() and
                player_rect.left() < platform_rect.right() and
                player.gravity_y > 0
            ):
                player.move(player.x() + dx, player.y())