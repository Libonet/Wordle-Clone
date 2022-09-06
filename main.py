from random import choice
from colorama import Fore, Style

def colorGuess(guess, gameWord, gameWordCount, wordSet): # gameWord = eerie, guess = (e, green)(e, green)(e, yellow)(e, none)n
    coloredGuess = [(guess[0], "none"), (guess[1], "none"), (guess[2], "none"), (guess[3], "none"), (guess[4], "none")]
    copy = gameWordCount.copy()
    for i, c in enumerate(gameWord): # coloreo los verdes
        if c == guess[i]:
            coloredGuess[i] = (c, "green")
            copy[c] -= 1
    for char in wordSet:
        for i, c in enumerate(coloredGuess):
            if copy[char]==0:
                continue
            if c == (char, "none"):
                coloredGuess[i] = (char, "yellow")
                copy[char] -= 1
    return coloredGuess

def colored(w):
    if w[1] == "green":
        return f"{Fore.GREEN}{w[0]}{Style.RESET_ALL}"
    elif w[1] == "yellow":
        return f"{Fore.YELLOW}{w[0]}{Style.RESET_ALL}"
    else:
        return f"{w[0]}"

def showTries(words, tries):
    for w in words:
        print(f"|{colored(w[0])}||{colored(w[1])}||{colored(w[2])}||{colored(w[3])}||{colored(w[4])}|")
    for x in range(5-tries):
        print("|_||_||_||_||_|")

def gameInput(wordList, gameWord, gameWordCount, wordSet):
    valid = False
    guess = []
    while(not valid):
        guess = input("Guess: ")
        if not guess.isalpha():
            print("Please enter only alphabetical characters for your guess.")
        elif len(guess) != 5:
            print("Word must be 5 characters long")
        elif guess not in wordList:
            print("Word not in list")
        else:
            valid = True
            guess = colorGuess(guess, gameWord, gameWordCount, wordSet)
    return guess

def startGame(wordList):
    win = False
    words = []
    gameWord = choice(wordList)
    wordSet = set(gameWord)
    gameWordCount = {}
    for c in gameWord:
        gameWordCount[c] = gameWord.count(c)
    for tries in range(6):
        guess = gameInput(wordList, gameWord, gameWordCount, wordSet)
        words.append(guess)
        showTries(words, tries)
        if words[tries] == gameWord:
            win = True
    if win:
        print("You won, chief.")
    else:
        print("You snooze, you lose")
    print(f"La palabra era {gameWord}")

def wordle():
    with open("words.txt", mode='rt') as f:
        wordList = f.readlines()
        for x in range(len(wordList)):
            wordList[x] = wordList[x].strip("\n")
        playAgain = True
        startGame(wordList)
        while(playAgain):
            if input("Do you want to play again? (y/n): ")=="y":
                startGame(wordList)
            else:
                playAgain = False

if __name__ == "__main__":
    wordle()