import math

class Box:
  def __init__(self, top, left, bottom, right):
    self.top    = top
    self.left   = left
    self.bottom = bottom
    self.right  = right

  def __repr__(self):
    return ('Box: (%s, %s, %s, %s)\n') \
             % (self.top, self.left, self.bottom, self.right)

  def intersect(self, target):
    image_box = Box(0,0,0,0)
    frame_box = Box(0,0,0,0)

    #fit x direction
    image_width  = self.right - self.left
    target_width = target.right - target.left
    if(image_width>=target_width):
      image_box.left  = math.floor(image_width/2 - target_width/2)
      image_box.right = math.floor(image_width/2 + target_width/2)
      frame_box.left  = target.left
      frame_box.right = target.right
    else:
      image_box.left  = 0
      image_box.right = image_width
      frame_box.left  = target.left + math.floor(target_width/2 - image_width/2)
      frame_box.right = frame_box.left + image_width

    #fit y direction
    image_height  = self.bottom - self.top
    target_height = target.bottom - target.top
    if(image_height>=target_height):
      image_box.top    = math.floor(image_height/2 - target_height/2)
      image_box.bottom = math.floor(image_height/2 + target_height/2)
      frame_box.top    = target.top
      frame_box.bottom = target.bottom
    else:
      image_box.top    = 0
      image_box.bottom = image_height
      frame_box.top    = target.top + math.floor(target_height/2 - image_height/2)
      frame_box.bottom = frame_box.top + image_height

    return [image_box, frame_box]