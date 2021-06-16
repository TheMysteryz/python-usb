import sys, os
import subprocess

# test mode
TEST_MODE = False

# set DISPLAY
os.environ["DISPLAY"] = ":0.0"
git --git-dir=/home/pi/python-usb/.git/ --work-tree=/home/pi/python-usb/ fetch
subprocess.Popen(["/usr/bin/git", "--git-dir=/home/pi/python-usb/.git/", "--work-tree=/home/pi/python-usb/", "fetch"])
subprocess.Popen(["/usr/bin/git", "--git-dir=/home/pi/python-usb/.git/", "--work-tree=/home/pi/python-usb/", "pull"])

if not TEST_MODE:
    # run script
    theproc = subprocess.Popen([sys.executable, "serial-ui.py"])
    theproc.communicate()
else:
    print("/!\\ In Test Mode")
