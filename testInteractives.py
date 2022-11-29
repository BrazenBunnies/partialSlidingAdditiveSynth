from interactives import *

def poop():
    print('poop')

def count():
    for i in range(5):
        print(i)

def appStarted(app):
    app.lineWidth = 3
    app.lineColor = 'RoyalBlue4'
    app.buttonColor = 'RoyalBlue2'
    app.b = Button(app, 500, 250, 100, 50, 'Poop', poop)
    app.c = Button(app, 300, 250, 100, 50, 'Count', count)
    app.buttons = [app.b, app.c]
    
def mousePressed(app, event):
    for button in app.buttons:
        if button.wasPressed(event.x, event.y):
            button.action()

def redrawAll(app, canvas):
    for button in app.buttons:
        button.draw(canvas)

def main():
    runApp(width=1000, height=500)

main()