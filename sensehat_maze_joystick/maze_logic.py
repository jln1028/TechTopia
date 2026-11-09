import random
from collections import deque

SIZE = 8
START = (1, 1)
GOAL = (6, 6)
WALL, PATH, TARGET = 1, 0, 2


def reachable(maze, start=START, goal=GOAL):
    queue = deque([start])
    seen = {start}
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            return True
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE and maze[ny][nx] != WALL and (nx, ny) not in seen:
                seen.add((nx, ny))
                queue.append((nx, ny))
    return False


def generate_maze(rng=None):
    rng = rng or random.Random()
    maze = [[WALL] * SIZE for _ in range(SIZE)]
    # Odd-coordinate cells, connected by one-cell corridors.
    stack = [START]
    maze[1][1] = PATH
    while stack:
        x, y = stack[-1]
        candidates = []
        for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
            nx, ny = x + dx, y + dy
            if 1 <= nx <= 5 and 1 <= ny <= 5 and maze[ny][nx] == WALL:
                candidates.append((nx, ny, dx, dy))
        if candidates:
            nx, ny, dx, dy = rng.choice(candidates)
            maze[y + dy // 2][x + dx // 2] = PATH
            maze[ny][nx] = PATH
            stack.append((nx, ny))
        else:
            stack.pop()
    # Connect the goal (6,6) to the carved network.
    if rng.choice((True, False)):
        maze[5][6] = PATH
    else:
        maze[6][5] = PATH
    maze[6][6] = TARGET
    return maze


def tilt_step(ax, ay, threshold=0.35):
    # Accelerometer axes can differ with physical display orientation.
    if max(abs(ax), abs(ay)) < threshold:
        return (0, 0)
    if abs(ax) >= abs(ay):
        return (-1 if ax > 0 else 1, 0)
    return (0, 1 if ay > 0 else -1)


class MazeGame:
    def __init__(self, rng=None):
        self.rng = rng or random.Random()
        self.maze = generate_maze(self.rng)
        self.position = START
        self.score = 0

    def move(self, dx, dy):
        x, y = self.position
        nx, ny = x + dx, y + dy
        if abs(dx) + abs(dy) != 1:
            return False
        if not (0 <= nx < SIZE and 0 <= ny < SIZE):
            return False
        if self.maze[ny][nx] == WALL:
            return False
        self.position = (nx, ny)
        if self.position == GOAL:
            self.score += 1
            return True
        return False

    def next_round(self):
        previous = self.maze
        for _ in range(30):
            candidate = generate_maze(self.rng)
            if candidate != previous:
                self.maze = candidate
                break
        else:
            # Extremely unlikely; a changed maze is not guaranteed with a
            # deliberately degenerate random generator.
            self.maze = generate_maze(random.Random())
        self.position = START
