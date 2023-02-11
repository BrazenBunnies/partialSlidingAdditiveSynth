# Preston Steimel
# 11/15/2022
# Handles all graphics
# Synthesizer GUI
# VIEW in MVC

from eventHandling import *

def drawKeyboard(app, canvas):
    # white keys
    whiteKeyHeight = app.height/5
    whiteKeyWidth = whiteKeyHeight/3
    whiteKeyCount = len(app.whiteKeys)
    margin = (app.width-whiteKeyCount*whiteKeyWidth)/2
    for key in app.whiteKeys:
        x0 = margin + app.whiteKeys[key][1]*whiteKeyWidth
        x1 = margin + (app.whiteKeys[key][1]+1)*whiteKeyWidth
        y0 = app.height - app.margin - whiteKeyWidth*3
        y1 = app.height - app.margin
        
        canvas.create_rectangle(x0, y0, x1, y1, outline='RoyalBlue4',
                                fill='white', width='4')
        canvas.create_text((x1+x0)/2, y1-whiteKeyHeight/6, text=key,
                            font=f'Ubuntu {app.height//25}', fill='black')
    
    # black keys
    blackKeyWidth = (app.width - margin*2)/(len(app.blackKeys)*4)
    blackKeyHeight = 3*whiteKeyHeight/5
    for key in app.blackKeys:
        cx = margin + app.blackKeys[key][1]*whiteKeyWidth
        x0 = cx - blackKeyWidth
        x1 = cx + blackKeyWidth
        y0 = app.height - app.margin - whiteKeyWidth*3
        y1 = y0 + blackKeyHeight
        
        canvas.create_rectangle(x0, y0, x1, y1, outline='RoyalBlue4',
                                fill='black', width='2')
        canvas.create_text((x1+x0)/2, y0+whiteKeyHeight/6, text=key,
                           font=f'Ubuntu {app.height//25}', fill='white')
    
    # octave indicator
    canvas.create_text(margin/2, app.height-blackKeyHeight,
                       text=f'Octave: {app.octave}',
                       font=f'Ubuntu {app.height//20}', fill='white')

# converts a frequency to a pixel position on a log scale
def convertLog(app, canvas, width, height, scale):
    pass

# draw a spectrum analyzer from the partials being generated
def spectrumAnalyzer(app, canvas):
    width = app.width/4
    height = app.height
    x0, x1 = app.width-width, app.width-app.margin
    y0, y1 = app.margin, height-app.margin
    canvas.create_rectangle(x0, y0, x1, y1, outline='RoyalBlue4',
                            fill='black', width=4)

def redrawAll(app, canvas):
    canvas.create_rectangle(-100, -100, app.width+100, app.height+100,
                            fill='RoyalBlue3')
    drawKeyboard(app, canvas)
    spectrumAnalyzer(app, canvas)