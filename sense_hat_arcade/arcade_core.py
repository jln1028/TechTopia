"""Hardware-independent 8x8 Sense HAT Arcade game rules."""
import random

BLACK=(0,0,0); GREEN=(0,220,0); RED=(230,20,20)
YELLOW=(255,230,0); BLUE=(0,60,220); BROWN=(130,65,20)
GRAY=(90,90,90); WHITE=(180,180,180)

class ArcadeMenu:
    names=('tetris','jumpy','flood')
    def __init__(self): self.selection=0
    def handle(self,direction):
        if direction in ('right','down'): self.selection=(self.selection+1)%3
        elif direction in ('left','up'): self.selection=(self.selection-1)%3
        elif direction=='middle': return self.names[self.selection]
        return None

class TetrisGame:
    interval=0.35
    def __init__(self,seed=None):
        self.rng=random.Random(seed); self.x=3; self.health=5; self.score=0
        self.crushers=[]; self.bullets=[]; self.ground=set(); self.ticks=0; self.status='playing'
    def crusher_size(self): return min(3,1+self.score//20)
    def _damage(self):
        self.health=max(0,self.health-1); self.score=max(0,self.score-2)
        if not self.health: self.status='lost'
    def _touch_ground(self):
        if self.x in self.ground:
            self.ground.remove(self.x); self._damage()
    def handle(self,direction):
        if self.status!='playing': return
        if direction=='left': self.x=max(0,self.x-1)
        elif direction=='right': self.x=min(7,self.x+1)
        elif direction in ('up','middle'): self.bullets.append((self.x,6))
        self._touch_ground()
    def step(self):
        if self.status!='playing': return
        self.ticks+=1
        if self.ticks%max(2,round(5*getattr(self,'spawn_factor',1.0)))==0:
            size=self.crusher_size()
            self.crushers.append({'x':self.rng.randint(0,8-size),'y':0,'size':size})
        # Move bullets first; a bullet can hit at its starting or next position.
        surviving=[]
        for bx,by in self.bullets:
            hit=False
            for ny in (by,by-1):
                for c in list(self.crushers):
                    if c['x']<=bx<c['x']+c['size'] and c['y']<=ny<c['y']+c['size']:
                        self.crushers.remove(c); self.score+=5; hit=True; break
                if hit: break
            if not hit and by>0: surviving.append((bx,by-1))
        self.bullets=surviving
        remaining=[]
        for c in self.crushers:
            c['y']+=1
            if c['y']+c['size']>7:
                for col in range(max(0,c['x']),min(8,c['x']+c['size'])):
                    self.ground.add(col)
                self.score+=1
            else: remaining.append(c)
        self.crushers=remaining
        self._touch_ground()
    def pixels(self):
        out=[(x,7,GRAY) for x in self.ground]
        for c in self.crushers:
            out += [(x,y,RED) for x in range(c['x'],c['x']+c['size']) for y in range(c['y'],c['y']+c['size']) if 0<=x<8 and 0<=y<8]
        out += [(x,y,YELLOW) for x,y in self.bullets if 0<=y<8]
        out.append((self.x,7,GREEN))
        return out

class JumpyGame:
    interval=0.22
    def __init__(self,seed=None):
        self.rng=random.Random(seed); self.x=2; self.y=7
        self.jump_phase=0; self.obstacles=[]; self.ticks=0
        self.health=3; self.score=0; self.status='playing'
    def handle(self,direction):
        if self.status!='playing': return
        if direction=='up' and self.jump_phase==0:
            self.jump_phase=1
    def step(self):
        if self.status!='playing': return
        self.ticks+=1
        # 6-frame arc, including time on top of approaching cubes.
        arc=(6,5,5,6,6,7)
        if self.jump_phase:
            self.y=arc[self.jump_phase-1]
            self.jump_phase=(self.jump_phase%6)+1
            if self.jump_phase==1: self.jump_phase=0; self.y=7
        else: self.y=7
        if self.ticks%max(3,round(8*getattr(self,'spawn_factor',1.0)))==0: self.obstacles.append(7)
        moved=[x-1 for x in self.obstacles if x-1>=0]
        if self.x in moved:
            if self.y==7:
                self.health-=1; self.obstacles=[]
                if self.health<=0: self.status='lost'
                return
            elif self.y==6:
                self.score+=3  # landed on top
        self.obstacles=moved
        self.score+=1  # survival points
    def pixels(self):
        return [(x,7,RED) for x in self.obstacles]+[(self.x,self.y,GREEN)]

class FloodGame:
    interval=0.23
    def __init__(self,seed=None):
        self.x=1; self.y=6; self.jump_remaining=0; self.ticks=0
        self.water=8; self.score=0; self.status='playing'
        self.platforms={(1,7):'safe',(3,6):'danger',(5,5):'safe',
                        (3,4):'danger',(1,3):'safe',(3,2):'safe',(5,1):'safe'}
        self.collapse={}; self.coins={(3,5),(5,4),(3,3),(1,2),(5,0)}
        self.total_coins=len(self.coins)
    def handle(self,direction):
        if self.status!='playing': return
        if direction in ('left','right'):
            nx=max(0,min(7,self.x+(-1 if direction=='left' else 1)))
            if (nx,self.y) not in self.platforms: self.x=nx
        elif direction=='up' and self.jump_remaining==0 and (self.x,self.y+1) in self.platforms:
            self.jump_remaining=3
    def step(self):
        if self.status!='playing': return
        self.ticks+=1
        if self.jump_remaining:
            ny=max(0,self.y-1)
            if (self.x,ny) not in self.platforms: self.y=ny
            self.jump_remaining-=1
        elif self.y<7 and (self.x,self.y+1) not in self.platforms:
            self.y+=1
        support=(self.x,self.y+1)
        if support in self.platforms and self.platforms[support]=='danger':
            self.collapse[support]=self.collapse.get(support,0)+1
        for p in list(self.collapse):
            if p!=support: continue
            if self.collapse[p]>=3:
                self.platforms.pop(p,None); self.collapse.pop(p,None)
        if (self.x,self.y) in self.coins:
            self.coins.remove((self.x,self.y)); self.score+=1
            if not self.coins:
                self.status='won'; return
        if self.ticks%max(8,round(35*getattr(self,'water_factor',1.0)))==0: self.water=max(0,self.water-1)
        if self.y>=self.water: self.status='lost'
    def pixels(self):
        out=[(x,y,BLUE) for y in range(self.water,8) for x in range(8)]
        out += [(x,y,BROWN if kind=='safe' else RED) for (x,y),kind in self.platforms.items()]
        out += [(x,y,YELLOW) for x,y in self.coins]
        out.append((self.x,self.y,GREEN))
        return out

DIFFICULTIES=('easy','normal','hard')
DIFFICULTY_SETTINGS={
    'easy': {'interval_factor':1.25,'spawn_factor':1.5,'water_factor':1.5},
    'normal': {'interval_factor':1.0,'spawn_factor':1.0,'water_factor':1.0},
    'hard': {'interval_factor':0.8,'spawn_factor':0.75,'water_factor':0.75},
}

class ArcadeController:
    """Hardware-independent menu flow. Screen: games -> difficulty -> playing -> result."""
    def __init__(self):
        self.screen='games'
        self.game_index=0
        self.difficulty_index=1
        self.game=None
        self.game_name=None
        self.difficulty=None

    @property
    def selected_game(self):
        return ArcadeMenu.names[self.game_index]

    @property
    def selected_difficulty(self):
        return DIFFICULTIES[self.difficulty_index]

    def handle(self, direction):
        if self.screen=='games':
            if direction in ('right','down'): self.game_index=(self.game_index+1)%3
            elif direction in ('left','up'): self.game_index=(self.game_index-1)%3
            elif direction=='middle': self.screen='difficulty'
        elif self.screen=='difficulty':
            if direction in ('right','up'): self.difficulty_index=(self.difficulty_index+1)%3
            elif direction in ('left','down'): self.difficulty_index=(self.difficulty_index-1)%3
            elif direction=='middle': self.start()
        elif self.screen=='result':
            if direction=='middle': self.start()
            elif direction in ('left','down'): self.screen='games'; self.game=None
            elif direction in ('right','up'): self.screen='difficulty'; self.game=None
        elif self.screen=='playing':
            if direction=='middle':
                self.screen='result'  # pause/exit current game, with restart option
            else:
                self.game.handle(direction)
        return self.screen

    def start(self):
        self.game_name=self.selected_game
        self.difficulty=self.selected_difficulty
        cls={'tetris':TetrisGame,'jumpy':JumpyGame,'flood':FloodGame}[self.game_name]
        self.game=cls()
        settings=DIFFICULTY_SETTINGS[self.difficulty]
        self.game.interval*=settings['interval_factor']
        self.game.spawn_factor=settings['spawn_factor']
        self.game.water_factor=settings['water_factor']
        self.screen='playing'

    def step(self):
        if self.screen!='playing': return
        self.game.step()
        if self.game.status!='playing': self.screen='result'
