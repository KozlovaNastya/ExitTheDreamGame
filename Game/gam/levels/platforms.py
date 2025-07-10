from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap, QTransform
from PyQt6.QtCore import Qt, QTimer, QRect
from gam.constants import BASE_DIR
import os

class Platform(QWidget):
    def __init__(self, x, y, width, height, image_path=None, rotation=0, parent=None):
        super().__init__(parent)
        if rotation in (90, 270):
            width, height = height, width
        self.setGeometry(x, y, width, height)
        self.rotation = rotation
        if image_path:      
            full_path = os.path.join(BASE_DIR, image_path)
            self.image = QPixmap(full_path)
        else:
            self.image = None


    def paintEvent(self, event):
        painter = QPainter(self)
        if self.image and not self.image.isNull():
            pixmap = self.image.transformed(
                QTransform().rotate(self.rotation), Qt.TransformationMode.SmoothTransformation
            )
            scaled_pixmap = pixmap.scaled(
                self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
        else:
            painter.fillRect(self.rect(), Qt.GlobalColor.darkGray)


class MovingPlatform(Platform):
    def __init__(
        self, x, y, width, height,
        image_path=None,
        speed=2,
        move_range_x=None,
        move_range_y=None,
        rotation=0,
        parent=None
    ):
        super().__init__(x, y, width, height, image_path, rotation, parent)

        self.speed = speed
        self.move_range_x = move_range_x  # кортеж (min_x, max_x)
        self.move_range_y = move_range_y  # кортеж (min_y, max_y)
        self.direction_x = 1
        self.direction_y = 1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_platform)
        self.timer.start(16)

    def move_platform(self):
        dx = dy = 0

        if self.move_range_x:
            old_x = self.x()
            new_x = self.x() + self.speed * self.direction_x
            if new_x < self.move_range_x[0]:
                new_x = self.move_range_x[0]
                self.direction_x = 1
            elif new_x + self.width() > self.move_range_x[1]:
                new_x = self.move_range_x[1] - self.width()
                self.direction_x = -1
            dx = new_x - old_x
        else:
            new_x = self.x()

        if self.move_range_y:
            old_y = self.y()
            new_y = self.y() + self.speed * self.direction_y
            if new_y < self.move_range_y[0]:
                new_y = self.move_range_y[0]
                self.direction_y = 1
            elif new_y + self.height() > self.move_range_y[1]:
                new_y = self.move_range_y[1] - self.height()
                self.direction_y = -1
            dy = new_y - old_y
        else:
            new_y = self.y()

        self.move(new_x, new_y)

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
                player.move(player.x() + dx, player.y() + dy)

class DisappearingPlatform(Platform):
    def __init__(self, x, y, width, height, image_path=None, rotation=0, disappear_delay=2000, parent=None):
        super().__init__(x, y, width, height, image_path, rotation, parent)
        self.disappear_delay = disappear_delay
        self._is_disappeared = False
        
        self.disappear_timer = QTimer(self)
        self.disappear_timer.setSingleShot(True)
        self.disappear_timer.timeout.connect(self.disappear)

        # Запускаем таймер сразу при создании платформы
        self.disappear_timer.start(self.disappear_delay)

    def disappear(self):
        if self._is_disappeared:
            return
        self._is_disappeared = True

        self.hide()
        self.disappear_timer.stop()
        self.disappear_timer.disconnect()

        parent = self.parent()
        if parent and hasattr(parent, "platforms"):
            try:
                parent.platforms.remove(self)
            except ValueError:
                pass
        self.deleteLater()


def create_platform_from_data(data, parent=None):
    if len(data) == 5:
        x, y, w, h, img = data
        return Platform(x, y, w, h, img, 0, parent)
    elif len(data) == 6:
        x, y, w, h, img, rot = data
        return Platform(x, y, w, h, img, rot, parent)
    elif len(data) == 7:
        x, y, w, h, img, rot, disappear_delay = data
        return DisappearingPlatform(x, y, w, h, img, rot, disappear_delay, parent)
    else:
        raise ValueError("ERROR format")


