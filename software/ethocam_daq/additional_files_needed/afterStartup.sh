#!/bin/bash
# file: afterStartup.sh
#
# This script will be executed in background after Witty Pi 3 gets initialized.
# If you want to run your commands after boot, you can place them here.
#

set +e
source /home/pi/ethocam/bin/activate
if [ ! -f /home/pi/nohalt ]; then 
    ethocam-acquire
else
    ethocam-acquire
    ethocam-info
fi

if [ ! -f /home/pi/nohalt ]; then 
    sudo halt
fi
