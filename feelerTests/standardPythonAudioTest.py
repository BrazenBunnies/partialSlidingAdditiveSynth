# https://zach.se/generate-audio-with-python/

import sys
import wave
import math
import struct
import random
import argparse
from itertools import *

def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5):
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    return (float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i)/float(framerate))) for i in count(0))

# def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5):
#     period = int(framerate / frequency)
#     if amplitude > 1.0: amplitude = 1.0
#     if amplitude < 0.0: amplitude = 0.0
#     lookup_table = [float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i%period)/float(framerate))) for i in range(period)]
#     return (lookup_table[i%period] for i in count(0))