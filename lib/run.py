from os.path import abspath, realpath, join
import subprocess
import cv2
import urllib
import numpy as np

from Box        import Box
from Config     import config, here
from Emulator   import Emulator
from Controller import Controller
from Button     import Button
from Stream     import Stream
from Stage      import Stage

# Background Subtraction Scanner
backsub = cv2.BackgroundSubtractorMOG()
# Image assets
assets_path = join(here, '../assets/')
image_path  = join(assets_path, 'images/')

#Define controller
controller = Controller(box = Box(config.CONTROLLER.TOP, 
                                  config.CONTROLLER.LEFT,
                                  config.CONTROLLER.BOTTOM,
                                  config.CONTROLLER.RIGHT),
                        buttons = [
                          Button('z', cv2.imread(abspath(join(image_path, "b.png")), 1),      Box(  0,   0, 160, 213)),
                          Button('x', cv2.imread(abspath(join(image_path, "a.png")), 1),      Box(160,   0, 320, 213)),
                          Button('w', cv2.imread(abspath(join(image_path, "up.png")), 1),     Box(320,   0, 480, 213)),
                          Button('s', cv2.imread(abspath(join(image_path, "down.png")), 1),   Box(  0, 213, 160, 426)),
                          Button('a', cv2.imread(abspath(join(image_path, "left.png")), 1),   Box(160, 213, 320, 426)),
                          Button('d', cv2.imread(abspath(join(image_path, "right.png")), 1),  Box(320, 213, 480, 426)),
                          Button('q', cv2.imread(abspath(join(image_path, "select.png")), 1), Box(  0, 426, 160, 639)),
                          Button('e', cv2.imread(abspath(join(image_path, "start.png")), 1),  Box(160, 426, 320, 639)),
                          Button('x',  cv2.imread(abspath(join(image_path, "empty.png")), 1), Box(320, 426, 480, 639))
                        ],
                        min_blob_width  = config.CONTROLLER.MIN_BLOB_WIDTH, 
                        min_blob_height = config.CONTROLLER.MIN_BLOB_HEIGHT)
print controller

#Define emulator
emulator = Emulator(box = Box(config.EMULATOR.TOP,
                              config.EMULATOR.LEFT,
                              config.EMULATOR.BOTTOM,
                              config.EMULATOR.RIGHT),
                    window_name   = config.EMULATOR.WINDOW_NAME,
                    keylog_length = config.KEYLOG.MAXLEN,
                    logdir        = join(here,config.EMULATOR.LOGDIR))
print emulator

#Define stage
stage = Stage(box = Box(config.STAGE.TOP,
                        config.STAGE.LEFT,
                        config.STAGE.BOTTOM,
                        config.STAGE.RIGHT),
              controller_box = controller.box,
              emulator_box   = emulator.box,
              keylog_box = Box(config.KEYLOG.TOP,
                               config.KEYLOG.LEFT,
                               config.KEYLOG.BOTTOM,
                               config.KEYLOG.RIGHT),
              keylog_step = config.KEYLOG.STEP,
              infopanel_box = Box(config.INFOPANEL.TOP,
                                  config.INFOPANEL.LEFT,
                                  config.INFOPANEL.BOTTOM,
                                  config.INFOPANEL.RIGHT),
              infopanel_text = config.INFOPANEL.TEXT)
stage_frame = stage.init_stage_frame()
print stage


#Define stream
stream = Stream(stage             = stage,
                key               = config.STREAM.KEY,
                ffmpeg_bin        = config.STREAM.FFMPEG_BIN,
                frames_per_second = config.STREAM.FRAMES_PER_SECOND,
                output_uri        = config.STREAM.OUTPUT_URI,
                emulator_window   = emulator.window)
print stream

stream=urllib.urlopen(config.CONTROLLER.CAPTURE)
bytes=''
while True:
  bytes+=stream.read(1024)
  a = bytes.find('\xff\xd8')
  b = bytes.find('\xff\xd9')
  if a!=-1 and b!=-1:
    jpg = bytes[a:b+2]
    bytes= bytes[b+2:]
    controller_frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
    
    #Find the position of the user
    users = controller.scan(frame   = controller_frame,
                            backsub = backsub)

    #Perform the user's action
    controller.bubble_vote(users    = users,
                           emulator = emulator)

    #Draw the controller on the capture_frame
    controller.render(frame = controller_frame)

    #Draw the stage
    stage.render( stage_frame      = stage_frame,
                  controller_frame = controller_frame, 
                  keylog           = emulator.keylog)
    #Display the results
    #cv2.imshow('Stage_frame', stage_frame)

    #Stream the results
    stream.broadcast(stage_frame)
    
    if cv2.waitKey(1) ==27:
      exit(0)

# Clean up everything before leaving
emulator.logfile.close()
cv2.destroyAllWindows()
