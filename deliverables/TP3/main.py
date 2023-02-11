# Preston Steimel
# 11/15/2022
# main
# runs the program

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
    app.margin = app.width/50
    app.modesX, app.modesY = app.width/10, app.height/10
    app.lineWidth = 2
    
    # colors
    app.bg = 'RoyalBlue3'
    app.buttonColor = 'RoyalBlue2'
    app.lineColor = 'RoyalBlue4'
    app.accentColor = 'yellow'
    app.fontColor = 'white'
    
    # modes
    app.deharmModes = [target, switch, extend, random, powers, primes]
    app.deharmMode = target
    
    app.waveformModes = [saw, square, triangle, threeSpike, sine, custom]
    app.waveformMode = saw
    
    # create voice
    app.env = Adsr(attack=0.01, decay=0.5, sustain=0.2, release=0.4,
    dur=1.11, mul = 0.7)
    app.portaTime = 0.1

    app.voice = Voice(69, app.env, app.portaTime, app.deharmMode,
                      app.waveformMode)
    app.octave = 4
    
    # draw modes
    modeX, modeY = app.margin, app.margin
    modeW, modeH = app.width/6, app.height/12
    
    app.modeHeader = Button(app, modeX, modeY, modeW, modeH, 'Deharmonization',
                            dummy, active=False)
    app.deharmMenu = Dropdown(app, modeX, modeY+modeH, modeW/2, modeH,
                            app.deharmMode, app.deharmModes)
    
    smallW = (app.modeHeader.x1 - app.deharmMenu.x1)/4
    app.modeIncr = Button(app, app.deharmMenu.x1, modeY+modeH, smallW, modeH,
                          '-', decrModeVal, fontColor=app.accentColor)
    app.modeVal = Button(app, app.modeIncr.x1, modeY+modeH, smallW*2, modeH,
                         app.deharmMode.value, dummy, active=False)
    app.modeDecr = Button(app, app.modeVal.x1, modeY+modeH, smallW, modeH, '+',
                          incrModeVal, fontColor=app.accentColor)
    
    app.percSlider = Slider(app, modeX, app.modeVal.y1+app.margin/3, modeW/6,
                            modeH/2, modeW, '', 'x', 1.0)
    app.perc0 = Button(app, modeX, app.percSlider.y1+app.margin/3, modeW/3,
                       modeH*2/3, 'b: 0.0', app.voice.updatePerc, color='white',
                       fontColor='black')
    app.perc50 = Button(app, modeX+modeW/3, app.percSlider.y1+app.margin/3,
                        modeW/3, modeH*2/3, 'n: 0.5', app.voice.updatePerc,
                        color='white', fontColor='black')
    app.perc100 = Button(app, modeX+modeW*2/3, app.percSlider.y1+app.margin/3,
                         modeW/3, modeH*2/3, 'm: 1.0', app.voice.updatePerc,
                         color='white', fontColor='black')
    
    # portamento slider
    app.portaSlider = Slider(app, app.margin, app.height-app.margin*2-modeH/2,
                             modeW/6, modeH/2, modeW, 'Portamento', 'x', 1.0)
    app.portaSlider.setValue(app.portaTime)
    
    # ADSR section
    adsrY = app.portaSlider.y0 - app.margin*3
    adsrL = adsrY - app.percSlider.y1 - app.margin
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
        
    # waveform shaping
    app.waveformHeader = Button(app, app.modeHeader.x1+app.margin, modeY,
                                modeW*2/3, modeH, 'Waveform', dummy,
                                active=False)
    app.waveformMenu = Dropdown(app, app.waveformHeader.x1, modeY, modeW/2,
                                modeH, app.waveformMode, app.waveformModes)
    app.waveSliders = SliderArray(app, app.modeHeader.x1+app.margin,
                                  app.attack.startY, (app.attack.startY-
                                  app.modeHeader.y1-app.margin),
                                  partialCount)
    
    app.waveformModes[-1].amps = app.waveSliders.sliderVals
    
    # keyboard inputs
    inputx0 = app.waveSliders.x0
    inputy0 = app.waveSliders.y1 + app.margin
    inputH = (app.height - app.margin - inputy0)/2
    app.octHead = Button(app, inputx0, inputy0, modeW/2, inputH, 'Octave',
                         dummy, active=False)
    app.octVal = Button(app, app.octHead.x1, inputy0, inputH, inputH,
                        app.octave, dummy, active=False)
    app.octDecr = Button(app, inputx0, inputy0+inputH,
                         (app.octVal.x1-inputx0)/2, inputH, 'z: -', dummy,
                         color='white', fontColor='black')
    app.octIncr = Button(app, (app.octVal.x1+inputx0)/2, inputy0+inputH,
                         (app.octVal.x1-inputx0)/2, inputH, 'x: +', dummy,
                         color='white', fontColor='black')
    
    keyW = (app.waveSliders.x1-app.octVal.x1-app.margin)/11
    keyx0 = app.octVal.x1 + app.margin
    app.whiteKeyButtons = []
    app.blackKeyButtons = []
    for key in app.whiteKeys:
        app.whiteKeyButtons.append(Button(app, keyx0+keyW*app.whiteKeys[key][1],
                                   inputy0+inputH, keyW, inputH, key, dummy,
                                   color='white', fontColor='black'))
    for key in app.blackKeys:
        app.blackKeyButtons.append(Button(app,
                                   keyx0+keyW*(app.blackKeys[key][1]-.5),
                                   inputy0, keyW, inputH, key, dummy,
                                   color='black'))
    
    # spectrum analyzer
    app.specx0 = int(app.waveSliders.x1+app.margin*2)
    app.specx1 = int(app.width-app.margin)
    app.specy0, app.specy1 = app.margin, app.height - app.margin
    
    app.timerDelay = 10
    defaultVals = app.voice.canvasLogList(app.specy0, app.specy1)
    app.timeSamples = 50
    app.sampleLength = (app.specx1 - app.specx0)/app.timeSamples
    app.specVals = [(defaultVals+[]) for time in range(app.timeSamples+1)]
    
    # interactives list
    app.menus = [app.deharmMenu, app.waveformMenu]
    app.percButtons = [app.perc0, app.perc50, app.perc100]
    app.drawButtons = [app.modeHeader, app.modeIncr, app.modeVal, app.modeDecr,
                       app.waveformHeader, app.perc0, app.perc50, app.perc100,
                       app.octHead, app.octVal, app.octDecr, app.octIncr,
                       app.deharmMenu, app.waveformMenu]
    app.sliders = [app.percSlider, app.attack, app.decay, app.sustain,
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