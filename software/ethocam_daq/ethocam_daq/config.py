import os
import configparser


class Config(configparser.ConfigParser):

    def __init__(self):
        super().__init__()
        config_filename = os.path.join(os.path.sep,'home', 'pi', '.config', 'ethocam')
        self.read(config_filename)

    def print(self):
        for section in self.sections():
            print(section)
            for k,v in self[section].items():
                print(f'  {k} = {v}')

    def dict(self):
        config_dict = {}
        for section in self.sections():
            config_dict[section] = dict(self[section])
        return config_dict



# -----------------------------------------------------------------------------
if __name__ == '__main__':
    config = Config()
    config.print()
    print(config.dict())



