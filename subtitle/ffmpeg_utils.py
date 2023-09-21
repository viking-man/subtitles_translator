import logging
import ffmpeg
from pathlib import Path


def add_subtitles(video_file, subtitle_file, output_file):
    # 使用 ffmpeg.input() 来指定输入文件和字幕文件
    input_video = ffmpeg.input(Path(video_file))
    input_subtitle = ffmpeg.input(Path(subtitle_file))

    # 使用 filter() 添加字幕
    output = ffmpeg.output(
        input_video,  # 输入视频文件
        input_subtitle,  # 输入字幕文件
        output_file,
        # vcodec='copy',  # 视频编解码器，此处保持原样
        acodec='copy',  # 音频编解码器，此处保持原样
        scodec='mov_text',  # 字幕编解码器
        f='mp4',  # 输出文件格式
        vf=f'subtitles={Path(subtitle_file)}',  # 添加字幕滤镜
        strict='experimental',  # 使用实验性字幕编解码器
    )

    # 运行 ffmpeg 命令以创建输出文件
    ffmpeg.run(output)

    logging.info(f'字幕已添加到 {output_file}')
