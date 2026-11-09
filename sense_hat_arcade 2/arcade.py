"""Hardware-independent 8x8 Sense HAT arcade logic."""
import random

CYAN=(0,255,255); GREEN=(0,200,0); RED=(255,0,0); BLUE=(0,0,200)
YELLOW=(255,220,0); WHITE=(255,255,255); PURPLE=(180,0,180)
GAMES=('Marble Maze','Tetris Survival','Snake','Asteroid Dodge','Joysticker','Light Racer')
VECTORS={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}
OPPOSITE={'up':'down','down':'up','left':'right','right':'left'}
MAZE=("########","#...#..#","#.#.#.##","#.#....#","#.####.#","#....#.#","####.#G#","########")
ARROWS={
 'up':((3,1),(4,1),(2,2),(3,2),(4,2),(5,2),(3,3),(4,3),(3,4),(4,4),(3,5),(4,5)),
 'down':((3,6),(4,6),(2,5),(3,5),(4,5),(5,5),(3,4),(4,4),(3,3),(4,3),(3,2),(4,2)),
 'left':((1,3),(1,4),(2,2),(2,3),(2,4),(2,5),(3,3),(4,3),(5,3),(3,4),(4,4),(5,4)),
 'right':((6,3),(6,4),(5,2),(5,3),(5,4),(5,5),(4,3),(3,3),(2,3),(4,4),(3,4),(2,4)),
}

# Each 8x8 menu icon is drawn over cyan. Characters identify colored pixels.
ICONS=(
 ("........",".BBBBBB.",".B...G B".replace(" ",""),".B.BB.B.",".B....B.",".BBB.BB.",".B...YB.",".BBBBBB."),
 ("...RR...","..RRRR..","...RR...","........",".R....R.","..R..R..","...GG...","..GGGG.."),
 ("........",".GGGG...","....G...",".GGGG...",".G......",".GGGG...",".....R..","........"),
 ("..R.....","...R..R.",".R......",".....R..","..R.....","........","...GG...","..GGGG.."),
 ("...B....","..BBB...",".BBBBB..","...B....","...B....","...B....","........","........"),
 ("........",".PPPP...","....P...",".PPP.P..",".P...P..",".PPPPP..",".....G..","........"),
)
DIGITS={
 3:("YYY","..Y",".YY","..Y","YYY"),
 2:("YYY","..Y","YYY","Y..","YYY"),
 1:(".Y.","YY.",".Y.",".Y.","YYY"),
}
ICON_COLORS={'B':BLUE,'G':GREEN,'R':RED,'Y':YELLOW,'P':PURPLE}

