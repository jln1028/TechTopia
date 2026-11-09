"""Sense HAT interactive compass. Run with python3 compass_app.py."""
import time
from sense_hat import SenseHat
from compass_core import MODES, cardinal, numeric_frames, arrow_pixels, next_mode

POLL_SECONDS=0.08
TEXT_SECONDS=0.6


def main():
    sense=SenseHat()
    sense.low_light=True
    mode='arrow'
    last_pixels=None
    last_text=None
    last_text_time=0
    text_index=0
    last_log_time=0
    print('Joystick: up/center/right = next, down/left = previous. Ctrl+C = quit')
    try:
        while True:
            for event in sense.stick.get_events():
                if event.action != 'pressed':
                    continue
                if event.direction in ('up','middle','right'):
                    mode=next_mode(mode,1)
                elif event.direction in ('down','left'):
                    mode=next_mode(mode,-1)
                else:
                    continue
                last_pixels=None
                last_text=None
                last_text_time=0
                text_index=0
                sense.clear()
                print('Mode:',mode)

            heading=sense.get_compass()%360
            now=time.monotonic()
            if mode=='arrow':
                pixels=arrow_pixels(heading)
                if pixels!=last_pixels:
                    sense.set_pixels(pixels)
                    last_pixels=pixels
            else:
                # show_letter is instantaneous; never use blocking show_message.
                text=cardinal(heading) if mode=='cardinal' else numeric_frames(heading)[0]
                if text!=last_text:
                    text_index=0
                    last_text_time=0
                    last_text=text
                if now-last_text_time>=TEXT_SECONDS:
                    sense.show_letter(text[text_index],
                                      text_colour=(255,255,255),
                                      back_colour=(0,0,30))
                    text_index=(text_index+1)%len(text)
                    last_text_time=now
            if now-last_log_time>=1.0:
                print(f'{heading:06.1f} degrees | {cardinal(heading):2s} | {mode}')
                last_log_time=now
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        print('\nCompass stopped.')
    finally:
        sense.clear()

if __name__=='__main__':
    main()
