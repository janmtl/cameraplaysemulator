import cv2
import numpy as np

class Box:
  def __init__(self, top, left, bottom, right):
    self.top    = top
    self.left   = left
    self.bottom = bottom
    self.right  = right

class Button:
  def __init__(self, keycode, image, box):
    self.keycode = keycode
    self.image   = image
    self.mask    = self.getMaskFromImage(image)
    self.box     = box

  def render(self, frame, **kwargs):
    position = kwargs.get('position', None)

    if position:
      cv2.rectangle(frame, (position.x,position.y), (position.x + (self.box.right-self.box.left), position.y + (self.box.bottom-self.box.top)), (255, 0, 0), 2)
      frame[  position.y:position.y + (self.box.bottom-self.box.top),
              position.x:position.x + (self.box.right-self.box.left)] *= self.mask
      frame[  position.y:position.y + (self.box.bottom-self.box.top),
              position.x:position.x + (self.box.right-self.box.left)] += self.image

    else:
      cv2.rectangle(frame, (self.box.left,self.box.top), (self.box.right, self.box.bottom), (255, 0, 0), 2)
      frame[  self.box.top:self.box.bottom,
              self.box.left:self.box.right] *= self.mask
      frame[  self.box.top:self.box.bottom,
              self.box.left:self.box.right] += self.image

  def hit(self,x,y):
    return (x >= self.box.left and x <= self.box.right) and (y >= self.box.top and y <= self.box.bottom)

  # Utility Methods
  @staticmethod
  def getMaskFromImage(image):
    mask = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    mask = cv2.threshold( mask, 10, 1, cv2.THRESH_BINARY_INV)[1]
    h,w = mask.shape
    return np.repeat( mask, 3).reshape( (h,w,3) )

