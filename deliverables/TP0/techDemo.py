from pyo import *
from cmu_112_graphics import *

s = Server().boot()
s.amp = 0.5

def appStarted(app):
    app.targetFreq = 440.0
    app.envelope = Adsr(attack=0.01, decay=0.1, sustain=2.8, release=1.2,
    dur=4, mul = 0.7)
    app.generator = Sine(app.targetFreq, mul=app.envelope).out()
    s.gui(locals())

def playSine(app):
    app.generator.freq = app.targetFreq
    app.envelope.play()

def keyPressed(app, event):
    if event.key == 'Left':
        prev = app.targetFreq
        app.targetFreq -= 50
        app.generator.freq = SigTo(app.targetFreq, time = 0.5, init = prev)
    if event.key == 'Right':
        app.targetFreq += 50
        app.generator.freq = app.targetFreq
    if event.key == 'p':
        playSine(app)

def mouseDragged(app, event):
    app.targetFreq += 10

def redrawAll(app, canvas):
    canvas.create_text(app.height//2, app.width//2,
    text=app.targetFreq, fill='black')

def runSynth():
    print('running synth!')
    runApp(width=500, height=500)

# simpleSine = Sine(freq).out()

# partials = [440.0]
# partial = 1
# while partials[-1] < 20000:
#     partial += 1
#     partials.append(partials[0]*partial)

# additiveOscs = Sine(partials).out()

def main():
    runSynth()

main()