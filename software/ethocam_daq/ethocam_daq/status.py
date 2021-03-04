import os
import json
import datetime
from . import utility

class StatusLogger:

    def __init__(self,config):
        self.filename = config['Logging']['status_file']

    def load(self): 
        try:
            with open(self.filename,'r') as f: 
                status_dict = json.load(f)
        except FileNotFoundError:
                status_dict = {'count': 0, 'datetime': None}
        return status_dict

    def reset(self):
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass

    def update(self):
        iso_datetime = utility.get_iso_datetime_str()
        status_dict = self.load()
        status_dict['count'] += 1
        status_dict['datetime'] = iso_datetime
        status_dir, _ = os.path.split(self.filename)
        if not os.path.exists(status_dir):
            os.makedirs(status_dir)
        with open(self.filename,'w') as f:
            json.dump(status_dict, f)
            f.write('\n')
        utility.chown(status_dir, 'pi') 
        return status_dict





