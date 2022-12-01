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
    app.accentColor = 'yellow'
    app.fontColor = 'white'
    app.b = Button(app, 500, 250, 100, 50, 'Poop', poop)
    app.c = Button(app, 300, 250, 100, 50, 'Count', count)
    app.d = Dropdown(app, 500, 100, 120, 50, 'Drops', droppies)
    app.buttons = [app.d, app.c, app.b]
    app.s = Slider(app, 100, 100, 30, 50, 300, 'x')
    app.sv = Slider(app, 700, 450, 30, 50, 300, 'y')
    app.sliders = [app.s, app.sv]
    
def mousePressed(app, event):
    for button in app.buttons:
        if button.wasPressed(event.x, event.y):
            button.action()
            # break skips other buttons
            break
    for slider in app.sliders:
        if slider.wasPressed(event.x, event.y):
            slider.action(event.x, event.y)

def mouseDragged(app, event):
    for slider in app.sliders:
        if slider.moving:
            slider.updatePos(event.x, event.y)

def mouseReleased(app, event):
    for slider in app.sliders:
        slider.moving = False

def redrawAll(app, canvas):
    # reversed so that the highest priority elements are drawn last
    for button in reversed(app.buttons):
        button.draw(canvas)
    for slider in app.sliders:
        slider.draw(canvas)

def main():
    runApp(width=1000, height=500)

main()