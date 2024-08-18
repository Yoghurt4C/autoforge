import os
from threading import Thread, Event
from time import sleep

from pynput.keyboard import GlobalHotKeys
from pynput.mouse import Button, Controller

mouse = Controller()
toggle = False
cursor = (0, 0)
thread = None
event = Event()


def notify(string: str):
    cmd = 'notify-send \"' + string + '\"'
    os.system(cmd)


def click(pos: tuple, amount=1):
    mouse.position = pos
    mouse.click(Button.left, amount)


def abort():
    global event
    event.set()
    exit(0)


def savePos():
    global cursor
    cursor = mouse.position
    notify("Item at " + str(cursor) + " will be clicked.")


def consumeTome():
    global cursor
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


def autoforge():
    click((1019, 694))
    sleep(0.1)
    click((1126, 694))
    sleep(2.15)


def loop(stop: Event, method=None):
    while True:
        if stop.is_set():
            stop.clear()
            break
        method()


def startThread(method=None, needsCursor=True):
    global toggle
    global cursor
    global thread
    global event
    if needsCursor is True and cursor == (0, 0):
        notify('Press CTRL+Q over an item slot before activating loop functions.')
    else:
        toggle = not toggle
        if toggle:
            thread = Thread(target=loop, args=(event, method))
            thread.start()
        else:
            event.set()


with GlobalHotKeys({
    '<ctrl>+p': abort,
    '<ctrl>+q': savePos,
    '<alt>+[': lambda: startThread(consumeTome),
    '<alt>+]': lambda: startThread(selectableContainer),
    '<alt>+k': lambda: startThread(autoforge, False)
}) as listener:
    listener.join()
