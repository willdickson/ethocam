import board
import adafruit_gps


class GPS:

    def __init__(self,config):
        self.max_attempt = config['GPS'].getint('max_attempt')
        self.dt = config['GPS'].getfloat('dt') 
        self.device = adafruit_gps.GPS_GtopI2C(board.I2C(), debug=False)  
        # Turn on the basic GGA and RMC info 
        self.device.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        # Set update rate to once a second (1hz) 
        self.device.send_command(b"PMTK220,1000")

    def read(self):
        data = {}
        attempt_cnt = 0
        while attempt_cnt < self.max_attempt:
            self.device.update()
            if self.device.has_fix:
                break
            else:
                attempt_cnt += 1
        if self.device.has_fix:
            data['latitude'] = self.device.latitude
            data['longitutde'] = self.device.longitude
            data['fix_quality'] = self.device.fix_quality
            if self.device.satellites is not None:
                data['satellites'] = self.device.satellites
            if self.device.altitude_m is not None:
                data['altitude_m'] = self.device.altitude_m
            if self.device.speed_knots is not None:
                data['speed_knots'] = self.device.speed_knots
            if self.device.track_angle_deg is not None:
                data['track_angle_deg'] = self.device.track_angle_deg
            if self.device.horizontal_dilution is not None:
                data['horizontal_dilution'] = self.device.horizontal_dilution
            if self.device.height_geoid is not None:
                data['height_geoid'] = self.device.height_geoid
        return data

# -----------------------------------------------------------------------------------
if __name__ == '__main__':

    import configparser
    config = configparser.ConfigParser()
    config['GPS'] = {'max_attempt':  10, 'dt':  0.1}


    gps = GPS(config)
    data = gps.read()
    for k,v in data.items():
        print(f'{k}: {v}')



