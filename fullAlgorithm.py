import time
import pyautogui

import newTileDetection as td
import trivialSearch as TS
import localSearch as LS
import probabilityEngine as PE
import bestGuess as BG


# returns list of number tiles which have at least 1 unrevealed tile not marked as a mine in it's surrounding area
def update_unfinished_numbers(gameboard, col_x_coords, row_y_coords) -> list[tuple]:
    unfinished_numbers = []
    for r in range(len(row_y_coords)):
        for c in range(len(col_x_coords)):
            if gameboard[r][c] <= 0 or gameboard[r][c] > 8:
                continue
            flag = 0
            # if tile is a number tile, we check all adjacent tiles to see if it should be added to the list
            for x in range(c-1, c+2):
                if flag == 1:
                    break
                for y in range(r-1, r+2):
                    if (x >= 0 and x < len(col_x_coords)) and (y >= 0 and y < len(row_y_coords)):
                        if gameboard[y][x] == -1:
                            unfinished_numbers.append((c, r))
                            flag = 1
                            break
    # print(len(unfinished_numbers))
    return unfinished_numbers


# runs the full algorithm from start to finish on the current game board displayed on user's screen and returns a
# list of metrics
def run_algorithm(gameboard, col_x_coords, row_y_coords, responses) -> list:
    # initializing variables from responses list
    restart_coords = responses[0]  # format: (x, y)
    zoom_size = int(responses[2])
    bombs_remaining = int(responses[4])
    site = responses[7]

    # metrics
    loss_status = 0  # note: if loss_status ever equals 1, the game results in a loss
    last_step = -1  # tracks which step of the aglorithm last fired before making the last move
    total_moves = 0
    total_guesses = 0
    # types of guesses
    lowest_eff_util_guesses = 0             # guess_type 1
    corner_guesses = 0                      # guess_type 2
    random_tile_guesses = 0                 # guess_type 3
    safest_tile_guesses = 0                 # guess_type 4
    second_safest_tile_3util_guesses = 0    # guess_type 5
    second_safest_tile_2util_guesses = 0    # guess_type 6
    last_guess_type = 0  # tracks the last guess type that was made


    # INITIAL STEP: restart board, click first tile, and update gameboard
    time.sleep(1)
    pyautogui.click(restart_coords[0], restart_coords[1] - 50)  # ensures the browser is clicked before starting
    td.restart(gameboard, col_x_coords, row_y_coords, restart_coords)
    time.sleep(0.25)
    if site == 2:
        # minesweeper.online
        loss_status = td.click_tile_and_update_board(gameboard, col_x_coords, row_y_coords, zoom_size, (0, 0), site)
    else:
        # minesweeper.one
        loss_status = td.click_tile_and_update_board(gameboard, col_x_coords, row_y_coords, zoom_size, (2, 2), site)


    # THE AGLORITHM...
    # note: loop runs until either 1.) unfinished_numbers is empty or 2.) a mine is clicked (return early in this case)
    start_time = time.time()
    unfinished_numbers = [(-1, -1)]  # this is only here so the while loop executes the first time
    while len(unfinished_numbers) > 0:
        print("NEW ITERATION")
        # initialize variables
        flag = 0  # set to 1 whenever a move is made (AKA when a mine is placed and/or a tile is clicked)
        last_step = -1
        click_tiles = []  # tiles that will be clicked at the end of the current iteration
        unfinished_numbers = update_unfinished_numbers(gameboard, col_x_coords, row_y_coords)
        if len(unfinished_numbers) == 0:
            break
        # print("unfinished_numbers: ", end="")  # for testing
        # print(unfinished_numbers)  # for testing


        # 1.) TRIVIAL SEARCH
        TS_RESULT = TS.trivial_search(gameboard, col_x_coords, row_y_coords, unfinished_numbers)
        # print("TS_RESULT: ", end="")  # for testing
        # print(TS_RESULT)  # for testing
        if TS_RESULT[0] != 0 or len(TS_RESULT[1]) > 0:
            bombs_remaining = bombs_remaining - TS_RESULT[0]
            click_tiles.extend(TS_RESULT[1])
            last_step = 1
            flag = 1


        # 2.) LOCAL SEARCH
        LS_RESULT =[0, [], [], []]
        aggregations = []
        mine_combinations = []
        if flag == 0:
            LS_RESULT = LS.local_search(gameboard, col_x_coords, row_y_coords, unfinished_numbers, bombs_remaining)
            # print("LS_RESULT: ", end="")  # for testing
            # print(LS_RESULT)  # for testing
            if LS_RESULT[0] != 0 or len(LS_RESULT[1]) > 0:
                bombs_remaining = bombs_remaining - LS_RESULT[0]
                click_tiles.extend(LS_RESULT[1])
                last_step = 2
                flag = 1
            else:
                aggregations = LS_RESULT[2]
                mine_combinations = LS_RESULT[3]


        # 3.) PROBABILITY ENGINE
        potential_clicks = []
        if flag == 0:
            potential_clicks = PE.probabilityEngine(gameboard, col_x_coords, row_y_coords, aggregations, mine_combinations, unfinished_numbers)
            print("potential_clicks: ", end="")  # for testing
            print(potential_clicks)  # for testing


        # 4.) BEST GUESS
        if flag == 0:
            BG_RESULT = BG.best_guess(gameboard, col_x_coords, row_y_coords, potential_clicks, aggregations, unfinished_numbers, bombs_remaining)
            print()  # for testing
            print("best_guess: ", end="")  # for testing
            print(BG_RESULT[0])  # for testing
            print()  # for testing
            last_step = 4
            click_tiles.append(BG_RESULT[0])
            last_guess_type = BG_RESULT[1]
            # update proper guess metrics
            total_guesses = total_guesses + 1
            match last_guess_type:
                case 1:
                    lowest_eff_util_guesses = lowest_eff_util_guesses + 1
                case 2:
                    corner_guesses = corner_guesses + 1
                case 3:
                    random_tile_guesses = random_tile_guesses + 1
                case 4:
                    safest_tile_guesses = safest_tile_guesses + 1
                case 5:
                    second_safest_tile_3util_guesses = second_safest_tile_3util_guesses + 1
                case 6:
                    second_safest_tile_2util_guesses = second_safest_tile_2util_guesses + 1


        # 5.) MAKE MOVE
        total_moves = total_moves + 1
        for tile in click_tiles:
            loss_status = td.click_tile_and_update_board(gameboard, col_x_coords, row_y_coords, zoom_size, tile, site)
            if loss_status == 1:
                break
        # break out of the while loop and terminate the algorithm for the current game by returning
        if loss_status == 1:
            break


    end_time = time.time()
    return [
        loss_status,
        end_time - start_time,
        total_moves,
        total_guesses,
        lowest_eff_util_guesses,
        corner_guesses,
        random_tile_guesses,
        safest_tile_guesses,
        second_safest_tile_3util_guesses,
        second_safest_tile_2util_guesses,
        last_guess_type,
        last_step
    ]
