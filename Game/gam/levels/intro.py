# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont

DIALOG_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #2a0845, stop:1 #7a1a5a);
        color: #ffffff;
        font-family: 'Minecraft';
        border: 2px solid #ba5a9a;
        border-radius: 10px;
    }
    QLabel {
        color: #ffffff;
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
        margin: 5px;
    }
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #5a2a75, stop:1 #9a3a7a);
        color: white;
        border: 2px solid #ba5a9a;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        min-width: 150px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #6a3a85, stop:1 #aa4a8a);
    }
"""

class StoryDialog(QDialog):
    def __init__(self, story_text, controls_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Story & Controls")
        self.setModal(True)
        self.setStyleSheet(DIALOG_STYLE)

        if parent:
            self.setFixedSize(parent.width() * 0.8, parent.height() * 0.7)
        else:
            self.setFixedSize(600, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.story_label = QLabel(story_text)
        self.story_label.setWordWrap(True)
        self.story_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.story_label)

        controls_html = """
        <div style='font-size: 16px;'>
            <b>Controls:</b><br>
            🡄 🡆 <b>Move</b> (or WASD)<br>
            <span style='color: #FFD700;'>[Space]</span> <b>Jump</b><br>
            <span style='color: #FF6347;'>1/2</span> <b>Gravity Down/Up</b><br>
            <span style='color: #FF6347;'>3/4</span> <b>Gravity Left/Right</b>
        </div>
        """
        self.controls_label = QLabel(controls_html)
        self.controls_label.setWordWrap(True)
        self.controls_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.controls_label)

        self.btn_close = QPushButton("Start Level")
        self.btn_close.clicked.connect(self.accept)
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.btn_close, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setWindowOpacity(0.0)
        self.fade_in()

    def fade_in(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()