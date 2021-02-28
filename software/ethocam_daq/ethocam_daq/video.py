import os
import subprocess

class VideoRecorder:

    def __init__(self,param,directory=None):
        self.directory = directory
        self.directory
        self.param = param

    def run(self):
        if self.directory is None:
            filename = self.param['filename']
        else:
            filename = os.path.join(self.directory,self.param['filename'])
        duration = sec_to_msec(self.param['duration'])
        cmd = [ 'raspivid', '-n', '-o', f'{filename}', '-t', f'{duration}'] 
        rtn = subprocess.call(cmd)
        if rtn == 0:
            return True 
        else:
            return False

# Utility
# ----------------------------------------------------------------------------
def sec_to_msec(value):
    return int(1000*value)

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    param = {
        'filename'  : 'vid.h264', 
        'duration'  :  10.0,
            }

    rec = VideoRecorder(param,'/home/pi/data')
    rec.run()
