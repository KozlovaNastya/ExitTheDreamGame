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
        # 1) Стандартный расчёт скоростей и гравитации
        self.vx = max(-self.max_speed, min(self.vx, self.max_speed))
        self.vy = max(-self.max_speed, min(self.vy, self.max_speed))
        self.vx += self.gravity_x * self.gravity
        self.vy += self.gravity_y * self.gravity

        # 2) Предсказание новых координат
        new_x = self.x() + self.vx
        new_y = self.y() + self.vy
        player_rect = QRect(new_x, new_y, self.width(), self.height())

        # 3) Смерть от шипов
        for platform in self.platforms:
            if isinstance(platform, Spikes) and player_rect.intersects(platform.geometry()):
                self.timer.stop()
                self.game.player_died()
                return

        # 4) Смерть от вылета за пределы (любое направление!)
        #    Берём «границы уровня» — родительский виджет (Level)
        lvl = self.parent()
        if (new_x <= 0 or
            new_y <= 0 or
            new_y + self.height() >= lvl.height()):
            self.timer.stop()
            self.game.player_died()
            return

        # 5) Коллизии по X (если гравитация вертикальная)
        if self.gravity_x == 0:
            rect_x = QRect(new_x, self.y(), self.width(), self.height())
            tol = 5
            for plat in self.platforms:
                pr = plat.geometry()
                if not rect_x.intersects(pr):
                    continue
                # провалились «сквозь» по Y?
                overlap_y = min(rect_x.bottom(), pr.bottom()) - max(rect_x.top(), pr.top())
                if overlap_y <= tol:
                    continue
                # настоящий боковой контакт
                if self.vx > 0:
                    new_x = pr.left() - self.width()
                else:
                    new_x = pr.right()
                self.vx = 0
                break

        # 6) Коллизии по Y
        rect_y = QRect(new_x, new_y, self.width(), self.height())
        for plat in self.platforms:
            pr = plat.geometry()
            if not rect_y.intersects(pr):
                continue
            if self.vy > 0:
                # падаем вниз — становимся на платформу
                new_y = pr.top() - self.height()
            else:
                # подлетаем вверх — упираемся в дно платформы
                new_y = pr.bottom()
            self.vy = 0
            break

        # 7) Ограничиваем движение внутри экрана
        new_x = max(0, min(new_x, lvl.width() - self.width()))
        new_y = max(0, min(new_y, lvl.height() - self.height()))
        self.move(new_x, new_y)
        print("DEATH-CHECK:", new_x, new_y, lvl.width(), lvl.height())

        # 8) Обновляем флаг on_ground
        self.on_ground = False
        pr = self.geometry()
        for plat in self.platforms:
            if self.check_on_ground(pr, plat.geometry()):
                self.on_ground = True
                break

        # 9) Проверка завершения уровня
        if hasattr(self.parent(), "check_level_complete"):
            self.parent().check_level_complete()
