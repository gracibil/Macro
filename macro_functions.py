import pyautogui as pyautogui
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import time
import csv
import ctypes


PROCESS_PER_MONITOR_DPI_AWARE = 2

ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

file_name = ''
toggle_listen_mouse = False
toggle_listen_keyboard = False
action_time = 0


def detect_mouse():
    listner = mouse.Listener(on_click=on_click)
    listner.start()


def detect_key():
    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()


def on_click(x, y, button, pressed):
    global toggle_listen_mouse
    if toggle_listen_mouse is True:
        if pressed:
            write_to_file_mouse(x, y, button, pressed, get_time())

        if not pressed:
            write_to_file_mouse(x, y, button, pressed, get_time())

    else :
        print('listener is off')


def on_press(key):
    global toggle_listen_keyboard
    if toggle_listen_keyboard:
         try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
            write_to_file_key(key.char, get_time())

         except AttributeError:
            if key == keyboard.Key.f6:
                 print('special key {0} pressed'.format(
                  key))
                 return end_record_mouse()
    else:
        print('listener is off')


def setup_listeners():
    detect_mouse()
    detect_key()


def terminate_listener():
    global toggle_listen_mouse
    toggle_listen_mouse = False


def create_file(name):
    global file_name
    global toggle_listen_mouse
    global action_time
    action_time = time.time()
    toggle_listen_mouse = True
    file_name = '{0}.csv'.format(name)


def delete_file(name):
    pass


def write_to_file_mouse(x, y, button, state, time=0.0):
    with open(file_name, 'a', newline='') as f:
        print(x, y, button, state)
        row = '{0},{1},{2},{3},{4}'.format(x, y, button, state,time)
        writer = csv.writer(f, quoting = csv.QUOTE_NONE, delimiter =' ')
        writer.writerow(row.split())


def write_to_file_key(key,time):
    with open(file_name, 'a', newline='') as f:
        row = '{0}{1}'.format(key,time)


def end_record_mouse():
    global toggle_listen_mouse
    toggle_listen_mouse = False


def end_record_key():
    global toggle_listen_keyboard
    toggle_listen_keyboard = False


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
    sleep_time = float(row[4])
    control.position = (x,y)
    time.sleep(sleep_time)
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


def play_keyboard_macro():
    pass

def get_time():
    global action_time
    current_time = time.time()
    new_action = current_time-action_time
    action_time = current_time
    print (round(new_action,2))
    return round(new_action, 2)