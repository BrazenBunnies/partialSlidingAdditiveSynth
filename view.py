# Preston Steimel
# 11/15/2022
# Handles all graphics
# Synthesizer GUI
# VIEW in MVC

from eventHandling import *
import math

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

# helper function, convert a frequency into a coordinate
def drawFreq(freq, y1, yRange):
    lowLog = math.log(20, 10)
    highLog = math.log(20000, 10)
    converted = math.log(freq, 10)
    return y1 - yRange*(converted-lowLog)/(highLog-lowLog)

def calculateColor(intensity):
    r = int(225*(0.75 + intensity*0.25))
    g = int(225*(0.5 + intensity*0.5))
    b = int(225*(0.4 - intensity*0.4))
    # from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    return f'#{r:02x}{g:02x}{b:02x}'

# draw a spectrum analyzer from the partials being generated
def spectrumAnalyzer(app, canvas):
    canvas.create_rectangle(app.specx0, app.specy0, app.specx1, app.specy1,
                            outline=app.lineColor, fill='black', width=0)
    
    for partial in range(len(app.specVals[0])):
        x0, y0 = app.specx0, app.specVals[0][partial]
        color = calculateColor(app.waveformMode.amps[partial])
        for time in range(len(app.specVals)):
            if app.specVals[time][partial] != y0:
                x1 = (time-1)*app.sampleLength+app.specx0
                x2 = time*app.sampleLength+app.specx0
                y1 = app.specVals[time-1][partial]
                y2 = app.specVals[time][partial]
                if y0 > app.specy0 and y1 > app.specy0:
                    canvas.create_line(x0, y0, x1, y1, fill=color)
                if y1 > app.specy0 and y2 > app.specy0:
                    canvas.create_line(x1, y1, x2, y2, fill=color)
                x0, y0, = x2, y2
            elif time == len(app.specVals)-1:
                if y0 > app.specy0:
                    canvas.create_line(x0, y0, app.specx1, y0, fill=color)
    
    # for i in range(len(app.specVals)-1):
    #     # CHANGE COLOR BASED ON AMPLITUDE?
    #     for partial in range(len(app.specVals[0])):
    #         if (app.specVals[i][partial] < app.specy0 and
    #         app.specVals[i+1][partial] < app.specy0): continue
    #         canvas.create_line(i*app.sampleLength+app.specx0,
    #                            app.specVals[i][partial],
    #                            (i+1)*app.sampleLength+app.specx0,
    #                            app.specVals[i+1][partial], fill='yellow')
    
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
    
    drawKeyboard(app, canvas)
    
    app.waveformSliderArray.draw(canvas)
    
    for slider in app.sliders:
        slider.draw(canvas)
    for button in app.drawButtons:
        button.draw(canvas)