from Config import config
from os.path import abspath, realpath, join
import cv2, subprocess
import numpy as np

class Window:
  def __init__(self, _id, x, y, h, w):
    self._id = _id
    self.x   = x
    self.y   = y
    self.h   = h
    self.w   = w

class Emulator:
  def __init__(self, window_name, keyloglength, logfile):
    self.window       = self.get_window(window_name)
    self.keylog       = []
    self.keyloglength = keyloglength
    self.logfile      = logfile

  def __repr__(self):
    return 'Emulator: \n  window (_id): %s\n  position (x,y): (%s, %s)\n  size (w,h): (%s, %s)\n' % (self.window._id, self.window.x, self.window.y, self.window.w, self.window.h)

  def get_window(self, window_name):
    #First find the right window
    result = subprocess.check_output(["xdotool", "search","--sync", "--name", window_name])
    _id = result.split("\n")[-2]

    #Now extract the geometry
    result = subprocess.check_output(["xdotool", "getwindowgeometry", str(_id)])
    position = result.split("\n")[1][12:].split(",")
    x = int(position[0])
    y = int(position[1].split(" ")[0])
    geometry = result.split("\n")[2][12:].split("x")
    h = int(geometry[0])
    w = int(geometry[1])

    return Window(_id, x, y, h, w)

  def press(self, button):
    if subprocess.call(["xdotool", "keydown", "--window", str(self.window._id), button.keycode]) != 0:
      return
    #ADD BUTTON TO KEYLOG HERE AND POP (KEYLOGLENGTH+1)th button
    return subprocess.call(["xdotool", "keyup", "--window", str(self.window._id), button.keycode])