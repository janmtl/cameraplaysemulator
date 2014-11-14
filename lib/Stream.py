import subprocess

class Stream:
  def __init__(self, stage, emulator, key, ffmpeg_bin, frames_per_second, output_uri):
    self.key               = key
    self.stage             = stage
    self.ffmpeg_bin        = ffmpeg_bin
    self.frames_per_second = frames_per_second
    self.output_uri        = output_uri
    self.emulator          = emulator
    self.stream_pipe       = None

  def __repr__(self):
    return ('Stream: \n'
            '  key: %s\n'
            '  ffmpeg_bin: %s\n'
            '  frames_per_second: %s\n'
            '  output_uri: %s\n') \
            % (self.key,
               self.ffmpeg_bin,
               self.frames_per_second,
               self.output_uri)

  def init_stream_pipe(self):
    if not self.stream_pipe:
      command = [ self.ffmpeg_bin,
        # Output
          '-y',
          '-f', 'rawvideo',
          '-vcodec','rawvideo',
          # Output frame size
          '-s', str(int(self.stage.box.right - self.stage.box.left)) + 'x' + str(int(self.stage.box.bottom - self.stage.box.top)),
          '-pix_fmt', 'rgb24',
          # Frames per second
          '-r', str(self.frames_per_second),
          '-i', '-',
        # Input from emulator
        '-f', 'x11grab',
          # Size of the emulator window
          '-s', str(int(self.emulator.box.right - self.emulator.box.left)) + 'x' + str(int(self.emulator.box.bottom - self.emulator.box.top)),
          ##'-s', 'cif',
          # Frames per second
          '-r', str(self.frames_per_second),
          # x11grab arguments
          '-i', ':0.0+' + str(self.emulator.window.x) + ',' + str(self.emulator.window.y),
        # Sound input
        '-f', 'alsa',
          '-i', 'pulse',
        # Input from stageframe
        '-f', 'flv',
          '-r', '10',
          # Overlay position
          '-filter_complex', 'overlay=' + str(self.emulator.box.left) + ':' + str(self.emulator.box.top),
          '-ac', '2',
          '-ar', '44100',
          '-vcodec', 'libx264',
          '-g', '20',
          '-keyint_min', '15',
          '-b', '900k',
          '-bufsize', '900k',
          '-minrate', '900k',
          '-maxrate', '900k',
          '-pix_fmt', 'yuv420p',
          '-crf', '30',
          # Size of the stageframe
          '-s', str(int(self.stage.box.right - self.stage.box.left)) + 'x' + str(int(self.stage.box.bottom - self.stage.box.top)),
          '-preset', 'ultrafast',
          '-tune', 'film',
          '-acodec', 'libmp3lame',
          '-threads', '0',
          '-strict', 'normal',
        self.output_uri + self.key ]
  
      print " ".join(command)
      self.stream_pipe = subprocess.Popen(command, stdin=subprocess.PIPE)

  def broadcast(self, frame):
    self.stream_pipe.stdin.write(frame.tostring())
