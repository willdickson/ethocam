import board
import adafruit_tsl2591


class LightSensor:

    def __init__(self):
        self.device = adafruit_tsl2591.TSL2591(board.I2C())
        self.device.gain = adafruit_tsl2591.GAIN_MED
        self.device.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS 

    @property
    def data(self):
        data = {
                'lux': self.device.lux,
                'visible': self.device.visible,
                'infrared': self.device.infrared,
                'full_spectrum': self.device.full_spectrum,
                }
        return data
        

