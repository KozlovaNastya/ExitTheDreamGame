from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer, QRect
import os
from gam.constants import BASE_DIR
from gam.levels.spikes import Spikes

class Player(QWidget):
    def __init__(self, x, y, width, height, image_path, parent=None, game=None):
        super().__init__(parent)
        self.game = game
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
        self.max_speed = 20

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
            self.vy = -self.gravity_y * self.jump_strength
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

    def deleteLater(self):
        if self.timer and self.timer.isActive():
            self.timer.stop()
        super().deleteLater()

    def update_position(self):
        self.vx = max(-self.max_speed, min(self.vx, self.max_speed))
        self.vy = max(-self.max_speed, min(self.vy, self.max_speed))
        # 1) Гравитация + интегрирование скоростей
        self.vx += self.gravity_x * self.gravity
        self.vy += self.gravity_y * self.gravity

        # 2) Предсказание новых координат
        new_x = self.x() + self.vx
        new_y = self.y() + self.vy

        player_rect = QRect(new_x, new_y, self.width(), self.height())
        for platform in self.platforms:
            if isinstance(platform, Spikes) and player_rect.intersects(platform.geometry()):
                # Сообщаем игре, что игрок умер (Game должен позаботиться о перезагрузке уровня)
                if self.game is not None:
                    self.timer.stop()  # Останавливаем таймер, чтобы избежать гонок
                    self.game.player_died()
                return



        # 3) Проверка столкновений по X
        if self.gravity_x == 0:  # блокировка по X только для вертикальной гравитации
            rect_x = QRect(new_x, self.y(), self.width(), self.height())
            tolerance_y = 5
            for platform in self.platforms:
                 plat_rect = platform.geometry()
                 if not rect_x.intersects(plat_rect):
                     continue
                 # вычисляем реальное вертикальное перекрытие
                 overlap_y = min(rect_x.bottom(), plat_rect.bottom()) - max(rect_x.top(), plat_rect.top())
                 if overlap_y <= tolerance_y:
                     # это касание “потолка” или лишь граничное — игнорируем
                     continue
                 # настоящий боковой контакт, блокируем
                 if self.vx > 0:   # идём вправо
                     new_x = plat_rect.left() - self.width()
                 elif self.vx < 0: # идём влево
                     new_x = plat_rect.right()
                 self.vx = 0
                 break

                # 4) Проверка столкновений по Y
        rect_y = QRect(new_x, new_y, self.width(), self.height())
        landed = False
        for platform in self.platforms:
            plat_rect = platform.geometry()
            if rect_y.intersects(plat_rect):
                if self.vy > 0:   # идём вниз
                    new_y = plat_rect.top() - self.height()
                    landed = True
                elif self.vy < 0: # идём вверх
                    new_y = plat_rect.bottom()
                self.vy = 0
                break

        # 5) Применяем перемещение — ВНЕ цикла
        new_x = max(0, min(new_x, self.parent().width() - self.width()))
        new_y = max(0, min(new_y, self.parent().height() - self.height()))

        self.move(new_x, new_y)

        # 6) Границы окна
        if new_y > self.parent().height() or new_y + self.height() < 0:
            if self.game is not None:
                self.game.player_died()
            return

        if new_x < 0:
            self.move(0, new_y);  self.vx = 0
        elif new_x + self.width() > self.parent().width():
            self.move(self.parent().width() - self.width(), new_y);  self.vx = 0

        # 7) Обновляем on_ground универсально
        self.on_ground = False
        player_rect = self.geometry()
        for platform in self.platforms:
            if self.check_on_ground(player_rect, platform.geometry()):
                self.on_ground = True
                break

        # 8) Проверка завершения уровня
        if hasattr(self.parent(), "check_level_complete"):
            self.parent().check_level_complete()

