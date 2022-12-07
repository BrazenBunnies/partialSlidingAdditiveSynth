# Preston Steimel
# 11/15/2022
# Mode classes
# Defines the various algorithms
# for generating deharmonization and waveform modes
# wprivrat helped me, he suggested I use numpy

import random as rand
# import numpy as np

partialCount = 128

# Natural Partials
# BE WARY OF ALIASES
natPartials = [float(i+2) for i in range(partialCount)]

class Mode:
    def __init__(self, name, function):
        self.name = name        # name string
        self.creator = function # creation function
    
    def __hash__(self):         # for dictionaries
        return hash(self.name)
    
    def __str__(self):          # for labels
        return self.name

class DeharmMode(Mode):
    def __init__(self, name, function, value):
        super().__init__(name, function)
        self.value = value      # miscellaneous integer
        self.ref = self.creator(self.value)
    
    def updateValue(self, value):
        self.value = value
        self.ref = self.creator(self.value)

def incrModeVal(mode):
    if mode.value < 99:
        mode.updateValue(mode.value + 1)

def decrModeVal(mode):
    if mode.value > 1:
        mode.updateValue(mode.value - 1)

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

# Create a random mapping for the partials
# randomizes mini-lists of length count
# should be recreated each time it's selected
def createRandomPartials(count):
    randomPartials = []
    for section in range(partialCount//count):
        slice = natPartials[section*count:(section+1)*count]
        rand.shuffle(slice)
        randomPartials.extend(slice)
    finalLen = partialCount%count
    if finalLen != 0:
        finalSlice = natPartials[-(partialCount%count):]
        rand.shuffle(finalSlice)
        randomPartials.extend(finalSlice)
    return randomPartials

# Put every partial to a power of itself
def createPowersPartials(exponent):
    powersPartials = []
    for partial in natPartials:
        powersPartials.append(partial**exponent)
    return powersPartials

# Converge partials on prime harmonics only
# each partial moves to the nearest prime partial
# added twist that you can offset the primes by a number
# so adding 1 will make the partials all not prime
# this is mostly an homage to the amount of times
# i've had to write isPrime in this course
def isPrime(n):
    if n < 2:
        return False
    for factor in range(2, int(n**0.5)+1):
        if n%factor == 0:
            return False
    return True

def nthPrime(n):
    found = 0
    guess = 0
    while found <= n:
        guess += 1
        if isPrime(guess):
            found += 1
    return guess

# add shifts the primes so that they effectively stop being prime
def createPrimesPartials(add):
    primesPartials = []
    currPrimeIndex = 0
    currPrime = nthPrime(currPrimeIndex)
    nextPrime = nthPrime(currPrimeIndex+1)
    for partial in natPartials:
        if partial-currPrime <= nextPrime-partial:
            primesPartials.append(float(currPrime))
        else:
            primesPartials.append(float(nextPrime))
        if partial == nextPrime:
            currPrimeIndex += 1
            currPrime = nextPrime
            nextPrime = nthPrime(currPrimeIndex+1)
    for i in range(len(primesPartials)):
        primesPartials[i] += add - 1
    return primesPartials

# Convert partials into 2d lists and perform matrix operations
# like transverse and whatnot and then convert back to 1d list

# Series thing

# create the actual objects
target = DeharmMode('Target', createTargetPartials, 5)
switch = DeharmMode('Switch', createSwitchPartials, 2)
extend = DeharmMode('Extend', createExtendPartials, 1)
random = DeharmMode('Random', createRandomPartials, 9)
powers = DeharmMode('Powers', createPowersPartials, 2)
primes = DeharmMode('Primes', createPrimesPartials, 1)

# Waveform Modes
class WaveformMode(Mode):
    amps = []
    def __init__(self, name, function):
        super().__init__(name, function)
        self.amps = function()

# sawtooth
def createSaw():
    return [1.0 for amp in range(partialCount)]

# square
def createSquare():
    square = []
    for partial in natPartials:
        if partial%2 == 0:
            square.append(0.0)
        else:
            square.append(1.0)
    return square

def createTriangle():
    triangle = []
    phase = 1
    for partial in natPartials:
        if partial%2 == 0:
            triangle.append(0.0)
        else:
            triangle.append(phase/partial)
            phase *= -1
    return triangle

def createThreeSpike():
    threeSpike = []
    for partial in natPartials:
        if (partial-1)%3 == 0:
            threeSpike.append(1.0)
        else:
            threeSpike.append(0.0)
    return threeSpike

def createSine():
    return [0.0 for amp in range(partialCount)]

saw = WaveformMode('Saw', createSaw)
square = WaveformMode('Square', createSquare)
triangle = WaveformMode('Triangle', createTriangle)
threeSpike = WaveformMode('3Spike', createThreeSpike)
sine = WaveformMode('Sine', createSine)
custom = WaveformMode('Custom', createSaw)

def setMode(app, mode):
    if isinstance(mode, DeharmMode):
        app.deharmMode = mode
    elif isinstance(mode, WaveformMode):
        app.waveformMode = mode