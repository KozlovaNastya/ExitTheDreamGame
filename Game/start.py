import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
from gam.main_menu import MainMenu
from main import Game

class AudioManager:
    def __init__(self):
        # Background music
        self.music_player = QMediaPlayer()
        self.music_output = QAudioOutput()
        self.music_player.setAudioOutput(self.music_output)
        
        # Click sound
        self.click_player = QMediaPlayer()
        self.click_output = QAudioOutput()
        self.click_player.setAudioOutput(self.click_output)
        
        # Hover sound
        self.hover_player = QMediaPlayer()
        self.hover_output = QAudioOutput()
        self.hover_player.setAudioOutput(self.hover_output)
        
        self.set_volume(80)  # Default volume 80%
        self.graphics_quality = "Medium"  # Default graphics quality
        
    def set_volume(self, volume):
        """Set volume for all sounds (0-100)"""
        volume = max(0, min(100, volume)) / 100.0
        self.music_output.setVolume(volume)
        self.click_output.setVolume(volume * 1.2)  # Click slightly louder
        self.hover_output.setVolume(volume * 0.8)  # Hover slightly quieter
    
    def set_music_volume(self, volume):
        """Set only music volume"""
        volume = max(0, min(100, volume)) / 100.0
        self.music_output.setVolume(volume)
    
    def play_music(self, file_path):
        """Play background music"""
        if os.path.exists(file_path):
            self.music_player.setSource(QUrl.fromLocalFile(file_path))
            self.music_player.setLoops(QMediaPlayer.Loops.Infinite)
            self.music_player.play()
    
    def play_click(self):
        """Play click sound"""
        if not self.click_player.source().isEmpty():
            self.click_player.stop()
            self.click_player.setPosition(0)
            self.click_player.play()
    
    def play_hover(self):
        """Play hover sound"""
        if not self.hover_player.source().isEmpty():
            self.hover_player.stop()
            self.hover_player.setPosition(0)
            self.hover_player.play()
    
    def load_click_sound(self, file_path):
        """Load click sound"""
        if os.path.exists(file_path):
            self.click_player.setSource(QUrl.fromLocalFile(file_path))
    
    def load_hover_sound(self, file_path):
        """Load hover sound"""
        if os.path.exists(file_path):
            self.hover_player.setSource(QUrl.fromLocalFile(file_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Initialize audio
    audio_manager = AudioManager()
    
    # Load sounds
    base_path = os.path.dirname(os.path.abspath(__file__))
    music_path = os.path.join(base_path, "sounds", "background.mp3")
    click_path = os.path.join(base_path, "sounds", "click.mp3")
    hover_path = os.path.join(base_path, "sounds", "hover.mp3")
    
    audio_manager.play_music(music_path)
    audio_manager.load_click_sound(click_path)
    audio_manager.load_hover_sound(hover_path)
    
    # Create menu
    menu = MainMenu(audio_manager)
    menu.current_game = None
    
    def handle_start(level, name):
        game = Game()
        game.audio_manager = audio_manager
        game.resize(800, 600)
        game.show()
        menu.hide()
        menu.current_game = game
        game.back_to_menu_signal.connect(handle_back_to_menu)

    def handle_back_to_menu():
        if menu.current_game:
            menu.current_game.hide()
            menu.current_game.deleteLater()
            menu.current_game = None
        menu.show()

    menu.start_game_signal.connect(handle_start)
    menu.show()
    sys.exit(app.exec())