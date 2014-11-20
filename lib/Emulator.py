from os.path import abspath, realpath, join
from collections import deque
import cv2, subprocess
import numpy as np

class Window:
  def __init__(self, _id, x, y, width, height):
    self._id    = _id
    self.x      = x
    self.y      = y
    self.width  = width
    self.height = height

class Emulator:
  def __init__(self, box, window_name, keylog_length, logdir):
    self.box           = box
    self.window        = self.get_window(window_name)
    self.keylog        = deque(maxlen=keylog_length)
    self.logdir        = logdir
    self.logfile       = open(join(self.logdir, 'keys.txt'), "w")
    self.keycount      = 0

  def __repr__(self):
    return ('Emulator: \n'
            '  box: (%s, %s, %s, %s)\n'
            '  window (_id): %s\n'
            '    position (x,y): (%s, %s)\n'
            '    size (w,h): (%s, %s)\n'
            '  logdir: %s\n') \
             % (self.box.top, self.box.left, self.box.bottom, self.box.right,
                self.window._id,
                self.window.x, self.window.y,
                self.window.width, self.window.height,
                self.logdir)

  def get_window(self, window_name):
    #First find the right window
    result = subprocess.check_output(["xdotool", "search","--sync", "--name", window_name])
    _id = result.split("\n")[-2]

    #Now extract the geometry
    result = subprocess.check_output(["xdotool", "getwindowgeometry", str(_id)])
    
    position = result.split("\n")[1][12:].split(",")
    x        = int(position[0])
    y        = int(position[1].split(" ")[0])
    
    geometry = result.split("\n")[2][12:].split("x")
    width    = int(geometry[0])
    height   = int(geometry[1])

    return Window(_id, x, y, width, height)

  def press(self, button):
    if subprocess.call(["xdotool", "keydown", "--window", str(self.window._id), button.keycode]) != 0:
      return

    self.keylog.appendleft(button)
    self.logfile.write(button.keycode)
    self.keycount += 1
    if self.keycount >= 10000:
      self.logfile.close()
      self.logfile = open(join(self.logdir, 'keys' + str(self.keycount+1) + '.txt'), "w")

    return subprocess.call(["xdotool", "keyup", "--window", str(self.window._id), button.keycode])