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
    status_logger = StatusLogger(config)
    status = status_logger.update()
    sensor_data['status'] = status

    # Get network information infomation
    host_data = utility.get_ip_and_hostname(config)

    # Update Display to show acquiring message
    display = Display(config)
    msg = [
        f"{status['datetime']}",
        f"{host_data['hostname']} {host_data['ip']}",
        f"mode = acquiring", 
        f"count = {status['count']}",
        ]
    display.show(msg)

    # Get current data directory name and create directory
    data_dir = utility.get_current_data_dir(config,status['datetime'])
    os.makedirs(data_dir)

    # Get temperature and humidity
    th_sensor = TempHumidSensor()
    sensor_data['temperature'] = th_sensor.temperature
    sensor_data['humidity'] = th_sensor.humidity

    # Get light sensor reading
    light_sensor = LightSensor()
    sensor_data['light'] = light_sensor.data 

    # Get battery and regulator voltages 
    volt_monitor = VoltageMonitor(config)
    sensor_data['power'] = {}
    sensor_data['power']['input_voltage'] = volt_monitor.input_voltage
    sensor_data['power']['output_voltage'] = volt_monitor.output_voltage

    # Start current monitor
    curr_monitor = CurrentMonitor(config)
    curr_monitor.start()

    # Record Video
    vid_rec = VideoRecorder(config, data_dir)
    vid_rec.run()

    # Send video data to remote host vis scp
    transfer_agent = TransferAgent(config, data_dir)
    transfer_agent.send_data_directory()

    # Get GPS reading
    gps = GPS(config)
    gps_data = gps.read()
    sensor_data['gps'] = gps_data

    # Stop current monitor, get data and save sensor data to file
    curr_monitor.stop()
    sensor_data['power']['output_current'] = curr_monitor.data
    utility.save_sensor_data(config, data_dir, sensor_data)

    # Send sensor data to remote host vis scp
    transfer_agent.send_sensor_file()
    transfer_agent.close()

    # Change owner of data file from root from pi user 
    utility.chown(data_dir, 'pi', recursive=True) 

    # Update Display to show sleeping message
    msg = [
        f"{status['datetime']}",
        f"{host_data['hostname']} {host_data['ip']}",
        f"mode = sleeping", 
        f"count = {status['count']}",
        ]
    display.show(msg)
    time.sleep(config['Display'].getfloat('shutdown_dt'))

