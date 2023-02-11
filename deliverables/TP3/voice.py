# Preston Steimel
# 11/15/2022
# Voice class
# creates all the sine waves to be added together

from pyo import *
from modes import *
import math

class Voice():
    def __init__(self, note, env, porta, deharmMode, waveformMode):
        # notes correspond to frequencies
        self.env = env
        self.porta = porta
        
        self.note = note
        self.freq = midiToHz(note)
        self.partials = []
        self.deharmMode = deharmMode
        self.perc = 0.0
        
        self.waveformMode = waveformMode
        
        # create fundamental
        self.fundamental = Sine(SigTo(self.freq, time=self.porta),
                                mul=self.env)
                
        # create partials
        for i in range(partialCount):
            multi = natPartials[i]
            self.partials.append(Sine(SigTo(self.freq*multi, time=self.porta), 
                                 mul=self.env/multi))
        
        # put all waves through a 20k Hz lowpass to avoid stupidity
        self.output = Tone([self.fundamental]+self.partials, 20000).out()
    
    # update all of the frequncies of each partial
    # according to fundamental and deharmonization
    def updateFreq(self):
        self.freq = midiToHz(self.note)
        self.fundamental.freq.setValue(self.freq)
        
        for i in range(partialCount):
            self.partials[i].freq.setValue(self.freq*self.ratio(i))
    
    def updatePerc(self, perc):
        self.perc = perc
        self.updateFreq()
    
    def updateWaveform(self):
        for i in range(partialCount):
            self.partials[i].mul = (self.waveformMode.amps[i]*
                                    self.env/natPartials[i])
    
    def setMode(self, mode):
        if isinstance(mode, DeharmMode):
            self.deharmMode = mode
        elif isinstance(mode, WaveformMode):
            self.waveformMode = mode
    
    def updatePortaTime(self, time):
        self.fundamental.freq.setTime(time)
        for partial in self.partials:
            partial.freq.setTime(time)
    
    def ratio(self, i):
        return natPartials[i]+self.perc*(self.deharmMode.ref[i]-natPartials[i])
    
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