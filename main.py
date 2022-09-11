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

def updateInput(actualFocus, event, values, guess):
    focus = False
    # if the event is an input, it will also be a tuple
    if isinstance(event, tuple):
        if not values[event].isalpha():
            actualFocus.update(value="")
        else:
            focus = True
            actualFocus.update(value=values[event].upper())
            guess = guess + values[event].upper()
    
    # if the event is a button, it will be the letter it displays
    if isinstance(event, str) and event in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        focus = True
        actualFocus.update(value=event)
        guess = guess + event

    return (guess, focus)

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
    window.bind("<Return>", "-ENTER-")

    window["-PRINT-"].update(visible=False) # this is done to get the proportions right
    actualFocus = window[(0,0)] # actualFocus follows the input element that the user writes in
    actualFocus.update(disabled=False)
    [window[(row, col)].set_cursor(cursor_color=darkGray) for col in range(5) for row in range(6)]

# -----------------------------------------------------------

    # Variables for game logic
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
        print(event)

        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED:
            break

        # on a new event, delete the warning
        window["-PRINT-"].update(visible=False)

        # if event is a backspace, go to the previous focus and delete the character
        if event == "-BACKSPACE-" and len(guess) > 0 and len(guess) <= 4:
            actualFocus.update(disabled=True) # disable this input box then
            actualFocus = actualFocus.get_previous_focus() # Go to last focus
            actualFocus.update(disabled=False)
            actualFocus.set_focus()
            actualFocus.update(value="")
            guess = guess[:-1]
            continue

        # if it's still possible to add letters to row
        if len(guess) < 4:
            if event == "-ENTER-":
                window["-PRINT-"].update("Not enough letters", visible=True)

            guess, focus = updateInput(actualFocus, event, values, guess)
            if focus:
                actualFocus = getNextFocus(actualFocus)
            continue

        # if it's possible to add a single letter to the row, we don't change the focus
        if len(guess) == 4:
            if event == "-ENTER-":
                window["-PRINT-"].update("Not enough letters", visible=True)

            guess, focus = updateInput(actualFocus, event, values, guess)
            actualFocus.update(disabled=True)
            continue

        # if it's not possible to add letters to row
        if len(guess) == 5:
            # if event is a backspace, delete the character
            if event == "-BACKSPACE-" and len(guess) > 0:
                actualFocus.update(disabled=False)
                actualFocus.update(value="")
                guess = guess[:-1]

            # if event is an enter, check the word
            if event == "-ENTER-":
                if guess not in wordList:
                    window["-PRINT-"].update("Word not in list", visible=True)
                # else:
                    # checkColor(guess)
            continue
                
    # Finish up by removing from the screen
    window.close()

if __name__ == "__main__":
    main()