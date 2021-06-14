import PySimpleGUI as sg

layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Text("hahaha")], [sg.Button("OK")]]

# Create the window
window = sg.Window(
            "Demo",
            layout,
            background_color = "#f00",
            element_justification = "center",
            size = (200, 100)
        )

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()
