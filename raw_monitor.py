from pynput import mouse
from pynput import keyboard
import datetime


start_timestamp = datetime.datetime.now().timestamp()

name = input('Give a unique name for this file: ')

def on_move(x, y):
    global name

    current_timestamp = datetime.datetime.now().timestamp()
    delta_timestamp = current_timestamp - start_timestamp

    log_string = f'{delta_timestamp},move,{x},{y}'

    file = open(f'log_{str(int(start_timestamp))}_{name}.csv', 'a')
    print(log_string, file=file)
    file.close()

def on_click(x, y, button, pressed):
    current_timestamp = datetime.datetime.now().timestamp()
    delta_timestamp = current_timestamp - start_timestamp

    event = 'pressed' if pressed else 'released'

    log_string = f'{delta_timestamp},{event},{button}'
    
    file = open(f'log_{str(int(start_timestamp))}_{name}.csv', 'a')
    print(log_string, file=file)
    file.close()

def on_press(key_raw):
    key = ''
    try:
        key = key_raw.char
    except AttributeError:
        key = key_raw

    current_timestamp = datetime.datetime.now().timestamp()
    delta_timestamp = current_timestamp - start_timestamp

    log_string = f'{delta_timestamp},keypress,{key}'
    
    file = open(f'log_{str(int(start_timestamp))}_{name}.csv', 'a')
    print(log_string, file=file)
    file.close()

def on_scroll(x, y, dx, dy):
    current_timestamp = datetime.datetime.now().timestamp()
    delta_timestamp = current_timestamp - start_timestamp

    log_string = f'{delta_timestamp},scroll,{x},{y},{dx},{dy}'
    
    file = open(f'log_{str(int(start_timestamp))}_{name}.csv', 'a')
    print(log_string, file=file)
    file.close()



# Collect events until released
listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
listener.start()

key_listener = keyboard.Listener(
    on_press=on_press
    )
key_listener.start()
key_listener.join()