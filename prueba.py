import pyglet
from pyglet.libs.win32 import constants
import PySimpleGUI as sg


constants.COINIT_MULTITHREADED = 0x2  # 0x2 = COINIT_APARTMENTTHREADED

pyglet.font.add_file(r".\MerryChristmasFlake.ttf")
pyglet.font.add_file(r".\MerryChristmasStar.ttf")

sg.theme("Default1")
font1 = ("Merry Christmas Flake", 40)
font2 = ("Merry Christmas Star", 40)

layout = [
    [sg.Text("Merry Christmas Flake", font=font1)],
    [sg.Text("Merry Christmas Star",  font=font2)],
    [sg.Input(), sg.FolderBrowse()],
]

window = sg.Window('Title', layout, finalize=True)

while True:

    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    print(event, values)

window.close()