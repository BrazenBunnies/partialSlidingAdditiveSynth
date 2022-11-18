# Preston Steimel
# 11/15/2022
# Generator class
# Herein lies the majority of the work

from pyo import *
from modes import *

class Generator():
    def __init__(self, note, env):
        self.note = note
        self.freq = midiToHz(note)
        self.env = env
        self.naturalPartials = []
        self.fundamental = Sine(self.freq, mul=self.env)
        for multi in naturalList:
            self.naturalPartials.append(Sine(self.freq*multi, 
            mul=self.env/multi).out())
        self.changedPartials = []
        self.mode = 'Target'
    
    def changeMode(self, mode):
        self.mode = mode
    
    def updateFreq(self):
        self.freq = midiToHz(self.note)
        self.fundamental.freq = self.freq
        for multi in naturalList:
            self.naturalPartials[multi-2].freq = self.freq*multi