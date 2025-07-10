from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QTransform
import os
from gam.constants import BASE_DIR
from gam.levels.spikes import Spikes


class Player(QWidget):
    def __init__(self, x, y, width, height, image_path, parent=None, game=None):
        super().__init__(parent)
        self.game = game
        self.setGeometry(x, y, width, height)

        #
        full_path = os.path.join(BASE_DIR, image_path)
        self.image_idle = QPixmap(full_path)
        self.image_anim = QPixmap(os.path.join(BASE_DIR, "assets/for game/sprite_gravity.png"))
        self.current_pixmap = self.image_idle  # что рисовать сейчас

        self.facing_left = False
        self.original_pixmap = self.image_idle.copy()

        self.last_input_direction = 0 

        self.rotation_angle = 0  # Угол поворота изображения
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.end_animation)

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
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        if self.current_pixmap and not self.current_pixmap.isNull():
            pixmap = self.current_pixmap
            if self.facing_left:
                pixmap = pixmap.transformed(QTransform().scale(-1, 1))

            center = self.rect().center()
            painter.translate(center)
            painter.rotate(self.rotation_angle)
            painter.translate(-center)

            painter.drawPixmap(self.rect(), pixmap)
        else:
            painter.fillRect(self.rect(), Qt.GlobalColor.red)



    def move_left(self):
        self.vx = -5
        self.last_input_direction = -1
        self.update_facing_direction()
        self.play_walk_animation()

    def move_right(self):
        self.vx = 5
        self.last_input_direction = 1
        self.update_facing_direction()
        self.play_walk_animation()


    def stop_movement(self):
        self.vx = 0
        self.last_input_direction = 0 

    def jump(self):
        if self.on_ground:
            if self.gravity_y != 0:
                self.vy = -self.gravity_y * self.jump_strength
            elif self.gravity_x != 0:
                self.vx = -self.gravity_x * self.jump_strength
            self.on_ground = False
            self.update_facing_direction()
            self.play_jump_animation()



    def set_gravity_down(self):
        self.gravity_x = 0
        self.gravity_y = 1
        self.rotation_angle = 0
        self.play_gravity_animation()

    def set_gravity_up(self):
        self.gravity_x = 0
        self.gravity_y = -1
        self.rotation_angle = 180
        self.play_gravity_animation()

    def set_gravity_left(self):
        self.gravity_x = -1
        self.gravity_y = 0
        self.rotation_angle = 90
        self.play_gravity_animation()

    def set_gravity_right(self):
        self.gravity_x = 1
        self.gravity_y = 0
        self.rotation_angle = -90
        self.play_gravity_animation()


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
        if self.animation_timer and self.animation_timer.isActive():
            self.animation_timer.stop()
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
        for plat in self.platforms:
            if not plat.isVisible() or getattr(plat, '_is_disappeared', False):
                continue
            if isinstance(plat, Spikes) and player_rect.intersects(plat.geometry()):
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

        # 5 Коллизии 
        if self.gravity_y != 0:
            # Гравитация вертикальная — обрабатываем X как боковое движение
            rect_x = QRect(new_x, self.y(), self.width(), self.height())
            tol = 5
            for plat in self.platforms:
                if not plat.isVisible() or getattr(plat, '_is_disappeared', False):
                    continue
                pr = plat.geometry()
                if not rect_x.intersects(pr):
                    continue
                # Провалились «сквозь» по Y?
                overlap_y = min(rect_x.bottom(), pr.bottom()) - max(rect_x.top(), pr.top())
                if overlap_y <= tol:
                    continue
                # Настоящий боковой контакт
                if self.vx > 0:
                    new_x = pr.left() - self.width()
                else:
                    new_x = pr.right()
                self.vx = 0
                break

            # Обработка по Y — основная ось гравитации
            rect_y = QRect(new_x, new_y, self.width(), self.height())
            for plat in self.platforms:
                if not plat.isVisible() or getattr(plat, '_is_disappeared', False):
                    continue
                pr = plat.geometry()
                if not rect_y.intersects(pr):
                    continue
                if self.vy > 0:
                    new_y = pr.top() - self.height()
                else:
                    new_y = pr.bottom()
                self.vy = 0
                break


        elif self.gravity_x != 0:
            # Гравитация горизонтальная — обрабатываем Y как боковое движение
            rect_y = QRect(self.x(), new_y, self.width(), self.height())
            tol = 5
            for plat in self.platforms:
                if not plat.isVisible() or getattr(plat, '_is_disappeared', False):
                    continue
                pr = plat.geometry()
                if not rect_y.intersects(pr):
                    continue
                overlap_x = min(rect_y.right(), pr.right()) - max(rect_y.left(), pr.left())
                if overlap_x <= tol:
                    continue
                if self.vy > 0:
                    new_y = pr.top() - self.height()
                else:
                    new_y = pr.bottom()
                self.vy = 0
                break

            # Обработка по X — основная ось гравитации
            rect_x = QRect(new_x, new_y, self.width(), self.height())
            for plat in self.platforms:
                if not plat.isVisible() or getattr(plat, '_is_disappeared', False):
                    continue
                pr = plat.geometry()
                if not rect_x.intersects(pr):
                    continue
                if self.vx > 0:
                    new_x = pr.left() - self.width()
                else:
                    new_x = pr.right()
                self.vx = 0
                break

        # 7) Ограничиваем движение внутри экрана
        new_x = max(0, min(new_x, lvl.width() - self.width()))
        new_y = max(0, min(new_y, lvl.height() - self.height()))
        self.update_facing_direction()
        self.move(new_x, new_y)

        # 8) Обновляем флаг on_ground
        self.on_ground = False
        pr = self.geometry()
        for plat in self.platforms:
            if not plat.isVisible() or getattr(plat, '_is_disappeared', False):
                continue
            if self.check_on_ground(pr, plat.geometry()):
                self.on_ground = True
                break

        # 9) Проверка завершения уровня
        if hasattr(self.parent(), "check_level_complete"):
            self.parent().check_level_complete()


    def play_gravity_animation(self):
        self.current_pixmap = self.image_anim
        self.animation_timer.start(800)
        self.update()

    def play_walk_animation(self):
        pixmap = QPixmap(os.path.join(BASE_DIR, "assets/for game/sprite_run1.png"))
        if self.facing_left:
            pixmap = pixmap.transformed(QTransform().scale(-1, 1))
        self.current_pixmap = pixmap
        self.animation_timer.start(120)
        self.update()

    def play_jump_animation(self):
        pixmap = QPixmap(os.path.join(BASE_DIR, "assets/for game/sprite_jump1.png"))
        if self.facing_left:
            pixmap = pixmap.transformed(QTransform().scale(-1, 1))
        self.current_pixmap = pixmap
        self.animation_timer.start(200)
        self.update()


    def end_animation(self):
        self.current_pixmap = self.image_idle
        self.animation_timer.stop()
        self.update()

    def update_sprite_orientation(self):
        if self.gravity_direction == "down":
            self.setRotation(0)
        elif self.gravity_direction == "left":
            self.setRotation(-90)
        elif self.gravity_direction == "right":
            self.setRotation(90)
        elif self.gravity_direction == "up":
            self.setRotation(180)

    def update_facing_direction(self):
        if self.last_input_direction == 0:
            return  # Не менять направление

        if self.gravity_y != 0:
            # Вертикальная гравитация — движение по X (влево/вправо)
            self.facing_left = self.last_input_direction < 0
        elif self.gravity_x != 0:
            # Горизонтальная гравитация — движение по Y (вверх/вниз)
            if self.gravity_x > 0:
                # Гравитация вправо
                self.facing_left = self.last_input_direction < 0
            else:
                # Гравитация влево
                self.facing_left = self.last_input_direction > 0


