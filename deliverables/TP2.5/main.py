# Preston Steimel
# 11/15/2022
# main

from voice import *
from view import *

s = Server(buffersize=256).boot()
s.amp = 0.7

def appStarted(app):
    # piano key dictionary
    # maybe make these all buttons...
    app.whiteKeys = {"a":[60,0], "s":[62,1], "d":[64,2], "f":[65,3],
                     "g":[67,4], "h":[69,5], "j":[71,6], "k":[72,7],
                     "l":[74,8], ";":[76,9], "'":[77,10]}
    # indices in the lists are more for graphics placement than actually index
    app.blackKeys = {"w":[61,1], "e":[63,2], "t":[66,4], "y":[68,5],
                     "u":[70,6], "o":[73,8], "p":[75,9]}
    
    # canvas attributes
    app.timerDelay = 50
    app.margin = app.width/50
    app.modesX, app.modesY = app.width/10, app.height/10
    app.lineWidth = 2
    
    # colors
    app.bg = 'RoyalBlue3'
    app.buttonColor = 'RoyalBlue2'
    app.lineColor = 'RoyalBlue4'
    app.accentColor = 'yellow'
    app.fontColor = 'white'
    app.interNeut = 'RoyalBlue2'
    app.interClic = 'RoyalBlue1'
    
    # modes
    app.modes = [target, switch, extend, random, powers, primes]
    app.deharmMode = target
    
    modeX, modeY = app.margin, app.margin
    modeW, modeH = app.width/5, app.height/12
    
    app.modeHeader = Button(app, modeX, modeY, modeW, modeH, 'Deharmonization',
                            dummy, active=False)
    app.modeMenu = Dropdown(app, modeX, modeY+modeH, modeW/2, modeH,
                            app.deharmMode, app.modes)
    
    smallW = (app.modeHeader.x1 - app.modeMenu.x1)/4
    app.modeIncr = Button(app, app.modeMenu.x1, modeY+modeH, smallW, modeH, '-',
                          decrModeVal, fontColor=app.accentColor)
    app.modeVal = Button(app, app.modeIncr.x1, modeY+modeH, smallW*2, modeH,
                         app.deharmMode.value, dummy, active=False)
    app.modeDecr = Button(app, app.modeVal.x1, modeY+modeH, smallW, modeH, '+',
                          incrModeVal, fontColor=app.accentColor)
    
    app.modeSlider = Slider(app, modeX, app.modeVal.y1+app.margin/3, modeW/8,
                            modeH/2,modeW, 'Amount', 'x', 1.0)
    
    # create voices
    app.env = Adsr(attack=0.01, decay=0.5, sustain=0.5, release=1.2,
    dur=1.8, mul = 0.7)
    app.portaTime = 0.1

    app.voice = Voice(69, app.env, app.portaTime, app.deharmMode)
    app.octave = 4
    
    # ADSR section
    adsrY = app.height*2/3
    adsrL = app.height*2/5
    adsrW, adsrH = modeW/15, app.height/24
    app.attack = Slider(app, app.margin, adsrY, adsrW*3, adsrH, adsrL, 'A', 'y',
                        2.0)
    app.decay = Slider(app, app.attack.x1+adsrW, adsrY, adsrW*3, adsrH, adsrL,
                       'D', 'y', 4.0)
    app.sustain = Slider(app, app.decay.x1+adsrW, adsrY, adsrW*3, adsrH, adsrL,
                         'S', 'y', 1.0)
    app.release = Slider(app, app.sustain.x1+adsrW, adsrY, adsrW*3, adsrH,
                         adsrL, 'R', 'y', 4.0)
    app.attack.setValue(app.env.attack)
    app.decay.setValue(app.env.decay)
    app.sustain.setValue(app.env.sustain)
    app.release.setValue(app.env.release)
    
    # portamento slider
    app.portaSlider = Slider(app, app.margin, app.attack.y1+app.margin*3/2,
                             modeW/8, modeH/2, modeW, 'Portamento', 'x', 1.0)
    app.portaSlider.setValue(app.portaTime)
        
    # spectrum analyzer
    app.specx0 = int(app.width*3/4-app.margin)
    app.specx1 = int(app.width-app.margin)
    app.specy0, app.specy1 = app.margin, app.height - app.margin
    
    defaultVals = app.voice.canvasLogList(app.specy0, app.specy1)
    app.timeSamples = 50
    app.sampleLength = (app.specx1 - app.specx0)//app.timeSamples
    app.specVals = [(defaultVals+[]) for time in range(app.timeSamples+1)]
    
    # interactives list
    app.buttons = [app.modeMenu]
    app.drawButtons = [app.modeHeader, app.modeMenu, app.modeIncr, app.modeVal,
                       app.modeDecr]
    app.sliders = [app.modeSlider, app.attack, app.decay, app.sustain,
                   app.release, app.portaSlider]
    
    # start audio server
    s.start()

def appStopped(app):
    # stop audio server
    s.stop()    

def runSynth():
    print('_'*50)
    print('Running Deharmonizing Additive Synthesizer!')
    print()
    runApp(width=1000, height=500, title='Deharmonizing Additive Synthesizer')

def main():
    runSynth()

main()