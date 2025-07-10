from gam.levels.base_level import BaseLevel
from gam.levels.platforms import MovingPlatform, DisappearingPlatform, create_platform_from_data
from gam.levels.spikes import Spikes

class LevelOne(BaseLevel):
    def __init__(self, parent=None,  game=None):
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
            player_start=(20, 400, 35, 50),
            finish_line_x=750,
            parent=parent,
            game=game
        )

class LevelTwo(BaseLevel):
    def __init__(self, parent=None,  game=None):
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
            player_start=(20, 400, 35, 50),
            finish_line_x=750,
            parent=parent,
            game=game
        )
        if not hasattr(self, 'platforms'):
            self.platforms = []
        
        spikes_data = [
            (115, 465, 70, 65, "assets/for game/spikes3.png", 0),
            (220, 465, 70, 65, "assets/for game/spikes3.png", 0),
            (730, 460, 70, 70, "assets/for game/spikes3.png", 0),
        ]
        
        for x, y, width, height, image_path, rotation in spikes_data:
            spikes = Spikes(x, y, width, height, image_path, rotation, parent=self)
            spikes.show()
            self.platforms.append(spikes)
        
        self.player.set_platforms(self.platforms)
       

class LevelThree(BaseLevel):
    def __init__(self, parent=None, game=None):
        super().__init__(
            background_path="assets/background/level3.png",
            platforms_data=[
                (40, 550, 120, 40, "assets/for game/platform.png"),
                (4, 450, 100, 40, "assets/for game/platform.png", 90),
                (80, 350, 100, 40, "assets/for game/platform.png", 90),
                (80, 270, 100, 40, "assets/for game/platform.png", 90),
                (120, 140, 100, 40, "assets/for game/platform.png", 90),
                (140, 10, 100, 40, "assets/for game/platform.png", 180),
                (235, 10, 100, 40, "assets/for game/platform.png", 180),
                (330, 10, 100, 40, "assets/for game/platform.png", 180),
                (290, 130, 150, 60, "assets/for game/platform.png", 270),
                (290, 250, 150, 60, "assets/for game/platform.png", 270),
                (290, 380, 150, 60, "assets/for game/platform.png", 270),
                (290, 510, 150, 60, "assets/for game/platform.png", 270),
                (400, 500, 100, 40, "assets/for game/platform.png"),
                (450, 300, 100, 40, "assets/for game/platform.png"),
                (550, 400, 100, 40, "assets/for game/platform.png"),
                (760, 300, 100, 40, "assets/for game/platform.png", 270),
            ],
            player_start=(80, 500, 35, 50),
            finish_line_x=750,
            parent=parent,
            game=game
        )

        if not hasattr(self, 'platforms'):
            self.platforms = []
        
        spikes_data = [
            (245, 145, 150, 70, "assets/for game/spikes.png", 270),
            (245, 295, 150, 70, "assets/for game/spikes.png", 270),
            (245, 445, 150, 70, "assets/for game/spikes.png", 270),
        ]
        
        for x, y, width, height, image_path, rotation in spikes_data:
            spikes = Spikes(x, y, width, height, image_path, rotation, parent=self)
            spikes.show()
            self.platforms.append(spikes)

class LevelFour(BaseLevel):
    def __init__(self, parent=None,  game=None):
        super().__init__(
            background_path="assets/background/level4.png",
            platforms_data=[
                (20, 500, 120, 50, "assets/for game/platform.png"),
                (280, 180, 120, 50, "assets/for game/platform.png"),
                (520, 0, 120, 50, "assets/for game/platform.png", 270),
                (520, 110, 120, 50, "assets/for game/platform.png", 270),
                (520, 220, 120, 50, "assets/for game/platform.png", 270),
                (520, 330, 120, 50, "assets/for game/platform.png", 270),
            ],
            player_start=(20, 400, 35, 50),
            finish_line_x=750,
            parent=parent,
            game=game
        )

        moving_platform1 = MovingPlatform(
            x=170, y=420, width=120, height=50,
            image_path="assets/for game/platform.png",
            speed=1,
            move_range_y=(220, 480),
            parent=self
        )
        self.platforms.append(moving_platform1)
        moving_platform1.show()

        moving_platform2 = MovingPlatform(
            x=540, y=550, width=120, height=50,
            image_path="assets/for game/platform.png",
            speed=1,
            move_range_x=(430, 700),
            parent=self
        )
        self.platforms.append(moving_platform2)
        moving_platform2.show()
        self.player.set_platforms(self.platforms)
        
        spikes_data = [
            (485, 30, 70, 60, "assets/for game/spikes3.png", 270),
            (500, 322, 55, 30, "assets/for game/spikes3.png", 270),
        ]
        
        for x, y, width, height, image_path, rotation in spikes_data:
            spikes = Spikes(x, y, width, height, image_path, rotation, parent=self)
            spikes.show()
            self.platforms.append(spikes)

       
class LevelFive(BaseLevel):
    def __init__(self, parent=None, game=None):
        super().__init__(
            background_path="assets/background/level5.png",
            platforms_data=[
                (20, 500, 120, 50, "assets/for game/platform.png", 0, 3000),
                (200, 480, 120, 50, "assets/for game/platform.png", 0, 3000),
                (320, 420, 120, 50, "assets/for game/platform.png", 0, 5000),
                (190, 100, 120, 50, "assets/for game/platform.png", 180, 7000),
                (10, 300, 120, 50, "assets/for game/platform.png", 90, 7000),
            ],
            player_start=(20, 450, 35, 50),
            finish_line_x=750,
            parent=parent,
            game=game
        )

        # Инициализация platforms уже выполнена в BaseLevel
        
        moving_platform1 = MovingPlatform(
            x=600, y=500, width=120, height=50,
            image_path="assets/for game/platform.png",
            speed=1,
            move_range_y=(100, 600),
            rotation=270,
            parent=self
        )
        self.platforms.append(moving_platform1)
        moving_platform1.show()

        moving_platform2 = MovingPlatform(
            x=700, y=200, width=120, height=50,
            image_path="assets/for game/platform.png",
            speed=1,
            move_range_y=(10, 500),
            rotation=270,
            parent=self
        )
        self.platforms.append(moving_platform2)
        moving_platform2.show()

        spikes1 = Spikes(
            x=520, y=450, width=150, height=70,
            image_path="assets/for game/spikes.png",
            rotation=270,
            parent=self
        )
        spikes1.show()
        self.platforms.append(spikes1)
        spikes2 = Spikes(
            x=520, y=10, width=150, height=70,
            image_path="assets/for game/spikes.png",
            rotation=270,
            parent=self
        )
        spikes2.show()
        self.platforms.append(spikes2)

        spikes3 = Spikes(
            x=530, y=160, width=70, height=50,
            image_path="assets/for game/spikes3.png",
            rotation=270,
            parent=self
        )
        spikes3.show()
        self.platforms.append(spikes3)

        if hasattr(self, 'player') and self.player:
            self.player.set_platforms(self.platforms)