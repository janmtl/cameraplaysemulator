from os.path import abspath, realpath, join
import cv2, subprocess
import numpy as np

from Config     import config, here
from Emulator   import Emulator
from Controller import Controller
from Button     import Button, Box
from Stream     import Stream

# Background Subtraction Scanner
backsub = cv2.BackgroundSubtractorMOG()
# Image assets
assets_path = join(here, '../assets/')
image_path  = join(assets_path, 'images/')

#Define controller
controller = Controller(config.CONTROLLER.WIDTH, config.CONTROLLER.HEIGHT, [
  Button('z', cv2.imread(abspath(join(image_path, "b.png")), 1),      Box(  0,   0, 160, 213)),
  Button('x', cv2.imread(abspath(join(image_path, "a.png")), 1),      Box(160,   0, 320, 213)),
  Button('w', cv2.imread(abspath(join(image_path, "up.png")), 1),     Box(320,   0, 480, 213)),
  Button('s', cv2.imread(abspath(join(image_path, "down.png")), 1),   Box(  0, 213, 160, 426)),
  Button('a', cv2.imread(abspath(join(image_path, "left.png")), 1),   Box(160, 213, 320, 426)),
  Button('d', cv2.imread(abspath(join(image_path, "right.png")), 1),  Box(320, 213, 480, 426)),
  Button('q', cv2.imread(abspath(join(image_path, "select.png")), 1), Box(  0, 426, 160, 639)),
  Button('e', cv2.imread(abspath(join(image_path, "start.png")), 1),  Box(160, 426, 320, 639)),
  Button('',  cv2.imread(abspath(join(image_path, "empty.png")), 1),  Box(320, 426, 480, 639))
], config.CONTROLLER.MIN_BLOB_WIDTH, config.CONTROLLER.MIN_BLOB_HEIGHT)
print controller

#Define emulator
emulator = Emulator(config.EMULATOR.NAME)
print emulator

#Define stage
stage = Stage(config.STREAM.WIDTH, config.STREAM.HEIGHT, controller, config.CONTROLLER.TOP, config.CONTROLLER.LEFT)
print stage

#Define stream
stream = Stream(config.STREAM.KEY,
                config.STREAM.FFMPEG_BIN,
                config.STREAM.FRAMES_PER_SECOND,
                config.STREAM.OUTPUT_URI,
                emulator.window,
                config.STREAM.HEIGHT,
                config.STREAM.WIDTH)
print stream

capture = cv2.VideoCapture(config.CONTROLLER.CAPTURE)
if capture.isOpened():
  stage_frame = controller.get_stage_frame()

  while True:
    ret, capture_frame = capture.read()
    if ret:
      #Find the position of the user
      users = controller.scan(capture_frame, backsub)

      #Display the controller
      controller.render(capture_frame)

      #Perform the user's action
      controller.vote(users, emulator)

      #Display the results
      cv2.imshow('Stream', stage_frame)

      #Stream the results
      #stream.broadcast(frame)
    else:
      print "No ret"
      break

    escape = cv2.waitKey(33)
    if escape == 27 or escape == 1048603:
      break
else:
  print "No capture"

# Clean up everything before leaving
cv2.destroyAllWindows()
capture.release()