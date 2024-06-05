import time
import pyautogui

import tileDetection as tD
import terminalPrompts
import developerMode
import initializeDataStructures as initDS

# IMPORTANT NOTE: don't run this file directly, as you run the risk of being in an infinite loop - instead, tun the
# program from the file 'launcher.py'


# for testing screen coordinate values
# while True:
#     print(pyautogui.position())
#     time.sleep(2)


# STEP #1: run introduction prompts and return list of values
responses = terminalPrompts.run_intro_prompts()
# index 0: START/RESTART BUTTON COORDINATES (tuple)
# index 1: CENTER OF FIRST TILE COORDINATES (tuple)
# index 2: ZOOM SIZE (string)
# index 3: BOARD SIZE (string)
# index 4: BOMB COUNT (string)
# index 5: DEVELOPER MODE (string: 'y' or 'n')


# STEP 2: initialize data structures and global variables
col_x_coords = initDS.return_coord_map_cols(int(responses[2]), responses[1], responses[3])  # dict
row_y_coords = initDS.return_coord_map_rows(int(responses[2]), responses[1], responses[3])  # dict
gameboard = initDS.return_gameboard(responses[3])  # 2D list
bombs_remaining = int(responses[4])
wins, losses, guesses = 0, 0, 0


# for testing colors
# while True:
#     print(tD.return_tile_type(30))
#     time.sleep(1)


# STEP #3: enter developer mode if necessary
print()
print()
if responses[5] == 'y':
    developerMode.run_developer_mode(gameboard, col_x_coords, row_y_coords, responses[0], responses[1], int(responses[2]))
    exit()


# STEP #4: begin running bot algorithm
# ...
