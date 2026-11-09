import json
import os
import tempfile
import unittest
from arcade_core import ArcadeController
from high_scores import HighScores

class ControllerTests(unittest.TestCase):
    def test_selection_difficulty_start_and_restart(self):
        c=ArcadeController()
        c.handle('right'); self.assertEqual(c.selected_game,'jumpy')
        c.handle('middle'); self.assertEqual(c.screen,'difficulty')
        c.handle('right'); self.assertEqual(c.selected_difficulty,'hard')
        c.handle('middle'); self.assertEqual(c.screen,'playing')
        self.assertEqual(c.game.health,3)
        c.game.score=9
        c.handle('middle'); self.assertEqual(c.screen,'result')
        c.handle('middle'); self.assertEqual(c.screen,'playing')
        self.assertEqual(c.game.score,0)

    def test_return_to_menu_or_difficulty(self):
        c=ArcadeController(); c.handle('middle'); c.handle('middle')
        c.handle('middle'); c.handle('left')
        self.assertEqual(c.screen,'games')
        c.handle('middle'); c.handle('middle'); c.handle('middle'); c.handle('right')
        self.assertEqual(c.screen,'difficulty')

    def test_difficulty_changes_game_speed_and_spawning(self):
        c=ArcadeController(); c.handle('middle'); c.handle('left'); c.handle('middle')
        easy_interval=c.game.interval
        easy_spawn=c.game.spawn_factor
        c.handle('middle'); c.handle('right'); c.handle('right'); c.handle('middle')
        hard_interval=c.game.interval
        self.assertGreater(easy_interval,hard_interval)
        self.assertGreater(easy_spawn,c.game.spawn_factor)

    def test_game_loss_transitions_to_result(self):
        c=ArcadeController(); c.handle('middle'); c.handle('middle')
        c.game.health=1
        c.game.ground={c.game.x}
        c.game._touch_ground()
        c.step()
        self.assertEqual(c.screen,'result')

class ScoreTests(unittest.TestCase):
    def test_save_reload_and_independent_difficulties(self):
        with tempfile.TemporaryDirectory() as directory:
            path=os.path.join(directory,'scores.json')
            s=HighScores(path)
            self.assertTrue(s.record('tetris','easy',10))
            self.assertFalse(s.record('tetris','easy',8))
            self.assertTrue(s.record('tetris','hard',3))
            s2=HighScores(path)
            self.assertEqual(s2.best('tetris','easy'),10)
            self.assertEqual(s2.best('tetris','hard'),3)
            self.assertEqual(s2.best('jumpy','easy'),0)

    def test_corrupt_scores_recover(self):
        with tempfile.TemporaryDirectory() as directory:
            path=os.path.join(directory,'scores.json')
            with open(path,'w') as f: f.write('{not json')
            s=HighScores(path)
            self.assertEqual(s.best('flood','normal'),0)
            self.assertTrue(s.record('flood','normal',4))
            with open(path) as f: self.assertEqual(json.load(f)['flood:normal'],4)

if __name__=='__main__': unittest.main()
