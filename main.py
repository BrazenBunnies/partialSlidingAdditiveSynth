# Preston Steimel
# 11/15/2022
# main

from voice import *
from view import *

s = Server().boot()
s.amp = 0.7

def appStarted(app):
    # create voices
    app.env = Adsr(attack=0.01, decay=0.1, sustain=1.8, release=1.2,
    dur=3.01, mul = 0.7)
    app.portaTime = 0.1
    
    app.voiceCount = 1
    app.voices = []
    for voice in range(app.voiceCount):
        app.voices.append(Voice(69, app.env))
    
    app.octave = 4
    
    # piano key dictionary
    app.whiteKeys = {'a':[60,0], 's':[62,1], 'd':[64,2], 'f':[65,3],
                     'g':[67,4], 'h':[69,5], 'j':[71,6], 'k':[72,7],
                     'l':[74,8], ';':[76,9], "'":[77,10]}
    # index 1 in the lists are more for graphics placement than actually index
    app.blackKeys = {'w':[61,1], 'e':[63,2], 't':[66,4], 'y':[68,5],
                     'u':[70,6], 'o':[73,8], 'p':[75,9]}
    
    # canvas attributes
    app.width = 1000
    app.height = 500
    app.margin = app.width//100
    
    # misc attributes
    app.lowFreq, app.highFreq = 20, 20000
    
    # start audio server
    s.gui(locals())

def runSynth():
    print('_'*50)
    print('Running Partial Sliding Additive Synthesizer!')
    print()
    runApp(width=1000, height=500, title='Slidittive')

def main():
    runSynth()

main()