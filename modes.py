partialCount = 516

# Natural Partials
naturalList = [i+1 for i in range(partialCount)]

# Target Specific Harmonic
def nearestTargetMultiple(n, target):
    multiple = n//target
    if multiple == 0:
        return target
    elif n-multiple*target <= (multiple+1)*target-n:
        return multiple*target
    else:
        return (multiple+1)*target

target = 5
targetList = []
for partial in naturalList:
    targetList.append(nearestTargetMultiple(partial, target))

# Cross Over Multiple Targets
crossList = []
for i in range(partialCount):
    pass

# Dictionary of the various modes
modes = {'Target':targetList, 'Cross':crossList}