# http://ajaxsoundstudio.com/pyodoc/examples/05-envelopes/04-simple-envelopes.html
from pyo import *
import random

s = Server().boot()

# Infinite sustain for the global envelope.
globalamp = Fader(fadein=2, fadeout=2, dur=0).play()

# Envelope for discrete events, sharp attack, long release.
env = Adsr(attack=0.01, decay=0.1, sustain=0.5, release=1.5, dur=2, mul=0.5)
# setExp method can be used to create exponential or logarithmic envelope.
env.setExp(0.75)

# Initialize  a simple wave player and apply both envelopes.
sig = SuperSaw(freq=[100, 101], detune=0.6, bal=0.8, mul=globalamp * env).out()


def play_note():
    "Play a new note with random frequency and jitterized envelope."
    freq = random.choice(midiToHz([36, 38, 41, 43, 45]))
    sig.freq = [freq, freq * 1.005]
    env.attack = random.uniform(0.002, 0.01)
    env.decay = random.uniform(0.1, 0.5)
    env.sustain = random.uniform(0.3, 0.6)
    env.release = random.uniform(0.8, 1.4)
    # Start the envelope for the event.
    env.play()


# Periodically call a function.
pat = Pattern(play_note, time=2).play()

s.gui(locals())
