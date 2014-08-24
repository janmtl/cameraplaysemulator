from Config import config
import cv2

class Controller:
  def __init__(self, width, height, buttons):
    self.width   = width
    self.height  = height
    self.buttons = buttons

  def render(self, frame):
    for button in self.buttons:
      button.render(frame)

  def press(self, x, y, emulator):
    for button in self.buttons:
      if button.hit(x,y):
        emulator.press(button)
        break

  @staticmethod
  def scan(frame, backsub):
    fgmask = backsub.apply(frame, None, 0.03)
    contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contourAreas = {cv2.contourArea(c):c for c in contours}

    ccenter = [None, None]
    if len(contours) != 0:
      maxarea = max(contourAreas.keys())
      if maxarea > config['VIDEO']['AREA_THRESHOLD']:
        largestContour = contourAreas[maxarea]
        ccenter, cradius = cv2.minEnclosingCircle(largestContour)
        cv2.circle(frame,(int(ccenter[0]), int(ccenter[1])),3,(0,255,255),2)

    return ccenter