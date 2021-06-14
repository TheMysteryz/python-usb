import PySimpleGUI as sg

layout = [
    [sg.InputText('Question: ', readonly=True, key='-IN-')],
    [sg.Text('Answer will be shown here', key='-OUT-')],
    [sg.Button('1'), sg.Button('2'), sg.Button('3')],
    [sg.Button('4'), sg.Button('5'), sg.Button('6')],
    [sg.Button('7'), sg.Button('8'), sg.Button('9')],
    [sg.Button('Enter'), sg.Button('Exit')]
]

window = sg.Window('calculator', layout)
input = window['-IN-']
while True:
    event, values = window.read()
    if event is None or event == 'Exit':
        break
    elif event in '1234567890':
        bleh = window['-IN-'].get()
        teh = f'{bleh}{event}'
        input.update(value=teh)
        input.Widget.xview("end")   # view end if text is too long to fit element

window.close()
