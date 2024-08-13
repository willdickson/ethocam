import os
import subprocess
from . import utility


class VideoRecorder:

    def __init__(self,config,directory=None):
        self.config = config
        self.filename = config['Video']['filename']
        self.duration = config['Video'].getfloat('duration')
        try:
            self.focus = config['Video'].getfloat('manual_focus')
        except ValueError:
            self.focus = 'auto'
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

    def run(self, tuning='regular'):
        if self.directory is None:
            filename = self.param['filename']
        else:
            filename = os.path.join(self.directory,self.filename)
        duration_ms = sec_to_msec(self.duration)
        ### libcamera-vid can be used for RPi HQ camera or camera-module 3 ###
        #cmd = [ 'libcamera-vid', '-n']
        cmd = ['libcamera-vid']
        cmd.extend(['-o', f'{filename}']) 
        cmd.extend(['-t', f'{duration_ms}'])

        ### picamera2 ###
        #picam2 = Picamera2()
        #if self.focus != 'auto':
        #    picam2.set_controls({'AfMode': controls.AfModeEnum.Manual})
        #    picam2.set_controls({'LensPosition': self.focus})

        #video_config = picam2.create_video_configuration(main={'size': (self.width,self.height)})
        #picam2.configure(video_config)
        #encoder = H264Encoder(bitrate=self.bitrate)
        #picam2.start(show_preview=True)
        #picam2.start_recording(encoder, self.filename)
        #time.sleep(self.duration)
        #picam2.stop_recording()
        #picam2.stop()
        
        if self.bitrate is not None:
            cmd.extend(['-b', f'{self.bitrate}'])
        if self.mode is not None:
            cmd.extend(['--width', f'{self.width}', '--height', f'{self.height}'])

        setting_keys = [ 'contrast', 'shutter']
        for key in setting_keys:
            try:
                value = self.config['Video'][key]
            except KeyError:
                continue
            cmd.extend([f'--{key}', value])
        if tuning == 'day':
            cmd.extend(['--tuning-file', '/usr/share/libcamera/ipa/rpi/vc4/imx477.json'])
        else:
            cmd.extend(['--tuning-file', '/usr/share/libcamera/ipa/rpi/vc4/imx708_wide_noir.json'])
        ## manual focus for camera-module 3 ##
        if self.focus != 'auto':
            cmd.extend(['--autofocus-mode', 'manual'])
            cmd.extend(['--lens-position='+ str(self.focus)])
        print (cmd)
        rtn = subprocess.call(cmd)
        if rtn == 0:
            utility.chown(filename, 'pi') 
            return True 
        else:
            return False

# Utility
# ----------------------------------------------------------------------------
def sec_to_msec(value):
    return int(1000*value)

