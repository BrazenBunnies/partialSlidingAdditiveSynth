# Preston Steimel
# 11/15/2022
# Handles all the event calls
# Key and mouse presses, MIDI Input
# CONTROLLER in MVC

from cmu_112_graphics import *

def keyPressed(app, event):
    if event.key == 'a':
        app.voices[0].note = 60
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'w':
        app.voices[0].note = 61
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 's':
        app.voices[0].note = 62
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'e':
        app.voices[0].note = 63
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'd':
        app.voices[0].note = 64
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'f':
        app.voices[0].note = 65
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 't':
        app.voices[0].note = 66
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'g':
        app.voices[0].note = 67
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'y':
        app.voices[0].note = 68
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'h':
        app.voices[0].note = 69
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'u':
        app.voices[0].note = 70
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'j':
        app.voices[0].note = 71
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'k':
        app.voices[0].note = 72
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'o':
        app.voices[0].note = 73
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'l':
        app.voices[0].note = 74
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == 'p':
        app.voices[0].note = 75
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == ';':
        app.voices[0].note = 76
        app.voices[0].updateFreq()
        app.env.play()
    if event.key == "'":
        app.voices[0].note = 77
        app.voices[0].updateFreq()
        app.env.play()