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
toggle_timing = False
action_time = 0

root = get_project_root()
mouse_dir = (root / 'Mouse Macros')
key_dir = (root/'Keyboard Macros')
combo_dir = (root/'Combo Macros')


def detect_mouse():
    listener = mouse.Listener(on_click=on_click)
    listener.start()


def detect_key():
    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()


def on_click(x, y, button, pressed):  #procceses mouse clicks
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


def on_press(key):  #processes keyboard presses
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

    elif toggle_listen_keyboard:
          try:
                write_to_file_key(key.char, get_time(), key_dir)

          except AttributeError:
                if key == keyboard.Key.f6:
                    pass

    else:
        if key == keyboard.Key.f5:
            print('f5 pressed')


def setup_listeners():
    detect_mouse()
    detect_key()


def create_file(name,directory, timing=False, mouse=False, keyboard=False ):
    global file_name
    global toggle_listen_mouse
    global toggle_listen_keyboard
    global toggle_timing
    global action_time
    if same_file_check(name, directory):
        print('same file exists!')
        return True
    else:
        action_time = time.time()
        toggle_listen_mouse = mouse
        toggle_listen_keyboard = keyboard
        toggle_timing = timing
        file_name = '{0}.csv'.format(name)


def delete_file(f_name, directory):
    name = (f_name + '.csv')
    file = Path(directory / name)
    file.unlink()


def write_to_file_mouse(x, y, button, state, directory, time):
    file = (directory/file_name)
    if toggle_timing:
        with open(file, 'a', newline='') as f:
            row = '0,{0},{1},{2},{3},{4}'.format(x, y, button, state,time)
            writer = csv.writer(f, quoting = csv.QUOTE_NONE, delimiter =' ')
            writer.writerow(row.split())
    else:
        with open(file, 'a', newline='') as f:
            row = '0,{0},{1},{2},{3},{4}'.format(x, y, button, state,0.5)
            writer = csv.writer(f, quoting = csv.QUOTE_NONE, delimiter =' ')
            writer.writerow(row.split())


def write_to_file_key(key, timing, directory):
    file = (directory / file_name)
    if toggle_timing:
        with open(file, 'a', newline='') as f:
            row = '1,{0},{1}'.format(key,timing)
            writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=' ')
            writer.writerow(row.split())
    else:
        with open(file, 'a', newline='') as f:
            row = '1,{0},{1}'.format(key, 0.5)
            writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=' ')
            writer.writerow(row.split())


def end_record(file, directory):
    global toggle_listen_mouse, toggle_listen_keyboard, toggle_timing
    toggle_listen_mouse = False
    toggle_listen_keyboard = False
    toggle_timing = False
    if same_file_check(file, directory):
        return True
    else:
        return False


def convert_macro_text(macro_name, directory):
    file = '{0}.csv'.format(macro_name)
    file_path = (directory/file)
    with open(file_path, newline='') as file:
        reader = csv.reader(file_path)

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


def same_file_check(macro_name, directory):
    file = '{0}.csv'.format(macro_name)
    file_path = (directory / file)
    for i in Path.glob(directory, '*.csv'):
        if i == file_path:
            print(i)
            return True
    return False


def get_time():
    global action_time
    current_time = time.time()
    new_action = current_time-action_time
    action_time = current_time
    return round(new_action, 2)