from tkinter import Grid
import PySimpleGUI as sg

for i in range(6):
    # Define the window's contents
    layout = [
            [sg.Input(size=(1, 1), key='-input1-'), sg.Input(size=(1, 1), key='-input2-'), sg.Input(size=(1, 1), key='-input3-'), sg.Input(size=(1, 1), key='-input4-'), sg.Input(size=(1, 1), key=f'-input5-')],
            [sg.Text(size=(40,1), key='-OUTPUT-')],
            [sg.Button('Ok'), sg.Button('Quit')]]

    # Create the window
    window = sg.Window('Wordle Game Thing', layout)

    # Display and interact with the Window using an Event Loop
    event, values = window.read()
    guess = values['-input1-']+values['-input2-']+values['-input3-']+values['-input4-']+values['-input5-']
    # while True:
        

    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    window['-OUTPUT-'].update('Hello ' + values['-input1-'] + "! Thanks for trying PySimpleGUI")

    # Finish up by removing from the screen
    window.close()