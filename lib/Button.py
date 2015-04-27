import cv2
import numpy as np
import math
from Box import Box

class Button:
  def __init__(self, keycode, image, box):
    self.keycode = keycode
    self.image   = image
    self.box     = box
    self.mask    = self.getMaskFromImage(self, image)
    self.votes   = 0

  def render(self, frame, **kwargs):
    box = kwargs.get('box', None)
    live = kwargs.get('live', None)
    tot_votes = kwargs.get('tot_votes', 1)
    tot_votes = max(tot_votes, 1)

    thickness = 6
    if live:
      # red   = min(4*self.votes/tot_votes, 255)
      red   = min(255*self.votes/tot_votes, 255)
      green = 0
      blue  = 0
    else:
      red   = 0
      green = 0
      blue  = 0   

    if box:
      if live: cv2.rectangle(frame, (box.left+thickness/2,box.top+thickness/2), (box.right-thickness/2, box.bottom-thickness/2), (blue, green, red), thickness)
      image_box = Box(0,0,self.mask.shape[0], self.mask.shape[1])
      [image_box, frame_box] = image_box.intersect(box)
      frame[frame_box.top:frame_box.bottom, frame_box.left:frame_box.right] \
        *= self.mask[image_box.top:image_box.bottom, image_box.left:image_box.right] 
      frame[frame_box.top:frame_box.bottom, frame_box.left:frame_box.right] \
        += self.image[image_box.top:image_box.bottom, image_box.left:image_box.right] 

    else:
      if live: cv2.rectangle(frame, (self.box.left+thickness/2,self.box.top+thickness/2), (self.box.right-thickness/2, self.box.bottom-thickness/2), (blue, green, red), thickness)
      image_box = Box(0,0,self.mask.shape[0], self.mask.shape[1])
      [image_box, frame_box] = image_box.intersect(self.box)
      frame[frame_box.top:frame_box.bottom, frame_box.left:frame_box.right] \
        *= self.mask[image_box.top:image_box.bottom, image_box.left:image_box.right]
      frame[frame_box.top:frame_box.bottom, frame_box.left:frame_box.right] \
        += self.image[image_box.top:image_box.bottom, image_box.left:image_box.right]

  def hit(self,x,y):
    return (x >= self.box.left and x <= self.box.right) and (y >= self.box.top and y <= self.box.bottom)

  # Utility Methods
  @staticmethod
  def getMaskFromImage(self, image):
    mask = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    mask = cv2.threshold( mask, 10, 1, cv2.THRESH_BINARY_INV)[1]
    h,w  = mask.shape

    return np.repeat( mask, 3).reshape( (h,w,3) )


