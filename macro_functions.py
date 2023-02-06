import pyautogui as pyautogui
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import time
import csv
import ctypes


PROCESS_PER_MONITOR_DPI_AWARE = 2

ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

file_name = ''
toggle_listen = False

def detect_mouse():
    listner = mouse.Listener(on_click=on_click)
    listner.start()

def detect_key():
    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()

def on_press(key):
    global toggle_listen
    if toggle_listen:
         try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
         except AttributeError:
            if key == keyboard.Key.f6:
                 print('special key {0} pressed'.format(
                  key))
                 toggle_listen = False
    else:
        print('listener is off')



def on_click(x, y, button, pressed):
    global toggle_listen
    if toggle_listen is True:
        if pressed:
            write_to_file(x, y, button, pressed)

        if not pressed:
            write_to_file(x, y, button, pressed)

    else :
        print('listener is off')


def terminate_listener():
    global toggle_listen
    toggle_listen = False


def create_file(name):
    global file_name
    global toggle_listen
    toggle_listen = True
    file_name = '{0}.csv'.format(name)



def setup_listeners():
    detect_mouse()
    detect_key()

def write_to_file(x, y, button, state):
    with open(file_name, 'a', newline='') as f:
        print(x, y, button, state)
        row = '{0},{1},{2},{3}'.format(x, y, button, state)
        writer = csv.writer(f, quoting = csv.QUOTE_NONE, delimiter =' ')
        writer.writerow(row.split())


def end_record():
    global toggle_listen
    toggle_listen = False



def convert_macro_text(macro_name):
    file_name = '{0}.csv'.format(macro_name)
    with open(file_name, newline='') as file:
        reader = csv.reader(file)

        for row in reader:
            play_mouse_macro(row)

    pass

def play_mouse_macro(row):
    control = Controller()
    x = row[0]
    y= row[1]
    button = row[2]
    action = row[3]
    control.position = (x,y)
    time.sleep(0.2)
    if button == 'Button.left' and action:
        control.press(Button.left)
        print(button, action)
    elif button == 'Button.left' and not action:
        control.release(Button.left)
        print(button,action)
    elif button == 'Button.right' and action:
        control.press(Button.right)
        print(button,action)
    elif button == 'Button.right' and not action:
        control.release(Button.right)
        print(button,action)













