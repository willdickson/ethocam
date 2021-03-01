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
            for k,v in config[section].items():
                print(f'  {k} = {v}')


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    config = Config()
    config.print()



