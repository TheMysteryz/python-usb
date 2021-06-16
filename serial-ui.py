import PySimpleGUI as sg
import serial
import urllib.request, json
import time, re, io, sys

TEST_WITHOUT_SER = False

# store
DATA_URL = "http://192.168.1.12:3000"
DATA_PATH = "/getdata"

# define serial
if not TEST_WITHOUT_SER:
    ser = serial.Serial()
    ser.port = '/dev/ttyACM0'
    ser.timeout = 1
    ser.open()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

# get datas from serv json
with urllib.request.urlopen(DATA_URL + DATA_PATH) as url:
    datas = json.loads(url.read().decode())

# func start truncate
def truncate(num):
    return re.sub(r'^(\d+\.\d{,2})\d*$',r'\1',str(num))
# end func

# func start compare data
def cmp_data(q):
    if q == "":
        return [None, None, None, None]
    with urllib.request.urlopen(DATA_URL + "?" + q) as url:
        mydata = json.loads(url.read().decode())
        if mydata == "nofound":
            return ["nofound", "Article non trouvé!", "Merci de réessayer ou\nde le signaler,", "A bientôt"]
        else:
            code = format(mydata[0])
            label = format(mydata[1]).upper()
            fprice = format(mydata[2])
            price = truncate('{:<011}'.format(fprice)) + " €"
            search = code + " " + label + " " +  price
            return [search, code, label, price]
# end func

# get screen width and height
print("Screen: {}".format(sg.Window.get_screen_size()))
w, h = sg.Window.get_screen_size()

# defines
BG_COLOR = "#00A2E8"
SCAN_HERE = ["SCANNEZ VOS ARTICLES", "ICI", ""]
aa = ""
my_font = "Arial 72"
my_font_small = "Arial 54"
is_wait = False
if sys.platform.startswith('win32'):
    filename = r'E:\Github\python-usb\img\triangle.png'
elif sys.platform.startswith('linux'):
    filename = r'~/python-usb/img/triangle.png'
print(filename)

layout = [
    [sg.Text(SCAN_HERE[0], size=(22, 1), font=my_font, justification="center", background_color=BG_COLOR, key='-CODE-')],
    [sg.Text(SCAN_HERE[1], size=(22, 2), font=my_font, justification="center", background_color=BG_COLOR, key='-LABEL-')],
    [sg.Text(SCAN_HERE[2], size=(22, 1), font=my_font, justification="center", background_color=BG_COLOR, text_color="#ff0", key='-PRICE-')],
    [sg.Image(filename, key='-IMAGE-')]
]

# Create the window
window = sg.Window(
    "Demo",
    layout,
    background_color = BG_COLOR,
    element_justification = "center",
    return_keyboard_events = True,
    no_titlebar = True,
    location = (0, 0),
    size = (w+350, h*2),
    margins = (0, h/4),
    keep_on_top = True
).Finalize()

window.Maximize()
window.set_cursor("none")

# Create an event loop
while True:
    event, values = window.read(timeout=1000) # timeout 1 sec
    # print event
    if event != "__TIMEOUT__":
    	print(event)

    # inputs
    if not is_wait and not TEST_WITHOUT_SER:
        while True:
            sio.flush()
            line = sio.readline()
            if line != "":
                aa = line.strip()
                break

    if (event == "OK" or "space" in event or event == " ") and TEST_WITHOUT_SER:
        aa = "3660715013473"

    # search input in datas
    [text, code, label, price] = cmp_data(aa)

    # when data founds
    if text == "nofound":
        # add 3 sec on end_time
        end_time = time.time() + 3
        is_wait = True # to enter reset timer
        print("{}".format(text))
        window['-CODE-'].update(code, text_color="#ff0")
        window['-LABEL-'].update(label)
        window['-PRICE-'].update(price, font=my_font_small, text_color="#fff")
        window['-IMAGE-'].update(visible=False)
    elif text:
        # add 3 sec on end_time
        end_time = time.time() + 3
        is_wait = True # to enter reset timer
        print("found: {}".format(text))
        window['-CODE-'].update(code, font=my_font_small)
        window['-LABEL-'].update(label)
        window['-PRICE-'].update(price)
        window['-IMAGE-'].update(visible=False)

    # reset timer
    if is_wait and time.time() > end_time:
        window['-CODE-'].update(SCAN_HERE[0], font=my_font, text_color="#fff")
        window['-LABEL-'].update(SCAN_HERE[1], font=my_font, text_color="#fff")
        window['-PRICE-'].update(SCAN_HERE[2], font=my_font, text_color="#ff0")
        window['-IMAGE-'].update(visible=True)
        is_wait = False
    # reset vals
    text = ""
    aa = ""
    # End program if user closes window or
    # presses the EXIT button or
    # ESC key pressed
    if event == "EXIT" or event == sg.WIN_CLOSED or "Escape" in event:
        # confirm exit
        if sg.popup_ok_cancel("Exit the program?", keep_on_top=True) == "OK":
            break

# close all
if not TEST_WITHOUT_SER:
    ser.close()
window.close()
