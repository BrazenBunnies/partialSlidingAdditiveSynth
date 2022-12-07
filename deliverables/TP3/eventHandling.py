# Preston Steimel
# 11/15/2022
# Handles all the event calls
# Key and mouse presses, MIDI Input
# CONTROLLER in MVC

from interactives import *

# qwerty keyboard input
def keyPressed(app, event):
    # piano keys
    if event.key in app.whiteKeys:
        app.voice.note = app.whiteKeys[event.key][0]
        app.voice.updateFreq()
        app.env.play()
    if event.key in app.blackKeys:
        app.voice.note = app.blackKeys[event.key][0]
        app.voice.updateFreq()
        app.env.play()
    
    # octave keys
    if event.key == 'z':
        if app.octave > 1:
            app.octave -= 1
            for key in app.whiteKeys:
                app.whiteKeys[key][0] -= 12
            for key in app.blackKeys:
                app.blackKeys[key][0] -= 12
    if event.key == 'x':
        if app.octave < 7:
            app.octave += 1
            for key in app.whiteKeys:
                app.whiteKeys[key][0] += 12
            for key in app.blackKeys:
                app.blackKeys[key][0] += 12
    app.octVal.label = app.octave
    
    # testing the modes using b n m
    if event.key == 'b':
        app.percSlider.setValue(0.0)
    if event.key == 'n':
        app.percSlider.setValue(0.5)
    if event.key == 'm':
        app.percSlider.setValue(1.0)
    
    app.voice.updatePerc(app.percSlider.value)
    app.voice.updateFreq()

def mousePressed(app, event):
    # when mode menu is opened, if a child is pressed,
    # update the label, the deharm mode, the voice mode, and the mode value
    
    # deharm menu
    if app.deharmMenu.wasPressed(event.x, event.y):
        app.deharmMenu.action()
        app.deharmMode = app.deharmMenu.label
        app.modeVal.label = app.deharmMode.value
        app.voice.setMode(app.deharmMode)
    else:
        if app.deharmMenu.open:
            app.deharmMenu.action()
        # these elements need to be in the else so they are only
        # activated if they have priority
        for slider in app.sliders:
            if slider.wasPressed(event.x, event.y):
                slider.action(event.x, event.y)
        if app.perc0.wasPressed(event.x, event.y):
            app.percSlider.setValue(0.0)
        if app.perc50.wasPressed(event.x, event.y):
            app.percSlider.setValue(0.5)
        if app.perc100.wasPressed(event.x, event.y):
            app.percSlider.setValue(1.0)
    app.voice.updatePerc(app.percSlider.value)
    
    # waveform menu
    if app.waveformMenu.wasPressed(event.x, event.y):
        app.waveformMenu.action()
        app.waveformMode = app.waveformMenu.label
        app.voice.setMode(app.waveformMode)
        app.voice.updateWaveform()
    else:
        if app.waveformMenu.open:
            app.waveformMenu.action()
        # same deal as before with the priority
        if app.waveSliders.wasPressed(event.x, event.y):
            app.waveSliders.action(event.x, event.y)
            app.waveformMode = app.waveformModes[-1]
            app.voice.setMode(app.waveformMode)
            app.waveformMenu.label = app.waveformMode
    
    app.waveSliders.updateAllVals(app.waveformMode.amps)
    
    # other buttons
    # modes increment
    if app.modeDecr.wasPressed(event.x, event.y):
        app.modeDecr.action(app.deharmMode)
        app.modeVal.label = app.deharmMode.value
    if app.modeIncr.wasPressed(event.x, event.y):
        app.modeIncr.action(app.deharmMode)
        app.modeVal.label = app.deharmMode.value
    # octaves increment
    if app.octDecr.wasPressed(event.x, event.y):
        if app.octave > 1:
            app.octave -= 1
            for key in app.whiteKeys:
                app.whiteKeys[key][0] -= 12
            for key in app.blackKeys:
                app.blackKeys[key][0] -= 12
    if app.octIncr.wasPressed(event.x, event.y):
        if app.octave < 7:
            app.octave += 1
            for key in app.whiteKeys:
                app.whiteKeys[key][0] += 12
            for key in app.blackKeys:
                app.blackKeys[key][0] += 12
    app.octVal.label = app.octave
    # keys
    for key in app.whiteKeyButtons:
        if key.wasPressed(event.x, event.y):
            app.voice.note = app.whiteKeys[key.label][0]
            app.voice.updateFreq()
            app.env.play()
    for key in app.blackKeyButtons:
        if key.wasPressed(event.x, event.y):
            app.voice.note = app.blackKeys[key.label][0]
            app.voice.updateFreq()
            app.env.play()

def mouseDragged(app, event):
    for slider in app.sliders:
        if slider.moving:
            slider.updatePos(event.x, event.y)
    
    if app.waveSliders.moving:
        app.waveSliders.updatePos(event.x, event.y)
    
    # mode perc update
    app.voice.updatePerc(app.percSlider.value)
    
    # adsr update
    app.env.setAttack(app.attack.value)
    app.env.setDecay(app.decay.value)
    app.env.setSustain(app.sustain.value)
    app.env.setRelease(app.release.value)
    app.env.setDur(app.attack.value+app.decay.value+app.release.value)
    
    # porta update
    app.portaTime = app.portaSlider.value
    app.voice.updatePortaTime(app.portaTime)

def mouseReleased(app, event):
    for slider in app.sliders:
        slider.moving = False
    app.waveSliders.moving = False
    app.voice.updateWaveform()

def timerFired(app):
    app.specVals.pop(0)
    app.specVals.append(app.voice.canvasLogList(app.specy0, app.specy1)+[])

# lock size
def sizeChanged(app):
    app.setSize(1000, 500)