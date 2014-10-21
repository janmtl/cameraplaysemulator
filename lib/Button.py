import cv2
import numpy as np
import math

class Button:
  def __init__(self, keycode, image, box):
    self.keycode = keycode
    self.image   = image
    self.mask    = self.getMaskFromImage(image)
    self.box     = box
    self.votes   = 0

  def render(self, frame, **kwargs):
    box = kwargs.get('box', None)

    red   = min(4*self.votes, 255)
    green = 0
    blue  = 0

    if box:
      cv2.rectangle(frame, (box.left,box.top), (box.right, box.bottom), (blue, green, red), 2)
      [image_box, frame_box] = self.box.intersect(box)
      frame[frame_box.top:frame_box.bottom, frame_box.left:frame_box.right] \
        *= self.mask[image_box.top:image_box.bottom, image_box.left:image_box.right] 
      frame[frame_box.top:frame_box.bottom, frame_box.left:frame_box.right] \
        += self.image[image_box.top:image_box.bottom, image_box.left:image_box.right] 

    else:
      cv2.rectangle(frame, (self.box.left,self.box.top), (self.box.right, self.box.bottom), (blue, green, red), 2)
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

