import logging
import ffmpeg
import os
import re
import sys
from pathlib import Path


def escape_windows_path(path):
    # 将单个反斜杠替换为双反斜杠
    sub = re.sub(r'\\', r'\\\\', path)
    split = sub.split(":")
    if len(split) == 2:
        return split[0] + "\\" + ":" + split[1]
    return sub


def is_windows():
    return sys.platform.startswith('win')


def add_subtitles(video_file, subtitle_file, output_file):
    # 使用 ffmpeg.input() 来指定输入文件和字幕文件
    input_video = ffmpeg.input(Path(video_file))
    input_subtitle = ffmpeg.input(Path(subtitle_file))

    # 区分系统
    if is_windows():
        subtitle_file = escape_windows_path(subtitle_file)
    logging.info(f'subtitle_file after transfer->{subtitle_file}')

    # 使用 filter() 添加字幕
    output = ffmpeg.output(
        input_video,  # 输入视频文件
        input_subtitle,  # 输入字幕文件
        Path(output_file),
        # vcodec='copy',  # 视频编解码器，此处保持原样
        acodec='copy',  # 音频编解码器，此处保持原样
        scodec='mov_text',  # 字幕编解码器
        f='mp4',  # 输出文件格式
        vf=f'subtitles={subtitle_file}',  # 添加字幕滤镜
        strict='experimental',  # 使用实验性字幕编解码器
    )

    # 运行 ffmpeg 命令以创建输出文件
    ffmpeg.run(output)

    logging.info(f'字幕已添加到 {output_file}')
