from pynput import mouse, keyboard
from screeninfo import get_monitors
from json import dumps
import sys
import os
import platform
import hashlib
from time import sleep
import datetime

print('''
Hello!
This software collects data that will be used to train the StratusAI system.
      
Every minute, this software will record
      - Which keyboard keys were pressed and how often in the last minute
      - Frequent mouse locations in the last minute
      - Time the mouse buttons were held in the last minute
      - Monitors and monitor resolution data
      - OS information
and enter the data as an entry in a log file. The log file will be stored in the "logs" folder inside the program's folder.
      
Data is not recorded chronologically, and comprehensible strings of text cannot be deciphered from the logs.
Nonetheless, you should use this program while working on non-sensitive tasks.
      
MAKE SURE TO CLOSE THE PROGRAM ONCE YOU'VE COMPLETED THE TASK!
      
Data from a wide variety of tasks (writing, typing, reading, playing FPS games, playing simpler games that don't lock the mouse, etc.) is preferred.
      
Once you've collected the data, you can inspect the logs in the "logs" folder, and then send the logs folder as a zip file to baconerie0001@gmail.com
      
''')

name = input('Please enter a descriptive name for the task (game name, "reading", "writing essay"): ')

start_time = datetime.datetime.now()
start_timestamp = start_time.timestamp()


if getattr(sys, 'frozen', False):
    filename = os.path.join(os.path.dirname(sys.executable), 'logs', f'stratus_log_{name}_{int(start_timestamp)}.txt')
else:
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', f'stratus_log_{name}_{start_timestamp}.txt')
    

file = open(filename, 'w')

print(f'\n\n\nWriting data to {filename}')

file.write('Started at ' + str(start_time) + '\n')

# Record OS and monitor data
file.write(str(platform.platform()) + '\n')
for m in get_monitors():
    file.write(str(m) + '\n')

file.write('\n')

file.close()


# Input stats in the last minute
# Comments below document key: value
last_min_x_pos = {} # x-pos: times mouse was recorded at that x-pos
last_min_y_pos = {} # y-pos: times mouse was recorded at that y-pos
keyup_counts = {} # key: times key was released
mouseup_counts = {} # button: times button was released
key_time_held = {} # key: timeheld
time_mouse_held = {} # button: timeheld
dx_scroll_counts = {} # dx: times this dx was recorded. Counts horizontal scroll inputs
dy_scroll_counts = {} # dy: times this dy was recorded. Counts vertical scroll inputs

# Below are used by the event handlers to calculate data for above variables
# These should not be logged
mouse_last_pressed = {} # button: timestamp the button was pressed/released
key_last_pressed = {} # key: timestamp the button was pressed/released

def reset():
    global last_min_x_pos
    global last_min_y_pos
    global keyup_counts
    global mouseup_counts
    global key_time_held
    global time_mouse_held
    global dx_scroll_counts
    global dy_scroll_counts

    last_min_x_pos = {} # x-pos: times mouse was recorded at that x-pos
    last_min_y_pos = {} # y-pos: times mouse was recorded at that y-pos
    keyup_counts = {} # key: times key was released
    mouseup_counts = {} # button: times button was released
    key_time_held = {} # key: timeheld
    time_mouse_held = {} # button: timeheld
    dx_scroll_counts = {} # dx: times this dx was recorded. Counts horizontal scroll inputs
    dy_scroll_counts = {} # dy: times this dy was recorded. Counts vertical scroll inputs


# MOUSE HANDLERS

def on_move(x, y):
    global last_min_x_pos
    global last_min_y_pos

    if x not in last_min_x_pos.keys():
        last_min_x_pos[x] = 1
    else:
        last_min_x_pos[x] += 1
    
    if y not in last_min_y_pos.keys():
        last_min_y_pos[y] = 1
    else:
        last_min_y_pos[y] += 1
    
    

def on_click(x, y, button, pressed):
    global last_min_x_pos
    global last_min_y_pos
    global mouse_last_pressed

    if x not in last_min_x_pos.keys():
        last_min_x_pos[x] = 1
    else:
        last_min_x_pos[x] += 1
    
    if y not in last_min_y_pos.keys():
        last_min_y_pos[y] = 1
    else:
        last_min_y_pos[y] += 1

    current_timestamp = datetime.datetime.now().timestamp()
    
    if not pressed and str(button) in mouse_last_pressed.keys():
        last_press_time = mouse_last_pressed[str(button)]
        time_mouse_held[str(button)] = current_timestamp-last_press_time

        if str(button) not in mouseup_counts.keys():
            mouseup_counts[str(button)] = 1
        else:
            mouseup_counts[str(button)] += 1

    mouse_last_pressed[str(button)] = current_timestamp

