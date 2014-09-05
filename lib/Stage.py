from config import config

class Stage:
  def __init__(self, width, height):
    self.width             = width
    self.height            = height

  def __repr__(self):
    return ('Stage: \n',
            '  size(w,h): (%s, %s)\n') \
            % (self.width, self.height)

  def render(self, stage_frame, controller_frame, emulator_keylog):
    pass