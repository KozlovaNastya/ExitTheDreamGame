from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

DIALOG_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #2a0845, stop:1 #7a1a5a);
        color: #ffffff;
        font-family: 'Minecraft';
    }
    QLabel {
        color: #ffffff;
        font-size: 20px;
        font-weight: bold;
    }
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #5a2a75, stop:1 #9a3a7a);
        color: white;
        border: 2px solid #ba5a9a;
        border-radius: 5px;
        padding: 12px 24px;
        font-family: 'Minecraft';
        font-size: 18px;
        font-weight: bold;
        min-width: 200px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #6a3a85, stop:1 #aa4a8a);
        border: 2px solid #da7aba;
    }
"""

class StoryDialog(QDialog):
    def __init__(self, story_text, controls_text, 
                 story_alignment=Qt.AlignmentFlag.AlignLeft, 
                 controls_alignment=Qt.AlignmentFlag.AlignLeft,
                 parent=None):
        super().__init__(parent)
        self.setWindowTitle("Story & Controls")
        self.setFixedSize(600, 500)
        self.setModal(True)
        self.setStyleSheet(DIALOG_STYLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Story
        story_label = QLabel(story_text)
        story_label.setWordWrap(True)
        story_label.setAlignment(story_alignment)
        layout.addWidget(story_label)

        # Controls
        controls_label = QLabel(controls_text)
        controls_label.setWordWrap(True)
        controls_label.setAlignment(controls_alignment)
        layout.addWidget(controls_label)

        # Button
        btn_close = QPushButton("Start Level")
        btn_close.clicked.connect(self.accept)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignCenter)
