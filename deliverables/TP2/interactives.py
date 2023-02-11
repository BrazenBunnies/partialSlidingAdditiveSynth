# Preston Steimel
# 11/26/2022
# interactive UI element classes

from cmu_112_graphics import *

class Button:
    # attributes
    active = True
    visible = True
    
    def __init__(self, app, cx, cy, width, height, label, action):
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
        self.fontColor = app.fontColor
    
    def wasPressed(self, x, y):
        if self.active:
            if self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1:
                return True
        return False
    
    def draw(self, canvas):
        if self.visible:
            canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1,
                                    fill=self.color, outline=self.borderColor,
                                    width=self.line)
            canvas.create_text(self.cx, self.cy, text=self.label, font=self.font,
                            fill=self.fontColor)

class Dropdown(Button):
    elementButtons = []
    
    def __init__(self, app, cx, cy, width, height, label, elements):
        # pass in
        super().__init__(app, cx, cy, width, height, label, self.toggleOpen)
        
        # draw vars
        self.x1 += self.height/2
        self.arrowColor = app.accentColor
        
        # control vars
        self.elements = elements
        self.current = elements[0]
        self.label = self.current
        self.open = False
        self.chr = '⋁'
        
        # make the buttons
        for i in range(len(elements)):
            self.elementButtons.append(Button(app, self.cx,
                                              self.cy+(height+1)*(i+1), width,
                                              height, elements[i], self.select))
            self.elementButtons[i].active = False
            self.elementButtons[i].visible = False
    
    def wasPressed(self, x, y):
        if self.active:
            if self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1:
                return True
            if self.open:
                for button in self.elementButtons:
                    if button.wasPressed(x, y):
                        button.action(button)
                        return True
        return False
    
    def draw(self, canvas):
        super().draw(canvas)
        
        # draw arrow
        canvas.create_text(self.x1-self.height/2, self.cy, text=self.chr,
                       font=self.font, fill=self.arrowColor)
        
        #draw other buttons
        for button in self.elementButtons:
            button.draw(canvas)
    
    def select(self, button):
        self.label = button.label
    
    def toggleOpen(self):
        self.open = not self.open
        if self.open:
            self.chr = '⋀'
        else: self.chr = '⋁'
        for button in self.elementButtons:
            button.visible = self.open
            button.active = self.open

class Slider(Button):
    def __init__(self, app, cx, cy, width, height, length, axis):
        # pass in
        self.startX, self.startY, self.length = cx, cy, length
        self.axis = axis
        
        if self.axis == 'x':
            self.eX, self.eY = self.sX + length, self.sY
        elif self.axis == 'y':
            self.eX, self.eY = self.sX, self.sY + length
        
        self.handlePos = 0.0
        self.handle = Button(app, self.sX, self.sY, 10, 5, '', self.setPos)
        
        self.lineWidth = app.lineWidth
        self.color, self.borderColor = app.buttonColor, app.lineColor
        self.handleColor = app.accentColor
    
    def setPos(self, pos):
        self.handlePos = pos
    
    def draw(self, canvas):
        canvas.create_line(self.sX, self.sY, self.eX, self.eY,
                           width=self.lineWidth, fill=self.color)
        super().draw(canvas)