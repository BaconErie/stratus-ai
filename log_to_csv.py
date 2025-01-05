'''
LOG TO CSV

Converts Stratus AI logs into CSV.

Each row in the CSV corresponds to one data point, which is one minute.

The columns include the features, label, as well as the file name from which it is taken.

PROGRAM FLOW

1. Take a file, break it into blocks, one for each minute
2. Turn that block into a CSV row with features and label
3. Write that to a main CSV file.
'''

from typing import Union
from json import loads
import numpy as np

from os import listdir
from os.path import isfile, join


from pprint import pprint

def process_file_contents(filename: str, label: str, contents: str) -> str:
    raw_blocks = contents.split('\n\n')
    header_data = raw_blocks[0]
    blocks = raw_blocks[1:-1] # Getting rid of monitor data and ending whitespace

    monitor_min_x, monitor_max_x, monitor_min_y, monitor_max_y = get_monitor_information(header_data)

    row_output = []

    for block in blocks:
        row = process_block(filename, label, block, monitor_min_x, monitor_max_x, monitor_min_y, monitor_max_y)
        row_output.append(row)

    return '\n'.join(row_output) + '\n'
    



def process_block(filename: str, label: str, block: str, monitor_min_x: int, monitor_max_x: int, monitor_min_y: int, monitor_max_y: int) -> str:
    '''Given block and other data, return CSV row as string
    
    label,
    filename,

    x_pos_mean, 
    x_pos_stdev, 

    y_pos_mean, 
    y_pos_std_dev, 

    mouse_event_counts,

    left_mouse_held_time,
    middle_mouse_held_time,
    right_mouse_held_time,
    
    left_mouseup_counts,
    middle_mouseup_counts,
    right_mouseup_counts,

    total_key_up_counts,
    keyup_keys_in_q1,

    total_key_time_held,
    key_held_keys_in_q1,

    alnum_keys_in_q1,

    movement_key_ratio
    '''

    lines = block.split('\n')
    lines_by_name = dict([ line.split('|', 1) for line in lines])


    # Mouse pos processing

    lines_by_name['x_histogram'] = loads(lines_by_name['x_histogram'])
    x_pos_list = bin_to_list(lines_by_name['x_histogram'])
    x_pos_list = [scale(x, monitor_min_x, monitor_max_x) for x in x_pos_list]

    if len(x_pos_list) == 0:
        # No mouse inputs
        x_pos_list = [-1]

    x_pos_mean = np.mean(x_pos_list) # feature
    x_pos_std_dev = np.std(x_pos_list) # feature


    lines_by_name['y_histogram'] = loads(lines_by_name['y_histogram'])
    y_pos_list = bin_to_list(lines_by_name['y_histogram'])
    y_pos_list = [scale(y, monitor_min_y, monitor_max_y) for y in y_pos_list]

    if len(y_pos_list) == 0:
        # No mouse inputs
        y_pos_list = [-1]

    y_pos_mean = np.mean(y_pos_list) # feature
    y_pos_std_dev = np.std(y_pos_list) # feature

    mouse_event_counts = len(x_pos_list)

    # Mouse button held

    lines_by_name['time_mouse_held'] = loads(lines_by_name['time_mouse_held'])

    left_mouse_held_time = 0.0 # feature
    middle_mouse_held_time = 0.0 # feature
    right_mouse_held_time = 0.0 # feature

    if 'Button.left' in lines_by_name['time_mouse_held'].keys():
        left_mouse_held_time = lines_by_name['time_mouse_held']['Button.left'] / 60.0

    if 'Button.middle' in lines_by_name['time_mouse_held'].keys():
        middle_mouse_held_time = lines_by_name['time_mouse_held']['Button.middle'] / 60.0
    
    if 'Button.right' in lines_by_name['time_mouse_held'].keys():
        right_mouse_held_time = lines_by_name['time_mouse_held']['Button.right'] / 60.0
    

    # Mouse up counts

    lines_by_name['mouseup_counts'] = loads(lines_by_name['mouseup_counts'])

    left_mouseup_counts = 0 # feature
    middle_mouseup_counts = 0 # feature
    right_mouseup_counts = 0 # feature
    
    if 'Button.left' in lines_by_name['mouseup_counts'].keys():
        left_mouseup_counts = lines_by_name['mouseup_counts']['Button.left']

    if 'Button.middle' in lines_by_name['mouseup_counts'].keys():
        middle_mouseup_counts = lines_by_name['mouseup_counts']['Button.middle']

    if 'Button.right' in lines_by_name['mouseup_counts'].keys():
        right_mouseup_counts = lines_by_name['mouseup_counts']['Button.right']

    # Clean up key up counts

    keyup_counts = clean_key_dict(loads(lines_by_name['keyup_counts']))

    # How many keys are 25% most keyup'd

    # 1. Find total keyup counts O(n)
    # 2. Find 25% of that number O(1)
    # 3. Sort keys from most to least keyup counts
    # 4. Go thru list of keys, adding up their keyup counts until the sum is 
    #    greater than 25% of that number

    total_key_up_counts = np.sum(list(keyup_counts.values()))
    first_quartile = total_key_up_counts / 4
    
    keyup_count_sum = 0
    keyup_keys_in_q1 = 0 # feature

    for key in keyup_counts.keys():
        if keyup_count_sum >= first_quartile: 
            break

        keyup_keys_in_q1 += 1
        keyup_count_sum += keyup_counts[key]

    # CLEANING UP KEY TIME HELD
    
    key_time_held = clean_key_dict(loads(lines_by_name['key_time_held']))
    
    
    # How many keys are in Q1 in terms of most held
    # Basically same method as above 

    total_key_time_held = np.sum(list(key_time_held.values()))
    first_quartile = total_key_time_held / 4
    
    key_time_held_sum = 0
    key_held_keys_in_q1 = 0 # feature

    for key in key_time_held.keys():
        if key_time_held_sum >= first_quartile: 
            break

        key_held_keys_in_q1 += 1
        key_time_held_sum += key_time_held[key]
    
    # Movement keys to non-movement keys hold time ratio

    movement_keys_hold_time = 0
    non_movement_keys_hold_time = 0

    for key in key_time_held.keys():
        if key in 'wasd' or key in ['key.space', 'key.shift', 'key.left', 'key.right', 'key.up', 'key.down']:
            movement_keys_hold_time += key_time_held[key]
        else:
            non_movement_keys_hold_time += key_time_held[key]

    movement_key_ratio = 0 if non_movement_keys_hold_time == 0 else movement_keys_hold_time / non_movement_keys_hold_time # feature

    # How many LETTERS AND NUMBERS ONLY keys are in Q1 in terms of most key up
    # ===
    # 1. Get sum of all alphanumeric keys hold times
    # 2. Calculate first_quartile
    # 3. Loop thru key_time_held again and see how many keys before >= Q1

    alnum_key_held_sum = 0

    for key in key_time_held.keys():
        if key.isalnum():
            alnum_key_held_sum += key_time_held[key]
    
    first_quartile = alnum_key_held_sum / 4

    alnum_keys_in_q1 = 0 # feature
    running_total = 0
    for key in key_time_held.keys():
        if not key.isalnum():
            continue

        if running_total >= first_quartile:
            break
        
        running_total += key_time_held[key]
        alnum_keys_in_q1 += 1

    feature_list = [
        filename,
        label,

        x_pos_mean, 
        x_pos_std_dev, 

        y_pos_mean, 
        y_pos_std_dev,

        mouse_event_counts,

        left_mouse_held_time,
        middle_mouse_held_time,
        right_mouse_held_time,

        left_mouseup_counts,
        middle_mouseup_counts,
        right_mouseup_counts,

        total_key_up_counts,
        keyup_keys_in_q1,

        total_key_time_held,
        key_held_keys_in_q1,

        alnum_keys_in_q1,

        movement_key_ratio
    ]

    return ','.join([str(x) for x in feature_list])
    
