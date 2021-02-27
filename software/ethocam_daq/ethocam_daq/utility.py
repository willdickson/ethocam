import os
import socket
import datetime
import netifaces
from . import config

def check_base_data_dir(create=True):
    """
    Checks to see whether or not the base data director exists. If it
    doesn't exist it creates it when the create flag is true.
    """
    if not os.path.exists(config.BASE_DATA_DIR) and create:
        os.makedirs(config.BASE_DATA_DIR)

def get_iso_datetime_str(): 
    """
    Returns iso datetime string for current time
    """ 
    return datetime.datetime.utcnow().isoformat(sep=' ',timespec='seconds')


def get_ip_and_hostname():
    """
    Returns the IP address and hostname
    """
    iface_list = netifaces.interfaces()
    if config.REQUIRED_IFACE not in iface_list:
        ip_address = 'no iface'
    else:
        ip_address = netifaces.ifaddresses(config.REQUIRED_IFACE)[netifaces.AF_INET][0]['addr']
    hostname = socket.gethostname()
    return {'ip': ip_address, 'hostname': hostname}

def get_current_data_dir(datetime_str):
    datetime_str_mod = datetime_str.replace(' ', '_')
    current_data_dir = os.path.join(config.BASE_DATA_DIR, datetime_str_mod)
    return current_data_dir


