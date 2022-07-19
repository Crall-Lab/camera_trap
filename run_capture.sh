#!/bin/bash

# source the virtualenv 'bugcam' from the users home directory
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
source $HOME/.virtualenvs/bugcam/bin/activate

# change directory to the local checkout of the repository
cd $HOME/r/Crall-Lab/camera_trap

# run the capture code
python3 capture.py >> run_capture.log

# reboot (if error as script should never end)
# sleep 60.0
# sudo reboot
