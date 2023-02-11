# Preston Steimel
# 11/26/2022
# interactive UI element classes

from cmu_112_graphics import *

class Button:
    def __init__(self, app, x0, y0, width, height, label, action, color=None,
                 fontColor=None, active=True, visible=True):
        # pass in
        self.x0, self.y0, self.width, self.height = x0, y0, width, height
        self.line = app.lineWidth
        self.color, self.borderColor = app.buttonColor, app.lineColor
        self.label = label
        self.action = action
        if color != None: self.color = color
        self.active = active
        self.visible = visible
        
        # calculate draw vars
        self.calculateBounds()
        self.fontSize = int(height//2)-1
        self.font = f'Ubuntu {self.fontSize}'
        self.fontColor = app.fontColor
        if fontColor != None: self.fontColor = fontColor
    
    def calculateBounds(self):
        self.x1, self.y1 = self.x0 + self.width, self.y0 + self.height
        self.cx, self.cy = (self.x0+self.x1)/2, (self.y0+self.y1)/2
    
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
            canvas.create_text(self.cx, self.cy, text=str(self.label),
                               font=self.font, fill=self.fontColor)

class Dropdown(Button):
    def __init__(self, app, x0, y0, width, height, label, elements):
        # pass in
        super().__init__(app, x0, y0, width, height, label, self.toggleOpen)
        
        # draw vars
        self.x1 += self.height/2
        self.arrowColor = app.accentColor
        
        # control vars
        self.elements = elements
        self.label = elements[0]
        self.open = False
        self.chr = '⋁'
        
        # make the buttons
        self.elementButtons = []
        for i in range(len(elements)):
            self.elementButtons.append(Button(app, self.x0,
                                              self.y0+height*(i+1), width,
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
    
    def __init__(self, app, x0, y0, width, height, length, title, axis, bound,
                 thickness=None):
        # pass in
        super().__init__(app, x0, y0, width, height, self.value, self.activate)
        self.startX, self.startY, self.length = self.cx, self.cy, length
        self.title = title
        self.axis = axis
        self.max = bound
        
        self.titleFont = f'Ubuntu {int(2*self.height/3)}'
        if width/3 >= height/2:
            self.fontSize = int(height//2)  # apparently integer divide is
        else: self.fontSize = int(width//3) # actually only floor divide
        self.font = f'Ubuntu {self.fontSize}'
        
        if self.axis == 'x':
            self.endX, self.endY = self.startX+length-self.width, self.cy
        elif self.axis == 'y':
            self.endX, self.endY = self.cx, self.startY-length+self.height
        
        # from https://stackoverflow.com/questions/6149006/how-to-display-a-float-with-two-decimal-places
        self.label = '%.2f' % self.value
        self.lineWidth = app.lineWidth
        self.trackWidth = app.lineWidth*4
        if thickness != None:
            self.trackWidth = thickness
        self.color, self.borderColor = app.buttonColor, app.lineColor
        self.accentColor = app.accentColor
    
    def setValue(self, value):
        self.value = value
        if self.axis == 'x':
            transformedVal = value/self.max * (self.endX-self.startX)
            transformedVal += self.startX
            self.pressedX, self.posX = self.cx, self.cx
            self.updatePos(transformedVal, self.cy)
        elif self.axis == 'y':
            transformedVal = value/self.max * (self.startY-self.endY)
            self.pressedY, self.posY = self.cy, self.cy
            self.updatePos(self.cx, self.startY-transformedVal)
    
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
            self.value = (self.cx-self.startX)*self.max/(self.endX-self.startX)
            self.x0, self.x1 = self.cx - self.width/2, self.cx + self.width/2
        
        elif self.axis == 'y':
            newY = y - self.pressedY + self.posY
            if newY > self.startY:
                self.cy = self.startY
            elif newY < self.endY:
                self.cy = self.endY
            else:
                self.cy = newY
            self.value = (self.cy-self.startY)*self.max/(self.endY-self.startY)
            self.y0, self.y1 = self.cy - self.height/2, self.cy + self.height/2
        
        self.label = '%.2f' % abs(self.value)
    
    def draw(self, canvas):
        # draw Title
        if self.axis == 'x':
            canvas.create_text((self.startX+self.endX)/2,
                               self.startY+self.height, text=self.title,
                               font=self.titleFont, fill=self.fontColor)
        elif self.axis == 'y':
            canvas.create_text((self.startX, self.startY+self.height/2+
                                self.fontSize),
                               text=self.title, font=self.titleFont,
                               fill=self.fontColor)
        
        # create the slider's track and also the level line
        canvas.create_line(self.startX, self.startY, self.endX, self.endY,
                           width=self.trackWidth, fill=self.borderColor)
        canvas.create_line(self.startX, self.startY, self.cx, self.cy,
                           width=self.lineWidth, fill=self.accentColor)
        super().draw(canvas)

class SliderArray(Slider):
    sliders = []
    sliderVals = []
    active = True
    visible = True
    def __init__(self, app, x0, y1, length, count):
        self.x0, self.y1, self.length = x0, y1, length
        self.count = count
        self.lineWidth = app.lineWidth*2
        self.x1 = x0 + self.lineWidth*count
        self.y0 = y1 - length
        
        self.action = self.activate
        
        for i in range(count):
            self.sliders.append(Slider(app, x0+(i*self.lineWidth), y1, 0, 0,
                                       length, '', 'y', 1.0, 
                                       thickness=app.lineWidth))
            self.sliderVals.append(1.0)
            self.sliders[i].setValue(1.0)
            self.sliders[i].visible = False
    
    def updateAllVals(self, values):
        for i in range(len(self.sliders)):
            self.sliderVals[i] = values[i]
            self.sliders[i].setValue(abs(values[i]))
            
    def activate(self, x, y):
        self.moving = True
        self.pressedX, self.pressedY = x, y
        self.updatePos(x, y)
    
    def updatePos(self, x, y):
        currentSlider = int((x - self.x0)/self.lineWidth)
        if currentSlider < 0: currentSlider = 0
        if currentSlider > self.count-1: currentSlider = self.count-1
        self.sliders[currentSlider].updatePos(x, y)
        self.sliderVals[currentSlider] = self.sliders[currentSlider].value
    
    def draw(self, canvas):
        for slider in self.sliders:
            slider.draw(canvas)

# dummy function if I want to make inactive buttons
def dummy():
    pass