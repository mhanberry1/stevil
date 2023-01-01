# stevil

A slightly evil AI assistant

## dependencies

- python3
- pip3

Note: On Mac (and maybe linux?) Homebrew may be required

### linux dependencies

- python3-pyaudio
- espeak

### python dependencies

To install python dependencies, you can run:

```
pip3 install -r requirements.txt
```

Then install the language model with:

```
python3 -m spacy download en_core_web_sm
```

## usage

To start stevil, run:

```
python3 stevil.py
```

Make sure you are in a reasonably quiet environment for the best results.
