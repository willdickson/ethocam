from setuptools import setup
from setuptools import find_packages
import os

setup(
    name='ethocam_daq', 
    version='0.0.1',
    description='Data acquisition software for the ethocam system',
    author='Will Dickson', 
    author_email='wbd@caltech', 
    license='MIT', 
    classifiers=[ 
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Science/Research', 
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3.7', 
        ], 
    packages=find_packages(exclude=['examples', 'config']),
    entry_points={
        'console_scripts': [
            'ethocam-acquire=ethocam_daq.cmd_line:cmd_acquire_data',
            'ethocam-reset=ethocam_daq.cmd_line:cmd_reset_status',
            ]
        }
    )
