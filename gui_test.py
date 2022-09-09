import pyglet
from pyglet.libs.win32 import constants
import PySimpleGUI as sg

constants.COINIT_MULTITHREADED = 0x2  # 0x2 = COINIT_APARTMENTTHREADED

pyglet.font.add_file(r"./clear-sans-main/TTF/ClearSans-Regular.ttf")

sg.theme("Default1")
gray = "#818384"
darkGray = "#1f1f1f"

def getInputGUI(value, coordinates):
    inputBox = sg.Input(
        value,
        key=coordinates,
        size=(2,1),
        background_color=darkGray,
        pad=2,
        text_color="white",
        justification="centered",
        font=("Clear sans", 35),
        disabled=True,
        disabled_readonly_background_color=darkGray,
        enable_events=True,
    )
    return inputBox

def getButtonGUI(char):
    buttonBox = sg.Button(
        char,
        key=char,
        size=(2,1),
        font=("Clear sans", 20),
        pad=2,
        button_color=("white", gray),
        
    )

    return buttonBox

def main():
    # Define the window's contents
    layout = [
        [[getInputGUI("", (row, column)) for column in range(5)] for row in range(6)], # las casillas del input del juego
        [sg.Text(background_color="#1f1f1f")],
        [sg.Text(background_color="#1f1f1f")],
        [sg.Text(background_color="#1f1f1f")],
        [getButtonGUI(char) for char in "QWERTYUIOP"],
        [getButtonGUI(char) for char in "ASDFGHJKL"],
        [getButtonGUI(char) for char in "ZXCVBNM"],
    ]

    # Create the window
    window = sg.Window(
        'Wordle clone',
        layout, 
        margins=(10, 10), 
        background_color="#1f1f1f", 
        element_justification="center", 
        finalize=True,)

    [window[(0, 0)].update(disabled=False)]
    [window[(row, col)].set_cursor(cursor_color=darkGray) for col in range(5) for row in range(6)]

    while True:
        # Display and interact with the Window using an Event Loop
        event, values = window.read()

            
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED:
            break

        # Output a message to the window
        # window["key"].update("What you want in there")

    # Finish up by removing from the screen
    window.close()

if __name__ == "__main__":
    main()