#!bin/bash
git --git-dir=/home/pi/python-usb/.git/ --work-tree=/home/pi/python-usb/ fetch &&
git --git-dir=/home/pi/python-usb/.git/ --work-tree=/home/pi/python-usb/ pull &&
python3 serial-ui.py
