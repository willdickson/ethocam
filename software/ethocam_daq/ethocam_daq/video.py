import os
import subprocess

class VideoRecorder:

    def __init__(self,config,directory=None):
        self.filename = config['Video']['filename']
        self.duration = config['Video'].getfloat('duration')
        self.directory = directory

    def run(self):
        if self.directory is None:
            filename = self.param['filename']
        else:
            filename = os.path.join(self.directory,self.filename)
        duration_ms = sec_to_msec(self.duration)
        cmd = [ 'raspivid', '-n', '-o', f'{filename}', '-t', f'{duration_ms}'] 
        rtn = subprocess.call(cmd)
        if rtn == 0:
            return True 
        else:
            return False

# Utility
# ----------------------------------------------------------------------------
def sec_to_msec(value):
    return int(1000*value)

