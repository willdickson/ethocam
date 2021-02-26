import os
import json
import datetime
from . import utility

class StatusLogger:

    def __init__(self,filename):
        self.filename  = filename

    def load(self): 
        try:
            with open(self.filename,'r') as f: 
                status_dict = json.load(f)
        except FileNotFoundError:
                status_dict = {'count': 0, 'last_update': None}
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
        status_dict['last_update'] = iso_datetime
        with open(self.filename,'w') as f:
            json.dump(status_dict, f)
        return status_dict





