# Deharmonizing Additive Synthesizer
This is an monophonic additive synthesizer. The main concept of an additive synthesizer is that it generates all individual sine waves that comprise a tone, known as partials. By varying the amplitude of the partials, different percieved timbres are created. 
Where this synthesizer differs from most is that it has deharmonization algorithms. Because all of the partials are being generated independently of each other, their frequencies can be changed independently of the fundamental tone. I have decided to call this effect deharmonization. I have come up with six deharmonization algorithms that create unique paths for the partials to follow. 
## Installation
This synthesizer is built using pyo, a powerful synthesis and DSP engine for python. To install it, first ensure that you are using python 3.8.x or 3.9.x. In terminal:

`python3 --version`

Install pyo

`python3 -m pip install --user pyo`

If building a wheel fails, install homebrew

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

Then install portaudio

`brew install portaudio`

If the install still fails... I'm not surprised. It's notoriously difficult to install. Just uninstall and try again. 
## Running
Run the main.py file to start the synthesizer. 
## User Input
While the mouse alone can demonstrate the full functionality of the synthesizer, it's recommended that you use keyboard input as well. Any box marked with a single character corresponds to a certain function, and the layout should make its function clear enough. 