import logging
import os.path
import time
from .whisper_model import WhisperModel
from whisper.utils import get_writer
from whisper.audio import load_audio
from translatepy import Translate
from .ffmpeg_utils import add_subtitles
from pathlib import Path


class Action:
    def __init__(self, args):
        self.args = args
        self.sampling_rate = 16000
        self.lang = self.args.lang
        self.target_lang = self.args.targetLang
        self.whisper_model = None
        self.vad_model = None
        self.detect_speech = None

        tic = time.time()
        self.whisper_model = WhisperModel(self.sampling_rate)
        self.whisper_model.load(self.args.whisper_model, self.args.device)

        logging.info(f"Done Init model in {time.time() - tic:.1f} sec")

    def transcribe(self):
        for input in self.args.inputs:
            logging.info(f'Translate {input}')
            start_time = time.time()
            path = Path(input)
            # 默认是当前路径

            audio = load_audio(input, self.sampling_rate)
            transcribe_result = self.whisper_model.transcribe(audio, self.args.lang)
            logging.info(f'Transcribe result for {input} is {transcribe_result}')

            # 输出目录
            output_dir = self.make_output_dir(self.args.outputDir, str(path.absolute().parent))
            # 生成字幕文件
            srt_file = self.writeSrtFile(output_dir, path, transcribe_result)

            srt_full_path = os.path.join(output_dir, srt_file)
            assert os.path.exists(srt_full_path), f"SRT file not generated?"
            logging.info(f"Save srt file [{input}] to [{srt_file}],time->[{time.time() - start_time:.1f}]")

            # self._save_md(filename + ".md", output, input)
            # logging.info(f'Saved texts to {filename + ".md"} to mark sentences')

    # 使用whisper自带的writer生成字幕文件
    def writeSrtFile(self, output_dir, path, transcribe_result):
        srt_writer = get_writer("srt", output_dir)
        srt_file = path.stem + ".srt"
        logging.info(f"output_dir->{output_dir},srt->{srt_file}")
        srt_writer(transcribe_result, srt_file)
        return srt_file

    def translate(self):
        for input in self.args.inputs:
            logging.info(f'Translate {input} from {self.lang} to {self.target_lang}')
            assert os.path.exists(input), f"File {input} does not exist"
            start_time = time.time()
            path = Path(input)
            #
            audio = load_audio(input, self.sampling_rate)
            translate_result = self.whisper_model.translate(audio, self.args.lang)
            logging.info(f'Translate result for {input} is {translate_result}')

            # 国内无法使用google翻译，默认使用英语
            self.translateToTargetLang(translate_result)

            # 默认是输入文件的当前目录
            output_dir = self.make_output_dir(self.args.outputDir, str(path.absolute().parent))
            # 生成字幕文件
            srt_file = self.writeSrtFile(output_dir, path, translate_result)

            srt_full_path = os.path.join(output_dir, srt_file)
            assert os.path.exists(srt_full_path), f"SRT file not generated?"
            logging.info(f"Translate srt file [{input}] to [{srt_file}],time->[{time.time() - start_time:.1f}]")

        logging.info(f'Translate for {self.args.inputs} end')

    def translateToTargetLang(self, translate_result):
        if not self.args.China and self.args.targetLang is not "en":
            logging.info(f"Translate to {self.args.targetLang} start.")
            translator = Translate()
            # translate
            for i in range(len(translate_result["segments"])):
                segment = translate_result["segments"][i]
                try:
                    translate_text = translator.translate(segment["text"], self.target_lang).result
                except Exception as e:
                    # 处理其他所有类型的异常
                    print("An exception occurred:", str(e))
                    translate_text = segment["text"]
                translate_result["segments"][i]["text"] = translate_text

    def add_subtitles(self):

        # 没有指定字幕文件，先自动生成
        target_subtitles = self.args.targetSubtitles
        if target_subtitles is None:
            logging.info(f'Did not specify target subtitles,transcribe subtitles for {self.args.inputs}')
            self.transcribe()

        self.addSubtitles()

    def addSubtitles(self):
        for i in range(len(self.args.inputs)):

            input = self.args.inputs[i]
            logging.info(f"Add subtitles for [{input}] starting")
            start_time = time.time()
            path = Path(input)
            input_name = path.stem
            suffix = path.suffix

            output_dir = self.make_output_dir(self.args.outputDir, str(path.absolute().parent))
            # 如果没有指定字幕文件，获取自动生成的字幕文件
            if self.args.targetSubtitles is None:
                # 默认是当前路径
                target_subtitle = os.path.join(output_dir, input_name + ".srt")
            else:
                target_subtitle = self.args.targetSubtitles[i]

            # 文件输出路径
            outputs = self.args.outputs
            if outputs is not None:
                output = outputs[i]
            else:
                output = os.path.join(output_dir, input_name + "_subtitle" + suffix)

            # 使用ffmpeg添加字幕
            logging.info(f'input_file->{input},subtitle_file->{target_subtitle},output_file->{output}')
            add_subtitles(input, target_subtitle, output)

            logging.info(f'Add subtitles for {input} end,output->{output},time->[{time.time() - start_time:.1f}]')

    def union(self):
        start_time = time.time()
        # translate
        self.translate()
        # add subtitles to video
        self.addSubtitles()

        logging.info(f'Union operations end,time->[{time.time() - start_time:.1f}]')

    # 生成视频对应的语言字幕，不做翻译
    def unionForTranscribe(self):
        # translate to english
        self.transcribe()
        # add subtitle to video
        self.addSubtitles()

        logging.info(f'Union operations for Transcribe end')

    def make_output_dir(self, output_dir, input_dir):
        if output_dir is None:
            output_dir = input_dir
        folder = os.path.abspath(output_dir)
        if not os.path.exists(folder):
            os.makedirs(folder)
        # os.chdir(folder)
        # assert os.getcwd() == folder
        return folder
