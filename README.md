Camera Plays Emulator
=====================
A python app that uses the feed from a webcam to send commands to a video game emulator. The output is also automatically streamed to Twitch.tv.

Based on [WhereIsTheFish](http://github.com/catherinemoresco/whereisthefish) which has been popularly implemented in [FishPlaysPokemon](http://www.twitch.tv/fishplayspokemon).

This project is in cooperation with Alex Leavitt's [uscplayspokemon](http://github.com/alexleavitt/uscplayspokemon).

Quickstart
----------
1. Make sure openCV is installed on your system
2. Start up [VBA](http://visualboyadvance.net/) with your desired ROM
3. Set `Options -> Emulator -> Show speed -> None`
4. Run `python lib/run.py`

Configuration
-------------
See the [default configuration](config/config.ini.default) that we provide. It has these sections:
### CONTROLLER
- Includes descriptors for a box (`TOP`, `LEFT`, `BOTTOM`, `RIGHT`)
- `CAPTURE` is the capture device (can be rtsp protocol too)
- `MIN_BLOB_WIDTH`, `MIN_BLOB_HEIGHT` filter out blobs in the scanner

### EMULATOR
- Includes descriptors for a box (`TOP`, `LEFT`, `BOTTOM`, `RIGHT`)
- `WINDOW_NAME` the X-window name for the emulator program (we use VBA)
- `LOGDIR` directory for logs relative to the lib directory

### KEYLOG
- Includes descriptors for a box (`TOP`, `LEFT`, `BOTTOM`, `RIGHT`)
- `MAXLEN` is the length of the key press history
- `STEP` is the pixel width of the keys when rendered in the keylog

### INFOPANEL
- Includes descriptors for a box (`TOP`, `LEFT`, `BOTTOM`, `RIGHT`)
- `TEXT` is the text that serves as a title and will be appended with a timestamp

### STAGE
- Includes descriptors for a box (`TOP`, `LEFT`, `BOTTOM`, `RIGHT`)

### STREAM
- `FFMPEG_BIN` is the binary for ffmpeg as you would call it in your terminal
- `FRAMES_PER_SECOND` is the rate set for ffmpeg
- `OUTPUT_URI` is usually an `rtmp` protocol URI from Twitch
- `KEY` is appended to the `OUTPUT_URI` when broadcasting
