# Preston Steimel
# 11/15/2022
# Mode class
# Defines the various algorithms
# for generating deharmonization modes

import random as rand

partialCount = 128

# Natural Partials
# BE WARY OF ALIASES
natPartials = [float(i+2) for i in range(partialCount)]

class DeharmMode:
    def __init__(self, name, function, value):
        self.name = name        # name string
        self.creator = function # creation function
        self.value = value      # miscellaneous integer
        self.perc = 0.0         # float, 0.0 to 1.0
        
        self.ref = self.creator(self.value)
        self.partials = natPartials + []    # break alias
    
    def __hash__(self): # for the dictionary!
        return hash(self.name)
    
    def updateValue(self, value):
        self.value = value
        self.perc = 0.0
        self.ref = self.creator(self.value)
        self.partials = natPartials + []    # break alias
    
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

# Create a random mapping for the partials
# divides into a certain amount of sections to be jumbled
# should be recreated each time it's selected
def createRandomPartials(sections):
    randomPartials = []
    for section in range(sections):
        elems = partialCount // sections
        group = natPartials[section*elems:(section+1)*elems]
        rand.shuffle(group)
        randomPartials.extend(group)
        # for i in range(len(group)):
        #     randomPartials.append(group[i])
    remainderGroup = natPartials[-(partialCount%sections):]
    rand.shuffle(remainderGroup)
    randomPartials.extend(remainderGroup)
    # for i in range(len(remainderGroup)):
    #     randomPartials.append(remainderGroup[i])
    return randomPartials

# Put every partial to a power of itself
def createPowersPartials(exponent):
    powersPartials = []
    for partial in natPartials:
        powersPartials.append(partial**2)
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

def createPrimesPartials(add):
    primesPartials = []
    currPrimeIndex = 0
    currPrime = nthPrime(currPrimeIndex)
    nextPrime = nthPrime(currPrimeIndex+1)
    for partial in natPartials:
        if partial-currPrime <= nextPrime-partial:
            primesPartials.append(float(currPrime-1+add))
        else:
            primesPartials.append(float(nextPrime-1+add))
        if partial == currPrime:
            currPrimeIndex += 1
            currPrime = nextPrime
            nextPrime = nthPrime(currPrimeIndex+1)
    return primesPartials

# create the actual objects
target = DeharmMode('Target', createTargetPartials, 5)
switch = DeharmMode('Switch', createSwitchPartials, 2)
extend = DeharmMode('Extend', createExtendPartials, 1)
random = DeharmMode('Random', createRandomPartials, 10)
powers = DeharmMode('Powers', createPowersPartials, 2)
primes = DeharmMode('Primes', createPrimesPartials, 3)