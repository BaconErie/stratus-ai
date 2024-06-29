'''
Record:
- 
'''

from pynput import mouse
from pynput import keyboard

import datetime

start_timestamp = datetime.datetime.now().timestamp()

unique_keys = []
total_x = 0
total_y = 0
mouse_move_counts = 0
mouse_input_counts = 0
left_mouse_held_time = 0
right_mouse_held_time = 0

file = open(f'log_{str(int(start_timestamp))}.csv', 'w')

def on_move(x, y):
    total_x += x
    total_y += y
    mouse_event_counts += 1

def on_click(x, y, button, pressed):
    current_timestamp = datetime.datetime.now().timestamp()
    delta_timestamp = current_timestamp - start_timestamp

    event = 'pressed' if pressed else 'released'

    log_string = f'{delta_timestamp},{event},{button}'
    
    file.write(log_string + '\n')
    
    print(log_string)

def on_press(key_raw):
    key = ''
    try:
        key = key_raw.char
    except AttributeError:
        key = key_raw

    key = str(key)

    if not key in key_dict.keys():
        key_dict[key] = len(key_dict)
    key = key_dict[key]

    current_timestamp = datetime.datetime.now().timestamp()
    delta_timestamp = current_timestamp - start_timestamp

    log_string = f'{delta_timestamp},keypress,{key}'
    
    file.write(log_string + '\n')
    
    print(log_string)

    if key_raw == keyboard.Key.esc:
        # Stop listener
        file.close()
        return False    

def on_scroll(x, y, dx, dy):
    current_timestamp = datetime.datetime.now().timestamp()
    delta_timestamp = current_timestamp - start_timestamp

    log_string = f'{delta_timestamp},scroll,{dx},{dy}'
    
    file.write(log_string + '\n')
    
    print(log_string)

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