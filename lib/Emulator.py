from os.path import abspath, realpath, join
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
  def __init__(self, box, window_name, keylog_length, logfile):
    self.box           = box
    self.window        = self.get_window(window_name)
    self.keylog        = []
    self.keylog_length = keylog_length
    self.logfile       = logfile

  def __repr__(self):
    return ('Emulator: \n'
            '  box: (%s, %s, %s, %s)\n'
            '  window (_id): %s\n'
            '    position (x,y): (%s, %s)\n'
            '    size (w,h): (%s, %s)\n'
            '  keylog_length: %s\n'
            '  logfile: %s\n') \
             % (self.box.top, self.box.left, self.box.bottom, self.box.right,
                self.window._id,
                self.window.x, self.window.y,
                self.window.width, self.window.height,
                self.keylog_length,
                self.logfile)

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
    height   = int(geometry[0])
    width    = int(geometry[1])

    return Window(_id, x, y, width, height)

  def press(self, button):
    if subprocess.call(["xdotool", "keydown", "--window", str(self.window._id), button.keycode]) != 0:
      return
    #ADD BUTTON TO KEYLOG HERE AND POP (KEYLOGLENGTH+1)th button
    print button.keycode
    return subprocess.call(["xdotool", "keyup", "--window", str(self.window._id), button.keycode])