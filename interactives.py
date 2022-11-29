# Preston Steimel
# 11/26/2022
# interactive UI element classes

from cmu_112_graphics import *

class Button:
    def __init__(self, app, cx, cy, width, height, label, action, active=True, visible=False):
        # pass in
        self.cx, self.cy, self.width, self.height = cx, cy, width, height
        self.line = app.lineWidth
        self.color, self.borderColor = app.buttonColor, app.lineColor
        self.label = label
        self.action = action
        
        # calculate draw vars
        self.x0, self.x1 = self.cx - self.width/2, self.cx + self.width/2
        self.y0, self.y1 = self.cy - self.height/2, self.cy + self.height/2
        self.font = f'Ubuntu {height//2}'
        
        # control vars
        self.active = active
        self.visible = visible
    
    def wasPressed(self, x, y):
        if self.active == True:
            if self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1:
                return True
        return False
    
    def draw(self, canvas):
        if self.visible:
            canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1,
                                    fill=self.color, outline=self.borderColor,
                                    width=self.line)
            canvas.create_text(self.cx, self.cy, text=self.label, font=self.font,
                            fill='white')

class Dropdown(Button):
    def __init__(self, app, cx, cy, width, height, label, action, elements):
        super.__init__(cx, cy, width, height, label, action)
        
        # control vars
        self.elements = elements
        self.current = elements[0]
        self.open = False
        
        # make the buttons
        elementButtons = []
        for i in range(elements):
            elementButtons.append(Button(app, self.cx, self.cy+(height+1)*i, width, height, elements[i], self.select))
    
    def wasPressed(self, x, y):
        if self.active == True:
            if self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1:
                return True
            if self.open == True:
                for button in self.elementButtons:
                    if button.wasPressed(x, y):
                        return True
        return False

class Slider:
    def __init__(self, sX, sY, length):
        self.sX, self.sY, self.length = sX, sY, length