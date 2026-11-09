import random
import unittest
from collections import deque
from maze_logic import MazeGame, generate_maze, reachable, tilt_step, START, GOAL, WALL, TARGET


class MazeTests(unittest.TestCase):
    def test_1000_mazes_are_valid_and_solvable(self):
        for seed in range(1000):
            maze = generate_maze(random.Random(seed))
            self.assertEqual((len(maze), len(maze[0])), (8, 8))
            self.assertTrue(all(len(row) == 8 for row in maze))
            self.assertEqual(maze[GOAL[1]][GOAL[0]], TARGET)
            self.assertEqual(maze[START[1]][START[0]], 0)
            self.assertTrue(reachable(maze))

    def test_maze_variety(self):
        layouts = {tuple(map(tuple, generate_maze(random.Random(seed)))) for seed in range(100)}
        self.assertGreater(len(layouts), 20)

    def test_wall_and_bounds(self):
        game = MazeGame(random.Random(1))
        self.assertFalse(game.move(-1, 0))
        self.assertEqual(game.position, START)
        self.assertFalse(game.move(8, 0))
        self.assertFalse(game.move(0, 0))

    def test_tilt_deadzone_and_single_axis(self):
        self.assertEqual(tilt_step(0.1, -0.2), (0, 0))
        self.assertEqual(tilt_step(0.8, 0.2), (-1, 0))
        self.assertEqual(tilt_step(0.1, 0.8), (0, 1))

    def test_goal_scores_and_next_round_resets(self):
        game = MazeGame(random.Random(42))
        old = game.maze
        # Find the shortest path and play it.
        q = deque([(START, [])]); seen = {START}
        while q:
            pos, moves = q.popleft()
            if pos == GOAL:
                break
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = pos[0]+dx, pos[1]+dy
                if 0 <= nx < 8 and 0 <= ny < 8 and game.maze[ny][nx] != WALL and (nx, ny) not in seen:
                    seen.add((nx, ny)); q.append(((nx, ny), moves+[(dx, dy)]))
        for i, move in enumerate(moves):
            self.assertEqual(game.move(*move), i == len(moves)-1)
        self.assertEqual(game.score, 1)
        game.next_round()
        self.assertEqual(game.position, START)
        self.assertNotEqual(game.maze, old)
        self.assertEqual(game.score, 1)


if __name__ == '__main__':
    unittest.main()
