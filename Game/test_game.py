# test_game.py
import os
import json
import unittest
from unittest.mock import patch
from PyQt6.QtWidgets import QApplication, QTableWidgetItem

class GameTests(unittest.TestCase):
    TEST_FILE = "test_leaderboard.json"
    
    @classmethod 
    def setUpClass(cls):
        cls.app = QApplication([])
    
    def setUp(self):
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)
    
    def test_full_workflow(self):
        from main import Game
        from gam.main_menu import LeaderboardDialog
        
        game = Game()
        game.hearts_widget.lives = 3
        game.current_level_index = 4
        
        with patch('PyQt6.QtWidgets.QInputDialog.getText', return_value=("TestPlayer", True)):
            game.save_score_to_leaderboard = lambda: self._save_test_data(game)
            game.load_level(5)
            
            self.assertEqual(game.score, 15)
            self.assertTrue(os.path.exists(self.TEST_FILE))
            
            with open(self.TEST_FILE, 'r') as f:
                data = json.load(f)
                self.assertEqual(data[0]["player"], "TestPlayer")
                self.assertEqual(data[0]["score"], 15)
            
            dialog = LeaderboardDialog(None)
            dialog.load_leaderboard = lambda: self._load_test_data(dialog) 
            dialog.load_leaderboard()
            
            self.assertEqual(dialog.table.rowCount(), 1)
            dialog.close()
    
    def _save_test_data(self, game):
        data = [{"player": game.player_name, "score": game.score}]
        with open(self.TEST_FILE, 'w') as f:
            json.dump(data, f)
    
    def _load_test_data(self, dialog):
        with open(self.TEST_FILE, 'r') as f:
            data = json.load(f)
            dialog.table.setRowCount(len(data))
            for row, entry in enumerate(data):
                dialog.table.setItem(row, 1, QTableWidgetItem(entry["player"]))
                dialog.table.setItem(row, 2, QTableWidgetItem(str(entry["score"])))
    
    def tearDown(self):
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_multiple_scores(self):
        test_data = [
            {"player": "PlayerA", "score": 50},
            {"player": "PlayerB", "score": 30}, 
            {"player": "PlayerC", "score": 70}
        ]
    
        with open(self.TEST_FILE, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
    
        from gam.main_menu import LeaderboardDialog
        dialog = LeaderboardDialog(None)
    
        def mock_load():
            with open(self.TEST_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data.sort(key=lambda x: x['score'], reverse=True)
                dialog.table.setRowCount(len(data))
                for row, entry in enumerate(data):
                    dialog.table.setItem(row, 1, QTableWidgetItem(entry["player"]))
                    dialog.table.setItem(row, 2, QTableWidgetItem(str(entry["score"])))
    
        dialog.load_leaderboard = mock_load
        dialog.load_leaderboard()
    
        self.assertEqual(dialog.table.item(0, 2).text(), "70")
        self.assertEqual(dialog.table.item(1, 2).text(), "50")
        self.assertEqual(dialog.table.item(2, 2).text(), "30")
        dialog.close()

    def test_empty_leaderboard(self):
        from gam.main_menu import LeaderboardDialog
        dialog = LeaderboardDialog(None)

        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)
        
        dialog.load_leaderboard()
        self.assertEqual(dialog.table.rowCount(), 0)
        dialog.close()

if __name__ == "__main__":
    unittest.main()