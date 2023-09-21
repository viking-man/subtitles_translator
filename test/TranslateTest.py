import logging
import os
import unittest

from parameterized import parameterized, param
from subtitle.action import Action
from config import TEST_MEDIA_FILE, TEST_ASSETS_PATH, TestArgs
from pathlib import Path


class testTranslate(unittest.TestCase):

    # @classmethod
    def removeFileAfterTest(cls):
        for file in os.listdir(TEST_ASSETS_PATH):
            if file.endswith("srt") or "_subtitle" in os.path.basename(file):
                logging.info(f"remove srt file->{file}")
                os.remove(os.path.join(TEST_ASSETS_PATH, file))

    def test_default_transcribe(self):
        logging.info("检查默认参数生成字幕")
        args = TestArgs()
        full_path = TEST_ASSETS_PATH + TEST_MEDIA_FILE
        # abspath = Path(full_path).absolute()
        # args.inputs = [abspath]
        args.inputs = [full_path]
        Action(args).transcribe()

        # os.chdir("../")
        srt_ = full_path.split(".")[0] + ".srt"
        logging.info(srt_)
        assert os.path.exists(srt_)

        self.removeFileAfterTest()

    def test_translate(self):
        logging.info("检查自动翻译成字幕")
        args = TestArgs()
        full_path = TEST_ASSETS_PATH + TEST_MEDIA_FILE
        args.inputs = [full_path]
        Action(args).translate()

        srt_ = full_path.split(".")[0] + ".srt"
        logging.info(srt_)
        assert os.path.exists(srt_)

        self.removeFileAfterTest()

    def test_translate_with_lang(self):
        logging.info("检查自动翻译成目标语言字幕")
        args = TestArgs()
        full_path = TEST_ASSETS_PATH + TEST_MEDIA_FILE
        args.inputs = [full_path]
        args.target_lang = "en"
        Action(args).translate()

        srt_ = full_path.split(".")[0] + ".srt"
        logging.info(srt_)
        assert os.path.exists(srt_)

        self.removeFileAfterTest()

    def test_union(self):
        logging.info("检查联合操作")
        args = TestArgs()
        full_path = TEST_ASSETS_PATH + TEST_MEDIA_FILE
        args.inputs = [full_path]
        Action(args).union()

        srt_ = full_path.split(".")[0] + ".srt"
        assert os.path.exists(srt_)
        subtitle_video = full_path.split(".")[0] + "_subtitle.mp4"
        assert os.path.exists(subtitle_video)

        self.removeFileAfterTest()

    def test_union_for_china(self):
        logging.info("检查中国联合操作")
        args = TestArgs()
        full_path = TEST_ASSETS_PATH + TEST_MEDIA_FILE
        args.inputs = [full_path]
        args.China = True
        Action(args).union()

        srt_ = full_path.split(".")[0] + ".srt"
        assert os.path.exists(srt_)
        subtitle_video = full_path.split(".")[0] + "_subtitle.mp4"
        assert os.path.exists(subtitle_video)

        self.removeFileAfterTest()

    def test_union_use_mediun_model(self):
        logging.info("检查使用中等模型")
        args = TestArgs()
        full_path = TEST_ASSETS_PATH + TEST_MEDIA_FILE
        args.inputs = [full_path]
        args.whisper_model = "medium"
        Action(args).union()

        srt_ = full_path.split(".")[0] + ".srt"
        assert os.path.exists(srt_)
        subtitle_video = full_path.split(".")[0] + "_subtitle.mp4"
        assert os.path.exists(subtitle_video)

        self.removeFileAfterTest()

    def test_add_subtitle(self):
        logging.info("检查添加字幕")
        args = TestArgs()
        full_path = TEST_ASSETS_PATH + TEST_MEDIA_FILE
        args.inputs = [full_path]
        args.target_subtitles = ["srt/tzuyu_20.srt"]
        Action(args).add_subtitles()

        subtitle_video = full_path.split(".")[0] + "_subtitle.mp4"
        assert os.path.exists(subtitle_video)

        self.removeFileAfterTest()

    def test_union_transcribe(self):
        logging.info("检查不包含翻译的联合操作")
        args = TestArgs()
        full_path = TEST_ASSETS_PATH + TEST_MEDIA_FILE
        args.inputs = [full_path]
        Action(args).unionForTranscribe()

        srt_ = full_path.split(".")[0] + ".srt"
        assert os.path.exists(srt_)
        subtitle_video = full_path.split(".")[0] + "_subtitle.mp4"
        assert os.path.exists(subtitle_video)

        self.removeFileAfterTest()
