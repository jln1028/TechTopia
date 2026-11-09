"""Physical Sense HAT runner. Best scores persist for this session."""
import time
from arcade import Arcade, GAMES, CYAN, WHITE, YELLOW
from sense_hat import SenseHat

sense = SenseHat()
sense.low_light = True
arcade = Arcade()
previous_mode = None
previous_selection = None
try:
    sense.show_message('ARCADE', text_colour=WHITE, back_colour=CYAN, scroll_speed=0.07)
    print('Sense HAT Arcade: joystick selects game; middle starts.')
    last = time.monotonic()
    while True:
        now = time.monotonic()
        delta = min(now - last, 0.2)
        last = now
        for event in sense.stick.get_events():
            if event.action != 'pressed':
                continue
            arcade.input(event.direction)
        arcade.tick(delta)
        if arcade.mode == 'menu' and (previous_mode != 'menu' or previous_selection != arcade.selection):
            print('Selected:', GAMES[arcade.selection], '| Best:', arcade.selected_best())
            previous_selection = arcade.selection
        if arcade.mode != previous_mode:
            if arcade.mode == 'countdown':
                print('Starting:', arcade.game, '| 3... 2... 1...')
            elif arcade.mode == 'playing':
                print('GO!', arcade.game)
            elif arcade.mode == 'over':
                print('Game Over:', arcade.game, 'Score:', arcade.score,
                      'Best:', arcade.scores[arcade.game])
                # Scroll the score and high score on the Sense HAT display.
                sense.show_message('S{} H{}'.format(arcade.score, arcade.scores[arcade.game]),
                                   text_colour=YELLOW, back_colour=CYAN, scroll_speed=0.07)
                print('Middle: restart | Left/Up: menu')
                # Discard joystick presses made while the blocking message scrolled.
                sense.stick.get_events()
                last = time.monotonic()
            previous_mode = arcade.mode
        sense.set_pixels(arcade.frame())
        time.sleep(0.03)
except KeyboardInterrupt:
    pass
finally:
    sense.clear()
