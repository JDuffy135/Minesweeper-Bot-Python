import sys
import time
import pyautogui

import tileDetection as tD
import terminalPrompts
import developerMode
import initializeDataStructures as initDS
import fullAlgorithm

# v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v
# IMPORTANT NOTE: don't run this file directly, as you run the risk of falling into an infinite loop - instead,
# run the program from the file 'launcher.py'
# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^


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
# index 7: WEBSITE (int: 1 is minesweeper.one, 2 is minesweeper.online)


# STEP 2: initialize data structures
col_x_coords = initDS.return_coord_map_cols(int(responses[2]), responses[1], responses[3])  # dict
row_y_coords = initDS.return_coord_map_rows(int(responses[2]), responses[1], responses[3])  # dict
gameboard = initDS.return_gameboard(responses[3])  # 2D list
responses[3] = initDS.return_board_size(responses[3])  # converts board size into a tuple of form (cols, rows)
bombs_remaining = int(responses[4])


# for testing colors
# while True:
#     print(tD.return_tile_type(30))
#     time.sleep(1)


# STEP #3: enter developer mode if necessary
print()
print()
if responses[5] == 'y':
    developerMode.run_developer_mode(gameboard, col_x_coords, row_y_coords, responses[0], responses[1], int(responses[2]), bombs_remaining, int(responses[7]))
    exit()


# STEP #4: run algorithm repeatedly until user kills the process or until the input number of games are played, and
# write current stats to file after each game ends

# metrics
wins = 0
losses = 0
short_losses = 0  # losses that occur in under 15 seconds
long_losses = 0  # losses that occur in over 45 seconds
infinite_loops = 0
times = []
win_times = []
total_moves = 0
total_guesses = 0
total_guess_losses = 0
successful_50_50_guesses = 0
total_50_50_guess_losses = 0
lowest_eff_util_guesses = 0             # guess_type 1 (total guesses)
guess_type_1_losses = 0
corner_guesses = 0                      # guess_type 2 (total guesses)
guess_type_2_losses = 0
random_tile_guesses = 0                 # guess_type 3 (total guesses)
guess_type_3_losses = 0
safest_tile_guesses = 0                 # guess_type 4 (total guesses)
guess_type_4_losses = 0
second_safest_tile_3util_guesses = 0    # guess_type 5 (total guesses)
guess_type_5_losses = 0
second_safest_tile_2util_guesses = 0    # guess_type 6 (total guesses)
guess_type_6_losses = 0
local_search_losses = 0
trivial_search_losses = 0
final_step_losses = 0
total_no_guess_wins = 0

# derived metrics
win_rate = float(0)  # wins / (wins + losses)
average_time = float(0)
average_win_time = float(0)
overall_guess_success_rate = float(0)  # (total_guesses - total_guess_losses) / total_guesses
guess_type_1_success_rate = float(0)  # (lowest_eff_util_guesses - guess_type_1_losses) / lowest_eff_util_guesses
guess_type_2_success_rate = float(0)  # (corner_guesses - guess_type_2_losses) / corner_guesses
guess_type_3_success_rate = float(0)  # (random_tile_guesses - guess_type_3_losses) / random_tile_guesses
guess_type_4_success_rate = float(0)  # (safest_tile_guesses - guess_type_4_losses) / safest_tile_guesses
guess_type_5_success_rate = float(0)  # (second_safest_tile_3util_guesses - guess_type_5_losses) / second_safest_tile_3util_guesses
guess_type_6_success_rate = float(0)  # (second_safest_tile_2util_guesses - guess_type_6_losses) / second_safest_tile_2util_guesses

