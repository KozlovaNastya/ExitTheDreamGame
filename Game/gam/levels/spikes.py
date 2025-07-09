from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt
import os
from gam.constants import BASE_DIR

class Spikes(QWidget):
    def __init__(self, x, y, width, height, image_path=None, parent=None):
        super().__init__(parent)
        self.setGeometry(x, y, width, height)
        
        # �������� ������� �����������
        if image_path:
            full_path = os.path.join(BASE_DIR, image_path)
            if os.path.exists(full_path):
                self.image = QPixmap(full_path)
            else:
                print(f"Spikes image not found: {full_path}")
                self.image = None
        else:
            self.image = None

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.image and not self.image.isNull():
            painter.drawPixmap(self.rect(), self.image)
        else:
            painter.fillRect(self.rect(), Qt.GlobalColor.red)