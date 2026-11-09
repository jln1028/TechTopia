import unittest
from arcade import Arcade, GAMES, CYAN, YELLOW

class ImprovementsTests(unittest.TestCase):
    def test_distinct_icons(self):
        frames=[]
        for i in range(len(GAMES)):
            a=Arcade(); a.selection=i; frames.append(tuple(a.frame()))
            self.assertEqual(len(frames[-1]),64)
            self.assertIn(CYAN,frames[-1])
        self.assertEqual(len(set(frames)),len(GAMES))
    def test_countdown_before_play(self):
        a=Arcade(); a.input('middle')
        self.assertEqual(a.mode,'countdown')
        self.assertEqual(a.frame().count(YELLOW)>0,True)
        a.tick(1.0); self.assertEqual(a.mode,'countdown')
        a.tick(1.0); self.assertEqual(a.mode,'countdown')
        a.tick(1.0); self.assertEqual(a.mode,'playing')
    def test_countdown_no_game_movement(self):
        a=Arcade(); a.start('Snake'); initial=list(a.snake)
        a.tick(2.9); self.assertEqual(a.snake,initial)
        a.tick(0.1); self.assertEqual(a.snake,initial)
    def test_restart_countdown(self):
        a=Arcade(); a.start('Snake'); a.tick(3); a.score=20
        a.input('middle'); self.assertEqual(a.mode,'countdown'); self.assertEqual(a.score,0)
    def test_score_survives_restart_and_menu(self):
        a=Arcade(); a.start('Snake'); a.tick(3); a.score=30; a.end()
        a.input('middle'); self.assertEqual(a.scores['Snake'],30)
        a.tick(3); a.end(); a.input('left'); self.assertEqual(a.mode,'menu')
        self.assertEqual(a.scores['Snake'],30)
    def test_countdown_direction_does_not_move(self):
        a=Arcade(); a.start('Marble Maze'); a.input('right'); self.assertEqual(a.player,(1,1))
    def test_menu_shows_best_score(self):
        a=Arcade(); a.scores[GAMES[0]]=100
        self.assertEqual(a.selected_best(),100)
