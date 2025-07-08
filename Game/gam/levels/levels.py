from gam.levels.base_level import BaseLevel
from gam.levels.platforms import MovingPlatform
from gam.levels.spikes import Spikes

class LevelOne(BaseLevel):
    def __init__(self, parent=None):
        super().__init__(
            background_path="assets/background/level1.png",
            platforms_data=[
                (10, 540, 150, 60, "assets/for game/platform.png"),
                (140, 450, 150, 60, "assets/for game/platform.png"),
                (260, 370, 150, 60, "assets/for game/platform.png"),
                (360, 280, 100, 60, "assets/for game/platform.png"),
                (470, 450, 100, 60, "assets/for game/platform.png"),
                (570, 410, 80, 40, "assets/for game/platform.png"),
                (650, 450, 80, 40, "assets/for game/platform.png"),
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
                (10, 500, 200, 80, "assets/for game/platform.png"),
                (190, 500, 200, 80, "assets/for game/platform.png"),
                (150, 450, 100, 40, "assets/for game/platform.png"),
                (320, 0, 230, 80, "assets/for game/platform.png", 180),
                (520, 0, 200, 80, "assets/for game/platform.png", 180),
                (380, 200, 150, 60, "assets/for game/platform.png", 90),
                (380, 340, 150, 60, "assets/for game/platform.png", 90),
                (580, 80, 150, 60, "assets/for game/platform.png", 270),
                (580, 220, 150, 60, "assets/for game/platform.png", 270),
                (500, 500, 190, 60, "assets/for game/platform.png"),
                (650, 500, 160, 60, "assets/for game/platform.png"),
            ], 
            player_start=(20, 400, 50, 50),
            finish_line_x=750,
            parent=parent
        )
        if not hasattr(self, 'platforms'):
            self.platforms = []
        
        spikes_data = [
            (115, 465, 50, 40, "assets/for game/spikes3.png"),
            (230, 465, 50, 40, "assets/for game/spikes3.png"),
            (740, 465, 50, 40, "assets/for game/spikes3.png"),
        ]
        
        for x, y, width, height, image_path in spikes_data:
            spikes = Spikes(x, y, width, height, image_path, parent=self)
            spikes.show()
            self.platforms.append(spikes)
        
        self.player.set_platforms(self.platforms)
       

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
            platforms_data=[
                (20, 500, 120, 40, "assets/for game/platform.png"),
                (300, 360, 100, 40, "assets/for game/platform.png"),
            ],
            player_start=(20, 400, 50, 50),
            finish_line_x=750,
            parent=parent
        )

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