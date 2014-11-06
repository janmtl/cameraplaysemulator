import subprocess

class Stream:
  def __init__(self, stage, key, ffmpeg_bin, frames_per_second, output_uri, emulator_window):
    self.key               = key
    self.stage             = stage
    self.ffmpeg_bin        = ffmpeg_bin
    self.frames_per_second = frames_per_second
    self.output_uri        = output_uri
    self.emulator_window   = emulator_window
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
	# The output
        '-y',
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-s', str(int(self.stage.box.right - self.stage.box.left)) + 'x' + str(int(self.stage.box.bottom - self.stage.box.top)), # size of one frame
        '-pix_fmt', 'rgb24',
        '-r', '10', # frames per second
        '-i', '-',
        '-f', 'x11grab',
	'-s', 'cif',
        #'-s', str(int(self.stage.emulator_box.right - self.stage.emulator_box.left)) + 'x' + str(int(self.stage.emulator_box.bottom - self.stage.emulator_box.top)),
        '-r', str(self.frames_per_second),
        '-i', ':0.0+' + str(self.emulator_window.x) + ',' + str(self.emulator_window.y),
        '-f', 'alsa',
        '-i', 'pulse',
        '-f', 'flv',
        '-r', '10',
        '-filter', 'overlay=' + str(self.stage.emulator_box.left) + ':' + str(self.stage.emulator_box.top),
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
        '-force_key_frames', 'expr:gte(t,n_forced*2)',
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
