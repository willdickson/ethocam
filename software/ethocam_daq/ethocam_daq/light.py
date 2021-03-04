import time
import board
import adafruit_tsl2591


class LightSensor:

    def __init__(self,config):
        self.number_of_reads = config['Light'].getint('number_of_reads')
        self.read_dt = config['Light'].getfloat('read_dt')
        self.device = adafruit_tsl2591.TSL2591(board.I2C())
        self.device.gain = adafruit_tsl2591.GAIN_MED
        self.device.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS 

    @property
    def data(self,num=1):
        data = {}
        for i in range(self.number_of_reads):
            data['lux'] = self.device.lux
            data['visible'] = self.device.visible
            data['infrared'] = self.device.infrared
            data['full_spectrum'] = self.device.full_spectrum
            time.sleep(self.read_dt)
        return data
        

