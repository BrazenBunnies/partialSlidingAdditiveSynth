# Preston Steimel
# 11/15/2022
# Mode class
# Defines the various algorithms
# for generating deharmonization modes

partialCount = 128

# Natural Partials
natPartials = [float(i+2) for i in range(partialCount)]

class Mode:
    def __init__(self, name, function, value):
        self.name = name        # name string
        self.creator = function # creation function
        self.value = value      # miscellaneous integer
        self.perc = 0.0         # float, 0.0 to 1.0
        
        self.ref = self.creator(self.value)
        self.partials = natPartials
    
    def __hash__(self): # for the dictionary!
        return hash(self.name)
    
    def updateValue(self, value):
        self.value = value
        self.perc = 0.0
        self.ref = self.creator(self.value)
        self.partials = natPartials
    
    # get the in between value of the reference and natural partials
    def updatePerc(self, perc):
        for i in range(partialCount):
            difference = self.ref[i]-natPartials[i]
            self.partials[i] = natPartials[i]+perc*difference

# Target specific harmonics
def nearestTargetMultiple(n, target):
    multiple = n//target
    if multiple == 0:
        return target
    elif n-multiple*target <= (multiple+1)*target-n:
        return multiple*target
    else:
        return (multiple+1)*target

def createTargetPartials(target):
    targetPartials = []
    for partial in natPartials:
        targetPartials.append(nearestTargetMultiple(partial, target))
    return targetPartials

# Switch each nth partial
# Likely works best with even numbers
# Because with odd numbers many partials don't move at all
def createSwitchPartials(switch):
    switchPartials = []
    for i in range(0, partialCount, switch):
        for subtract in range(switch, 0, -1):
            if i+subtract-1 < partialCount:
                switchPartials.append(natPartials[i+subtract-1])
    return switchPartials

# Extend all partials up by a certain amount
# On its own it sounds like a missing first harmonic
# But the sliding gives more character
def createExtendPartials(stretch):
    stretchPartials = []
    for partial in natPartials:
        stretchPartials.append(partial+stretch)
    return stretchPartials

# create the actual objects
target = Mode('Target', createTargetPartials, 5)
switch = Mode('Switch', createSwitchPartials, 2)
extend = Mode('Extend', createExtendPartials, 1)