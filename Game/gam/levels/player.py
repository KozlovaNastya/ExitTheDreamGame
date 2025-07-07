from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer

class Player(QWidget):
    def __init__(self, x, y, width, height, image_path, parent=None):
        super().__init__(parent)
        self.setGeometry(x, y, width, height)
        self.image = QPixmap(image_path)

        self.vx = 0
        self.vy = 0
        self.gravity = 1
        self.jump_strength = -15
        self.on_ground = False
        self.platforms = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(16)  # ~60 FPS

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
            self.vy = self.jump_strength
            self.on_ground = False

    def update_position(self):
        self.vy += self.gravity

        new_x = self.x() + self.vx
        new_y = self.y() + self.vy
        self.move(new_x, new_y)

        self.on_ground = False

        # Проверка столкновений с платформами
        for platform in self.platforms:
            if self.geometry().intersects(platform.geometry()):
                if self.vy > 0:  # Падение вниз
                    self.move(self.x(), platform.y() - self.height())
                    self.vy = 0
                    self.on_ground = True

        # Ограничения по окну
        if self.y() > self.parent().height():
            self.move(self.x(), self.parent().height() - self.height())
            self.vy = 0
            self.on_ground = True

        if self.x() < 0:
            self.move(0, self.y())
        elif self.x() + self.width() > self.parent().width():
            self.move(self.parent().width() - self.width(), self.y())
