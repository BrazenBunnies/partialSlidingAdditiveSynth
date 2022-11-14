# https://stackoverflow.com/questions/59137542/pyaudio-play-continuous-stream-in-a-thread-and-let-change-the-frequency

import PySimpleGUI as sg      
from pydub.generators import Sine
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import time

sr = 44100  # sample rate
bd = 16     # bit depth
l  = 10000.0     # duration in millisec

sg.ChangeLookAndFeel('BluePurple')
silent = AudioSegment.silent(duration=10000)
FREQ = 200

def get_sine(freq):
  #create sine wave of given freq
  sine_wave = Sine(freq, sample_rate=sr, bit_depth=bd)

  #Convert waveform to audio_segment for playback and export
  sine_segment = sine_wave.to_audio_segment(duration=l)

  return sine_segment

# Very basic window.  Return values as a list      
layout = [
              [sg.Button('<<'), sg.Button('>>')],
              [sg.Text('Processing Freq [Hz]:'), sg.Text(size=(15,1), justification='center', key='-OUTPUT-')]
          ]

window = sg.Window('Piano reference', layout)

count = 0
play_obj = _play_with_simpleaudio(silent)

while 100 <= FREQ <= 20000 :  # Event Loop
    count += 1
    event, values = window.Read()

    if event in  (None, 'Exit'):
        break
    if event == '<<':
      if not FREQ < 100:
        FREQ -= 100
        window['-OUTPUT-'].update(FREQ)

    if event == '>>':
      if not FREQ > 20000:
        FREQ += 200
        window['-OUTPUT-'].update(FREQ)

    print(event, FREQ)

    sound = get_sine(FREQ)

    try:
      play_obj.stop()
      time.sleep(0.1)
      sound = sound.fade_in(100).fade_out(100)
      play_obj = _play_with_simpleaudio(sound)
      time.sleep(0.1)
    except KeyboardInterrupt:
      play_obj.stop_all()


window.close()