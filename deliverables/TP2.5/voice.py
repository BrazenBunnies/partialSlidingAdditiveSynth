# Preston Steimel
# 11/15/2022
# Voice class
# Herein lies the majority of the work

from pyo import *
from deharmModes import *
import math

class Voice():
    def __init__(self, note, env, porta, deharmMode):
        # notes correspond to frequencies
        self.env = env
        self.porta = porta
        
        self.note = note
        self.freq = midiToHz(note)
        self.partials = []
        self.deharmMode = deharmMode
        
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
        self.fundamental.freq.setValue(self.freq)
        
        for i in range(partialCount):
            # amplitude low too quick, maybe just use a filter at 20k
            if self.freq*self.deharmMode.partials[i] > 20000:
                self.partials[i].mul = 0
            else: self.partials[i].mul = self.env/natPartials[i]
            self.partials[i].freq.setValue(self.freq*
                                           self.deharmMode.partials[i])
    
    def setMode(self, mode):
        if isinstance(mode, DeharmMode):
            self.deharmMode = mode
    
    def updatePortaTime(self, time):
        self.fundamental.freq.setTime(time)
        for partial in self.partials:
            partial.freq.setTime(time)
    
    def canvasLogList(self, y0, y1):
        canvasLog = []
        yRange = y1 - y0
        lowLog = math.log(20, 10)
        highLog = math.log(20000, 10)
        converted = math.log(self.fundamental.freq.value, 10)
        fundY = y1 - yRange*(converted-lowLog)/(highLog-lowLog)
        canvasLog.append(int(fundY))
        for partial in self.partials:
            freq = partial.freq.value
            converted = math.log(freq, 10)
            partialY = y1 - (yRange*(converted-lowLog)/(highLog-lowLog))
            canvasLog.append(int(partialY))
        return canvasLog