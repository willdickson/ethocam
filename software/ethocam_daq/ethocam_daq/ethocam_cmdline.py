import os
import argparse
from . import config
from . import utility
from .display import Display
from .status_logger import StatusLogger

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

    # Update status file
    status_logger = StatusLogger(config.STATUS_FILE)
    status_dict = status_logger.update()

    # Get host infomation
    ip_address, hostname = utility.get_ip_and_hostname()
    print(f'{hostname} {ip_address}')



    # Update Display to show acquiring message
    #display = Display()
    if 0:
        msg = [
            f"{status_dict['last_update']}",
            f"{hostname} {ip_address}",
            f"mode = acquiring", 
            f"count = {status_dict['count']}",
            ]
        display.show(msg)

    # Update Display to show sleeping message
    if 0:
        msg = [
            f"{status_dict['last_update']}",
            f"{hostname} {ip_address}",
            f"mode = sleeping", 
            f"count = {status_dict['count']}",
            ]
        display.show(msg)


    




