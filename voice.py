# Preston Steimel
# 11/15/2022
# Voice class
# Herein lies the majority of the work

from pyo import *
from modes import *

class Voice():
    def __init__(self, note, env):
        # notes correspond to frequencies
        self.porta = 0.1
        self.env = env
        
        self.note = note
        self.freq = midiToHz(note)
        self.partials = []
        
        # create fundamental
        self.fundamental = Sine(SigTo(self.freq, time=self.porta),
                                mul=self.env).out()
        
        # create partials
        for i in range(partialCount):
            multi = natPartials[i]
            self.partials.append(Sine(self.freq*multi, 
                                 mul=self.env/multi).out())
        self.changedPartials = []
        self.mode = 'Target'
    
    def updateFreq(self):
        prevFund = self.freq
        self.freq = midiToHz(self.note)
        self.fundamental.setFreq(SigTo(self.freq, time=self.porta,
                                 init=prevFund))
        
        for i in range(partialCount):
            prevPartial = prevFund*natPartials[i]
            if self.freq*natPartials[i] > 20000:
                self.partials[i].mul = 0
            else: self.partials[i].mul = self.env/natPartials[i]
            self.partials[i].setFreq(SigTo(self.freq*natPartials[i],
            time=self.porta, init=prevPartial))
    
    def updatePortaTime(self):
        pass