# Preston Steimel
# 11/15/2022
# Handles all graphics
# Synthesizer GUI
# VIEW in MVC

from eventHandling import *
import math

# helper function, convert a frequency into a coordinate
def drawFreq(freq, y1, yRange):
    lowLog = math.log(20, 10)
    highLog = math.log(20000, 10)
    converted = math.log(freq, 10)
    return y1 - yRange*(converted-lowLog)/(highLog-lowLog)

def calculateColor(intensity):
    intensity = abs(intensity)
    r = int(225*(0.8 + intensity*0.2))
    g = int(225*(0.4 + intensity*0.6))
    b = int(225*(0.4 - intensity*0.4))
    if intensity == 0:
        r = 0
        g = 0
        b = 0
    # from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    return f'#{r:02x}{g:02x}{b:02x}'

# draw a spectrum analyzer from the partials being generated
def spectrumAnalyzer(app, canvas):
    canvas.create_rectangle(app.specx0, app.specy0, app.specx1, app.specy1,
                            outline=app.lineColor, fill='black', width=0)
    
    for partial in range(len(app.specVals[0])):
        # keep track of the last partial's values
        # so lines aren't drawn twice
        prevy0, prevy1, prevy2 = 0, 0, 0
        x0, y0 = app.specx0, app.specVals[0][partial]
        if partial == 0:
            color = 'yellow'
        else:
            color = calculateColor(app.waveformMode.amps[partial-1])
        
        for time in range(len(app.specVals)):
            if app.specVals[time][partial] != y0:
                x1 = (time-1)*app.sampleLength+app.specx0
                x2 = time*app.sampleLength+app.specx0
                y1 = app.specVals[time-1][partial]
                y2 = app.specVals[time][partial]
                if y0 > app.specy0 or y1 > app.specy0:
                    if y0 != prevy0 or y1 != prevy1:
                        canvas.create_line(x0, y0, x1, y1, fill=color)
                if y1 > app.specy0 or y2 > app.specy0:
                    if y1 != prevy1 or y2 != prevy2:
                        canvas.create_line(x1, y1, x2, y2, fill=color)
                x0, y0, = x2, y2
            elif time == len(app.specVals)-1:
                if y0 > app.specy0:
                    if prevy0 != y0:
                        canvas.create_line(x0, y0, app.specx1, y0, fill=color)
    
    # cover lines that go above
    canvas.create_rectangle(0, 0, app.width, app.specy0, fill=app.bg, width=0)
    canvas.create_rectangle(app.specx0, app.specy0, app.specx1, app.specy1,
                            outline=app.lineColor, fill='',
                            width=app.lineWidth)
    
    # scale labels
    labelX = app.specx0 - app.margin
    canvas.create_text(labelX, app.specy1, text='20', fill=app.fontColor,
                       font='Ubuntu 12')
    canvas.create_text(labelX, drawFreq(50,app.specy1,app.specy1-app.specy0),
                       text='50', fill=app.fontColor, font='Ubuntu 12')
    canvas.create_text(labelX, drawFreq(100,app.specy1,app.specy1-app.specy0),
                       text='100', fill=app.fontColor, font='Ubuntu 12')
    canvas.create_text(labelX, drawFreq(200,app.specy1,app.specy1-app.specy0),
                       text='200', fill=app.fontColor, font='Ubuntu 12')
    canvas.create_text(labelX, drawFreq(500,app.specy1,app.specy1-app.specy0),
                       text='500', fill=app.fontColor, font='Ubuntu 12')
    canvas.create_text(labelX, drawFreq(1000,app.specy1,app.specy1-app.specy0),
                       text='1k', fill=app.fontColor, font='Ubuntu 12')
    canvas.create_text(labelX, drawFreq(2000,app.specy1,app.specy1-app.specy0),
                       text='2k', fill=app.fontColor, font='Ubuntu 12')
    canvas.create_text(labelX, drawFreq(5000,app.specy1,app.specy1-app.specy0),
                       text='5k', fill=app.fontColor, font='Ubuntu 12')
    canvas.create_text(labelX, drawFreq(10000,app.specy1,app.specy1-app.specy0),
                       text='10k', fill=app.fontColor, font='Ubuntu 12')
    canvas.create_text(labelX, app.specy0, text='20k', fill=app.fontColor,
                       font='Ubuntu 12')

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.bg, width=0)
    spectrumAnalyzer(app, canvas)
    
    app.waveSliders.draw(canvas)
    
    for slider in app.sliders:
        slider.draw(canvas)
    for button in app.drawButtons:
        button.draw(canvas)
    for key in app.whiteKeyButtons:
        key.draw(canvas)
    for key in app.blackKeyButtons:
        key.draw(canvas)