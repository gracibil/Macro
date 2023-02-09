from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import time
import csv
import ctypes
import git
from pathlib import Path



def get_project_root():
    return Path(git.Repo('.', search_parent_directories=True).working_tree_dir)

PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

file_name = ''
toggle_listen_mouse = False
toggle_listen_keyboard = False
toggle_timeing = False
action_time = 0

root = get_project_root()
mouse_dir = (root / 'Mouse Macros')
key_dir = (root/'Keyboard Macros')
combo_dir = (root/'Combo Macros')


def detect_mouse():
    listner = mouse.Listener(on_click=on_click)
    listner.start()


def detect_key():
    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()


def on_click(x, y, button, pressed): #procceses mouse clicks
    global toggle_listen_mouse
    if toggle_listen_mouse is True and toggle_listen_keyboard:
        if pressed:
            write_to_file_mouse(x, y, button, pressed, combo_dir, get_time())

        if not pressed:
            write_to_file_mouse(x, y, button, pressed, combo_dir, get_time())

    elif toggle_listen_mouse is True:
        if pressed:
            write_to_file_mouse(x, y, button, pressed, mouse_dir, get_time())

        if not pressed:
            write_to_file_mouse(x, y, button, pressed, mouse_dir, get_time())

    else:
        pass


def on_press(key): #processes keybooard presses
    global toggle_listen_keyboard, toggle_listen_mouse
    if toggle_listen_keyboard and toggle_listen_mouse:
          try:
                print('alphanumeric key {0} pressed'.format(
                       key.char))
                write_to_file_key(key.char, get_time(), combo_dir)

          except AttributeError:
                if key == keyboard.Key.f6:
                     print('special key {0} pressed'.format(
                            key))
                     return end_record()
    elif toggle_listen_keyboard:
          try:
                print('alphanumeric key {0} pressed'.format(
                       key.char))
                write_to_file_key(key.char, get_time(), key_dir)

          except AttributeError:
                if key == keyboard.Key.f6:
                     print('special key {0} pressed'.format(
                            key))
                     return end_record()
    else:
        if key == keyboard.Key.f5:
            print('f5 pressed')


def setup_listeners():
    detect_mouse()
    detect_key()


def create_file(name, timeing=False, mouse=False, keyboard=False ):
    global file_name
    global toggle_listen_mouse
    global toggle_listen_keyboard
    global toggle_timeing
    global action_time
    action_time = time.time()
    toggle_listen_mouse = mouse
    toggle_listen_keyboard = keyboard
    toggle_timeing = timeing
    file_name = '{0}.csv'.format(name)


def delete_file(f_name, directory):
    name = (f_name + '.csv')
    file = Path(directory / name)
    file.unlink()


def write_to_file_mouse(x, y, button, state, directory, time):
    file = (directory/file_name)
    if toggle_timeing:
        with open(file, 'a', newline='') as f:
            row = '0,{0},{1},{2},{3},{4}'.format(x, y, button, state,time)
            writer = csv.writer(f, quoting = csv.QUOTE_NONE, delimiter =' ')
            writer.writerow(row.split())
    else:
        with open(file, 'a', newline='') as f:
            row = '0,{0},{1},{2},{3},{4}'.format(x, y, button, state,0.5)
            writer = csv.writer(f, quoting = csv.QUOTE_NONE, delimiter =' ')
            writer.writerow(row.split())


def write_to_file_key(key, time, directory):
    file = (directory / file_name)
    if toggle_timeing:
        with open(file, 'a', newline='') as f:
            row = '1,{0},{1}'.format(key,time)
            writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=' ')
            writer.writerow(row.split())
    else:
        with open(file, 'a', newline='') as f:
            row = '1,{0},{1}'.format(key, 0.5)
            writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=' ')
            writer.writerow(row.split())


def end_record():
    global toggle_listen_mouse, toggle_listen_keyboard, toggle_timeing
    toggle_listen_mouse = False
    toggle_listen_keyboard = False
    toggle_timeing = False



def convert_macro_text(macro_name, directory):
    file_name = '{0}.csv'.format(macro_name)
    file = (directory/file_name)
    with open(file, newline='') as file:
        reader = csv.reader(file)

        for row in reader:
            play_macro(row)


def play_macro(row):
    control = Controller()
    key_control = keyboard.Controller()
    if row[0] == '0':
        x = row[1]
        y= row[2]
        button = row[3]
        action = row[4]
        sleep_time = float(row[5])
        control.position = (x,y)
        time.sleep(sleep_time)
        if button == 'Button.left' and action:
            control.press(Button.left)
        elif button == 'Button.left' and not action:
            control.release(Button.left)
        elif button == 'Button.right' and action:
            control.press(Button.right)
        elif button == 'Button.right' and not action:
             control.release(Button.right)

    elif row[0] == '1':
        key = row[1]
        sleep_time = float(row[2])
        key_control.press(key)
        time.sleep(sleep_time)


def play_keyboard_macro():
    pass


def get_time():
    global action_time
    current_time = time.time()
    new_action = current_time-action_time
    action_time = current_time
    return round(new_action, 2)