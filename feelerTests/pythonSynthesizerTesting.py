# https://github.com/yuma-m/synthesizer

from synthesizer import Player, Synthesizer, Waveform

p = Player()
p.open_stream()
synth = Synthesizer(osc1_waveform=Waveform.sine,
osc1_volume=1.0, use_osc2=False)

p.play_wave(synth.generate_constant_wave(440.0, 3.0))

chord = [440.0]
partial = 1
while chord[-1] < 20000:
    partial += 1
    chord.append(chord[0]*partial)
print(chord)

p.play_wave(synth.generate_chord(chord, 3.0))

p.play_wave(synth.generate_constant_wave(440.0, 3.0))
p.play_wave(synth.generate_constant_wave(880.0, 2.0))
p.play_wave(synth.generate_constant_wave(440.0, 3.0))
p.play_wave(synth.generate_constant_wave(880.0, 2.0))

chord = {440.0}
fundamental = 440.0
partial = 1

while max(chord) < 20000:
    partial += 1
    chord.add(fundamental*partial)
print(chord)

p.play_wave(synth.generate_chord(list(chord), 3.0))