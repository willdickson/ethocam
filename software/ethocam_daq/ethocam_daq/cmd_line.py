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
from .file_transfer import TransferAgent
from .gps import GPS
from pprint import pprint

def cmd_reset_status():
    description_str = 'Reset ethocam acquistion status'
    parser = argparse.ArgumentParser(description=description_str)
    parser.parse_args()
    config = Config()
    utility.check_base_data_dir(config)
    status_logger = StatusLogger(config)
    status_logger.reset()

def cmd_acquire_data():
    description_str = 'acquire data from camera + other sensors and save/send data'
    parser = argparse.ArgumentParser(description=description_str)
    parser.parse_args()

    sensor_data = {}

    # Load configuration and check data directory (create if required)
    config = Config()
    sensor_data['config'] = config.dict()
    utility.check_base_data_dir(config)

    # Update status file
    utility.debug_print('updating status file',config)
    status_logger = StatusLogger(config)
    status = status_logger.update()
    sensor_data['status'] = status

    # Get network information infomation
    utility.debug_print('getting network information',config)
    host_data = utility.get_ip_and_hostname(config)

    # Update Display to show acquiring message
    utility.debug_print('display acquiring message',config)
    display = Display(config)
    msg = [
        f"{status['datetime']}",
        f"{host_data['hostname']} {host_data['ip']}",
        f"mode = acquiring", 
        f"count = {status['count']}",
        ]
    display.show(msg)

    # Get current data directory name and create directory
    utility.debug_print('get/create current data dir',config)
    data_dir = utility.get_current_data_dir(config,status['datetime'])
    os.makedirs(data_dir)

    # Change owner of data file from root from pi user 
    utility.chown(data_dir, 'pi', recursive=True) 

    # Get temperature and humidity
    utility.debug_print('get temperature and humidity',config)
    th_sensor = TempHumidSensor()
    sensor_data['temperature'] = th_sensor.temperature
    sensor_data['humidity'] = th_sensor.humidity

    # Get light sensor reading
    utility.debug_print('get light sensor reading',config)
    light_sensor = LightSensor(config)
    sensor_data['light'] = light_sensor.data 

    # Get battery and regulator voltages 
    utility.debug_print('get voltages',config)
    volt_monitor = VoltageMonitor(config)
    sensor_data['power'] = {}
    sensor_data['power']['input_voltage'] = volt_monitor.input_voltage
    sensor_data['power']['output_voltage'] = volt_monitor.output_voltage

    # Start current monitor
    utility.debug_print('start current monitor',config)
    curr_monitor = CurrentMonitor(config)
    curr_monitor.start()

    # Record Video
    utility.debug_print('start video recording',config)
    vid_rec = VideoRecorder(config, data_dir)
    vid_rec.run()
    utility.debug_print('video recording done',config)

    # Send video data to remote host vis scp
    utility.debug_print('begin video file transfer',config)
    transfer_agent = TransferAgent(config, data_dir)
    transfer_agent.send_data_directory()
    utility.debug_print('video file transfer done',config)

    # Get GPS reading
    utility.debug_print('get gps reading',config)
    gps = GPS(config)
    gps_data = gps.read()
    sensor_data['gps'] = gps_data

    # Stop current monitor, get data and save sensor data to file
    utility.debug_print('stop current monitor',config)
    curr_monitor.stop()
    utility.debug_print('get current',config)
    sensor_data['power']['output_current'] = curr_monitor.data
    utility.save_sensor_data(config, data_dir, sensor_data)

    # Send sensor data to remote host vis scp
    utility.debug_print('send sensor data',config)
    transfer_agent.send_sensor_file()
    transfer_agent.close()

    # Change owner of data file from root from pi user 
    utility.chown(data_dir, 'pi', recursive=True) 

    # Update Display to show sleeping message
    utility.debug_print('dislplay sleeping message',config)
    msg = [
        f"{status['datetime']}",
        f"{host_data['hostname']} {host_data['ip']}",
        f"mode = sleeping", 
        f"count = {status['count']}",
        ]
    display.show(msg)
    time.sleep(config['Display'].getfloat('shutdown_dt'))
    
    utility.debug_print('done',config)

