import pyautogui

import tileDetection as tD
import trivialSearch as triv
import localSearch as loc
# import probabilityEngine as prob
import fullAlgorithm


# when use enters 'help' command
def print_command_list() -> None:
    print("List of commands...")
    print("   * 'q': terminates program")
    print("   * 'help': prints command list")
    print("   1.) 'ct <col_#> <row_#>': clicks the specified tile and updates gameboard accordingly")
    print("   2.) 'dt <col_#> <row_#>': detects the tile type of the specified tile without updating gameboard")
    print("   3.) 'pb': prints gameboard as it is currently represented in memory")
    print("   4.) 'rs': clicks the restart button and clears gameboard in memory")
    print("   5.) 'un': returns unfinished numbers list for current gameboard setup")
    print("   6.) 'triv': runs trivial search on the current board")
    print("   7.) 'loc': runs local search on the current board")
    print("   8.) 'prob': runs the probability engine on the current board")
    return


# when user enters 'ct' command
def click_tile(gameboard, col_x_coords, row_y_coords, zoom_size, col_num, row_num, single_click:bool) -> None:
    if single_click == False:
        pyautogui.doubleClick(col_x_coords.get(col_num), row_y_coords.get(row_num))
    else:
        pyautogui.click(col_x_coords.get(col_num), row_y_coords.get(row_num))
    tD.update_tiles_dev_mode(gameboard, col_x_coords, row_y_coords, col_num, row_num, zoom_size)
    return


# when user enters 'dt' command
def detect_tile(gameboard, col_x_coords, row_y_coords, zoom_size, col_num, row_num) -> None:
    pyautogui.moveTo(col_x_coords.get(col_num), row_y_coords.get(row_num))
    print(tD.return_tile_type(zoom_size))
    return


# when user enters 'pb' command
def print_board(gameboard, col_x_coords, row_y_coords) -> None:
    for i in range(len(row_y_coords)):
        print(gameboard[i])
    return


# when user enters 'rs' command
def restart(gameboard, col_x_coords, row_y_coords, restart_coords) -> None:
    for i in range(len(row_y_coords)):
        for j in range(len(col_x_coords)):
            gameboard[i][j] = -1
    pyautogui.doubleClick(restart_coords[0], restart_coords[1])
    return


# when user enters 'triv' command
def trivial_search_dev(gameboard, col_x_coords, row_y_coords, zoom_size) -> None:
    # print board before running trivial search
    print("gameboard BEFORE running trivial search...")
    print_board(gameboard, col_x_coords, row_y_coords)
    print()
    # get unfinished_numbers list
    unfinished_numbers = fullAlgorithm.update_unfinished_numbers(gameboard, col_x_coords, row_y_coords)
    # run trivial search
    results = triv.trivial_search(gameboard, col_x_coords, row_y_coords, unfinished_numbers)
    print("results of trivial search: ", end="")
    print(results)
    print()
    print("   ^^ format is [ #_of_mines_placed, [tiles_clicked] ]")
    print()
    # click the tiles which were found to be safe (if any)
    if len(results[1]) > 0:
        for tile in results[1]:
            click_tile(gameboard, col_x_coords, row_y_coords, zoom_size, tile[0], tile[1], False)
    # print board before running trivial search
    print("gameboard AFTER running trivial search...")
    print_board(gameboard, col_x_coords, row_y_coords)
    print()

    return


# when user enters 'loc' command
def local_search_dev(gameboard, col_x_coords, row_y_coords, zoom_size, initial_bomb_count) -> None:
    # print board before running local search
    print("gameboard BEFORE running local search...")
    print_board(gameboard, col_x_coords, row_y_coords)
    print()
    # get unfinished_numbers list
    unfinished_numbers = fullAlgorithm.update_unfinished_numbers(gameboard, col_x_coords, row_y_coords)
    # find remaining bombs
    bombs_remaining = initial_bomb_count
    for c in range(len(col_x_coords)):
        for r in range(len(row_y_coords)):
            if gameboard[r][c] == 9:
                bombs_remaining = bombs_remaining - 1
    # run local search
    print("bombs remaining before local search: ", end="")
    print(bombs_remaining)
    results = loc.local_search(gameboard, col_x_coords, row_y_coords, unfinished_numbers, bombs_remaining)
    print("number of aggregations: ",end="")
    print(len(results[2]))
    print("aggregations...")
    for i in range(len(results[2])):
        print("length is ", end="")
        print(len(results[2][i]), end="")
        print(": ", end="")
        print(results[2][i])
    print()
    print("number of valid mine combinations for each aggregation...")
    for i in range(len(results[2])):
        print(len(results[3][i]))
    print()
    print("results of local search: ", end="")
    print(results)
    print()
    print("   ^^ format is [ #_of_mines_placed, [tiles_clicked], [[border_tile_aggregations]], [[[valid_mine_combinations_per_aggregation]]] ]")
    print()
    # click the tiles which were found to be safe (if any)
    if len(results[1]) > 0:
        for tile in results[1]:
            click_tile(gameboard, col_x_coords, row_y_coords, zoom_size, tile[0], tile[1], False)
    # print board before running local search
    print("gameboard AFTER running local search...")
    print_board(gameboard, col_x_coords, row_y_coords)
    print()

    return


# when user enters 'prob' command
def probability_engine_dev(gameboard, col_x_coords, row_y_coords, restart_coords) -> None:
    return

def run_developer_mode(gameboard, col_x_coords, row_y_coords, restart_coords, first_tile_coords, zoom_size, bombs_remaining) -> None:
    print("DEVELOPER MODE ACTIVATED: enter 'q' or press escape to terminate program")
    print()

    user_input = ''
    while user_input != 'q':
        print("enter a command (enter 'help' for command list): ", end="")
        user_input = input()
        inputs = user_input.split()  # splits user_input by spaces to differentiate between command and parameters
        match inputs[0]:
            case 'help':
                print_command_list()
            case 'ct':
                click_tile(gameboard, col_x_coords, row_y_coords, zoom_size, int(inputs[1]), int(inputs[2]), False)
            case 'dt':
                detect_tile(gameboard, col_x_coords, row_y_coords, zoom_size, int(inputs[1]), int(inputs[2]))
            case 'pb':
                print_board(gameboard, col_x_coords, row_y_coords)
            case 'rs':
                restart(gameboard, col_x_coords, row_y_coords, restart_coords)
            case 'un':
                print(fullAlgorithm.update_unfinished_numbers(gameboard, col_x_coords, row_y_coords))
            case 'triv':
                trivial_search_dev(gameboard, col_x_coords, row_y_coords, zoom_size)
            case 'loc':
                local_search_dev(gameboard, col_x_coords, row_y_coords, zoom_size, bombs_remaining)
            case 'prob':
                print("PLACEHOLDER")

    return
