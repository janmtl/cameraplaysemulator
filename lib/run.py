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
backsub = cv2.bgsegm.createBackgroundSubtractorMOG()
# Image assets
assets_path = join(here, '../assets/')
image_path  = join(assets_path, 'images/')

#Define controller
controller = Controller(box = Box(config.CONTROLLER.TOP, 
                                  config.CONTROLLER.LEFT,
                                  config.CONTROLLER.BOTTOM,
                                  config.CONTROLLER.RIGHT),
                        buttons = [
                          Button('q', cv2.imread(abspath(join(image_path, "select.png")), 1), Box(  0,   0, 192, 212)),
                          Button('w', cv2.imread(abspath(join(image_path, "up.png")), 1),     Box(  0, 213, 192, 427)),
                          Button('e', cv2.imread(abspath(join(image_path, "start.png")), 1),  Box(  0, 426, 192, 640)),

                          Button('a', cv2.imread(abspath(join(image_path, "left.png")), 1),   Box(192,   0, 384, 212)),
                          Button('s', cv2.imread(abspath(join(image_path, "down.png")), 1),   Box(192, 213, 384, 427)),
                          Button('d', cv2.imread(abspath(join(image_path, "right.png")), 1),  Box(192, 426, 384, 640)),

                          Button('z', cv2.imread(abspath(join(image_path, "b.png")), 1),      Box(384,   0, 480, 320)),
                          Button('x', cv2.imread(abspath(join(image_path, "a.png")), 1),      Box(384, 320, 480, 640)),

                          # Button('$', cv2.imread(abspath(join(image_path, "empty.png")), 1),  Box(320, 213, 480, 246))
                          # '$' means random keypress
                        ],
                        min_blob_width  = config.CONTROLLER.MIN_BLOB_WIDTH, 
                        min_blob_height = config.CONTROLLER.MIN_BLOB_HEIGHT,
                        press_interval  = config.CONTROLLER.PRESS_INTERVAL)
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
if hasattr(config, 'STREAM'):
  stream = Stream(stage             = stage,
                  emulator          = emulator,
                  key               = config.STREAM.KEY,
                  ffmpeg_bin        = config.STREAM.FFMPEG_BIN,
                  frames_per_second = config.STREAM.FRAMES_PER_SECOND,
                  output_uri        = config.STREAM.OUTPUT_URI)
  print stream
else:
  print "Streaming disabled in config"


if str(config.CONTROLLER.CAPTURE)[0:4]=="http":
  capture_uri = urllib.urlopen(config.CONTROLLER.CAPTURE)
  bytes=''
  captureisopen = True
  captureMode='http'
else:
  capture = cv2.VideoCapture(config.CONTROLLER.CAPTURE)
  captureisopen = capture.isOpened()
  captureMode='other'


if captureisopen:
  stage_frame = stage.init_stage_frame()
  try: 
    while True:
      if captureMode=='http':
        bytes+=capture_uri.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
          jpg = bytes[a:b+2]
          bytes= bytes[b+2:]
          controller_frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
      else:
        ret, controller_frame = capture.read()
      
      #Find the position of the user
      users = controller.scan(frame   = controller_frame,
                              backsub = backsub)

      #Perform the user's action
      controller.vote(users    = users,
                      emulator = emulator)

      #Draw the controller on the capture_frame
      controller.render(frame = controller_frame)

      #Draw the stage
      stage.render( stage_frame      = stage_frame,
                    controller_frame = controller_frame, 
                    keylog           = emulator.keylog)
      #Display the results
      cv2.imshow('Stage_frame', stage_frame)

      #Stream the results
      if hasattr(config, 'STREAM'):
        stream.init_stream_pipe()
        stream.broadcast(stage_frame)
      
      if cv2.waitKey(1) ==27:
        exit(0)
  except KeyboardInterrupt:
    pass

else:
  print("config.CONTROLLER.CAPTURE did not open\n")

# Clean up everything before leaving
stream.kill()
emulator.logfile.close()
cv2.destroyAllWindows()
