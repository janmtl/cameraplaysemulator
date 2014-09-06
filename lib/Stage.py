import cv2
import numpy as np

class Stage:
  def __init__(self, box, controller_box, emulator_box, keylog_box, infopanel_box):
    self.box            = box
    self.controller_box = controller_box
    self.emulator_box   = emulator_box
    self.keylog_box     = keylog_box
    self.infopanel_box  = infopanel_box

  def __repr__(self):
    return ('Stage: \n'
            '  box: (%s, %s, %s, %s)\n'
            '  controller box: (%s, %s, %s, %s)\n'
            '  keylog box: (%s, %s, %s, %s)\n'
            '  infopanel box: (%s, %s, %s, %s)\n') \
            % (self.box.top, self.box.left, self.box.bottom, self.box.right,
               self.controller_box.top, self.controller_box.left, self.controller_box.bottom, self.controller_box.right,
               self.keylog_box.top, self.keylog_box.left, self.keylog_box.bottom, self.keylog_box.right,
               self.infopanel_box.top, self.infopanel_box.left, self.infopanel_box.bottom, self.infopanel_box.right,)

  def init_stage_frame(self):
    return np.zeros((self.box.bottom-self.box.top,self.box.right-self.box.left,3), np.uint8)

  def render(self, stage_frame, controller_frame, keylog):
    #Place the controller frame
    stage_frame[self.controller_box.top : self.controller_box.bottom,
                self.controller_box.left : self.controller_box.right] = controller_frame

    #Draw a placeholder for emulator box
    cv2.rectangle(stage_frame, (self.emulator_box.left,self.emulator_box.top), (self.emulator_box.right,self.emulator_box.bottom), (0, 255, 0), 2)
    cv2.line(stage_frame, (self.emulator_box.left,self.emulator_box.top), (self.emulator_box.right,self.emulator_box.bottom), (0, 255, 0), 2)
    cv2.line(stage_frame, (self.emulator_box.left,self.emulator_box.bottom), (self.emulator_box.right,self.emulator_box.top), (0, 255, 0), 2)

    #Draw the keylog

    #Draw the infopanel