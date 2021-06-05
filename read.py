import urllib.request, json
import pyperclip
from evdev import InputDevice, categorize, ecodes
#dev = InputDevice('/dev/input/event8') # scanner
dev = InputDevice('/dev/input/event0') # keyboard

print(dev) # print the current device
inpt = ""
DATA_URL = "http://192.168.1.12:3000/getdata"
scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

# get datas from serv json
with urllib.request.urlopen(DATA_URL) as url:
    datas = json.loads(url.read().decode())

# func start compare data
def cmp_data(q):
    search = ""

    for data in datas:
        code = format(data[0])
        label = format(data[1]).upper()
        price = format(data[2])

        if q in code or q in label:
            search = code + " " + label + " " +  price
            break

    if search:
        print("found: {}".format(search))
    else:
        print("not found")
# end func


for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        data = categorize(event)  # Save the event temporarily to introspect it
        if data.keystate == 1:  # Down events only
            key_lookup = scancodes.get(data.scancode) or ('UNKNOWN: {}'.format(data.scancode))  # Lookup or return UNKNOWN:XX
            code = data.scancode
            print('You Pressed the {} key! '.format(key_lookup))  # Print it all out!
            print(code)
			# 2 - 11, 16 - 25, 30 - 38, 44 - 50
            if key_lookup == "CRLF":
                # cmp_data(inpt)
                print(inpt)
                pyperclip.copy(inpt)
                inpt = ""
            elif key_lookup == "BKSP":
                inpt = ""
            elif code >= 2 and code <= 11 or code >= 16 and code <= 25 or code >= 30 and code <= 38 or code >= 44 and code <= 50 or code == 57:
                inpt += key_lookup
