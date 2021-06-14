import serial
import io

ser = serial.Serial()
ser.port = '/dev/ttyACM0'
ser.timeout = 1
ser.open()
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

while True:
    sio.flush()
    line = sio.readline()
    if line != "":
        print(line.strip())
