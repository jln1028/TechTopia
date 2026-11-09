import unittest
from arcade import Arcade, CYAN, GAMES

class ArcadeTests(unittest.TestCase):
    def test_menu_wraps(self):
        a=Arcade(); a.input('up'); self.assertEqual(a.selection,len(GAMES)-1)
    def test_start_and_restart(self):
        a=Arcade(); a.input('middle'); self.assertEqual(a.mode,'countdown'); a.tick(3); a.score=17; a.input('middle'); self.assertEqual(a.score,0)
    def test_snake_apple_increase(self):
        a=Arcade(); a.start('Snake'); a.eaten=3; a._refill_apples(); self.assertEqual(len(a.apples),4)
    def test_snake_no_overlap(self):
        a=Arcade(); a.start('Snake'); self.assertTrue(set(a.apples).isdisjoint(a.snake))
    def test_background(self):
        a=Arcade(); self.assertEqual(a.frame()[0],CYAN)
    def test_all_games_start(self):
        for game in GAMES:
            a=Arcade(); a.start(game); self.assertEqual(len(a.frame()),64)
    def test_score_saved_on_game_over(self):
        a=Arcade(); a.start('Light Racer'); a.tick(3); a.score=8; a.end(); self.assertEqual(a.scores['Light Racer'],8)
    def test_no_reverse_snake(self):
        a=Arcade(); a.start('Snake'); a.input('left'); self.assertEqual(a.direction,'right')
    def test_joysticker_correct_direction(self):
        a=Arcade(); a.start('Joysticker'); a.tick(3); d=a.target; a.input(d); self.assertEqual(a.score,10)
    def test_maze_walls(self):
        a=Arcade(); a.start('Marble Maze'); a.input('left'); self.assertEqual(a.player,(1,1))

if __name__=='__main__': unittest.main()
