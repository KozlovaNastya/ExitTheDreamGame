from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt
from gam.constants import BASE_DIR
import os

class Platform(QWidget):
    def __init__(self, x, y, width, height, image_path=None, parent=None):
        super().__init__(parent)
        self.setGeometry(x, y, width, height)
        if image_path:      
            full_path = os.path.join(BASE_DIR, image_path)
            self.image = QPixmap(full_path)
        else:
            self.image = None

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.image and not self.image.isNull():
            scaled_pixmap = self.image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
        else:
            painter.fillRect(self.rect(), Qt.GlobalColor.darkGray)
