"""Sense HAT Marble Maze: joystick or tilt; press joystick center to toggle."""
import time
from sense_hat import SenseHat
from maze_logic import MazeGame, WALL, TARGET
from controls import Controls

WHITE = (160, 160, 160)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


def draw(sense, game):
    pixels = [WHITE if cell == WALL else GREEN if cell == TARGET else BLACK
              for row in game.maze for cell in row]
    x, y = game.position
    pixels[y * 8 + x] = BLUE
    sense.set_pixels(pixels)


def main():
    sense = SenseHat()
    sense.low_light = True
    game = MazeGame()
    controls = Controls(mode='joystick')
    sense.show_message('JOY', text_colour=YELLOW, back_colour=BLUE, scroll_speed=0.07)
    try:
        while True:
            move, toggled = controls.process_events(sense.stick.get_events())
            if toggled:
                sense.show_message('TILT' if controls.mode == 'tilt' else 'JOY',
                                   text_colour=YELLOW, back_colour=BLUE, scroll_speed=0.07)
                sense.stick.get_events()  # discard presses during the message
            elif controls.mode == 'tilt':
                move = controls.tilt_move(sense.get_accelerometer_raw())
            if move is not None and game.move(*move):
                sense.show_message('Score!', text_colour=YELLOW,
                                   back_colour=BLUE, scroll_speed=0.08)
                game.next_round()
                sense.stick.get_events()  # discard stale inputs
            draw(sense, game)
            time.sleep(0.18)
    finally:
        sense.clear()


if __name__ == '__main__':
    main()
