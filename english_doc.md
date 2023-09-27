# *subtitles_translator*
#### Automated Subtitle Generation, Translation, and Addition Program

## This program accomplishes the following tasks
1. Using Whisper: Automatically detects the language based on video/audio files and generates subtitles in the corresponding language.
2. Using Whisper: Automatically detects the language based on video/audio files and generates translated English subtitles.
3. Using Whisper + translatepy: Automatically detects the language based on video/audio files and generates subtitles in a specified translated language.
4. Using Whisper + translatepy + ffmpeg: Automatically detects the language based on video/audio files, generates subtitles in a specified translated language, and automatically adds them to the video file.
  
The functions for generating subtitle files, translating subtitle files, and adding subtitle files are relatively independent. Users can first generate the required subtitle files on their own, make modifications, and then use the program to add subtitles to the video as needed.

## Download and Installation 
Python version 3.9 or higher is required. 

1. `git clone git@github.com:viking-man/subtitles_translator.git`
2. `cd subtitles_translator`
3. `pip install .`
4. `brew install ffmpeg`  - You need to install ffmpeg manually

***For Windows systems, the commands are similar. In the third step, simply use the python setup.py install command for installation. You will also need to install ffmpeg manually.***
   
## Common Commands
- Generate subtitles in the corresponding language. The generated subtitle file will be placed in the same directory as the video file.

  `subtitle -t /your/video/file/path/file.mp4`

- Generate subtitle files and translate them into a specified language. The default translation language is Chinese,you can choose your language using `--target-lang yourlang`.

  `subtitle -tl /your/video/file/path/file.mp4 --target-lang "zh"`


- Generate subtitle files and translate them into a specified language. Automatically generate a video containing the translated subtitle file. This command will create two new files:

  1. Translated subtitle file.
  2. Video file with subtitles added.
  3. The original video file remains unchanged.

  `subtitle -u /your/video/file/path/file.mp4` 
    
    Default translation to Chinese, specify the target language with`--target-lang "your language"`

- Add specified subtitle files to a video. This function can be done separately using ffmpeg, and the program calls ffmpeg methods.
  
  `subtitle -a /your/video/file/path/file.mp4 --target-subtitles "your subtitle file path"`

- Generate subtitle files in the language corresponding to the video and add subtitles to the video without translation.

  `subtitle -ut /your/video/file/path/file.mp4`
  

## Other Optional Parameters  

| Parameter | Description | Example |
|--------|--------|--------|
|  --output-dir  | Specify the file output directory. Default is the same directory as the source video file.  | --outputDir /Users/your_name/xx/xx/xx   |
| --outputs  | Specify output file names, one for each input. Default names are "source file name" + "_subtitles" + source file format.   | --outputs xxxx.mp4   |
| --lang  | Specify the language used in the source file. It is automatically detected by default.   | --lang “Korean”   |
| --target-lang  | Specify the language you want to translate to. Default is 'zh' for Chinese translation.  | --targetLang "Japanese"   |
| --whisper-model  | Specify the Whisper model type. Default is small, which provides moderate translation quality. If you have enough memory and a fast internet connection, you can choose medium or large.  | --whisper-model medium   |
| --device  | Specify the type of GPU to use for code execution. Default is cuda, and if not available, it uses CPU.   | --device cuda   |



## Effect Display
1. Generated .srt subtitle file

   [![字幕文件](img/srt_short.png)](srt/tzuyu_secret_friend.srt)

2. Video Example 1: Automatically adding subtitles from Korean to Chinese
   <a href="video/tzuyu_secret_friend_subtitle.mp4">
    <img src="img/video_shoot.png" alt="子瑜的秘密挚友">
   </a>


3. Video Example 2: Automatically adding subtitles from English to Chinese
   <a href="video/trump_speech_subtitle.mp4">
    <img src="img/trump_speech.png" alt="川普演讲">
   </a>


