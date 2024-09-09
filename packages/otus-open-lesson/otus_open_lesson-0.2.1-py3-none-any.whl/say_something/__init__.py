import os
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

TMP_FILE_NAME = 'current.mp3'
INPUT_FILE_NAME = 'text.txt'
DEFAULT_LANG = 'en'

def show_text(text, speaker='mouse'):  # cat dog mouse ...
    command = f'echo "{text}" | boxes -d {speaker}'
    os.system(command)

def say(text, separator='/'):
    lang = DEFAULT_LANG
    if separator in text:
        text, lang = text.split(separator)
    print('language - >', lang)
    tts = gTTS(text, lang=lang)
    tts.save(TMP_FILE_NAME)
    sound = AudioSegment.from_file(TMP_FILE_NAME)
    play(sound)