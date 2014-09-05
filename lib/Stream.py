from config import config
import subprocess

class Stream:
  def __init__(self, key, ffmpeg_bin, frames_per_second, output_uri, emulator_window, height, width):
    self.key               = key
    self.ffmpeg_bin        = ffmpeg_bin
    self.frames_per_second = frames_per_second
    self.output_uri        = output_uri
    self.emulator_window   = emulator_window
    self.height            = height
    self.width             = width
    self.stream_pipe       = self.get_stream_pipe()

  def __repr__(self):
    return ('Stream: \n',
            '  key: %s\n',
            '  ffmpeg_bin: %s\n',
            '  frames_per_second: %s\n',
            '  output_uri: %s\n',
            '  height: %s\n',
            '  width: %s\n') \
            % (self.key, self.ffmpeg_bin, self.frames_per_second, self.output_uri, self.height, self.width)

  def get_stream_pipe(self):
    command = [ self.ffmpeg_bin,
      '-y', # (optional) overwrite output file if it exists
      '-f', 'rawvideo',
      '-vcodec','rawvideo',
      '-s', str(self.width) + 'x' + str(self.height), # size of one frame
      '-pix_fmt', 'rgb24',
      '-r', '10', # frames per second
      '-i', '-', # The imput comes from a pipe
      '-f', 'x11grab',
      '-s', str(self.emulator_window.w) + 'x' + str(self.emulator_window.h),
      '-r', str(self.frames_per_second),
      '-i', ':0.0',
      '-f', 'alsa',
      '-i', 'pulse',
      '-f', 'flv',
      '-r', '10',
      '-filter_complex', 'overlay=0:0',
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
      '-s', str(self.width) + 'x' + str(self.height),
      '-preset', 'ultrafast',
      '-tune', 'film',
      '-acodec', 'libmp3lame',
      '-threads', '0',
      '-strict', 'normal',
      self.output_uri ]

    return subprocess.Popen(command, stdin=subprocess.PIPE)

  def broadcast(self, frame):
    self.stream_pipe.stdin.write(frame.tostring())