# running the algorithm...
for i in range(int(responses[6])):
    # RUN ALGORITHM FOR CURRENT GAME
    results = fullAlgorithm.run_algorithm(gameboard, col_x_coords, row_y_coords, responses)

    # PRINTING GAME RESULTS TO CONSOLE
    print("RESULTS OF GAME ",end="")
    print(i, end="")
    print(":")
    print(results)
    print()
    print("ending gameboard...")
    for row in gameboard:
        print(row)
    print()

    # UPDATING METRICS
    # wins & losses
    if results[0] == 1:
        losses = losses + 1
        if results[1] <= 15:
            short_losses = short_losses + 1
        elif results[1] >= 45:
            long_losses = long_losses + 1
    else:
        wins = wins + 1
        win_times.append(results[1])
    # times
    times.append(results[1])
    # total_moves
    total_moves = total_moves + results[2]
    # total_guesses
    total_guesses = total_guesses + results[3]
    # total_no_guess_wins
    if results[3] == 0 and results[0] == 0:
        total_no_guess_wins = total_no_guess_wins + 1
    # lowest_eff_util_guesses
    lowest_eff_util_guesses = lowest_eff_util_guesses + results[4]
    # corner_guesses
    corner_guesses = corner_guesses + results[5]
    # random_tile_guesses
    random_tile_guesses = random_tile_guesses + results[6]
    # safest_tile_guesses
    safest_tile_guesses = safest_tile_guesses + results[7]
    # second_safest_tile_3util_guesses
    second_safest_tile_3util_guesses = second_safest_tile_3util_guesses + results[8]
    # second_safest_tile_2util_guesses
    second_safest_tile_2util_guesses = second_safest_tile_2util_guesses + results[9]
    # updating local_search_losses and trivial_search_losses (should remain at 0)
    last_step = results[11]
    if results[0] == 1 and last_step == 2:
        local_search_losses = local_search_losses + 1
    elif results[0] == 1 and last_step == 1:
        trivial_search_losses = trivial_search_losses + 1
    elif results[0] == 1 and last_step == 0:
        final_step_losses = final_step_losses + 1
    # updating guess type losses if necessary
    last_guess_type = results[10]
    if last_step == 4 and results[0] == 1:
        # in this case, the last move was a guess and we lost
        total_guess_losses = total_guess_losses + 1
        match last_guess_type:
            case 1:
                guess_type_1_losses = guess_type_1_losses + 1
            case 2:
                guess_type_2_losses = guess_type_2_losses + 1
            case 3:
                guess_type_3_losses = guess_type_3_losses + 1
            case 4:
                guess_type_4_losses = guess_type_4_losses + 1
            case 5:
                guess_type_5_losses = guess_type_5_losses + 1
            case 6:
                guess_type_6_losses = guess_type_6_losses + 1
    # update total_50_50_guess_losses if necessary
    if results[12] == 1:
        total_50_50_guess_losses = total_50_50_guess_losses + 1
    # update successful_50_50_guesses
    successful_50_50_guesses = successful_50_50_guesses + results[13]
    # infinite loops
    if results[14] == 1:
        infinite_loops = infinite_loops + 1
    # win rate
    if wins >= 1 and losses == 0:
        win_rate = float(1)
    elif wins == 0 and losses >= 1:
        win_rate = float(0)
    else:
        win_rate = float(wins / (wins + losses))
    # average overall time
    average_time = float(0)
    for t in times:
        average_time = average_time + t
    average_time = float(average_time / len(times))
    # average win time
    average_win_time = 0
    for t in win_times:
        average_win_time = average_win_time + t
    if average_win_time > 0:
        average_win_time = float(average_win_time / len(win_times))
    # overall guess success rate
    if total_guesses == 0:
        overall_guess_success_rate = float(0)
    else:
        overall_guess_success_rate = float((total_guesses - total_guess_losses) / total_guesses)
    # guess type 1 success rate
    if lowest_eff_util_guesses == 0:
        guess_type_1_success_rate = float(0)
    else:
        guess_type_1_success_rate = float((lowest_eff_util_guesses - guess_type_1_losses) / lowest_eff_util_guesses)
    # guess type 2 success rate
    if corner_guesses == 0:
        guess_type_2_success_rate = float(0)
    else:
        guess_type_2_success_rate = float((corner_guesses - guess_type_2_losses) / corner_guesses)
    # guess type 3 success rate
    if random_tile_guesses == 0:
        guess_type_3_success_rate = float(0)
    else:
        guess_type_3_success_rate = float((random_tile_guesses - guess_type_3_losses) / random_tile_guesses)
    # guess type 4 success rate
    if safest_tile_guesses == 0:
        guess_type_4_success_rate = float(0)
    else:
        guess_type_4_success_rate = float((safest_tile_guesses - guess_type_4_losses) / safest_tile_guesses)
    # guess type 5 success rate
    if second_safest_tile_3util_guesses == 0:
        guess_type_5_success_rate = float(0)
    else:
        guess_type_5_success_rate = float((second_safest_tile_3util_guesses - guess_type_5_losses) / second_safest_tile_3util_guesses)
    # guess type 6 success rate
    if second_safest_tile_2util_guesses == 0:
        guess_type_6_success_rate = float(0)
    else:
        guess_type_6_success_rate = float((second_safest_tile_2util_guesses - guess_type_6_losses) / second_safest_tile_2util_guesses)

    # OUTPUT METRICS TO FILE (metrics.txt)
    file = open("metrics.txt", "w")
    file.write("")
    file.close()
    file = open("metrics.txt", "a")
    file.write("CURRENT METRICS AFTER ")
    file.write(str(i + 1))
    file.write(" GAMES:\n")
    file.write("\n")
    # win_rate
    file.write("Win Rate: ")
    file.write(str(win_rate))
    file.write("   [after ")
    file.write(str(wins))
    file.write(" wins and ")
    file.write(str(losses))
    file.write(" losses]\n")
    # short_losses
    file.write("Losses Occurring In <= 15 Seconds: ")
    file.write(str(short_losses))
    file.write("\n")
    # long_losses
    file.write("Losses Occurring In >= 45 Seconds: ")
    file.write(str(long_losses))
    file.write("\n")
    # infinite_loops
    file.write("Infinite Loops: ")
    file.write(str(infinite_loops))
    file.write("\n")
    # total_no_guess_wins
    file.write("Total No-Guess Wins: ")
    file.write(str(total_no_guess_wins))
    file.write("\n")
    # total_50_50_guess_losses
    file.write("Total 50-50 Guess Losses: ")
    file.write(str(total_50_50_guess_losses))
    file.write("\n")
    # successful_50_50_guesses
    file.write("Total Successful 50-50 Guesses: ")
    file.write(str(successful_50_50_guesses))
    file.write("\n")
    # trivial_search_losses
    file.write("Trivial Search Losses: ")
    file.write(str(trivial_search_losses))
    file.write("\n")
    # local_search_losses
    file.write("Local Search Losses: ")
    file.write(str(local_search_losses))
    file.write("\n")
    # final_step_losses
    file.write("Final Step Losses: ")
    file.write(str(final_step_losses))
    file.write("\n")
    # average_time
    file.write("Average Time: ")
    file.write(str(average_time))
    file.write("\n")
    # average_win_time
    file.write("Average Win Time: ")
    file.write(str(average_win_time))
    file.write("\n")
    # overall_guess_success_rate
    file.write("Guess Success Rate (overall): ")
    file.write(str(overall_guess_success_rate))
    file.write("   [after ")
    file.write(str(total_guesses))
    file.write(" guesses]\n")
    # guess_type_1_success_rate
    file.write("Guess Type 1 Success Rate: ")
    file.write(str(guess_type_1_success_rate))
    file.write("   [after ")
    file.write(str(lowest_eff_util_guesses))
    file.write(" guesses]\n")
    # guess_type_2_success_rate
    file.write("Guess Type 2 Success Rate: ")
    file.write(str(guess_type_2_success_rate))
    file.write("   [after ")
    file.write(str(corner_guesses))
    file.write(" guesses]\n")
    # guess_type_3_success_rate
    file.write("Guess Type 3 Success Rate: ")
    file.write(str(guess_type_3_success_rate))
    file.write("   [after ")
    file.write(str(random_tile_guesses))
    file.write(" guesses]\n")
    # guess_type_4_success_rate
    file.write("Guess Type 4 Success Rate: ")
    file.write(str(guess_type_4_success_rate))
    file.write("   [after ")
    file.write(str(safest_tile_guesses))
    file.write(" guesses]\n")
    # guess_type_5_success_rate
    file.write("Guess Type 5 Success Rate: ")
    file.write(str(guess_type_5_success_rate))
    file.write("   [after ")
    file.write(str(second_safest_tile_3util_guesses))
    file.write(" guesses]\n")
    # guess_type_6_success_rate
    file.write("Guess Type 6 Success Rate: ")
    file.write(str(guess_type_6_success_rate))
    file.write("   [after ")
    file.write(str(second_safest_tile_2util_guesses))
    file.write(" guesses]\n")
    file.close()
