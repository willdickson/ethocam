import os
import time
import argparse
from . import utility
from .config import Config
from .display import Display
from .status import StatusLogger
from .light import LightSensor
from .temp_humid import TempHumidSensor
from .wittypi import VoltageMonitor
from .wittypi import CurrentMonitor
from .video import VideoRecorder
from pprint import pprint

def cmd_reset_status():
    description_str = 'Reset ethocam acquistion status'
    parser = argparse.ArgumentParser(description=description_str)
    parser.parse_args()
    config = Config()
    utility.check_base_data_dir()
    status_logger = StatusLogger(config['Logging']['status_file'])
    status_logger.reset()

def cmd_acquire_data():
    description_str = 'acquire data from camera + other sensors and save/send data'
    parser = argparse.ArgumentParser(description=description_str)
    parser.parse_args()

    data = {}

    # Load configuration and check data directory (create if required)
    config = Config()
    utility.check_base_data_dir(config)


    # Update Display to show acquiring message
    display = Display(config)
    if 0:
        msg = [
            f"{status['datetime']}",
            f"{host_data['hostname']} {host_data['ip_address']}",
            f"mode = acquiring", 
            f"count = {status['count']}",
            ]
        display.show(msg)

    # Update status file
    status_logger = StatusLogger(config)
    status = status_logger.update()
    data['status'] = status

    # Get network information infomation
    host_data = utility.get_ip_and_hostname(config)

    # Get current data directory name and create directory
    current_data_dir = utility.get_current_data_dir(config,status['datetime'])
    os.makedirs(current_data_dir)

    # Get temperature and humidity
    th_sensor = TempHumidSensor()
    data['temperature'] = th_sensor.temperature
    data['humidity'] = th_sensor.temperature

    # Get light sensor reading
    light_sensor = LightSensor()
    data['light'] = light_sensor.data 

    # Get battery and regulator voltages 
    volt_monitor = VoltageMonitor(config)
    data['power'] = {}
    data['power']['input_voltage'] = volt_monitor.input_voltage
    data['power']['output_voltage'] = volt_monitor.output_voltage

    # Start current monitor
    curr_monitor = CurrentMonitor(config)
    curr_monitor.start()
    time.sleep(2.0)

    # Record Video
    vid_param = {
            'duration': 30.0,
            'filename': 'vid.h264',
            }
    vid_rec = VideoRecorder(vid_param, current_data_dir)
    vid_rec.run()

    # Stop current monitor and get data
    time.sleep(2.0)
    curr_monitor.stop()
    data['power']['output_current'] = curr_monitor.data
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


    




