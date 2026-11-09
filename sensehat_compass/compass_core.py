"""Hardware-independent compass logic for the Sense HAT classroom project."""
import math

BLACK=(0,0,0)
RED=(255,0,0)
BLUE=(0,0,35)
WHITE=(180,180,180)
DIRECTIONS=('N','NE','E','SE','S','SW','W','NW')
MODES=('arrow','cardinal','numeric')

def cardinal(heading):
    """Return nearest of eight directions; 0 degrees is north."""
    return DIRECTIONS[int(((heading % 360)+22.5)//45)%8]

def numeric_frames(heading):
    """Return three-character heading text, rounded and wrapped."""
    return [f'{round(heading)%360:03d}']

def arrow_pixels(heading):
    """Draw an 8-direction arrow, with zero at the top and 90 at right."""
    angle=math.radians((round((heading%360)/45)*45)%360)
    dx=round(math.sin(angle))
    dy=-round(math.cos(angle))
    pixels=[BLUE]*64
    # Tail at center; shaft points outwards toward the perimeter.
    cx,cy=3,3
    for distance in range(0,5):
        x,y=cx+dx*distance,cy+dy*distance
        if 0<=x<8 and 0<=y<8: pixels[y*8+x]=RED
    # Arrowhead branches to either side of the direction vector.
    tipx,tipy=cx+dx*4,cy+dy*4
    for side in (-1,1):
        x=tipx-dx+side*(-dy)
        y=tipy-dy+side*dx
        if 0<=x<8 and 0<=y<8: pixels[y*8+x]=WHITE
    return pixels

def compass_frame(heading, mode):
    """A valid fallback frame; text modes are rendered by the hardware app."""
    if mode not in MODES: raise ValueError(f'Unknown mode: {mode}')
    if mode=='arrow': return arrow_pixels(heading)
    return [BLACK]*64

def next_mode(current, step=1):
    return MODES[(MODES.index(current)+step)%len(MODES)]
