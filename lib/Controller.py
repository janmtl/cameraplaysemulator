import cv2
from datetime import datetime

class Controller:
  def __init__(self, box, buttons, min_blob_width, min_blob_height, press_interval):
    self.box             = box
    self.buttons         = buttons
    self.min_blob_width  = min_blob_width
    self.min_blob_height = min_blob_height
    self.epoch           = datetime.now()
    self.votes           = [0]*len(self.buttons)
    self.press_interval  = press_interval

  def __repr__(self):
    return ('Controller: \n'
            '  box: (%s, %s, %s, %s)\n'
            '  buttons: %s\n'
            '  min blob size (w,h): (%s, %s)\n') \
            % (self.box.top, self.box.left, self.box.bottom, self.box.right,
               len(self.buttons),
               self.min_blob_width, self.min_blob_height)

  def render(self, frame):
    for idx, button in enumerate(self.buttons):
      button.votes = self.votes[idx]
      button.render(frame)

  # def press(self, x, y, emulator):
  #   for button in self.buttons:
  #     if button.hit(x,y):
  #       emulator.press(button)
  #       break

  def vote(self, users, emulator):
    for user in users:
      for k in xrange(0,len(self.buttons)):
        if self.buttons[k].hit(user['x'],user['y']):
          self.votes[k] += 1
    # Has an interval gone by?
    if ((datetime.now()-self.epoch).seconds > self.press_interval):
      # Have we accumulated any votes?
      if max(self.votes) > 0:
        # Which button should we press?
        b = self.buttons[self.votes.index(max(self.votes))]
        # Check if the button is the randomize button
        emulator.press(b)
      # Reset votes and epoch
      self.votes = [0]*len(self.buttons)
      self.epoch = datetime.now()

  def scan(self, frame, backsub, blur = 5):
    fgmask = backsub.apply(cv2.blur(frame,(blur, blur)), None, 0.03)
    contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
    ccenters = []
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        if w > self.min_blob_width and h > self.min_blob_height:
            midx = (x+(w/2))
            midy = (y+(h/2))
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
            cv2.drawContours(frame, contour, -1, (255, 0, 0), 1)    
            ccenters.append({'x': midx, 'y': midy})
  
    return ccenters
