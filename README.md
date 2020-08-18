# ToARPAbet
Converts LJSpeech format transcripts to ARPAbet.

## Usage
Run it from the command line by typing `python3 to_arpabet.py [path to ARPAbet dictionary] [path to transcript file]`. Make sure you've installed nltk (`pip3 install nltk`). Windows users may need to run `python`/`pip` rather than `python3`/`pip3`.

## Additional options
The script can optionally add trailing newline symbols, output both ARPAbet and graphemes, and a few other things. Run `python3 to_arpabet.py -h` for more information.
