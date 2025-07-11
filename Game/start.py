import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
from gam.main_menu import MainMenu
from main import Game
from gam.levels.intro import StoryDialog

class AudioManager:
    def __init__(self):
        self.music_player = QMediaPlayer()
        self.music_output = QAudioOutput()
        self.music_player.setAudioOutput(self.music_output)
        
        self.click_player = QMediaPlayer()
        self.click_output = QAudioOutput()
        self.click_player.setAudioOutput(self.click_output)
        
        self.hover_player = QMediaPlayer()
        self.hover_output = QAudioOutput()
        self.hover_player.setAudioOutput(self.hover_output)
        
        self.set_volume(80)
        self.graphics_quality = "Medium"
        self.control_scheme = "Arrow Keys"
        
    def set_volume(self, volume):
        volume = max(0, min(100, volume)) / 100.0
        self.music_output.setVolume(volume)
        self.click_output.setVolume(volume * 1.2)
        self.hover_output.setVolume(volume * 0.8)
    
    def set_music_volume(self, volume):
        volume = max(0, min(100, volume)) / 100.0
        self.music_output.setVolume(volume)
    
    def play_music(self, file_path):
        if os.path.exists(file_path):
            self.music_player.setSource(QUrl.fromLocalFile(file_path))
            self.music_player.setLoops(QMediaPlayer.Loops.Infinite)
            self.music_player.play()
    
    def play_click(self):
        if not self.click_player.source().isEmpty():
            self.click_player.stop()
            self.click_player.setPosition(0)
            self.click_player.play()
    
    def play_hover(self):
        if not self.hover_player.source().isEmpty():
            self.hover_player.stop()
            self.hover_player.setPosition(0)
            self.hover_player.play()
    
    def load_click_sound(self, file_path):
        if os.path.exists(file_path):
            self.click_player.setSource(QUrl.fromLocalFile(file_path))
    
    def load_hover_sound(self, file_path):
        if os.path.exists(file_path):
            self.hover_player.setSource(QUrl.fromLocalFile(file_path))

def handle_start(level, name, menu, audio_manager):
    story = "Oh... That dream again...\nI need to wake up quickly or\nI'll get sucked into the abyss of endless dreams."
    controls = """Controls:
    - Left/Right arrows or WASD to move
    - Space to jump
    On level2 use:
    1 - gravity down
    2 - gravity up
    On level3 use:
    3 - gravity left
    4 - gravity right"""
    
    dialog = StoryDialog(story, controls)
    dialog.exec()
    
    game = Game()
    game.audio_manager = audio_manager
    game.resize(800, 600)
    game.show()
    menu.hide()
    menu.current_game = game
    game.back_to_menu_signal.connect(lambda: handle_back_to_menu(menu))

def handle_back_to_menu(menu):
    if menu.current_game:
        menu.current_game.hide()
        menu.current_game.deleteLater()
        menu.current_game = None
    menu.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    audio_manager = AudioManager()
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    audio_manager.play_music(os.path.join(base_path, "sounds", "background.mp3"))
    audio_manager.load_click_sound(os.path.join(base_path, "sounds", "click.mp3"))
    audio_manager.load_hover_sound(os.path.join(base_path, "sounds", "hover.mp3"))
    
    menu = MainMenu(audio_manager)
    menu.current_game = None
    menu.start_game_signal.connect(lambda level, name: handle_start(level, name, menu, audio_manager))
    menu.show()
    
    sys.exit(app.exec())