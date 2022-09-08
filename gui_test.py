import PySimpleGUI as sg
from pynput import keyboard

def keyPress(key, cache, count):
    if hasattr(key,'char') and key.char!=None and count[0]<5:
        if key.char.isalpha():
            cache[count[0]]=key.char
            count[0] = count[0] + 1
    if key == keyboard.Key.backspace and count[0]>0:    
        cache[count[0]-1]=""
        count[0] = count[0] - 1
    print(cache)

def main():
    cache = ["","","","",""]
    count = [0]
    def on_press(key):
        keyPress(key, cache, count)

    """ def on_release(key):
        print('{0} released'.format(
            key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False """

    # Collect events until released
    #with keyboard.Listener(on_press=on_press) as listener:
    #    listener.join()

    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()

    # Define the window's contents
    layout = [
            # esto debería ser un output de las letras que capturo con el listener [],
            [sg.Input(size=(20, 1), key='-INPUT-')],
            [sg.Text(size=(40,1), key='-OUTPUT-')],
            [sg.Button('Ok'), sg.Button('Quit')]]

    # Create the window
    window = sg.Window('Wordle Game Thing', layout)

    while True:
        # Display and interact with the Window using an Event Loop
        event, values = window.read()
        # while True:
            
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        # Output a message to the window
        if event == 'Ok':
            window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

        # Finish up by removing from the screen
    window.close()
    listener.stop()

if __name__ == "__main__":
    main()