# Preston Steimel
# 11/15/2022
# Generator class
# Herein lies the majority of the work

from pyo import *
from modes import *

class Generator():
    def __init__(self, freq, env):
        self.freq = freq
        self.env = env
        self.naturalPartials = []
        for multi in naturalList:
            self.naturalPartials.append(Sine(self.freq*multi, 
            mul=self.env/multi).out())
        self.changedPartials = []
        self.mode = 'Target'
    
    def changeMode(self, mode):
        self.mode = mode