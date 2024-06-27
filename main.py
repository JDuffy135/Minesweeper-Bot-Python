import time
import pyautogui

import tileDetection as tD
import terminalPrompts
import developerMode
import initializeDataStructures as initDS
import fullAlgorithm

# IMPORTANT NOTE: don't run this file directly, as you run the risk of falling into an infinite loop - instead,
# run the program from the file 'launcher.py'


# for testing screen coordinate values
# while True:
#     print(pyautogui.position())
#     time.sleep(2)


# STEP #1: run introduction prompts and return list of values
responses = terminalPrompts.run_intro_prompts()
# index 0: START/RESTART BUTTON COORDINATES (tuple)
# index 1: CENTER OF FIRST TILE COORDINATES (tuple)
# index 2: ZOOM SIZE (string)
# index 3: BOARD SIZE (string) -> NOTE: converted to a tuple of form (cols, rows)
# index 4: BOMB COUNT (string)
# index 5: DEVELOPER MODE (string: 'y' or 'n')
# index 6: NUMBER OF GAMES TO PLAY (string: default is '10')


# STEP 2: initialize data structures and global variables representing statistics
col_x_coords = initDS.return_coord_map_cols(int(responses[2]), responses[1], responses[3])  # dict
row_y_coords = initDS.return_coord_map_rows(int(responses[2]), responses[1], responses[3])  # dict
gameboard = initDS.return_gameboard(responses[3])  # 2D list
responses[3] = initDS.return_board_size(responses[3])  # converts board size into a tuple of form (cols, rows)
bombs_remaining = int(responses[4])
total_wins, total_losses, total_guesses, avg_win_time, avg_loss_time = 0, 0, 0, 0, 0
win_times = []  # when a win occurs, the total runtime is added here
loss_times = []  # when a loss occurs, the total runtime is added here
guesses = []  # the amount of guesses per game is added here regardless of outcome


# for testing colors
# while True:
#     print(tD.return_tile_type(30))
#     time.sleep(1)


# STEP #3: enter developer mode if necessary
print()
print()
if responses[5] == 'y':
    developerMode.run_developer_mode(gameboard, col_x_coords, row_y_coords, responses[0], responses[1], int(responses[2]), bombs_remaining)
    exit()


# STEP #4: run algorithm repeatedly until user kills the process or until the input number of games are played, and
# write current stats to file after each game ends
# for i in range(int(responses[6])):
#     fullAlgorithm.run_algorithm()
