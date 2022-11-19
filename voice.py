# Preston Steimel
# 11/15/2022
# Voice class
# Herein lies the majority of the work

from pyo import *
from modes import *

class Voice():
    def __init__(self, note, env):
        # notes correspond to frequencies
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
    
    def updateFreq(self):
        prevFund = self.freq
        self.freq = midiToHz(self.note)
        self.fundamental.freq = self.freq
        for i in range(partialCount):
            # self.naturalPartials[partialCount].freq = self.freq*multi
            prevPartial = prevFund*naturalList[i]
            self.naturalPartials[i].freq = SigTo(self.freq*naturalList[i],
            time=0.1, init=prevPartial)