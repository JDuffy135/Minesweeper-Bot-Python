import pyautogui

import tileDetection as tD


# when use enters 'help' command
def print_command_list() -> None:
    print("List of commands...")
    print("   * 'q': terminates program")
    print("   * 'help': prints command list")
    print("   1.) 'ct <col_#> <row_#>': clicks the specified tile and updates gameboard accordingly")
    print("   2.) 'dt <col_#> <row_#>': detects the tile type of the specified tile without clicking")
    print("   3.) 'pb': prints gameboard as it is currently represented in memory")
    print("   4.) 'rs': clicks the restart button and clears gameboard in memory")
    return


# when user enters 'ct' command
def click_tile(gameboard, col_x_coords, row_y_coords, zoom_size, col_num, row_num) -> None:
    pyautogui.doubleClick(col_x_coords.get(col_num), row_y_coords.get(row_num))
    tD.update_tiles(gameboard, col_x_coords, row_y_coords, col_num, row_num, zoom_size)
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
def restart(gameboard, col_x_coords, row_y_coords, restart_coords):
    for i in range(len(row_y_coords)):
        for j in range(len(col_x_coords)):
            gameboard[i][j] = -1
    pyautogui.doubleClick(restart_coords[0], restart_coords[1])
    return

def run_developer_mode(gameboard, col_x_coords, row_y_coords, restart_coords, first_tile_coords, zoom_size) -> None:
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
                click_tile(gameboard, col_x_coords, row_y_coords, zoom_size, int(inputs[1]), int(inputs[2]))
            case 'dt':
                detect_tile(gameboard, col_x_coords, row_y_coords, zoom_size, int(inputs[1]), int(inputs[2]))
            case 'pb':
                print_board(gameboard, col_x_coords, row_y_coords)
            case 'rs':
                restart(gameboard, col_x_coords, row_y_coords, restart_coords)

    return
