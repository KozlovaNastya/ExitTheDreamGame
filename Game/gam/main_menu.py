# -*- coding: utf-8 -*-
import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QPainter, QPixmap, QFont, QColor, QPen, QBrush, QFontDatabase
from PyQt6.QtCore import Qt, QRect, QTimer, pyqtSignal

class MainMenu(QMainWindow):
    start_game_signal = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exit the Dream - Main Menu")
        self.setFixedSize(800, 600)
        
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.normpath(os.path.join(self.base_path, "..", "assets"))
        
        self.current_level = 1
        self.player_name = "Player"
        
        font_path = os.path.join(self.assets_path, "fonts", "Minecraft.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
        
        self.load_assets()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)
        
        self.hovered_button = None
        self.pressed_button = None
       
    def load_assets(self):
        bg_path = os.path.join(self.assets_path, "background", "level0.png")
        if os.path.exists(bg_path):
            bg = QPixmap(bg_path)
            if not bg.isNull():
                self.background = bg.scaled(
                    800, 600, 
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.background = self.background.copy(
                    (self.background.width() - 800) // 2,
                    (self.background.height() - 600) // 2,
                    800,
                    600
                )
        else:
            self.background = QPixmap(800, 600)
            self.background.fill(QColor(0, 0, 0))

        logo_path = os.path.join(self.assets_path, "for game", "gameOver.png")
        if os.path.exists(logo_path):
            self.logo = QPixmap(logo_path)
            if not self.logo.isNull():
                self.logo = self.logo.scaledToHeight(120, Qt.TransformationMode.SmoothTransformation)
        else:
            self.logo = QPixmap(400, 100)
            self.logo.fill(Qt.GlobalColor.transparent)
            painter = QPainter(self.logo)
            painter.setFont(QFont("Exit the Dream", 32))
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(self.logo.rect(), Qt.AlignmentFlag.AlignCenter, "GAME DUER")
            painter.end()
        
        self.button_texts = {
            "start": "START",
            "restart": "RESTART",
            "options": "OPTIONS",
            "leaderboard": "LEADERBOARD",
            "exit": "EXIT"
        }
        
        self.hover_colors = {
            "start": QColor(50, 255, 50, 120), 
            "exit": QColor(220, 0, 0, 120),
            "restart": QColor(255, 200, 0, 120),
            "leaderboard": QColor(160, 0, 255, 120),
            "options": QColor(0, 150, 255, 120) 
        }
        
        btn_width, btn_height = 200, 50
        start_x = (800 - btn_width) // 2
        start_y = 280 
        btn_spacing = 60 
        
        self.button_rects = {
            "start": QRect(start_x, start_y, btn_width, btn_height),
            "restart": QRect(start_x, start_y + btn_spacing, btn_width, btn_height),
            "options": QRect(start_x, start_y + 2*btn_spacing, btn_width, btn_height),
            "leaderboard": QRect(start_x, start_y + 3*btn_spacing, btn_width, btn_height),
            "exit": QRect(start_x, start_y + 4*btn_spacing, btn_width, btn_height)
        }
        
        self.button_states = {}
        for btn in self.button_texts.keys():
            normal = QPixmap(btn_width, btn_height)
            normal.fill(QColor(0, 0, 0, 0))
            p = QPainter(normal)
            self.draw_minecraft_button(p, QRect(0, 0, btn_width, btn_height), 
                                     self.button_texts[btn], pressed=False)
            p.end()
            
            pressed = QPixmap(btn_width, btn_height)
            pressed.fill(QColor(0, 0, 0, 0))
            p = QPainter(pressed)
            self.draw_minecraft_button(p, QRect(0, 0, btn_width, btn_height), 
                                     self.button_texts[btn], pressed=True)
            p.end()
            
            self.button_states[btn] = {"normal": normal, "pressed": pressed}
    
    def draw_minecraft_button(self, painter, rect, text, pressed=False):
        border_color = QColor(85, 85, 85)
        bg_color = QColor(0, 0, 0, 150)
        text_color = QColor(255, 255, 255)
        
        if pressed:
            rect = rect.translated(0, 2)
            border_color = QColor(85, 85, 85)
            bg_color = QColor(0, 0, 0, 200)
        
        painter.setPen(QPen(border_color, 2))
        painter.setBrush(QBrush(bg_color))
        painter.drawRect(rect)
        
        painter.setFont(QFont("Minecraft", 12))
        painter.setPen(text_color)
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
            pixmap = self.button_states[btn][state]
            
            painter.drawPixmap(rect, pixmap)
            
            if is_hovered and not is_pressed:
                hover_color = self.hover_colors.get(btn, QColor(255, 255, 255, 30))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(hover_color))
                painter.drawRoundedRect(rect.adjusted(-3, -3, 3, 3), 5, 5)
    
    def mousePressEvent(self, event):
        for btn, rect in self.button_rects.items():
            if rect.contains(event.pos()):
                self.pressed_button = btn
                self.update()
                break
    
    def mouseReleaseEvent(self, event):
        if self.pressed_button:
            for btn, rect in self.button_rects.items():
                if btn == self.pressed_button and rect.contains(event.pos()):
                    self.handle_button_click(btn)
                    break
            self.pressed_button = None
            self.update()
    
    def handle_button_click(self, button):
        if button == "start":
            self.start_game_signal.emit(1)
        elif button == "exit":
            QApplication.quit()
        elif button == "options":
            print("Options clicked")
        elif button == "leaderboard":
            print("Leaderboard clicked")
        elif button == "restart":
            print("Restart clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec())