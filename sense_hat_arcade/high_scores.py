"""Persistent scores, kept separate from the Sense HAT device."""
import json
import os
import tempfile

class HighScores:
    def __init__(self, path=None):
        self.path=path or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'high_scores.json')
        self.scores={}
        self.load()

    def load(self):
        try:
            with open(self.path, encoding='utf-8') as f:
                data=json.load(f)
            if isinstance(data,dict):
                self.scores={k:v for k,v in data.items() if isinstance(k,str) and type(v) is int and v>=0}
        except (OSError,ValueError,TypeError):
            self.scores={}

    def best(self, game, difficulty):
        return self.scores.get(game+':'+difficulty,0)

    def record(self, game, difficulty, score):
        key=game+':'+difficulty
        if type(score) is not int or score<=self.best(game,difficulty): return False
        self.scores[key]=score
        directory=os.path.dirname(os.path.abspath(self.path))
        temp_path=None
        try:
            with tempfile.NamedTemporaryFile('w',encoding='utf-8',dir=directory,delete=False) as f:
                temp_path=f.name
                json.dump(self.scores,f,indent=2,sort_keys=True)
                f.write('\n')
            os.replace(temp_path,self.path)
        finally:
            if temp_path and os.path.exists(temp_path): os.unlink(temp_path)
        return True
