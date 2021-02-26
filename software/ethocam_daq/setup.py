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
    packages=find_packages(exclude=['examples',]),
    entry_points={
        'console_scripts': [
            'ethocam_daq=ethocam_daq:test',
            ]
        }
    )
