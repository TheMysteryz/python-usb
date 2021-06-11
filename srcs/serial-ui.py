import PySimpleGUI as sg
import urllib.request, json
import time

DATA_URL = "http://192.168.1.19:3000/getdata"

# get datas from serv json
with urllib.request.urlopen(DATA_URL) as url:
    datas = json.loads(url.read().decode())

# func start compare data
def cmp_data(q):
    search = ""
    if q == "":
        return [None, None, None, None];

    for data in datas:
        code = format(data[0])
        label = format(data[1]).upper()
        price = format(data[2]) + " €"

        if q in code or q in label:
            
            search = code + " " + label + " " +  price
            return [search, code, label, price]
            break

    return search
# end func

# get screen width and height
print("Screen: {}".format(sg.Window.get_screen_size()))
w, h = sg.Window.get_screen_size()

# defines
BG_COLOR = "#00A2E8"
SCAN_HERE = ["SCANNEZ VOS ARTICLES", "ICI", ""]
aa = ""
is_wait = False

layout = [
    [sg.Text(SCAN_HERE[0], size=(50, 1), justification="center", background_color=BG_COLOR, key='-CODE-')],
    [sg.Text(SCAN_HERE[1], size=(50, 1), justification="center", background_color=BG_COLOR, key='-LABEL-')],
    [sg.Text(SCAN_HERE[2], size=(50, 1), justification="center", background_color=BG_COLOR, text_color="#ff0", key='-PRICE-')],
    [sg.Button("OK", button_color="#f00")],
    [sg.Button("EXIT", button_color="#f00")]
]

# Create the window
window = sg.Window(
    "Demo",
    layout,
    background_color = BG_COLOR,
    element_justification = "center",
    return_keyboard_events = True,
    no_titlebar = True,
    location= (0, 0),
    size = (w, h),
    keep_on_top = True
).Finalize()

window.Maximize()

# Create an event loop
while True:
    event, values = window.read(timeout=1000) # timeout 1 sec
    # print event
    if event != "__TIMEOUT__":
        print(event)
    
    # inputs
    if event == "OK":
        aa = "99911"

    # search input in datas
    [text, code, label, price] = cmp_data(aa)

    # when data founds
    if text:
        # add 3 sec on end_time
        end_time = time.time() + 3
        is_wait = True # to enter reset timer
        print("found: {}".format(text))
        window['-CODE-'].update(code)
        window['-LABEL-'].update(label)
        window['-PRICE-'].update(price)

    # reset timer
    if is_wait and time.time() > end_time:
        window['-CODE-'].update(SCAN_HERE[0])
        window['-LABEL-'].update(SCAN_HERE[1])
        window['-PRICE-'].update(SCAN_HERE[2])
        is_wait = False
    # reset vals
    text = ""
    aa = ""
    # End program if user closes window or
    # presses the EXIT button or
    # ESC key pressed
    if event == "EXIT" or event == sg.WIN_CLOSED or event == "Escape:27":
        # confirm exit
        if sg.popup_ok_cancel("Exit the program?", keep_on_top=True) == "OK":
            break

window.close()
