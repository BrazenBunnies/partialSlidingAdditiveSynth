# Preston Steimel
# 11/15/2022
# Handles all the event calls
# Key and mouse presses, MIDI Input
# CONTROLLER in MVC

from cmu_112_graphics import *

def keyPressed(app, event):
    if event.key == 'a':
        app.env.play()