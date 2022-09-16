import enum
from optparse import Values
import pyglet
from pyglet.libs.win32 import constants

# import json # need to learn to use this for saving and loading to files
from random import choice
import PySimpleGUI as sg

# Styling for the window
constants.COINIT_MULTITHREADED = 0x2  # 0x2 = COINIT_APARTMENTTHREADED

pyglet.font.add_file(r"./clear-sans-main/TTF/ClearSans-Regular.ttf")

sg.theme("Default1")
gray = "#818384"
darkGray = "#1f1f1f"
notInWord = "#3a3a3c"
green = "#538d4e"
yellow = "#b59f3b"

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

def getColors(guess, gameWord, letterCounts, wordSet):
    colors = ["", "", "", "", ""]
    countCopy = letterCounts.copy()
    copyGuess = guess
    for i, c in enumerate(guess): # Color the green
        if c == gameWord[i]:
            colors[i] = "G"
            countCopy[c] -= 1
            copyGuess = copyGuess[:i]+copyGuess[i+1:]
    a = 0
    for i, char in enumerate(guess): # then color the yellows
        if char not in wordSet:
            colors[i] = "N"
        elif colors[i]=="":
            if countCopy[char]==0:
                continue
            colors[i] = "Y"
            countCopy[char] -= 1
        

    return colors

# creates the window in which the game will be played
def createGameWindow():
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
        [sg.Text(background_color=darkGray)],
        [warnings],
        [sg.Text(background_color=darkGray)],
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
        background_color=darkGray, 
        element_justification="center", 
        finalize=True,)

    return window

# all the code of the layout and the game logic is in here
def startGame():
    window = createGameWindow()

    # Setting up the backspace and enter keys 
    window.bind("<BackSpace>", "-BACKSPACE-")
    window.bind("<Return>", "-ENTER-")

    window["-PRINT-"].update(visible=False) # this is done to get the proportions right
    actualFocus = window[(0,0)] # actualFocus follows the input element that the user writes in
    actualFocus.update(disabled=False)
    [window[(row, col)].set_cursor(cursor_color=darkGray) for col in range(5) for row in range(6)] # This is done so the keyboard cursor appears to be invisible

# -----------------------------------------------------------

    # Variables for game logic
    won = False
    actualRow = 0
    wordList = []
    with open("words.txt", mode='rt') as f:
        wordList = f.readlines()
        for x in range(len(wordList)):
            wordList[x] = wordList[x].strip("\n").upper()
    gameWord = choice(wordList)
    print(gameWord)
    letterCounts = {}
    for char in gameWord:
        letterCounts[char] = gameWord.count(char)
    gameSet = set(gameWord)
    guess = ""

# -----------------------------------------------------------

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read() # getting the events

        # See if window was closed
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
            guess, focus = updateInput(actualFocus, event, values, guess)
            actualFocus.update(disabled=True)

            if event == "-ENTER-":
                window["-PRINT-"].update("Not enough letters", visible=True)
                actualFocus.update(disabled=False)
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
                else:
                    colors = getColors(guess, gameWord, letterCounts, gameSet)
                    for col, color in enumerate(colors):
                        if color=="G":
                            window[actualRow, col].update(disabled=False, # TODO, not working right now
                        background_color=green)
                        elif color=="Y":
                            window[actualRow, col].update(disabled=False,
                        background_color=yellow)
                        elif color=="N":
                            window[actualRow, col].update(disabled=False, background_color=notInWord)
                    if guess == gameWord:
                        won = True
                        break
                    if actualRow < 6:
                        actualRow += 1
                        guess = ""
                        actualFocus = window[actualRow, 0]
                        actualFocus.update(disabled=False)
                        actualFocus.set_focus()
                    elif actualRow == 6:
                        break
            continue
    if event != sg.WINDOW_CLOSED:
        if won:
            window["-PRINT-"].update("You won!", visible=True)
            sg.popup("Press ENTER to leave", auto_close=True, auto_close_duration=2)
            while(True):
                event, values = window.read() # getting the events
                if event == "-ENTER-" or event == sg.WINDOW_CLOSED:
                    break
        else:
            window["-PRINT-"].update("You lost :c", visible=True)

    return (window, event)

# control the state of the program before and after the game
def main():
    # try to load an unfinished game
    # try:
    #     with open("game_data/game_state.txt") as f:
    #         
    # except (FileNotFoundError, json.decoder.JSONDecodeError):

        # load stats
        # loadStats()
        
    window, event = startGame()
        
        # if event != sg.WINDOW_CLOSED:
        #     # save stats
        #     saveStats()

        #     # show stats
        #     statsWindow = showStats()

        #     # popup after game asking to play again
        #     playAgain = True
        #     while(playAgain):
        #         playAgainWindow, response = playAgain()
        #         if response=="-YES-":
        #             window.close()
        #             statsWindow.close()
        #             playAgainWindow.close()
        #             window, event = startGame(wordList)
        #             statsWindow = showStats()
        #         else:
        #             playAgain = False
        # else: # if the window was closed, save the game state until the program is executed again
        #     saveGameState()

    # Finish up by removing from the screen
    window.close()
    # statsWindow.close()
    # playAgainWindow.close()
        

if __name__ == "__main__":
    main()