class Arcade:
    def __init__(self, rng=None):
        self.rng=rng or random.Random()
        self.selection=0; self.mode='menu'; self.game=None
        self.scores={name:0 for name in GAMES}
        self.score=0; self.elapsed=0.0; self.delay=0.35; self.countdown=0.0

    def start(self, name):
        if name not in GAMES: raise ValueError(name)
        self.game=name; self.mode='countdown'; self.countdown=0.0; self.score=0; self.elapsed=0.0
        self.player=(1,1); self.direction='right'; self.pending='right'
        self.snake=[(3,3)]; self.eaten=0; self.apples=[]
        self.trail=[(3,3)]; self.fall=(self.rng.randrange(8),0)
        self.player_x=3; self.target=self.rng.choice(tuple(VECTORS))
        self.round_time=0.0; self.delay=0.35
        if name=='Snake': self._refill_apples()
        if name=='Light Racer': self.direction='right'
        if name=='Joysticker': self.delay=2.0
        if name=='Marble Maze': self.delay=0.35

    def _refill_apples(self):
        desired=min(8,3+self.eaten//3)
        free=[(x,y) for y in range(8) for x in range(8)
              if (x,y) not in self.snake and (x,y) not in self.apples]
        self.rng.shuffle(free)
        self.apples.extend(free[:max(0,desired-len(self.apples))])

    def selected_best(self):
        return self.scores[GAMES[self.selection]]

    def end(self):
        if self.mode!='playing': return
        self.scores[self.game]=max(self.scores[self.game],self.score)
        self.mode='over'

    def input(self, direction):
        if self.mode=='menu':
            if direction in ('up','left'): self.selection=(self.selection-1)%len(GAMES)
            elif direction in ('down','right'): self.selection=(self.selection+1)%len(GAMES)
            elif direction=='middle': self.start(GAMES[self.selection])
            return
        if self.mode=='over':
            if direction=='middle': self.start(self.game)
            elif direction in ('left','up'): self.mode='menu'
            return
        if self.mode=='countdown':
            if direction=='middle': self.start(self.game)
            return
        if direction=='middle': self.start(self.game); return
        if direction not in VECTORS: return
        if self.game=='Marble Maze':
            dx,dy=VECTORS[direction]; x,y=self.player; nx,ny=x+dx,y+dy
            if 0<=nx<8 and 0<=ny<8 and MAZE[ny][nx]!='#':
                self.player=(nx,ny)
                if MAZE[ny][nx]=='G': self.score+=100; self.end()
        elif self.game in ('Snake','Light Racer'):
            if direction!=OPPOSITE[self.direction]: self.pending=direction
        elif self.game in ('Asteroid Dodge','Tetris Survival'):
            if direction=='left': self.player_x=max(0,self.player_x-1)
            if direction=='right': self.player_x=min(7,self.player_x+1)
        elif self.game=='Joysticker':
            if direction==self.target:
                self.score+=10; self.target=self.rng.choice(tuple(VECTORS)); self.round_time=0.0
            else: self.end()

    def tick(self, seconds):
        if self.mode=='countdown':
            self.countdown+=max(0,seconds)
            if self.countdown>=3.0:
                self.mode='playing'; self.elapsed=0.0
            return
        if self.mode!='playing': return
        if self.game=='Marble Maze': return
        self.elapsed+=seconds
        if self.game=='Joysticker':
            self.round_time+=seconds
            if self.round_time>=2.0: self.end()
            return
        while self.elapsed>=self.delay and self.mode=='playing':
            self.elapsed-=self.delay
            if self.game in ('Snake','Light Racer'):
                self.direction=self.pending
                dx,dy=VECTORS[self.direction]
                path=self.snake if self.game=='Snake' else self.trail
                x,y=path[-1]; new=(x+dx,y+dy)
                eating=self.game=='Snake' and new in self.apples
                occupied=path if self.game=='Light Racer' or eating else path[1:]
                if not (0<=new[0]<8 and 0<=new[1]<8) or new in occupied:
                    self.end(); break
                path.append(new)
                if self.game=='Snake':
                    if eating:
                        self.apples.remove(new); self.eaten+=1; self.score+=10
                        self._refill_apples()
                        if len(self.snake)==64: self.end()
                    else: path.pop(0)
                else: self.score+=1
            else:
                x,y=self.fall; y+=1
                if y==7 and x==self.player_x:
                    self.fall=(x,y); self.end(); break
                if y>7:
                    self.score+=1; self.fall=(self.rng.randrange(8),0)
                else: self.fall=(x,y)

    def frame(self):
        pixels=[CYAN]*64
        def put(x,y,color):
            if 0<=x<8 and 0<=y<8: pixels[y*8+x]=color
        if self.mode=='menu':
            for y,line in enumerate(ICONS[self.selection]):
                for x,c in enumerate(line):
                    if c in ICON_COLORS: put(x,y,ICON_COLORS[c])
            # Bottom-right selection indicator.
            put(7,7,YELLOW)
        elif self.mode=='countdown':
            digit=max(1,3-int(self.countdown))
            for y,line in enumerate(DIGITS[digit],start=1):
                for x,c in enumerate(line,start=2):
                    if c=='Y': put(x,y,YELLOW)
        elif self.game=='Marble Maze':
            for y,line in enumerate(MAZE):
                for x,c in enumerate(line):
                    if c=='#': put(x,y,BLUE)
                    elif c=='G': put(x,y,YELLOW)
            put(*self.player,GREEN)
        elif self.game=='Snake':
            for x,y in self.apples: put(x,y,RED)
            for x,y in self.snake: put(x,y,GREEN)
        elif self.game=='Light Racer':
            for x,y in self.trail: put(x,y,PURPLE)
            put(*self.trail[-1],GREEN)
        elif self.game in ('Tetris Survival','Asteroid Dodge'):
            put(*self.fall,RED)
            put(self.player_x,7,GREEN)
        elif self.game=='Joysticker':
            for x,y in ARROWS[self.target]: put(x,y,BLUE)
        if self.mode=='over':
            for x in range(8): put(x,0,RED); put(x,7,RED)
        return pixels
