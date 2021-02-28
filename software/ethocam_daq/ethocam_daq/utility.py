import os
import socket
import datetime
import netifaces

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
    return datetime.datetime.utcnow().isoformat(sep=' ',timespec='seconds')


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

def get_current_data_dir(config,datetime_str):
    """
    Returns the path for current data directory
    """
    base_data_dir = config['Logging']['data_directory']
    datetime_str_mod = datetime_str.replace(' ', '_')
    current_data_dir = os.path.join(base_data_dir, datetime_str_mod)
    return current_data_dir


def make_tarfile(output_filename, source_dir): 
    """
    Creates a gzipped tar archive containing a single top-level folder with the
    same name and contents as source_dir.o
    """
    with tarfile.open(output_filename, "w:gz") as tar: 
        tar.add(source_dir, arcname=os.path.basename(source_dir))


