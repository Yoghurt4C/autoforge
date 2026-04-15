import os
import sys
from threading import Thread, Event
from time import sleep

import pynput.keyboard
from pynput.keyboard import GlobalHotKeys
from pynput.mouse import Button, Controller

mouse = Controller()
keeb = pynput.keyboard.Controller()
key = pynput.keyboard.Key
toggle = False
cursor = (0, 0)
thread = None
event = Event()


def notify(string: str):
    # todo replace with tkinter msgbox
    if sys.platform.startswith("linux"):
        cmd = 'notify-send \"' + string + '\"'
        os.system(cmd)


def click(pos: tuple, amount=1):
    mouse.position = pos
    mouse.click(Button.left, amount)


def abort():
    event.set()
    listener.stop()
    exit(0)


def savePos():
    global cursor
    cursor = mouse.position
    notify("Item at " + str(cursor) + " will be clicked.")


def consumeTome():
    click(cursor, 2)
    sleep(0.25)
    click((947, 590))
    sleep(0.025)


def selectableContainer():
    click(cursor, 2)
    sleep(0.25)
    click((1060, 514))
    sleep(0.1)
    click((954, 680))
    sleep(0.1)
    click((954, 588))
    sleep(0.025)


def firework():
    sleep(0.65)
    click(cursor, 2)
    sleep(0.45)
    click((689, 1035))


def autoforge():
    click((1019, 694))
    sleep(0.1)
    click((1126, 694))
    sleep(2.15)


def autoclick():
    click(mouse.position, amount=2)
    sleep(0.05)


def loop(stop: Event, method=None):
    while True:
        if stop.is_set():
            stop.clear()
            break
        method()


from pynput.mouse import Listener


def jumproll(x: int, y: int, button: Button, pressed: bool):
    if pressed and button == button.button9:
        keeb.tap(key.space)
        keeb.tap('v')


meece = Listener(on_click=jumproll)
meece.start()


def startThread(method=None, needsCursor=True):
    global toggle
    global thread
    if needsCursor is True and cursor == (0, 0):
        notify('Press CTRL+Q over an item slot before activating loop functions.')
    else:
        toggle = not toggle
        if toggle:
            thread = Thread(target=loop, args=(event, method))
            thread.start()
        else:
            event.set()


keys = {
    '<ctrl>+p': abort,
    '<ctrl>+q': savePos,
    '<alt>+[': lambda: startThread(consumeTome),
    '<alt>+]': lambda: startThread(selectableContainer),
    '<alt>+k': lambda: startThread(autoforge, False),
    '<alt>+f': lambda: startThread(firework),
    '<alt>+y': lambda: startThread(autoclick, False)
}

hint = {
    'Ctrl + P': 'Exit Autoforge',
    'Ctrl + Q': 'Save Cursor Position',
    'Alt + [': 'Consume Tomes of Knowledge (Requires saved cursor pos.)',
    'Alt + ]': 'Consume Selectable Containers (Requires saved cursor pos.)',
    'Alt + K': 'Automatic Mystic Forge Crafting & Refilling',
    'Alt + F': 'Spam Dragon Bash Fireworks (Requires saved cursor pos.)',
    'Alt + Y': 'Autoclick (Current cursor pos.)',
    'MB5': 'Roll-jump (For SAB)'
}

for e in hint:
    print(e + ": " + hint[e])

with GlobalHotKeys(keys) as listener:
    listener.join()