def on_scroll(x, y, dx, dy):
    global last_min_x_pos
    global last_min_y_pos
    global dx_scroll_counts
    global dy_scroll_counts

    if x not in last_min_x_pos.keys():
        last_min_x_pos[x] = 1
    else:
        last_min_x_pos[x] += 1
    
    if y not in last_min_y_pos.keys():
        last_min_y_pos[y] = 1
    else:
        last_min_y_pos[y] += 1
    
    if dx not in dx_scroll_counts.keys():
        dx_scroll_counts[dx] = 1
    else:
        dx_scroll_counts[dx] += 1
    
    if dy not in dy_scroll_counts.keys():
        dy_scroll_counts[dy] = 1
    else:
        dy_scroll_counts[dy] += 1



# KEYBOARD HANDLERS

def on_press(key_raw):
    global key_last_pressed

    key = str(key_raw)
    
    current_timestamp = datetime.datetime.now().timestamp()
    if key not in key_last_pressed.keys():
        key_last_pressed[key] = current_timestamp

def on_release(key_raw):
    global key_last_pressed
    global key_time_held
    global keyup_counts

    key = str(key_raw)

    current_timestamp = datetime.datetime.now().timestamp()
    if key in key_last_pressed.keys():
        key_time_held[key] = current_timestamp - key_last_pressed[key]
        key_last_pressed.pop(key)

    if key not in keyup_counts.keys():
        keyup_counts[key] = 1
    else:
        keyup_counts[key] += 1

# Start listeners
mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll
)
mouse_listener.start()

keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release
)
keyboard_listener.start()

print('\nData collection started. MAKE SURE TO CLOSE THE PROGRAM ONCE YOU\'VE COMPLETED THE TASK!!')

def create_histogram_from_dict(dict):
    dict_min = min(dict.keys())
    dict_max = max(dict.keys())

    histogram_min = dict_min - dict_min % 50
    histogram_max = dict_max - dict_max % 50

    histogram = {}

    # Creating keys for the histogram
    for x in range(histogram_min, histogram_max+50, 50):
        histogram[x] = 0
    
    # Populating the histogram
    for key in dict.keys():
        histogram[key - key % 50] += dict[key]

    return histogram


# Logging loop
# Every minute:
# - Log time and time since start
# - Turn last_min_x_pos and last_min_y_pos into histogram, and record
# - Record all other variables directly
# - Reset variables
while True:
    sleep(60)

    file = open(filename, 'a')
    
    if len(last_min_x_pos.keys()) > 0:
        x_histogram = create_histogram_from_dict(last_min_x_pos)
    else:
        x_histogram = {}
    
    if len(last_min_y_pos.keys()) > 0:
        y_histogram = create_histogram_from_dict(last_min_y_pos)
    else:
        y_histogram = {}

    file.write('time|' + str(datetime.datetime.now()) + '\n')
    file.write('minutes_since_start|' + str(int((datetime.datetime.now().timestamp() - start_timestamp) / 60)) + '\n')
    file.write('x_histogram|' + dumps(x_histogram) + '\n')
    file.write('y_histogram|' + dumps(y_histogram) + '\n')
    file.write('keyup_counts|' + dumps(dict(sorted(keyup_counts.items()))) + '\n')
    file.write('mouseup_counts|' + dumps(dict(sorted(mouseup_counts.items()))) + '\n')
    file.write('key_time_held|' + dumps(dict(sorted(key_time_held.items()))) + '\n')
    file.write('time_mouse_held|' + dumps(dict(sorted(time_mouse_held.items()))) + '\n')
    file.write('dx_scroll_counts|' + dumps(dict(sorted(dx_scroll_counts.items()))) + '\n')
    file.write('dy_scroll_counts|' + dumps(dict(sorted(dy_scroll_counts.items()))) + '\n')
    file.close()

    # Read file and add checksum hash
    file = open(filename, 'r')
    contents = file.read()

    # For some reason stray new line at the end of the file
    if contents[-1] == '\n':
        contents = contents[:-1]

    file.close()

    file = open(filename, 'a')
    file.write('Hash|' + hashlib.sha256(contents.encode('utf-8')).hexdigest() + '\n\n')
    file.close()

    reset()