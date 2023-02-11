from pyo import *

s = Server().boot()

s.amp = 0.5

porta = SigTo(value=0.3, time = 2.0, init = 0.0)

freq = SigTo(440.0, time=0.01)
freq.ctrl([SLMap(0, 0.25, "lin", "time", 0.01, dataOnly=True)])

# freq = 440.0

simpleSine = Sine(freq,mul=porta).out()

# partials = [440.0]
# partial = 1
# while partials[-1] < 20000:
#     partial += 1
#     partials.append(partials[0]*partial)

# additiveOscs = Sine(partials).out()

s.gui(locals())