# Preston Steimel
# 11/15/2022
# main

from generators import *
from eventHandling import *

s = Server().boot()

def appStarted(app):
    app.env = Adsr(attack=0.01, decay=0.1, sustain=2.8, release=1.2,
    dur=4, mul = 0.7)
    app.freq = 440.0
    app.voice = Generator(app.freq, app.env)
    s.gui(locals())

def runSynth():
    print('Running Partial Sliding Additive Synthesizer!')
    runApp(width=500, height=500)

def main():
    runSynth()

main()