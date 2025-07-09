# -*- coding: utf-8 -*-
import sys
import os
import json
from PyQt6.QtWidgets import (QMainWindow, QApplication, QMessageBox, 
                            QDialog, QVBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QComboBox, QSlider, QHBoxLayout, QWidget)
from PyQt6.QtGui import (QPainter, QPixmap, QFont, QColor, QPen, 
                         QBrush, QFontDatabase, QLinearGradient)
from PyQt6.QtCore import Qt, QRect, QTimer, pyqtSignal

DIALOG_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #2a0845, stop:1 #7a1a5a);
        color: #ffffff;
        font-family: 'Minecraft';
    }
    QLabel {
        color: #ffffff;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #5a2a75, stop:1 #9a3a7a);
        color: white;
        border: 2px solid #ba5a9a;
        border-radius: 3px;
        padding: 5px 10px;
        font-family: 'Minecraft';
        font-weight: bold;
        min-width: 80px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #6a3a85, stop:1 #aa4a8a);
        border: 2px solid #da7aba;
    }
"""

class ConfirmDialog(QDialog):
    def __init__(self, parent=None, message="", confirm_text="Confirm"):
        super().__init__(parent)
        self.setWindowTitle("Confirmation")
        self.setFixedSize(350, 150)
        self.setStyleSheet(DIALOG_STYLE)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message_label)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.confirm_button = QPushButton(confirm_text)
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.confirm_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(500, 350)
        self.setStyleSheet(DIALOG_STYLE + """
            QComboBox, QSlider {
                background: rgba(40, 10, 60, 180);
                border: 2px solid #9a3a7a;
                border-radius: 2px;
                padding: 5px;
                min-height: 25px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.volume_label = QLabel("Audio Volume:")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)
        
        self.quality_label = QLabel("Graphics Quality:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["Low", "Medium", "High", "Ultra"])
        layout.addWidget(self.quality_label)
        layout.addWidget(self.quality_combo)
        
        self.controls_label = QLabel("Control Scheme:")
        self.controls_combo = QComboBox()
        self.controls_combo.addItems(["Arrow Keys", "WASD"])
        layout.addWidget(self.controls_label)
        layout.addWidget(self.controls_combo)
        
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

class LeaderboardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Leaderboard")
        self.setFixedSize(600, 450)
        self.setStyleSheet(DIALOG_STYLE + """
            QTableWidget {
                background: rgba(40, 10, 60, 180);
                border: 2px solid #9a3a7a;
                gridline-color: #7a2a65;
                font-size: 14px;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a2a75, stop:1 #9a3a7a);
                padding: 5px;
                border: 1px solid #ba5a9a;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("TOP 10")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #ff66cc;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Rank", "Player", "Score"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
        self.load_leaderboard()
        layout.addWidget(self.table)
        
        self.close_button = QPushButton("Close")
        self.close_button.setFixedSize(120, 35)
        layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        self.close_button.clicked.connect(self.close)
    
    def load_leaderboard(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            leaderboard_path = os.path.join(base_path, "leaderboard.json")
            
            if os.path.exists(leaderboard_path):
                with open(leaderboard_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                data.sort(key=lambda x: x['score'], reverse=True)
                top_10 = data[:10]
                
                self.table.setRowCount(len(top_10))
                for row, entry in enumerate(top_10):
                    self.add_table_row(row, entry)
                
                self.table.setColumnWidth(0, 80)
                self.table.setColumnWidth(1, 250)
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
    
    def add_table_row(self, row, entry):
        """Helper method to add a row to the table with proper formatting"""
        rank_item = QTableWidgetItem(str(row+1))
        player_item = QTableWidgetItem(entry['player'])
        score_item = QTableWidgetItem(str(entry['score']))
        
        for item in [rank_item, player_item, score_item]:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
       
        if row == 0:
            color = QColor(255, 215, 0)
        elif row == 1:
            color = QColor(192, 192, 192)
        elif row == 2:
            color = QColor(205, 127, 50)
        else:
            color = QColor(255, 255, 255)
            
        for item in [rank_item, player_item, score_item]:
            item.setForeground(color)
        
        self.table.setItem(row, 0, rank_item)
        self.table.setItem(row, 1, player_item)
        self.table.setItem(row, 2, score_item)

class MainMenu(QMainWindow):
    start_game_signal = pyqtSignal(int, str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exit the Dream - Main Menu")
        self.setFixedSize(800, 600)
        
        self.current_level = 1
        self.player_name = "Player"
        self.scores = []
        
        self.init_resources()
        self.load_scores()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)
        
        self.hovered_button = None
        self.pressed_button = None
    
    def init_resources(self):
        """Initialize all graphical resources"""
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.normpath(os.path.join(self.base_path, "..", "assets"))
        
        font_path = os.path.join(self.assets_path, "fonts", "Minecraft.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
        
        self.background = self.create_background()
        
        self.logo = self.create_logo()
        
        self.init_buttons()
    
    def create_background(self):
        """Create background image, either from file or gradient"""
        bg_path = os.path.join(self.assets_path, "background", "level0.png")
        if os.path.exists(bg_path):
            bg = QPixmap(bg_path)
            if not bg.isNull():
                bg = bg.scaled(800, 600, 
                             Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                             Qt.TransformationMode.SmoothTransformation)
                return bg.copy((bg.width()-800)//2, (bg.height()-600)//2, 800, 600)
        
        bg = QPixmap(800, 600)
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0, QColor(42, 8, 69))
        gradient.setColorAt(1, QColor(122, 26, 90))
        bg.fill(gradient)
        return bg
    
    def create_logo(self):
        """Create logo image, either from file or generated"""
        logo_path = os.path.join(self.assets_path, "for game", "gameOver.png")
        if os.path.exists(logo_path):
            logo = QPixmap(logo_path)
            if not logo.isNull():
                return logo.scaledToHeight(120, Qt.TransformationMode.SmoothTransformation)
        
        logo = QPixmap(400, 100)
        logo.fill(Qt.GlobalColor.transparent)
        painter = QPainter(logo)
        painter.setFont(QFont("Minecraft", 32, QFont.Weight.Bold))
        
        painter.setPen(QColor(0, 0, 0, 150))
        painter.drawText(logo.rect().translated(2, 2), Qt.AlignmentFlag.AlignCenter, "EXIT THE DREAM")
        
        painter.setPen(QColor(255, 102, 204))
        painter.drawText(logo.rect(), Qt.AlignmentFlag.AlignCenter, "EXIT THE DREAM")
        painter.end()
        return logo
    
    def init_buttons(self):
        """Initialize menu buttons"""
        self.button_texts = {
            "start": "START",
            "restart": "RESTART",
            "options": "OPTIONS",
            "leaderboard": "LEADERBOARD",
            "exit": "EXIT"
        }
        
        self.hover_colors = {
            "start": QColor(100, 255, 100, 150),
            "exit": QColor(255, 80, 80, 150),
            "restart": QColor(255, 220, 100, 150),
            "leaderboard": QColor(200, 100, 255, 150),
            "options": QColor(100, 180, 255, 150)
        }
        
        btn_width, btn_height = 220, 45
        start_x = (800 - btn_width) // 2
        start_y = 280
        btn_spacing = 55
        
        self.button_rects = {
            "start": QRect(start_x, start_y, btn_width, btn_height),
            "restart": QRect(start_x, start_y + btn_spacing, btn_width, btn_height),
            "options": QRect(start_x, start_y + 2*btn_spacing, btn_width, btn_height),
            "leaderboard": QRect(start_x, start_y + 3*btn_spacing, btn_width, btn_height),
            "exit": QRect(start_x, start_y + 4*btn_spacing, btn_width, btn_height)
        }
        
        self.button_states = {}
        for btn in self.button_texts:
            self.button_states[btn] = {
                "normal": self.create_button_pixmap(btn, False),
                "pressed": self.create_button_pixmap(btn, True)
            }
    
    def create_button_pixmap(self, btn_key, pressed=False):
        """Create a button pixmap in specified state"""
        btn_width, btn_height = 220, 45
        pixmap = QPixmap(btn_width, btn_height)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        self.draw_button(painter, QRect(0, 0, btn_width, btn_height), 
                        self.button_texts[btn_key], pressed)
        painter.end()
        
        return pixmap
    
    def draw_button(self, painter, rect, text, pressed=False):
        """Draw a button with the specified state"""
        if pressed:
            rect = rect.translated(0, 2)
        
        gradient = QLinearGradient(0, 0, rect.width(), rect.height())
        if pressed:
            gradient.setColorAt(0, QColor(70, 30, 80))
            gradient.setColorAt(1, QColor(120, 50, 110))
            border_color = QColor(100, 50, 90)
        else:
            gradient.setColorAt(0, QColor(90, 40, 100))
            gradient.setColorAt(1, QColor(150, 70, 140))
            border_color = QColor(90, 40, 100)
        
        painter.setPen(QPen(border_color, 3))
        painter.setBrush(QBrush(gradient))
        painter.drawRect(rect)
        
        painter.setFont(QFont("Minecraft", 12, QFont.Weight.Bold))
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
    
    def paintEvent(self, event):
        """Main painting event"""
        painter = QPainter(self)
        
        painter.drawPixmap(0, 0, self.background)
        
        if not self.logo.isNull():
            logo_x = (800 - self.logo.width()) // 2
            painter.drawPixmap(logo_x, 100, self.logo)
        
        self.draw_buttons(painter)
    
    def draw_buttons(self, painter):
        """Draw all menu buttons"""
        cursor_pos = self.mapFromGlobal(self.cursor().pos())
        
        for btn, rect in self.button_rects.items():
            is_pressed = self.pressed_button == btn
            is_hovered = rect.contains(cursor_pos)
            
            state = "pressed" if is_pressed else "normal"
            painter.drawPixmap(rect, self.button_states[btn][state])
            
            if is_hovered and not is_pressed:
                hover_color = self.hover_colors.get(btn, QColor(255, 255, 255, 30))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(hover_color))
                painter.drawRect(rect.adjusted(-2, -2, 2, 2))
    
    def mousePressEvent(self, event):
        """Handle mouse press on buttons"""
        for btn, rect in self.button_rects.items():
            if rect.contains(event.pos()):
                self.pressed_button = btn
                self.update()
                break
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release and button clicks"""
        if self.pressed_button:
            btn = self.pressed_button
            if self.button_rects[btn].contains(event.pos()):
                self.handle_button_click(btn)
            self.pressed_button = None
            self.update()
    
    def handle_button_click(self, button):
        """Route button clicks to appropriate handlers"""
        handlers = {
            "start": self.start_game,
            "exit": self.confirm_exit,
            "options": self.show_options,
            "leaderboard": self.show_leaderboard,
            "restart": self.confirm_restart
        }
        handlers.get(button, lambda: None)()
    
    def start_game(self):
        """Emit signal to start the game"""
        self.start_game_signal.emit(self.current_level, self.player_name)
    
    def confirm_restart(self):
        """Show restart confirmation dialog"""
        dialog = ConfirmDialog(
            self,
            "Are you sure you want to restart?\nAll progress will be lost.",
            "Restart"
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.current_level = 1
            self.start_game_signal.emit(1, self.player_name)
    
    def confirm_exit(self):
        """Show exit confirmation dialog"""
        dialog = ConfirmDialog(
            self,
            "Are you sure you want to exit the game?",
            "Exit"
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            QApplication.quit()
    
    def show_options(self):
        """Show options dialog"""
        dialog = SettingsDialog(self)
        dialog.exec()
    
    def show_leaderboard(self):
        """Show leaderboard dialog"""
        dialog = LeaderboardDialog(self)
        dialog.exec()
    
    def load_scores(self):
        """Load scores from leaderboard file"""
        try:
            leaderboard_path = os.path.join(self.base_path, "leaderboard.json")
            if os.path.exists(leaderboard_path):
                with open(leaderboard_path, 'r', encoding='utf-8') as f:
                    self.scores = json.load(f)
        except Exception as e:
            print(f"Error loading scores: {e}")
            self.scores = []

if __name__ == "__main__":
    app = QApplication(sys.argv)

    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    menu = MainMenu()

    def handle_start(level, name):
        print(f"Starting game: level {level}, player {name}")
        game = Game()
        game.resize(800, 600)
        game.show()
        menu.hide()

    menu.start_game_signal.connect(handle_start)
    menu.show()
    sys.exit(app.exec())
