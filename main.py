from enum import auto
import pyglet
from pyglet.libs.win32 import constants
import PySimpleGUI as sg

constants.COINIT_MULTITHREADED = 0x2  # 0x2 = COINIT_APARTMENTTHREADED

pyglet.font.add_file(r"./clear-sans-main/TTF/ClearSans-Regular.ttf")

sg.theme("Default1")
gray = "#818384"
darkGray = "#1f1f1f"

# -----------------------------------------------------------

# returns an sg.Input for the guesses' boxes
def getInputGUI(coordinates):
    inputBox = sg.Input(
        default_text="",
        key=coordinates, # (row, column)
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

# -----------------------------------------------------------

# returns an sg.Button for the on-screen keyboard
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

# -----------------------------------------------------------

# Gets the next focus of an input and disables the previous input box
def getNextFocus(actualFocus):
    actualFocus.update(disabled=True)
    actualFocus = actualFocus.get_next_focus() # Now focusing the next input
    actualFocus.update(disabled=False)
    actualFocus.set_focus()
    return actualFocus

# -----------------------------------------------------------

# all the code of the layout and the game logic is in here
def main():
    # Setting up the layout:

    # text to be printed on screen as warnings
    warnings = sg.Text(
        background_color="white",
        key="-PRINT-",
        justification="center",
        size=(20, 1),
        font=("Helvetica neue", 20, "bold"),
        pad=(20, 10),
        visible=True,
        )

    # setting up the keyboard on screen
    enterButton = sg.Button("Enter", key="-ENTER-", size=(4,1), font=("Clear sans", 20), pad=2, button_color=("white", gray), bind_return_key=True)
    deleteButton = sg.Button("Erase", key="-BACKSPACE-", size=(4,1), font=("Clear sans", 20), pad=2, button_color=("white", gray), enable_events=True)
    lowRow = [getButtonGUI(char) for char in "ZXCVBNM"]
    lowerKeyboardRow = [enterButton] + lowRow + [deleteButton]

    # sort the window's contents in place
    layout = [
        [[getInputGUI((row, column)) for column in range(5)] for row in range(6)], # las casillas del input del juego
        [sg.Text(background_color="#1f1f1f")],
        [warnings],
        [sg.Text(background_color="#1f1f1f")],
        [getButtonGUI(char) for char in "QWERTYUIOP"],
        [getButtonGUI(char) for char in "ASDFGHJKL"],
        [lowerKeyboardRow],
    ]

# -----------------------------------------------------------

    # Create the window
    window = sg.Window(
        'Wordle clone',
        layout, 
        margins=(10, 10), 
        background_color="#1f1f1f", 
        element_justification="center", 
        finalize=True,)
    window.bind("<BackSpace>", "-BACKSPACE-")

    window["-PRINT-"].update(visible=False) # this is done to get the proportions right
    actualFocus = window[(0,0)]
    actualFocus.update(disabled=False)
    [window[(row, col)].set_cursor(cursor_color=darkGray) for col in range(5) for row in range(6)]

# -----------------------------------------------------------

    # Variables for game logic
    letterCount = 0
    win = False
    wordList = []
    with open("words.txt", mode='rt') as f:
        wordList = f.readlines()
        for x in range(len(wordList)):
            wordList[x] = wordList[x].strip("\n").upper()
    guess = ""

# -----------------------------------------------------------

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read() # getting the events
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED:
            break

        # on a new event, delete the warning
        window["-PRINT-"].update(visible=False)

        # if the event is an input, it will also be a tuple
        if isinstance(event, tuple) and letterCount < 5:
            if not values[event].isalpha():
                actualFocus.update(value="")
            else:
                letterCount+=1
                actualFocus.update(value=values[event].upper())
                actualFocus = getNextFocus(actualFocus)
                guess = guess + values[event].upper()
                

        # if event is a backspace, go to the previous focus and delete the character
        elif event == "-BACKSPACE-" and letterCount > 0:
            letterCount-=1
            actualFocus.update(disabled=True)
            actualFocus = actualFocus.get_previous_focus() # Go to last focus
            actualFocus.update(disabled=False)
            actualFocus.update(value="")
            actualFocus.set_focus()
            guess = guess[:-1]

        # if event is an enter, check the word
        elif event == "-ENTER-":
            if letterCount!=5:
                window["-PRINT-"].update("Not enough letters", visible=True)
            elif guess not in wordList:
                window["-PRINT-"].update("Word not in list", visible=True)

        # if the event is a button, it will be the letter it displays
        elif event in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            letterCount+=1
            actualFocus.update(value=event)
            actualFocus = getNextFocus(actualFocus)
            guess = guess + event


    # Finish up by removing from the screen
    window.close()

if __name__ == "__main__":
    main()