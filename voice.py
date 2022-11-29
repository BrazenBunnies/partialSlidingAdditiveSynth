# Preston Steimel
# 11/15/2022
# Voice class
# Herein lies the majority of the work

from pyo import *
from deharmModes import *

class Voice():
    def __init__(self, note, env, porta):
        # notes correspond to frequencies
        self.env = env
        self.porta = porta
        
        self.note = note
        self.freq = midiToHz(note)
        self.partials = []
        self.deharmMode = primes
        
        # create fundamental
        self.fundamental = Sine(SigTo(self.freq, time=self.porta),
                                mul=self.env).out()
        
        # create partials
        for i in range(partialCount):
            multi = natPartials[i]
            self.partials.append(Sine(SigTo(self.freq*multi, time=self.porta), 
                                 mul=self.env/multi).out())
    
    # update all of the frequncies of each partial
    # according to fundamental and deharmonization
    def updateFreq(self):
        self.freq = midiToHz(self.note)
        self.fundamental.freq.setValue(self.freq)   # tapping the SigTo value
        
        for i in range(partialCount):
            # amplitude low too quick, maybe just use a filter at 20k
            if self.freq*self.deharmMode.partials[i] > 20000:
                self.partials[i].mul = 0
            else: self.partials[i].mul = self.env/natPartials[i]
            self.partials[i].freq.setValue(self.freq*self.deharmMode.partials[i])
    
    def setMode(self, mode):
        if isinstance(mode, DeharmMode):
            self.deharmMode = mode
    
    def updatePortaTime(self):
        pass