# Preston Steimel
# 11/15/2022
# main

from generators import *
from eventHandling import *

s = Server().boot()

def appStarted(app):
    app.voiceCount = 1
    app.voices = []
    app.env = Adsr(attack=0.01, decay=0.1, sustain=2.8, release=1.2,
    dur=4, mul = 0.7)
    for voice in range(app.voiceCount):
        app.voices.append(Generator(69, app.env))
    s.gui(locals())

def runSynth():
    print('_'*50)
    print('Running Partial Sliding Additive Synthesizer!')
    runApp(width=500, height=500)

def main():
    runSynth()

main()