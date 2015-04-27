import cv2
import numpy as np
import math
from datetime    import datetime
from collections import deque
from Box         import Box

class Stage:
  def __init__(self, box, controller_box, emulator_box, keylog_box, keylog_step, infopanel_box, infopanel_text):
    self.box             = box
    self.controller_box  = controller_box
    self.emulator_box    = emulator_box
    self.keylog_box      = keylog_box
    self.keylog_step     = keylog_step
    self.infopanel_box   = infopanel_box
    self.infopanel_text  = infopanel_text
    self.infopanel_epoch = datetime.now()

  def __repr__(self):
    return ('Stage: \n'
            '  box: (%s, %s, %s, %s)\n'
            '  controller box: (%s, %s, %s, %s)\n'
            '  keylog box: (%s, %s, %s, %s)\n'
            '  keylog step: %s\n'
            '  infopanel box: (%s, %s, %s, %s)\n'
            '  infopanel text: %s\n') \
            % (self.box.top, self.box.left, self.box.bottom, self.box.right,
               self.controller_box.top, self.controller_box.left, self.controller_box.bottom, self.controller_box.right,
               self.keylog_box.top, self.keylog_box.left, self.keylog_box.bottom, self.keylog_box.right,
               self.keylog_step,
               self.infopanel_box.top, self.infopanel_box.left, self.infopanel_box.bottom, self.infopanel_box.right,
               self.infopanel_text)

  def init_stage_frame(self):
    return np.zeros((self.box.bottom-self.box.top,self.box.right-self.box.left,3), np.uint8)

  def render(self, stage_frame, controller_frame, keylog):
    #Place the controller frame
    stage_frame[self.controller_box.top : self.controller_box.bottom,
                self.controller_box.left : self.controller_box.right] = controller_frame

    #Draw a placeholder for emulator box
    cv2.rectangle(stage_frame, (self.emulator_box.left,self.emulator_box.top), (self.emulator_box.right,self.emulator_box.bottom), (10, 10, 10), 2)
    cv2.line(stage_frame, (self.emulator_box.left,self.emulator_box.top), (self.emulator_box.right,self.emulator_box.bottom), (10, 10, 10), 2)
    cv2.line(stage_frame, (self.emulator_box.left,self.emulator_box.bottom), (self.emulator_box.right,self.emulator_box.top), (10, 10, 10), 2)

    #Draw the keylog
    stage_frame[self.keylog_box.top:self.keylog_box.bottom, self.keylog_box.left:self.keylog_box.right] = (0,0,153)
    cv2.putText(stage_frame,
                ('Last Press'),
                (self.keylog_box.left+15, self.keylog_box.top + int(math.floor((self.keylog_box.bottom - self.keylog_box.top)/2))),
                cv2.FONT_HERSHEY_TRIPLEX, #font face
                (self.keylog_box.bottom - self.keylog_box.top)/100, #font scale
                (255, 255, 255), 2) #color and thickness    
    cursor = 0
    for button in keylog:
      key_box = Box(top = self.keylog_box.top,
                    left = self.keylog_box.left + cursor + 200, 
                    bottom = self.keylog_box.bottom,
                    right = self.keylog_box.left + cursor + self.keylog_step + 200)
      button.render(stage_frame, box = key_box)
      cursor += self.keylog_step

    #Draw the infopanel
    stage_frame[self.infopanel_box.top:self.infopanel_box.bottom, self.infopanel_box.left:self.infopanel_box.right] = (0,204,255)
    elapsed_time = (datetime.now()-self.infopanel_epoch).seconds
    cv2.putText(stage_frame,
                (self.infopanel_text + ' (' + '{:02}:{:02}:{:02}'.format(elapsed_time // 3600, elapsed_time % 3600 // 60, elapsed_time % 60) + ')'),
                (self.infopanel_box.left+15, self.infopanel_box.top + int(math.floor((self.infopanel_box.bottom - self.infopanel_box.top)/2))),
                cv2.FONT_HERSHEY_TRIPLEX, #font face
                (self.infopanel_box.bottom - self.infopanel_box.top)/100, #font scale
                (0, 0, 153), 2) #color and thickness