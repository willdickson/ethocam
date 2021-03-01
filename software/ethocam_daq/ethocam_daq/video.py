import os
import subprocess

class VideoRecorder:

    def __init__(self,config,directory=None):
        self.filename = config['Video']['filename']
        self.duration = config['Video'].getfloat('duration')
        try:
            self.bitrate = config['Video'].getint('bitrate')
        except ValueError:
            self.bitrate = None
        self.mode = config['Video']['mode']
        if self.mode == '1080p':
            self.width = 1920
            self.height = 1080
        elif self.mode == '720p':
            self.width = 1280
            self.height = 720
        elif self.mode == '480p':
            self.width = 640 
            self.height = 480
        else:
            self.mode = None
            self.width = None
            self.height = None
        self.directory = directory

    def run(self):
        if self.directory is None:
            filename = self.param['filename']
        else:
            filename = os.path.join(self.directory,self.filename)
        duration_ms = sec_to_msec(self.duration)
        cmd = [ 'raspivid', '-n']
        cmd.extend(['-o', f'{filename}']) 
        cmd.extend(['-t', f'{duration_ms}'])
        if self.bitrate is not None:
            cmd.extend(['-b', f'{self.bitrate}'])
        if self.mode is not None:
            cmd.extend(['-w', f'{self.width}', '-h', f'{self.height}'])
        rtn = subprocess.call(cmd)
        if rtn == 0:
            return True 
        else:
            return False

# Utility
# ----------------------------------------------------------------------------
def sec_to_msec(value):
    return int(1000*value)

