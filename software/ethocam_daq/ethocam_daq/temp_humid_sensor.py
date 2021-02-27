import board
import adafruit_si7021
 

class TempHumidSensor:

    def __init__(self):
        self.device = adafruit_si7021.SI7021(board.I2C()) 

    @property
    def temperature(self):
        return self.device.temperature

    @property
    def humidity(self):
        return sel.device.humidity





