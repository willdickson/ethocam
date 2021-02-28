import os
import argparse
from pprint import pprint
from . import config
from . import utility
from .display import Display
from .status_logger import StatusLogger
from .light_sensor import LightSensor
from .temp_humid_sensor import TempHumidSensor
from .wittypi import WittyPi
from .wittypi import CurrentMonitor

def cmd_reset_status():
    description_str = 'Reset ethocam acquistion status'
    parser = argparse.ArgumentParser(description=description_str)
    parser.parse_args()
    utility.check_base_data_dir()
    status_logger = StatusLogger(config.STATUS_FILE)
    status_logger.reset()

def cmd_acquire_data():
    description_str = 'acquire data from camera + other sensors and save/send data'
    parser = argparse.ArgumentParser(description=description_str)
    parser.parse_args()

    utility.check_base_data_dir()

    data = {}

    # Update Display to show acquiring message
    display = Display()
    if 0:
        msg = [
            f"{status['datetime']}",
            f"{host_data['hostname']} {host_data['ip_address']}",
            f"mode = acquiring", 
            f"count = {status['count']}",
            ]
        display.show(msg)

    # Update status file
    status_logger = StatusLogger(config.STATUS_FILE)
    status = status_logger.update()
    data['status'] = status

    # Get network information infomation
    host_data = utility.get_ip_and_hostname()

    # Get current data directory name and create directory
    current_data_dir = utility.get_current_data_dir(status['datetime'])
    if 0:
        os.makedirs(current_data_dir)

    # Get temperature and humidity
    th_sensor = TempHumidSensor()
    data['temperature'] = th_sensor.temperature
    data['humidity'] = th_sensor.temperature

    # Get light sensor reading
    light_sensor = LightSensor()
    data['light'] = light_sensor.data 

    # Get battery data
    wittypi = WittyPi()
    data['power'] = {}
    data['power']['input_voltage'] = wittypi.input_voltage
    data['power']['output_voltage'] = wittypi.output_voltage

    pprint(data)



    # Update Display to show sleeping message
    if 0:
        msg = [
            f"{status['datetime']}",
            f"{host_data['hostname']} {host_data['ip_address']}",
            f"mode = sleeping", 
            f"count = {status['count']}",
            ]
        display.show(msg)


    




