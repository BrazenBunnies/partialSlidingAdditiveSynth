from interactives import *
from deharmModes import *

def poop():
    print('poop')

def count():
    for i in range(5):
        print(i)

droppies = ['target', 'switch', 'extend', 'random', 'powers', 'primes']

def appStarted(app):
    app.lineWidth = 3
    app.lineColor = 'RoyalBlue4'
    app.buttonColor = 'RoyalBlue2'
    app.accentColor = 'yellow2'
    app.fontColor = 'white'
    app.b = Button(app, 500, 250, 100, 50, 'Poop', poop)
    app.c = Button(app, 300, 250, 100, 50, 'Count', count)
    app.d = Dropdown(app, 500, 100, 120, 50, 'Drops', droppies)
    app.buttons = [app.d, app.c, app.b]
    app.s = Slider(app, 100, 100, 300, 'x')
    
def mousePressed(app, event):
    for button in app.buttons:
        if button.wasPressed(event.x, event.y):
            button.action()
            # break skips other buttons
            break

def redrawAll(app, canvas):
    # reversed so that the highest priority elements are drawn last
    for button in reversed(app.buttons):
        button.draw(canvas)
    app.s.draw(canvas)

def main():
    runApp(width=1000, height=500)

main()