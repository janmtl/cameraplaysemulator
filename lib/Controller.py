from Config import config
import cv2

def draw_detections(img, rects, thickness = 1):
  for x, y, w, h in rects:
    pad_w, pad_h = int(0.15*w), int(0.05*h)
    cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

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
        print button.keycode
        emulator.press(button)
        break

  def vote(self, users, emulator):
    votes = [0]*len(self.buttons)
    for user in users:
      for k in xrange(0,len(self.buttons)):
        if self.buttons[k].hit(user['x'],user['y']):
          votes[k] += 1
    
    print self.buttons[votes.index(max(votes))].keycode
    emulator.press(self.buttons[votes.index(max(votes))])

  @staticmethod
  def scan(frame, backsub, blur = 5):
    fgmask = backsub.apply(cv2.blur(frame,(blur, blur)), None, 0.03)
    contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
    ccenters = []
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        if w > 5 and h > 10:
            midx = (x+(w/2))
            midy = (y+(h/2))
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
            cv2.drawContours(frame, contour, -1, (255, 0, 0), 1)    
            ccenters.append({'x': midx, 'y': midy})
  
    return ccenters