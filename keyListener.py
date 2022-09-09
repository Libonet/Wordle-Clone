from pynput import keyboard

def keyPress(key, cache, count):
    if hasattr(key,'char') and key.char!=None and count[0]<5:
        if key.char.isalpha():
            cache[count[0]]=key.char.upper()
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
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # other code goes here

    listener.stop()