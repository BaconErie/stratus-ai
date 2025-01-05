import log_to_csv
import numpy as np
from json import dumps

##############
# X POS TEST #
##############

x_rand_array = np.random.randint(10, size=10)
unique, counts = np.unique(x_rand_array, return_counts=True)
unique = [x.item() for x in unique]
counts = [x.item() for x in counts]

x_histogram = dict(zip(unique, counts))

actual_x_pos_mean = np.mean(x_rand_array)
actual_x_pos_std_dev = np.std(x_rand_array)

##############
# Y POS TEST #
##############

y_rand_array = np.random.randint(10, size=10)
unique, counts = np.unique(y_rand_array, return_counts=True)
unique = [x.item() for x in unique]
counts = [x.item() for x in counts]
y_histogram = dict(zip(unique, counts))

actual_y_pos_mean = np.mean(y_rand_array)
actual_y_pos_std_dev = np.std(y_rand_array)

####################
# MOUSE HOLD TIMES #
####################

actual_left_mouse_held_time = 0.7428338527679443 / 60.0
actual_middle_mouse_held_time = 0.0
actual_right_mouse_held_time = 0.0

####################
# MOUSE UP COUNTS #
####################

actual_left_mouseup_counts = 9
actual_middle_mouseup_counts = 0
actual_right_mouseup_counts = 0

####################
# KEYUP KEYS IN Q1 #
####################

actual_keyup_keys_in_q1 = 2

#######################
# KEY HELD KEYS IN Q1 #
#######################

actual_key_held_keys_in_q1 = 1

####################
# ALNUM KEYS IN Q1 #
####################

actual_alnum_keys_in_q1 = 2

####################
# ALNUM KEYS IN Q1 #
####################

actual_movement_key_ratio = 100/8

filename = 'filename.txt'
label = 'active'

actual_feature_list = [
    filename,
    label,

    actual_x_pos_mean, 
    actual_x_pos_std_dev, 

    actual_y_pos_mean, 
    actual_y_pos_std_dev,

    actual_left_mouse_held_time,
    actual_middle_mouse_held_time,
    actual_right_mouse_held_time,

    actual_left_mouseup_counts,
    actual_middle_mouseup_counts,
    actual_right_mouseup_counts,

    actual_keyup_keys_in_q1,

    actual_key_held_keys_in_q1,

    actual_alnum_keys_in_q1,

    actual_movement_key_ratio
]

actual = ', '.join([str(x) for x in actual_feature_list])

block = r'''time|2024-08-09 00:47:12.839074
minutes_since_start|3
x_histogram|''' + dumps(x_histogram) + r'''
y_histogram|''' + dumps(y_histogram) + r'''
keyup_counts|{"'z'": 2, "'x'": 2, "'w'": 1, "'a'": 1, "'s'": 1, "'d'": 1, "Key.space": 1, "Key.shift": 1}
mouseup_counts|{"Button.left": 9}
key_time_held|{"Key.space": 100, "'1'": 1, "'2'": 1, "'3'": 1, "'4'": 1, "'5'": 1, "'6'": 1, "'7'": 1, "'8'": 1}
time_mouse_held|{"Button.left": 0.7428338527679443}
dx_scroll_counts|{"0": 395}
dy_scroll_counts|{"-1": 292, "1": 103}
Hash|01f0dd97e0869f08d325aff13638bfbe64c2bd8f2eed4b04a27201f2449eb890'''

result = log_to_csv.process_block(filename, label, block)



print(result)
print('\n')
print(actual)

assert(result == actual)