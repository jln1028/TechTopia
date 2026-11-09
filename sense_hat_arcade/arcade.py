"""Sense HAT Arcade launcher: python3 arcade.py"""
import time
from sense_hat import SenseHat
from arcade_core import ArcadeController, BLACK, GREEN, RED, BLUE, YELLOW, BROWN, WHITE
from high_scores import HighScores

sense=SenseHat()
sense.low_light=True
scores=HighScores()
controller=ArcadeController()
LABELS={'tetris':'TETRIS','jumpy':'JUMPY','flood':'FLOOD'}
ICONS={
    'tetris':[(2,2,RED),(3,2,RED),(4,2,RED),(3,3,RED),(3,6,GREEN)],
    'jumpy':[(2,3,GREEN),(5,6,RED),(6,6,RED)],
    'flood':[(1,2,GREEN),(3,3,YELLOW),(4,5,BROWN)]+[(x,7,BLUE) for x in range(8)],
}
DIFFICULTY_COLORS={'easy':GREEN,'normal':YELLOW,'hard':RED}

def render(pixels):
    frame=[BLACK]*64
    for x,y,color in pixels:
        if 0<=x<8 and 0<=y<8: frame[y*8+x]=color
    sense.set_pixels(frame)

def message(value,color=GREEN):
    sense.show_message(str(value),text_colour=color,scroll_speed=0.055)

def get_events():
    return [event.direction for event in sense.stick.get_events() if event.action=='pressed']

def menu_image():
    if controller.screen=='games':
        render(ICONS[controller.selected_game])
    elif controller.screen=='difficulty':
        color=DIFFICULTY_COLORS[controller.selected_difficulty]
        # E / N / H in 3x5 block lettering, plus a color strip.
        letters={
            'easy':['111','100','110','100','111'],
            'normal':['101','111','111','111','101'],
            'hard':['101','101','111','101','101'],
        }
        pixels=[(x+2,y+1,color) for y,row in enumerate(letters[controller.selected_difficulty]) for x,bit in enumerate(row) if bit=='1']
        pixels += [(x,7,color) for x in range(8)]
        render(pixels)
    elif controller.screen=='result':
        render([(x,y,GREEN if controller.game.status=='won' else RED) for x,y in [(2,2),(3,2),(4,2),(2,3),(4,3),(2,4),(3,4),(4,4)]])

def show_result():
    game=controller.game
    if game.status=='won': message('YOU WIN!',YELLOW)
    elif game.status=='lost': message('GAME OVER',RED)
    else: message('GAME PAUSED',YELLOW)
    message('SCORE '+str(game.score),YELLOW)
    try:
        is_record=scores.record(controller.game_name,controller.difficulty,game.score)
    except OSError:
        is_record=False
        message('SCORE NOT SAVED',RED)
    if is_record: message('NEW HIGH SCORE!',GREEN)
    message('BEST '+str(scores.best(controller.game_name,controller.difficulty)),WHITE)
    if hasattr(game,'health'): message('HP '+str(game.health),GREEN)
    message('CENTER RETRY LEFT MENU RIGHT LEVEL',WHITE)
    sense.stick.get_events()
    menu_image()

def main():
    menu_image()
    previous_screen=controller.screen
    next_tick=time.monotonic()
    try:
        while True:
            for direction in get_events():
                # During play, center returns to result screen (and never fires).
                controller.handle(direction)
                if controller.screen=='playing' and previous_screen!='playing':
                    message(LABELS[controller.game_name]+' '+controller.difficulty.upper(),YELLOW)
                    next_tick=time.monotonic()+controller.game.interval
                    sense.stick.get_events()
                elif controller.screen=='result' and previous_screen=='playing':
                    show_result()
                elif controller.screen!='playing':
                    menu_image()
                previous_screen=controller.screen
            if controller.screen=='playing':
                now=time.monotonic()
                if now>=next_tick:
                    controller.step()
                    render(controller.game.pixels())
                    next_tick=now+controller.game.interval
                    if controller.screen=='result':
                        show_result()
                        previous_screen='result'
            time.sleep(0.02)
    except KeyboardInterrupt:
        pass
    finally:
        sense.clear()

if __name__=='__main__': main()
