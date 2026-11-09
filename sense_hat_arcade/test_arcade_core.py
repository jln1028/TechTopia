import unittest
from arcade_core import TetrisGame, JumpyGame, FloodGame, ArcadeMenu

class MenuTests(unittest.TestCase):
    def test_selection_wraps_and_launches(self):
        m=ArcadeMenu()
        m.handle('left')
        self.assertEqual(m.selection,2)
        self.assertEqual(m.handle('middle'),'flood')

class TetrisTests(unittest.TestCase):
    def test_shooting_destroys_crusher_and_scores(self):
        g=TetrisGame()
        g.crushers=[{'x':3,'y':5,'size':1}]
        g.handle('up')
        g.step()
        self.assertFalse(g.crushers)
        self.assertEqual(g.score,5)
    def test_fallen_obstacle_contact_hurts_once_and_clears(self):
        g=TetrisGame()
        g.ground={4}
        g.handle('right')
        self.assertEqual(g.health,4)
        self.assertNotIn(4,g.ground)
    def test_crusher_size_grows_not_speed(self):
        g=TetrisGame()
        initial=g.interval
        g.score=40
        self.assertGreater(g.crusher_size(),1)
        self.assertEqual(g.interval,initial)
    def test_three_dimensions_stay_in_bounds(self):
        g=TetrisGame()
        g.crushers=[{'x':7,'y':6,'size':2}]
        g.step()
        for x,y,c in g.pixels():
            self.assertTrue(0<=x<8 and 0<=y<8)

class JumpyTests(unittest.TestCase):
    def test_side_collision_costs_one_health_and_clears_all(self):
        g=JumpyGame()
        g.obstacles=[3,7]
        g.step()
        self.assertEqual(g.health,2)
        self.assertEqual(g.obstacles,[])
    def test_three_hits_end_game_and_keep_score(self):
        g=JumpyGame()
        for _ in range(3):
            g.obstacles=[3]
            g.step()
        self.assertEqual(g.health,0)
        self.assertEqual(g.status,'lost')
        self.assertIsInstance(g.score,int)
    def test_jump_can_land_on_cube_and_score(self):
        g=JumpyGame()
        g.handle('up')
        g.obstacles=[3]
        g.step()
        self.assertEqual(g.health,3)
        self.assertGreater(g.score,0)

class FloodTests(unittest.TestCase):
    def test_water_rises_and_drowns_player(self):
        g=FloodGame()
        g.water=6
        g.step()
        self.assertEqual(g.status,'lost')
    def test_red_platform_collapses_after_contact(self):
        g=FloodGame()
        g.x,g.y=3,5
        for _ in range(3): g.step()
        self.assertNotIn((3,6),g.platforms)
    def test_collect_all_coins_wins(self):
        g=FloodGame()
        for pos in list(g.coins):
            g.x,g.y=pos
            g.step()
        self.assertEqual(g.status,'won')
    def test_jump_and_gravity_obey_bounds(self):
        g=FloodGame()
        g.handle('up')
        for _ in range(12):
            g.step()
            self.assertTrue(0<=g.y<8)

if __name__=='__main__': unittest.main()
