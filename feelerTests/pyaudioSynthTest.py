# https://www.delftstack.com/howto/python/python-audio-synthesis/#use-pyaudio-to-generate-audio-synthesis-in-python

import math
import pyaudio

PyAudio = pyaudio.PyAudio

bit_rate = 16000
frequency = 440
length = 1

bit_rate = max(bit_rate, frequency+100)
number_of_frames = int(bit_rate * length)
rest_frames = number_of_frames % bit_rate
wave_data = ''

for x in range(number_of_frames):
  wave_data = wave_data+chr(int(math.sin(x/((bit_rate/frequency)/math.pi))*127+128))

for x in range(rest_frames):
  wave_data = wave_data+chr(128)

p = PyAudio()
stream = p.open(format = p.get_format_from_width(1),
              channels = 1,
              rate = bit_rate,
              output = True)

stream.write(wave_data)
stream.stop_stream()
stream.close()
p.terminate()