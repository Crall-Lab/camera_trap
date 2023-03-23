install raspberry pi os (latest bullseye is required)

# Set up
```bash
sudo apt update && sudo apt upgrade
```

# install virtualenvwrapper
```bash
sudo apt install virtualenvwrapper
echo "source /usr/share/virtualenvwrapper/virtualenvwrapper.sh" >> ~/.bashrc
. ~/.bashrc
mkvirtualenv --python=`which python3` --system-site-packages bugcam
echo "source /home/pi/.virtualenvs/bugcam/bin/activate" >> ~/.bashrc
. ~/.bashrc
pip install --upgrade pip

sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_camera 0

sudo apt install -y i2c-tools libgpiod-dev
pip install --upgrade RPi.GPIO
pip install --upgrade adafruit-blinka

pip install adafruit-circuitpython-aw9523
```

# install picamera2
```bash
sudo apt install -y python3-libcamera python3-kms++
sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip
pip3 install numpy --upgrade
pip3 install picamera2
```

run focus.py to focus camera

run capture.py to start image acquisition

To run code automatically on reboot, add the following to the users crontab

```bash
@reboot bash $HOME/r/Crall-Lab/camera_trap/run_capture.sh
```
Note the above line assumes the code is at ~/r/Crall-Lab/camera_trap
