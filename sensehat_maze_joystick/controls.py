"""Hardware-independent control selection and event processing."""
from maze_logic import tilt_step

DIRECTIONS = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}

class Controls:
    def __init__(self, mode='joystick'):
        if mode not in ('joystick', 'tilt'):
            raise ValueError('mode must be joystick or tilt')
        self.mode = mode

    def process_events(self, events):
        """Return (move, toggled). Center press switches modes."""
        move = None
        toggled = False
        for event in events:
            if event.action != 'pressed':
                continue
            if event.direction == 'middle':
                self.mode = 'tilt' if self.mode == 'joystick' else 'joystick'
                toggled = True
                move = None
            elif self.mode == 'joystick' and not toggled and event.direction in DIRECTIONS:
                move = DIRECTIONS[event.direction]
        return move, toggled

    def tilt_move(self, acceleration):
        if self.mode != 'tilt':
            return None
        step = tilt_step(acceleration['x'], acceleration['y'])
        return step if step != (0, 0) else None
