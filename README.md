# subtitles_translator 自动生成字幕、翻译字幕、添加字幕程序
## 该程序实现以下功能：
1. 通过whisper实现：根据video/audio文件自动检测语言并生成对应语言的字幕
2. 通过whisper实现：根据video/audio文件自动检测语言，并生成翻译后的英文字幕
3. 通过whisper+translatepy实现：根据video/audio文件自动检测语言，并生成指定翻译后语言的字幕
4. 通过whisper+translatepy+ffmpeg实现：根据video/audio自动检测语言，生成指定翻译后语言的字幕，并自动添加到video文件中

其中生成字幕文件、翻译字幕文件、添加字幕文件功能相对独立，使用者可以先自己生成需要的字幕文件，修改后再通过程序添加字幕到视频中

## 下载安装    
python版本需要>=3.9  

1. `git clone git@github.com:viking-man/subtitles_translator.git`
2. `cd subtitles_translator`
3. `pip install .`
4. `brew install ffmpeg`  需要自己安装ffmpeg，通过pip安装的话，与whisper使用的ffmpeg-python有冲突
   
## 常用命令
- 生成对应语言的字幕文件，生成的字幕文件放到与video文件同一目录下

  `subtitle -t /your/video/file/path/file.mp4`

- 生成字幕文件并翻译成指定语言，默认翻译成中文，注意！！因为使用了Google翻译，国内如果没有vpn的话，无法使用翻译功能，只能生成英文字幕。并且需要在命令行指定--China避免调用Google服务。


  国外或者有VPN：
  `subtitle -tl /your/video/file/path/file.mp4 --targetLang "zh"`

  国内：
  `subtitle -tl /your/video/file/path/file.mp4 --China`

- 生成字幕文件并翻译成指定语言，自动生成一个包含已翻译字幕文件的视频，通过以下命令会新生成两个文件：
  1.翻译后的字幕文件
  2.添加了字幕的视频文件
  3.原视频文件保留不变

  国外：
  `subtitle -u /your/video/file/path/file.mp4` 默认翻译成中文，需要指定对应语言添加 --targetLang "your language"

  国内：
  `subtitle -u /your/video/file/path/file.mp4 --China` 翻译成英文，并自动添加到视频中

- 添加指定的字幕文件到视频中，此功能可以由ffmpeg单独完成，程序也只是调用了ffmpeg的方法
  
  `subtitle -a /your/video/file/path/file.mp4 --targetSubtitle "your subtitle file path"`

## 效果展示
1. 生成的.srt字幕文件

   ![ 字幕文件](img/srt_short.png)
2. 自动生成的字幕视频
  
   ![ 字幕截图](img/video_shoot.png)


