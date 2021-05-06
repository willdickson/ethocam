import os
import json
import shutil
import socket
import datetime
import netifaces

def debug_print(msg,config):
    debug_enabled = config['Debug'].getboolean('enabled')
    if debug_enabled:
        print(msg)

def check_base_data_dir(config, create=True):
    """
    Checks to see whether or not the base data director exists. If it
    doesn't exist it creates it when the create flag is true.
    """
    base_data_dir = config['Logging']['data_directory']
    if not os.path.exists(base_data_dir) and create:
        os.makedirs(base_data_dir)

def get_iso_datetime_str(): 
    """
    Returns iso datetime string for current time
    """ 
    return datetime.datetime.now().isoformat(sep=' ',timespec='seconds')

def get_ip_and_hostname(config):
    """
    Returns the IP address and hostname
    """
    iface_list = netifaces.interfaces()
    iface = config['Network']['interface']
    if iface not in iface_list:
        ip_address = 'no iface'
    else:
        ip_address = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
    hostname = socket.gethostname()
    return {'ip': ip_address, 'hostname': hostname}

def get_current_data_dir(config, datetime_str):
    """
    Returns the path for current data directory
    """
    base_data_dir = config['Logging']['data_directory']
    datetime_str_mod = datetime_str.replace(' ', '_')
    current_data_dir = os.path.join(base_data_dir, datetime_str_mod)
    return current_data_dir

def save_sensor_data(config, data_dir, sensor_data):
    """
    Save sensor data file, in json, to the data directory.
    """
    filename = os.path.join(data_dir,config['Sensor']['filename'])
    with open(filename,'w') as f:
        json.dump(sensor_data,f)
    chown(filename, 'pi') 

def make_tarfile(output_filename, source_dir): 
    """
    Creates a gzipped tar archive containing a single top-level folder with the
    same name and contents as source_dir.o
    """
    with tarfile.open(output_filename, "w:gz") as tar: 
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def chown(path, user, group=None, recursive=False):
    """
    Recersive version of chown command
    """
    if group is None:
        group = user
    try:
        if not recursive or os.path.isfile(path):
            shutil.chown(path, user, group)
        else:
            for root, dirs, files in os.walk(path):
                shutil.chown(root, user, group)
                for item in dirs:
                    shutil.chown(os.path.join(root, item), user, group)
                for item in files:
                    shutil.chown(os.path.join(root, item), user, group)
    except OSError as e:
        raise e 

