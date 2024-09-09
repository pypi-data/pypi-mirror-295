# team-lead-ci-cd-open-lesson
Python package code and GitHub actions examples for OTUS open lesson for Team-Lead learning course

## In debian based linux

```commandline
sudo apt update
sudo apt install boxes
sudo apt install ffmpeg
```

## Install package

```commandline
pip install otus-open-lesson
```

## Usage

```python
from say_something import show_text, say


while True:
    text = input()
    if text:
        show_text(text)
        say(text)
    else:
        break
```
