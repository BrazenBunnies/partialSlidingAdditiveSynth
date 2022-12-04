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
        
        canvas.create_rectangle(x0, y0, x1, y1, outline=app.lineColor,
                                fill='white', width=4)
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
        
        canvas.create_rectangle(x0, y0, x1, y1, outline=app.lineColor,
                                fill='black', width=2)
        canvas.create_text((x1+x0)/2, y0+whiteKeyHeight/6, text=key,
                           font=f'Ubuntu {app.height//25}', fill='white')
    
    # octave indicator
    canvas.create_text(margin/2, app.height-blackKeyHeight,
                       text=f'Octave: {app.octave}',
                       font=f'Ubuntu {app.height//20}', fill='white')

# draw a spectrum analyzer from the partials being generated
def spectrumAnalyzer(app, canvas):
    canvas.create_rectangle(app.specx0, app.specy0, app.specx1, app.specy1,
                            outline=app.lineColor, fill='black', width=0)
    
    for i in range(len(app.specVals)-1):
        # CHANGE COLOR BASED ON AMPLITUDE?
        for partial in range(len(app.specVals[0])):
            canvas.create_line(i*app.sampleLength+app.specx0,
                               app.specVals[i][partial],
                               (i+1)*app.sampleLength+app.specx0,
                               app.specVals[i+1][partial], fill='yellow')
    
    # cover everything but the analyzer
    canvas.create_rectangle(0, 0, app.specx0, app.height, fill=app.bg, width=0)
    canvas.create_rectangle(app.specx1, 0, app.width, app.height, fill=app.bg,
                            width=0)
    canvas.create_rectangle(0, 0, app.width, app.specy0, fill=app.bg, width=0)
    canvas.create_rectangle(0, app.specy1, app.width, app.height, fill=app.bg,
                            width=0)
    canvas.create_rectangle(app.specx0, app.specy0, app.specx1, app.specy1,
                            outline=app.lineColor, fill='', width=4)
    
    # scale labels
    labelX = app.specx0 - app.margin
    canvas.create_text(labelX, app.specy1, text='20', fill=app.fontColor,
                       font='Ubuntu 12')
    canvas.create_text(labelX, 419, text='50', fill=app.fontColor,
                       font='Ubuntu 12')
    canvas.create_text(labelX, 373, text='100', fill=app.fontColor,
                       font='Ubuntu 12')
    canvas.create_text(labelX, 327, text='200', fill=app.fontColor,
                       font='Ubuntu 12')
    canvas.create_text(labelX, 266, text='500', fill=app.fontColor,
                       font='Ubuntu 12')
    canvas.create_text(labelX, 219, text='1k', fill=app.fontColor,
                       font='Ubuntu 12')
    canvas.create_text(labelX, 173, text='2k',
                       fill=app.fontColor, font='Ubuntu 12')
    canvas.create_text(labelX, 112, text='5k', fill=app.fontColor,
                       font='Ubuntu 12')
    canvas.create_text(labelX, 66, text='10k', fill=app.fontColor,
                       font='Ubuntu 12')
    canvas.create_text(labelX, app.specy0, text='20k', fill=app.fontColor,
                       font='Ubuntu 12')

def redrawAll(app, canvas):
    spectrumAnalyzer(app, canvas)
    
    drawKeyboard(app, canvas)
    for slider in app.sliders:
        slider.draw(canvas)
    for button in app.drawButtons:
        button.draw(canvas)