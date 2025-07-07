from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from platforms import Platform

class LevelOne(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 600)
        self.background = QPixmap("assets/background/level1.png")

        platform = Platform(100, 500, 200, 40, "assets/for game/platform.png", parent=self)
        platform.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)