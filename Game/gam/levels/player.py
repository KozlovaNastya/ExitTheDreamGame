from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer

class Player(QWidget):
    def __init__(self, x, y, width, height, image_path, parent=None):
        super().__init__(parent)
        self.setGeometry(x, y, width, height)
        self.image = QPixmap(image_path)

        self.vx = 0  # Горизонтальная скорость
        self.vy = 0  # Вертикальная скорость
        self.gravity = 1  # Сила гравитации
        self.jump_strength = -15  # Сила прыжка
        self.on_ground = False

        # Таймер обновления позиции
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(16)  # ~60 FPS

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
        # Гравитация
        self.vy += self.gravity

        # Движение
        new_x = self.x() + self.vx
        new_y = self.y() + self.vy

        # Обновляем позицию
        self.move(new_x, new_y)

        # Границы окна (можно убрать или изменить)
        if self.y() > self.parent().height():
            self.move(self.x(), self.parent().height() - self.height())
            self.vy = 0
            self.on_ground = True
