import PySimpleGUI as sg

layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Text("hahaha")], [sg.Button("OK")]]

print("Screen: {}".format(sg.Window.get_screen_size()))
w, h = sg.Window.get_screen_size()

# Create the window
window = sg.Window(
            "Demo",
            layout,
            background_color = "#f00",
            element_justification = "center",
            no_titlebar=True,
            location=(0,0),
            size=(w, h),
            keep_on_top=True
        ).Finalize()
window.Maximize()

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()
