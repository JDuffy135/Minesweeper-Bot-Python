import time
import pyautogui

import tileDetection as tD


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


# runs the full algorithm from start to finish on the current game board displayed on user's screen
# returns a list with 3 indeces...
# index 0: loss status (0 = win, 1 = loss) -> int
# index 1: total guesses made -> int
# index 2: total elapsed time from start to end -> float
def run_algorithm(gameboard, col_x_coords, row_y_coords, responses) -> list:
    # initializing global variables and data structures
    restart_coords = responses[1]  # format: (x, y)
    zoom_size = int(responses[2])
    # board_size = responses[3]  # format: (cols, rows)
    bombs_remaining = int(responses[4])
    loss_status, total_guesses = 0, 0  # note: if loss_status ever equals 1, the game results in a loss

    unfinished_numbers = []  # holds tuples (cols, rows) for all number tiles with unopened, non-mine tiles around them
    clicks = []  # will hold at least one tuple (cols, rows) representing the tile(s) to be clicked at end of iteration


    # INITIAL STEP: restart board, start timer, click top left tile + update gameboard, update 'unfinished_numbers'
    pyautogui.click(restart_coords[0] + 100, restart_coords[1])  # ensures the browser is clicked before starting
    td.restart(gameboard, col_x_coords, row_y_coords, restart_coords)
    start_time = time.time()
    loss_status = td.click_tile_and_update_gameboard(gameboard, col_x_coords, row_y_coords, zoom_size, 0, 0)
    unfinished_numbers = update_unfinished_numbers(gameboard, col_x_coords, row_y_coords)


    # algorithm runs until unfinished_numbers is empty or until a mine is clicked (return early in this case)
    while len(unfinished_numbers > 0):
        flag = 0

        # 1.) TRIVIAL SEARCH
        # ...


        # 2.) LOCAL SEARCH
        # ...


        # 3.) PROBABILITY ENGINE
        # ...


        # 4.) BEST GUESS


        # 5.) MAKE MOVE
        # ...

    end_time = time.time()
    return [loss_status, total_guesses, end_time - start_time]
