# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QDialog, QVBoxLayout, 
    QLabel, QLineEdit, QPushButton, QTableWidget, 
    QTableWidgetItem, QComboBox, QSlider, QHBoxLayout, 
    QWidget, QHeaderView
)
from PyQt6.QtGui import (
    QPainter, QPixmap, QFont, QColor, QPen, 
    QBrush, QFontDatabase, QLinearGradient
)
from PyQt6.QtCore import Qt, QRect, QTimer, pyqtSignal

def get_leaderboard_path():
    base_dir = Path(__file__).parent.parent
    return base_dir / "leaderboard.json"

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
        self.audio_manager = parent.audio_manager
        self.setWindowTitle("Settings")
        self.setFixedSize(500, 400)
        
        self.setStyleSheet("""
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
                margin-bottom: 5px;
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
            QComboBox {
                background: rgba(60, 20, 80, 220);
                border: 2px solid #9a3a7a;
                border-radius: 3px;
                padding: 8px 35px 8px 10px;
                min-height: 30px;
                margin-bottom: 15px;
                font-family: 'Minecraft';
                color: white;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 30px;
                border-left: 1px solid #7a2a65;
            }
            QComboBox::down-arrow {
                image: none;
                font-family: 'Arial';
                font-size: 16px;
                content: "...";
                color: white;
                padding-right: 10px;
            }
            QComboBox QAbstractItemView {
                background: rgba(50, 15, 70, 255);
                border: 2px solid #9a3a7a;
                selection-background-color: #7a2a65;
                selection-color: white;
                outline: none;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item {
                height: 28px;
                padding: 0 10px;
                border-bottom: 1px solid #5a2a75;
            }
            QSlider {
                margin: 10px 0 15px 0;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #4a1a6a;
                border-radius: 3px;
                border: 1px solid #7a3a8a;
            }
            QSlider::handle:horizontal {
                width: 16px;
                height: 16px;
                margin: -5px 0;
                background: qradialgradient(
                    cx:0.5, cy:0.5, radius:0.5,
                    fx:0.5, fy:0.5, 
                    stop:0 #ba5a9a, stop:1 #9a3a7a
                );
                border: 1px solid #da7aba;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 20)
        layout.setSpacing(10)
        
        self.volume_label = QLabel("Audio Volume:")
        layout.addWidget(self.volume_label)
        
        slider_container = QWidget()
        slider_layout = QHBoxLayout(slider_container)
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.setSpacing(15)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        
        self.volume_value = QLabel("80")
        self.volume_value.setFixedWidth(40)
        self.volume_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.volume_value.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        slider_layout.addWidget(self.volume_slider)
        slider_layout.addWidget(self.volume_value)
        layout.addWidget(slider_container)
        
        self.quality_label = QLabel("Graphics Quality:")
        layout.addWidget(self.quality_label)
        
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["Low", "Medium", "High", "Ultra"])
        layout.addWidget(self.quality_combo)
        
        self.controls_label = QLabel("Control Scheme:")
        layout.addWidget(self.controls_label)
        
        self.controls_combo = QComboBox()
        self.controls_combo.addItems(["Arrow Keys", "WASD"])
        layout.addWidget(self.controls_combo)
        
        layout.addStretch()
        
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(60)
        
        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(120, 35)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(120, 35)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        
        layout.addWidget(button_container)
        self.setLayout(layout)
        
        self.initial_volume = int(self.audio_manager.music_output.volume() * 100)
        self.initial_quality = self.audio_manager.graphics_quality
        
        self.volume_slider.setValue(self.initial_volume)
        self.volume_value.setText(str(self.initial_volume))
        self.quality_combo.setCurrentText(self.initial_quality)
        self.controls_combo.setCurrentText(self.audio_manager.control_scheme)
        
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.on_cancel)
    
    def on_volume_changed(self, value):
        self.volume_value.setText(str(value))
        if self.audio_manager:
            self.audio_manager.set_volume(value)
    
    def on_cancel(self):
        if self.audio_manager:
            self.audio_manager.set_volume(self.initial_volume)
            self.audio_manager.graphics_quality = self.initial_quality
        self.reject()
    
    def accept(self):
        if self.audio_manager:
            self.audio_manager.set_volume(self.volume_slider.value())
            self.audio_manager.graphics_quality = self.quality_combo.currentText()
            self.audio_manager.control_scheme = self.controls_combo.currentText()
            self.save_settings()
        super().accept()

    def save_settings(self):
        settings = {
            'volume': self.volume_slider.value(),
            'quality': self.quality_combo.currentText(),
            'controls': self.controls_combo.currentText()
        }
        
        try:
            settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
            with open(settings_path, 'w') as f:
                json.dump(settings, f)
        except Exception:
            pass

class LeaderboardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Leaderboard")
        self.setFixedSize(600, 450)
        self.setStyleSheet(self.get_dialog_style())
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title = QLabel("TOP DREAMERS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #ff66cc;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 15px;
            }
        """)
        layout.addWidget(title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Rank", "Player", "Score"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet(self.get_table_style())
        layout.addWidget(self.table)
        
        close_btn = QPushButton("Close")
        close_btn.setFixedSize(120, 40)
        close_btn.setStyleSheet(self.get_button_style())
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.load_leaderboard()

    def load_leaderboard(self):
        try:
            leaderboard_path = get_leaderboard_path()
            
            if not leaderboard_path.exists():
                self.table.setRowCount(0)
                return

            with open(leaderboard_path, 'r', encoding='utf-8') as f:
                scores = json.load(f)

            self.table.setRowCount(len(scores))
            for row, entry in enumerate(scores):
                self.add_table_row(row, entry)
                
        except Exception:
            self.table.setRowCount(0)

    def add_table_row(self, row, entry):
        rank_item = QTableWidgetItem(str(row + 1))
        player_item = QTableWidgetItem(entry.get('player', 'Unknown'))
        score = min(entry.get('score', 0), 15)
        score_item = QTableWidgetItem(str(score))
    
        actual_position = row + 1
    
        if actual_position == 1:
            text_color = QColor(40, 40, 40)
            bg_color = QColor(255, 200, 0)
        elif actual_position == 2:
            text_color = QColor(40, 40, 40)
            bg_color = QColor(220, 220, 220)
        elif actual_position == 3:
            text_color = QColor(255, 255, 255)
            bg_color = QColor(200, 120, 50)
        elif score == 15:
            text_color = QColor(255, 255, 255)
            bg_color = QColor(0, 150, 0)
        else:
            text_color = QColor(230, 230, 255)
            bg_color = QColor(70, 30, 90)
    
        font_size = 12 if actual_position <= 3 else 10
        font = QFont('Arial', font_size, QFont.Weight.Bold)
    
        for item in [rank_item, player_item, score_item]:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(text_color)
            item.setBackground(bg_color)
            item.setFont(font)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    
        self.table.setItem(row, 0, rank_item)
        self.table.setItem(row, 1, player_item)
        self.table.setItem(row, 2, score_item)
        self.table.setRowHeight(row, 40)

    def get_dialog_style(self):
        return """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2a0845, stop:1 #7a1a5a);
                color: #ffffff;
                font-family: 'Minecraft';
                border: 2px solid #ba5a9a;
                border-radius: 10px;
            }
        """
    
    def get_table_style(self):
        return """
            QTableWidget {
                background: rgba(40, 10, 60, 180);
                border: 2px solid #9a3a7a;
                gridline-color: #7a2a65;
                font-size: 14px;
                color: white;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a2a75, stop:1 #9a3a7a);
                padding: 5px;
                border: 1px solid #ba5a9a;
                color: white;
                font-weight: bold;
            }
        """
    
    def get_button_style(self):
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a2a75, stop:1 #9a3a7a);
                color: white;
                border: 2px solid #ba5a9a;
                border-radius: 5px;
                padding: 5px 10px;
                font-family: 'Minecraft';
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6a3a85, stop:1 #aa4a8a);
                border: 2px solid #da7aba;
            }
        """

class MainMenu(QMainWindow):
    start_game_signal = pyqtSignal(int, str)
    
    def __init__(self, audio_manager=None):
        super().__init__()
        self.audio_manager = audio_manager
        self.load_settings()
        self.click_sound = os.path.join(os.path.dirname(__file__), "sounds", "click.mp3")
        self.hover_sound = os.path.join(os.path.dirname(__file__), "sounds", "hover.mp3")
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
        
        self.ensure_leaderboard_file()

    def ensure_leaderboard_file(self):
        leaderboard_path = get_leaderboard_path()
        if not leaderboard_path.exists():
            demo_data = [
                {"player": "Dream Champion", "score": 15},
                {"player": "Silver Runner", "score": 12},
                {"player": "Bronze Player", "score": 9},
                {"player": "New Challenger", "score": 6}
            ]
            with open(leaderboard_path, 'w', encoding='utf-8') as f:
                json.dump(demo_data, f, indent=4)

    def init_resources(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.normpath(os.path.join(self.base_path, "..", "assets"))
        
        font_path = os.path.join(self.assets_path, "fonts", "Minecraft.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
        
        self.background = self.create_background()
        self.logo = self.create_logo()
        self.init_buttons()
    
    def create_background(self):
        quality = self.audio_manager.graphics_quality if self.audio_manager else "Medium"
        bg_path = os.path.join(self.assets_path, "background", "level0.png")
        
        if os.path.exists(bg_path):
            bg = QPixmap(bg_path)
            if not bg.isNull():
                if quality == "Low":
                    bg = bg.scaled(200, 150, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.FastTransformation)
                    bg = bg.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.FastTransformation)
                elif quality == "Medium":
                    bg = bg.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.FastTransformation)
                    bg = bg.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                elif quality == "High":
                    bg = bg.scaled(600, 450, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                    bg = bg.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                else:
                    bg = bg.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                return bg.copy((bg.width()-800)//2, (bg.height()-600)//2, 800, 600)
        
        bg = QPixmap(800, 600)
        painter = QPainter(bg)
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0, QColor(42, 8, 69))
        gradient.setColorAt(1, QColor(122, 26, 90))
        painter.fillRect(bg.rect(), gradient)
        painter.end()
        return bg
    
    def create_logo(self):
        quality = self.audio_manager.graphics_quality if self.audio_manager else "Medium"
        logo_path = os.path.join(self.assets_path, "for game", "gameOver.png")
        
        if os.path.exists(logo_path):
            logo = QPixmap(logo_path)
            if not logo.isNull():
                if quality == "Low":
                    logo = logo.scaled(100, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
                    logo = logo.scaled(400, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
                elif quality == "Medium":
                    logo = logo.scaled(200, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
                    logo = logo.scaled(400, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                elif quality == "High":
                    logo = logo.scaled(300, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    logo = logo.scaled(400, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                else:
                    logo = logo.scaled(400, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                return logo
        
        logo = QPixmap(400, 100)
        logo.fill(Qt.GlobalColor.transparent)
        painter = QPainter(logo)
        
        font_size = 24 if quality == "Low" else 32
        painter.setFont(QFont("Minecraft", font_size, QFont.Weight.Bold))
        painter.setPen(QColor(0, 0, 0, 150))
        painter.drawText(logo.rect().translated(2, 2), Qt.AlignmentFlag.AlignCenter, "EXIT THE DREAM")
        painter.setPen(QColor(255, 102, 204))
        painter.drawText(logo.rect(), Qt.AlignmentFlag.AlignCenter, "EXIT THE DREAM")
        painter.end()
        return logo
    
    def init_buttons(self):
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
        btn_width, btn_height = 220, 45
        pixmap = QPixmap(btn_width, btn_height)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        self.draw_button(painter, QRect(0, 0, btn_width, btn_height), 
                        self.button_texts[btn_key], pressed)
        painter.end()
        return pixmap
    
    def draw_button(self, painter, rect, text, pressed=False):
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
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.background)
        
        if not self.logo.isNull():
            logo_x = (800 - self.logo.width()) // 2
            painter.drawPixmap(logo_x, 100, self.logo)
        
        self.draw_buttons(painter)
    
    def draw_buttons(self, painter):
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

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        current_hover = None
        
        for btn, rect in self.button_rects.items():
            if rect.contains(event.pos()):
                current_hover = btn
                break
        
        if (current_hover != self.last_hovered_button and 
            current_hover is not None and 
            self.audio_manager and 
            os.path.exists(self.hover_sound)):
            self.audio_manager.play_sound(self.hover_sound)
        
        self.last_hovered_button = current_hover
    
    def mousePressEvent(self, event):
        for btn, rect in self.button_rects.items():
            if rect.contains(event.pos()):
                self.pressed_button = btn
                self.update()
                break
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        if self.pressed_button:
            btn = self.pressed_button
            if self.button_rects[btn].contains(event.pos()):
                if hasattr(self, 'audio_manager') and self.audio_manager:
                    self.audio_manager.play_click()
                self.handle_button_click(btn)
            self.pressed_button = None
            self.update()
        super().mouseReleaseEvent(event)

    def handle_button_click(self, button):
        if self.audio_manager:
            self.audio_manager.play_click()
            
        handlers = {
            "start": self.start_game,
            "exit": self.confirm_exit,
            "options": self.show_options,
            "leaderboard": self.show_leaderboard,
            "restart": self.confirm_restart
        }
        handlers.get(button, lambda: None)()

    def start_game(self):
        self.start_game_signal.emit(self.current_level, self.player_name)
    
    def confirm_restart(self):
        dialog = ConfirmDialog(
            self,
            "Are you sure you want to restart?\nAll progress will be lost.",
            "Restart"
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.current_level = 1
            self.start_game_signal.emit(1, self.player_name)
    
    def confirm_exit(self):
        dialog = ConfirmDialog(
            self,
            "Are you sure you want to exit the game?",
            "Exit"
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            QApplication.quit()
    
    def show_options(self):
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.background = self.create_background()
            self.logo = self.create_logo()
            self.update()
    
    def show_leaderboard(self):
        dialog = LeaderboardDialog(self)
        dialog.exec()
    
    def load_scores(self):
        try:
            leaderboard_path = os.path.join(self.base_path, "leaderboard.json")
            if os.path.exists(leaderboard_path):
                with open(leaderboard_path, 'r', encoding='utf-8') as f:
                    self.scores = json.load(f)
        except Exception:
            self.scores = []

    def load_settings(self):
        if not self.audio_manager:
            return
            
        try:
            settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
            if os.path.exists(settings_path):
                with open(settings_path) as f:
                    settings = json.load(f)
                    self.audio_manager.control_scheme = settings.get('controls', 'Arrow Keys')
        except Exception:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    menu = MainMenu()

    def handle_start(level, name):
        game = Game()
        game.resize(800, 600)
        game.show()
        menu.hide()

    menu.start_game_signal.connect(handle_start)
    menu.show()
    sys.exit(app.exec())