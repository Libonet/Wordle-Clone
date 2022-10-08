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
        pad=(2,4),
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

def getTextGUI(char, color, row, column):
    if color == "G":
        color = green
    elif color == "Y":
        color = yellow
    elif color == "N":
        color = notInWord

    textBox = sg.Text(
        text=char,
        key=f"T-({row},{column})",
        size=(2,1),
        border_width=3,
        background_color=color,
        pad=(3, 2),
        text_color="white",
        justification="centered",
        font=("Clear sans", 35),
        visible=False,
    )

    return textBox

# -----------------------------------------------------------

# Gets the next focus of an input and disables the previous input box
def getNextFocus(actualFocus):
    actualFocus.update(disabled=True)
    actualFocus = actualFocus.get_next_focus() # Now focusing the next input
    actualFocus.update(disabled=False)
    actualFocus.set_focus()
    return actualFocus

# -----------------------------------------------------------

# checks the source of the input to handle it and adds it to the "guess"
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

# -----------------------------------------------------------

# colors the guess on screen
def colorGuess(guess, gameWord, letterCounts, wordSet, window, actualRow):
    colors = ["", "", "", "", ""]
    countCopy = letterCounts.copy()
    copyGuess = guess
    colorLetter = {}
    for i, c in enumerate(guess): # Color the green
        if c == gameWord[i]:
            window[c].update(button_color=green)
            colorLetter[c]="G"
            colors[i] = "G"
            countCopy[c] -= 1
            copyGuess = copyGuess[:i]+copyGuess[i+1:]
    a = 0
    for i, char in enumerate(guess): # then color the yellows
        if char not in wordSet:
            colors[i] = "N"
            window[char].update(button_color=notInWord)
            colorLetter[char]="N"
        elif colors[i]=="":
            if countCopy[char]==0:
                colors[i] = "N"
                continue
            if colorLetter.get(char, "N")!="G":
                window[char].update(button_color=yellow)
            colors[i] = "Y"
            colorLetter[char]="Y"
            countCopy[char] -= 1

    for col, color in enumerate(colors): # paint the boxes
        if color=="G":
            window[f"T-({actualRow},{col})"].update(visible=True, background_color=green, value=guess[col])
            window[(actualRow, col)].hide_row()
        elif color=="Y":
            window[f"T-({actualRow},{col})"].update(visible=True, background_color=yellow, value=guess[col])
            window[(actualRow, col)].hide_row()
        elif color=="N":
            window[f"T-({actualRow},{col})"].update(visible=True, background_color=notInWord, value=guess[col])
            window[(actualRow, col)].hide_row()
    
    """ setGuess = set(guess)
    for char in "QWERTYUIOPASDFGHJKLZXCVBNM":
        if char in setGuess:
            
     """

    return window

# -----------------------------------------------------------

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
    
    layout = [
        [[getTextGUI("", "N", row, column) for column in range(5)] for row in range(6)], 
        [[getInputGUI((row, column)) for column in range(5)] for row in range(6)], # las casillas del input del juego
        [sg.Text(background_color=darkGray)],
        [warnings],
        [sg.Text(background_color=darkGray)],
        [getButtonGUI(char) for char in "QWERTYUIOP"],
        [getButtonGUI(char) for char in "ASDFGHJKL"],
        [lowerKeyboardRow],
    ]

    # Create the window
    window = sg.Window(
        'Wordle clone',
        layout, 
        margins=(10, 10), 
        background_color=darkGray, 
        element_justification="center", 
        finalize=True,
        # size=(500,800),
        )

    # Setting up the backspace and enter keys 
    window.bind("<BackSpace>", "-BACKSPACE-")
    window.bind("<Return>", "-ENTER-")

    window["-PRINT-"].update(visible=False) # this is done to get the proportions right
    [window[(row, col)].set_cursor(cursor_color=darkGray) for col in range(5) for row in range(6)] # This is done so the keyboard cursor appears to be invisible

    return window

# -----------------------------------------------------------

# all the code of the layout and the game logic is in here
def startGame(window, wordList):
    actualFocus = window[(0,0)] # actualFocus follows the input element that the user writes in
    actualFocus.update(disabled=False)

    # Variables for game logic
    won = None
    actualRow = 0
    wordList = []
    gameWord = choice(wordList)
    print(gameWord)
    letterCounts = {}
    for char in gameWord:
        letterCounts[char] = gameWord.count(char)
    gameSet = set(gameWord)
    guess = ""

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
            if event == "-BACKSPACE-":
                actualFocus.update(disabled=False)
                actualFocus.update(value="")
                guess = guess[:-1]

            # if event is an enter, check the word
            if event == "-ENTER-":
                if guess not in wordList:
                    window["-PRINT-"].update("Word not in list", visible=True)
                else:
                    if actualRow < 5:
                        window = colorGuess(guess, gameWord, letterCounts, gameSet, window, actualRow) # Get the colors of the word
                        if guess == gameWord:
                            won = True
                            break
                        guess = ""
                        actualRow += 1
                        actualFocus = window[(actualRow, 0)]
                        actualFocus.update(disabled=False)
                        actualFocus.set_focus()
                        continue
                    if actualRow == 5:
                        window = colorGuess(guess, gameWord, letterCounts, gameSet, window, actualRow) # Get the colors of the word
                        if guess == gameWord:
                            won = True
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
        if won==None:
            won=False
            window["-PRINT-"].update("You lost :c", visible=True)
            sg.popup("Press ENTER to leave", auto_close=True, auto_close_duration=2)
            while(True):
                event, values = window.read() # getting the events
                if event == "-ENTER-" or event == sg.WINDOW_CLOSED:
                    break

    return (window, event, won)

# -----------------------------------------------------------

# control the state of the program before and after the game
# TODO: save and load stats, play again, and continue a previous game
def main():
    # try to load an unfinished game # [ ]: load a previous unfinished game
    # try:
    #     with open("game_data/previous_game_state.json") as f:
    #         
    # except (FileNotFoundError, json.decoder.JSONDecodeError):

        # load stats # [ ]: load the stats from "game_data/stats.json"
        # loadStats()

        # show stats
        # statsWindow = showStats()
    window = createGameWindow()

        # [ ]: load next word in the wordList instead of choosing at random
    with open("words.txt", mode='rt') as f:
        wordList = f.readlines()
        for x in range(len(wordList)):
            wordList[x] = wordList[x].strip("\n").upper()

    window, event, won = startGame(window, wordList)
        
        # if won!=None: # if game was finished, save stats and ask to play again
        #     # save stats then reload the stats window # [ ]: save the stats to "game_data/stats.json"
        #     statsWindow.close()
        #     saveStats()
        #     statsWindow = showStats()

        #     # [ ]: popup after game asking to play again
        #     playAgain = True
        #     while(playAgain):
        #         playAgainWindow, response = playAgain()
        #         if response=="-YES-":
        #             window.close()
        #             statsWindow.close()
        #             playAgainWindow.close()
        #             statsWindow = showStats()
        #             window, event = startGame(wordList)
        #         else:
        #             playAgain = False
        # else: # if the window was closed and game unfinished, save the game state until the program is executed again
        #     saveGameState() # [ ]: save an unfinished game
    # 

    # Finish up by removing from the screen
    window.close()
    # statsWindow.close()
    # playAgainWindow.close()
        

if __name__ == "__main__":
    main()