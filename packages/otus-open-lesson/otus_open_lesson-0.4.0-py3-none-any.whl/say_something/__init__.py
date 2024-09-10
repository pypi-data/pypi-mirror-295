"""
Say something package
"""
import os
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


def show_text(text, speaker='mouse'):
    """
    Show text
    :param text:
    :param speaker:
    :return:
    """
    command = f'echo "{text}" | boxes -d {speaker}'
    os.system(command)


def say(text):
    """
    Say text
    :param text:
    :return:
    """
    tts = gTTS(text)
    tts.save('tmp.audio')
    sound = AudioSegment.from_file('tmp.audio')
    play(sound)
