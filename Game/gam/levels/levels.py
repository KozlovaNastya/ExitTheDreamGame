from gam.levels.base_level import BaseLevel
from gam.levels.platforms import MovingPlatform

class LevelOne(BaseLevel):
    def __init__(self, parent=None):
        super().__init__(
            background_path="assets/background/level1.png",
            platforms_data=[
                (10, 500, 100, 40, "assets/for game/platform.png"),
                (110, 450, 80, 40, "assets/for game/platform.png"),
                (190, 390, 80, 40, "assets/for game/platform.png"),
                (290, 350, 80, 40, "assets/for game/platform.png"),
                (390, 270, 80, 40, "assets/for game/platform.png"),
                (470, 350, 80, 40, "assets/for game/platform.png"),
                (550, 350, 80, 40, "assets/for game/platform.png"),
                (640, 400, 100, 40, "assets/for game/platform.png"),
            ],
            player_start=(20, 400, 50, 50),
            finish_line_x=750,
            parent=parent
        )

class LevelTwo(BaseLevel):
    def __init__(self, parent=None):
        super().__init__(
            background_path="assets/background/level2.png",
            platforms_data=[
                (20, 500, 120, 40, "assets/for game/platform.png"),
                (160, 430, 100, 40, "assets/for game/platform.png"),
                (300, 360, 100, 40, "assets/for game/platform.png"),
                (300, 200, 100, 40, "assets/for game/platform.png"),
                (500, 100, 100, 40, "assets/for game/platform.png"),
                (620, 400, 100, 40, "assets/for game/platform.png"),
            ],
            player_start=(20, 400, 50, 50),
            finish_line_x=750,
            parent=parent
        )

class LevelThree(BaseLevel):
    def __init__(self, parent=None):
        super().__init__(
            background_path="assets/background/level3.png",
            platforms_data=[
                (20, 500, 120, 40, "assets/for game/platform.png"),
                (160, 430, 100, 40, "assets/for game/platform.png"),
                (300, 360, 100, 40, "assets/for game/platform.png"),
                (400, 320, 100, 40, "assets/for game/platform.png"),
                (500, 280, 100, 40, "assets/for game/platform.png"),
                (680, 240, 100, 40, "assets/for game/platform.png"),
            ],
            player_start=(20, 400, 50, 50),
            finish_line_x=750,
            parent=parent
        )

class LevelFour(BaseLevel):
    def __init__(self, parent=None):
        super().__init__(
            background_path="assets/background/level4.png",
            platforms_data=[  # статичные платформы
                (20, 500, 120, 40, "assets/for game/platform.png"),
                (300, 360, 100, 40, "assets/for game/platform.png"),
            ],
            player_start=(20, 400, 50, 50),
            finish_line_x=750,
            parent=parent
        )

        # Добавляем движущуюся платформу отдельно
        moving_platform1 = MovingPlatform(
            x=160, y=430, width=100, height=40,
            image_path="assets/for game/platform.png",
            speed=1,
            move_range=(150, 450),
            parent=self
        )
        self.platforms.append(moving_platform1)
        moving_platform1.show()

        moving_platform2 = MovingPlatform(
            x=570, y=430, width=100, height=40,
            image_path="assets/for game/platform.png",
            speed=1,
            move_range=(470, 700),
            parent=self
        )
        self.platforms.append(moving_platform2)
        moving_platform2.show()


        # Обновляем платформы у игрока, чтобы он знал и о движущейся
        self.player.set_platforms(self.platforms)


class LevelFive(BaseLevel):
    def __init__(self, parent=None):
        super().__init__(
            background_path="assets/background/level3.png",
            platforms_data=[
                (20, 500, 120, 40, "assets/for game/platform.png"),
                (160, 430, 100, 40, "assets/for game/platform.png"),
                (300, 360, 100, 40, "assets/for game/platform.png"),
                (400, 320, 100, 40, "assets/for game/platform.png"),
                (500, 280, 100, 40, "assets/for game/platform.png"),
                (680, 240, 100, 40, "assets/for game/platform.png"),
            ],
            player_start=(20, 400, 50, 50),
            finish_line_x=750,
            parent=parent
        )