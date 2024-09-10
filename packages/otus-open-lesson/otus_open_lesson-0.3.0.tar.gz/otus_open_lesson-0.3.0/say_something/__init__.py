"""
Say something package
"""
import os

def show_text(text, speaker='mouse'):
    """
    Show text
    :param text:
    :param speaker:
    :return:
    """
    command = f'echo "{text}" | boxes -d {speaker}'
    os.system(command)
