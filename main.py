# Preston Steimel
# 11/15/2022
# main

from voice import *
from view import *

s = Server().boot()

def appStarted(app):
    # create voices
    app.voiceCount = 1
    app.voices = []
    app.env = Adsr(attack=0.01, decay=0.1, sustain=1.8, release=1.2,
    dur=3.01, mul = 0.7)
    for voice in range(app.voiceCount):
        app.voices.append(Voice(69, app.env))
    
    # start audio server
    s.gui(locals())

def runSynth():
    print('_'*50)
    print('Running Partial Sliding Additive Synthesizer!')
    runApp(width=500, height=500)

def main():
    runSynth()

main()