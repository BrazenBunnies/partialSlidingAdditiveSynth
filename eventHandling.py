# Preston Steimel
# 11/15/2022
# Handles all the event calls
# Key and mouse presses, MIDI Input
# CONTROLLER in MVC

from cmu_112_graphics import *

# qwerty keyboard input
def keyPressed(app, event):
    # piano keys
    if event.key in app.whiteKeys:
        app.voices[0].note = app.whiteKeys[event.key][0]
        app.voices[0].updateFreq()
        app.env.play()
    if event.key in app.blackKeys:
        app.voices[0].note = app.blackKeys[event.key][0]
        app.voices[0].updateFreq()
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

def mouseDragged(app, event):
    print(event.x, event.x)

def mousePressed(app, event):
    print(event.x, event.y)

# lock aspect ratio
def sizeChanged(app):
    app.setSize(2*app.height, app.height)