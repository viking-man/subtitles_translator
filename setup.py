from setuptools import setup, find_packages

requirements = [
    "openai-whisper",
    "parameterized",
    "srt",
    "ffmpeg-python",
    "translatepy"
]

setup(
    name="auto_subtitles_translator",
    version="1.0",
    description="Generate subtitles for video",
    install_requires=requirements,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "subtitle = subtitle.main:main",
        ]
    },
)
