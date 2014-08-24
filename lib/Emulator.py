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
  def __init__(self):
    self.window = self.get_window()

  def get_window(self):
    #First find the right window
    result = subprocess.check_output(["xdotool", "search","--sync", "--name", config.EMULATOR.NAME])
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
    subprocess.call(["sleep", ".1"])
    return subprocess.call(["xdotool", "keyup", "--window", str(self.window._id), button.keycode])