def bin_to_list(dict) -> list[int]:
    result = []

    for key in dict.keys():
        key = key

        for x in range(dict[key]):
            result.append(int(key))

    return result

def clean_key_dict(key_dict: dict[str, Union[int, float]]) -> dict[str, Union[int, float]]:
    new_dict = {}

    for orig_key in key_dict.keys():
        key = orig_key.lower()
        
        if len(key) == 3:
            key = key[1]

        if key not in new_dict.keys():
            new_dict[key] = key_dict[orig_key]
        else:
            new_dict[key] += key_dict[orig_key]
    
    new_dict = dict(sorted(new_dict.items(), key=lambda item: item[1], reverse=True))

    return new_dict

def get_monitor_information(content: str) -> tuple[int, int, int, int]:
    for line in content.split('\n'):
        if line.startswith('Monitor') and bool(line[line.index('is_primary=')+11:-1]): # second part is checking if its primary
            monitor_min_x = int(line[line.index('x=') + 2:line.index(', y=')])
            monitor_max_x = monitor_min_x + int(line[line.index('width=') + 6:line.index(', height=')])

            monitor_min_y = int(line[line.index('y=') + 2:line.index(', width=')])
            monitor_max_y = monitor_min_y + int(line[line.index('height=') + 7:line.index(', width_mm=')])
    
    return monitor_min_x, monitor_max_x, monitor_min_y, monitor_max_y

def scale(x: Union[int, float], min: Union[int, float], max: Union[int, float]) -> float:
    return (1/(max-min))*(x-min)

def process_category(csv_path: str, category_logs_path: str, label: str):
    log_names = [join(category_logs_path, f) for f in listdir(category_logs_path) if isfile(join(category_logs_path, f))]

    csv_file = open(csv_path, 'a')

    csv_file.write('label,filename,x_pos_mean,x_pos_stdev,y_pos_mean,y_pos_std_dev,mouse_event_counts,left_mouse_held_time,middle_mouse_held_time,right_mouse_held_time,left_mouseup_counts,middle_mouseup_counts,right_mouseup_counts,total_key_up_counts,keyup_keys_in_q1,total_key_time_held,key_held_keys_in_q1,alnum_keys_in_q1,movement_key_ratio\n')

    for name in log_names:
        file_obj = open(name, 'r')
        contents = file_obj.read()
        file_obj.close()

        csv_string = process_file_contents(name, label, contents)
        csv_file.write(csv_string)
    
    csv_file.close()


if __name__ == '__main__':
    active_folder = './logs/active'
    games_folder = './logs/games'
    passive_folder = './logs/passive'

    active_csv = './active.csv'
    games_csv = './games.csv'
    passive_csv = './passive.csv'

    combined_csv = './new_data.csv'

    process_category(active_csv, active_folder, 'active')
    process_category(games_csv, games_folder, 'games')
    process_category(passive_csv, passive_folder, 'passive')

    process_category(combined_csv, active_folder, 'active')
    process_category(combined_csv, games_folder, 'games')
    process_category(combined_csv, passive_folder, 'passive')
    

    

