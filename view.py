# Preston Steimel
# 11/15/2022
# Handles all graphics
# Synthesizer GUI
# VIEW in MVC

from eventHandling import *

def drawKey(app, canvas):
    canvas.create_rectangle()

# def drawKeyboard(app, canvas):
    # for key in whiteKeys()

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='purple4')
    # drawKeyboard()