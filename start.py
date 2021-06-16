import sys, os
import subprocess

# set DISPLAY
if os.environ["DISPLAY"] != ":0.0":
    os.environ["DISPLAY"] = ":0.0"

# run script
theproc = subprocess.Popen([sys.executable, "serial-ui.py"])
theproc.communicate()
