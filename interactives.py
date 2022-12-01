# Preston Steimel
# 11/26/2022
# interactive UI element classes

from cmu_112_graphics import *

class Button:    
    def __init__(self, app, cx, cy, width, height, label, action, color=None,
                 active=True, visible=True):
        # pass in
        self.cx, self.cy, self.width, self.height = cx, cy, width, height
        self.line = app.lineWidth
        self.color, self.borderColor = app.buttonColor, app.lineColor
        self.label = label
        self.action = action
        if color != None: self.color = color
        self.active = active
        self.visible = visible
        
        # calculate draw vars
        self.calculateBounds()
        if width >= height:
            self.font = f'Ubuntu {height//2}'
        else: self.font = f'Ubuntu {width//3}'
        self.fontColor = app.fontColor
    
    def calculateBounds(self):
        self.x0, self.x1 = self.cx - self.width/2, self.cx + self.width/2
        self.y0, self.y1 = self.cy - self.height/2, self.cy + self.height/2
    
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
    moving = False
    value = 0.0
    
    def __init__(self, app, cx, cy, width, height, length, axis):
        # pass in
        super().__init__(app, cx, cy, width, height, self.value, self.activate)
        self.startX, self.startY, self.length = cx, cy, length
        self.axis = axis
        
        if self.axis == 'x':
            self.endX, self.endY = self.cx + length, self.cy
        elif self.axis == 'y':
            self.endX, self.endY = self.cx, self.cy - length
        
        # from https://stackoverflow.com/questions/6149006/how-to-display-a-float-with-two-decimal-places
        self.label = '%.2f' % self.value
        self.lineWidth = app.lineWidth
        self.color, self.borderColor = app.buttonColor, app.lineColor
        self.accentColor = app.accentColor
    
    def activate(self, x, y):
        self.moving = True
        self.pressedX, self.pressedY = x, y
        self.posX, self.posY = self.cx, self.cy
    
    def updatePos(self, x, y):
        if self.axis == 'x':
            newX = x - self.pressedX + self.posX
            if newX < self.startX:
                self.cx = self.startX
            elif newX > self.endX:
                self.cx = self.endX
            else:
                self.cx = newX
            self.value = (self.cx-self.startX)/(self.endX-self.startX)
        elif self.axis == 'y':
            newY = y - self.pressedY + self.posY
            if newY > self.startY:
                self.cy = self.startY
            elif newY < self.endY:
                self.cy = self.endY
            else:
                self.cy = newY
            self.value = (self.cy-self.startY)/(self.endY-self.startY)
        self.calculateBounds()
        self.label = '%.2f' % abs(self.value)
    
    def draw(self, canvas):
        canvas.create_line(self.startX, self.startY, self.endX, self.endY,
                           width=self.lineWidth*3, fill=self.color)
        canvas.create_line(self.startX, self.startY, self.cx, self.cy,
                           width=self.lineWidth, fill=self.accentColor)
        super().draw(canvas)