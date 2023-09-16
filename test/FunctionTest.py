import pytest
from translatepy import Translator
from translatepy.translators.google import GoogleTranslate
from pathlib import Path
import torch
import os
from subtitle.main import main


def test_tranlator():
    translator = Translator()
    result = translator.translate("이번에 마리또하잖아요", "Chinese")
    print(type(result))
    assert str == type(result.result)
    print(result.result)

    google_translate = GoogleTranslate()
    result_google = google_translate.translate("이번에 마리또하잖아요", "Chinese")
    print(result_google)


def test_path():
    path = Path("test.mp4")
    assert path.stem == "test"
    assert path.suffix == ".mp4"
    print(path)
    print(path.name)

    folder = os.path.abspath("test.mp3")
    print(folder)
    print(os.getcwd())
    assert os.path.exists(os.path.abspath("."))
    print(os.path.abspath("."))

    path_absolute = Path("/Users/viking/video/trump_speech.mp4")
    assert path_absolute.stem == "trump_speech"
    print(path_absolute)

    path3 = os.path.abspath("/Users/viking/video/trump_speech.mp4")
    print(path3)
    print(os.path.dirname("/Users/viking/video/trump_speech.mp4"))


def test_loop():
    array = [1, 2, 3, 4, 5, 6]
    for i in range(len(array)):
        array[i] = array[i] + 1
    for e in array:
        print(e)


def test_not():
    assert not None == True
    assert not False == True
