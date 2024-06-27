import pyautogui
import time  # for testing


# returns a screenshot of the entire board (tiles only)
def screenshot_board(zoom_size: int, col_x_coords: dict, row_y_coords: dict):
    width = (zoom_size * len(col_x_coords)) + 10
    height = (zoom_size * len(row_y_coords)) + 10
    origin_x_coord = col_x_coords.get(0)
    origin_y_coord = row_y_coords.get(0)

    screenshot = pyautogui.screenshot(region=(origin_x_coord - int(zoom_size / 2) - 8, origin_y_coord - int(zoom_size / 2) - 8, width, height))
    return screenshot


# returns the tile type of the tile at position (col, row) given a screenshot of the entire board
# -1 is a closed space, 0 is an open space, 1 - 8 are the number tiles, and 9 is a bomb
# if the function returns -2, then none of the known tiles were detected
def return_tile_type(zoom_size: int, col_x_coords: dict, row_y_coords: dict, screenshot, tile: tuple[int, int], site: int) -> int:
    # obtaining pixel colors of given tile
    margin = int(zoom_size / 5) + 1
    offset = int(margin / 2)
    col = tile[0]
    row = tile[1]

    tile_colors = set()
    x_start = int(zoom_size / 2) + (col * zoom_size) - offset
    x_end = x_start + margin
    y_start = int(zoom_size / 2) + (row * zoom_size) - offset
    y_end = y_start + margin
    for x in range(x_start, x_end + 1):
        for y in range(y_start, y_end + 1):
            cur_pixel_color = screenshot.getpixel((x, y))
            tile_colors.add(cur_pixel_color)

    tile_type = -2
    if site == 2:  # tile detection for minesweeper.online
        # checking if a bomb is detected at the given tile coordinate
        for color in tile_colors:
            if (color[0] > 0 and color[1] > 0 and color[2] > 0) and (color[0] < 26 and color[1] < 26 and color[2] < 26):
                return 9
        # now checking for numbers 1 - 8
        for color in tile_colors:
            match color:
                case (0, 13, 248, 255):
                    return 1
                case (0, 12, 239, 255):
                    return 1
                case (0, 116, 22, 255):
                    return 2
                case (0, 107, 20, 255):
                    return 2
                case (255, 7, 27, 255):
                    return 3
                case (245, 6, 24, 255):
                    return 3
                case (0, 6, 114, 255):
                    return 4
                case (123, 3, 12, 255):
                    return 5
                case (0, 117, 116, 255):
                    return 6
                case (0, 0, 0, 255):
                    return 7
                case (117, 117, 117, 255):
                    return 8
                case (123, 123, 123, 255):
                    return 8
                case(146, 146, 146, 255):
                    return 8
        # if not a number or bomb, we must distinguish between an open or closed space by checking the colors
        # near the top of the given tile (to see if pure white is present)
        if (191, 191, 191, 255) in tile_colors and len(tile_colors) < 3:
            new_colors = set()
            x_start = int(zoom_size / 2) + (col * zoom_size) - offset
            x_end = x_start + margin
            y_start = (row * zoom_size) - offset + int(margin/2)
            y_end = y_start + margin
            for x in range(x_start, x_end + 1):
                for y in range(y_start, y_end + 1):
                    cur_pixel_color = screenshot.getpixel((x, y))
                    new_colors.add(cur_pixel_color)
            # print("new colors: ", end="")  # for testing
            # print(new_colors)  # for testing
            if (255, 255, 255, 255) in new_colors:
                return -1
            else:
                return 0
    else:  # tile detection for minesweeper.one
        # checking if a bomb is detected at the given tile coordinate
        for color in tile_colors:
            if color == (16, 16, 16, 255):
                return 9
        # for color in tile_colors:
        #     if (color[0] > 0 and color[1] > 0 and color[2] > 0) and (color[0] < 20 and color[1] < 20 and color[2] < 20):
        #         return 9
        # checking for number 8
        for color in tile_colors:
            if (color[0] >= 100 and color[1] >= 100 and color[2] >= 100) and (color[0] <= 130 and color[1] <= 130 and color[2] <= 130) and (color[0] == color[1] and color[0] == color[2]):
                return 8
        # now checking for numbers 1 - 7
        for color in tile_colors:
            match color:
                case (34, 45, 235, 255):
                    return 1
                case (79, 87, 219, 255):
                    return 1
                case (0, 111, 21, 255):
                    return 2
                case (11, 115, 31):
                    return 2
                case (255, 7, 27, 255):
                    return 3
                case (236, 51, 66, 255):
                    return 3
                case (0, 6, 109, 255):
                    return 4
                case (34, 39, 123, 255):
                    return 4
                case (117, 3, 12, 255):
                    return 5
                case (0, 112, 111, 255):
                    return 6
                case (45, 129, 128, 255):
                    return 6
                case (0, 0, 0, 255):
                    return 7
        # if not a number or bomb, we must distinguish between an open or closed space by checking the colors
        # near the top of the given tile (to see if pure white is present)
        if (181, 181, 181, 255) in tile_colors and len(tile_colors) < 3:
            new_colors = set()
            x_start = int(zoom_size / 2) + (col * zoom_size) - offset
            x_end = x_start + margin
            y_start = (row * zoom_size) - offset + int(margin / 2)
            y_end = y_start + margin
            for x in range(x_start, x_end + 1):
                for y in range(y_start, y_end + 1):
                    cur_pixel_color = screenshot.getpixel((x, y))
                    new_colors.add(cur_pixel_color)
            # print("new colors: ", end="")  # for testing
            # print(new_colors)  # for testing
            if (255, 255, 255, 255) in new_colors:
                return -1
            else:
                return 0


    return tile_type


# optimized version of my original BFS algorithm (uses less pyautogui function calls - roughly 25% faster on average)
def bfs(gameboard, col_x_coords, row_y_coords, tile, zoom_size, screenshot, site) -> None:
    # overall_start_time = time.time()  # for testing

    col_num = tile[0]
    row_num = tile[1]
    queue = [(col_num, row_num)]
    visited = []
    while len(queue) > 0:
        # start = time.time()  # for testing

        # returns and deletes first element (tuple) in queue
        cur_tile = queue.pop(0)
        visited.append(cur_tile)

        # checks current tile type and updates gameboard (or skips to next item in queue if tile is a number)
        cur_tile_type = return_tile_type(zoom_size, col_x_coords, row_y_coords, screenshot, cur_tile, site)
        if cur_tile_type <= 0:
            gameboard[cur_tile[1]][cur_tile[0]] = cur_tile_type
        else:
            gameboard[cur_tile[1]][cur_tile[0]] = cur_tile_type
            continue

        # adds 8 adjacent neighbors to queue if they are 1.) within the range of the board size, 2.) not already in
        # the queue, and 3.) not already in visited
        if (cur_tile[0] - 1 >= 0) and ((cur_tile[0] - 1, cur_tile[1]) not in queue and (cur_tile[0] - 1, cur_tile[1]) not in visited):
            queue.append((cur_tile[0] - 1, cur_tile[1]))
        if (cur_tile[0] + 1 < len(col_x_coords)) and ((cur_tile[0] + 1, cur_tile[1]) not in queue and (cur_tile[0] + 1, cur_tile[1]) not in visited):
            # note: col_x_coords.len() gives us the number of columns
            queue.append((cur_tile[0] + 1, cur_tile[1]))
        if (cur_tile[1] - 1 >= 0) and ((cur_tile[0], cur_tile[1] - 1) not in queue and (cur_tile[0], cur_tile[1] - 1) not in visited):
            queue.append((cur_tile[0], cur_tile[1] - 1))
        if (cur_tile[1] + 1 < len(row_y_coords)) and ((cur_tile[0], cur_tile[1] + 1) not in queue and (cur_tile[0], cur_tile[1] + 1) not in visited):
            # note: row_y_coords.len() gives us the number of rows
            queue.append((cur_tile[0], cur_tile[1] + 1))

        if (cur_tile[0] - 1 >= 0 and cur_tile[1] - 1 >= 0) and ((cur_tile[0] - 1, cur_tile[1] - 1) not in queue and (cur_tile[0] - 1, cur_tile[1] - 1) not in visited):
            queue.append((cur_tile[0] - 1, cur_tile[1] - 1))
        if (cur_tile[0] + 1 < len(col_x_coords) and cur_tile[1] - 1 >= 0) and ((cur_tile[0] + 1, cur_tile[1] - 1) not in queue and (cur_tile[0] + 1, cur_tile[1] - 1) not in visited):
            # note: col_x_coords.len() gives us the number of columns
            queue.append((cur_tile[0] + 1, cur_tile[1] - 1))
        if (cur_tile[0] - 1 >= 0 and cur_tile[1] + 1 < len(row_y_coords)) and ((cur_tile[0] - 1, cur_tile[1] + 1) not in queue and (cur_tile[0] - 1, cur_tile[1] + 1) not in visited):
            queue.append((cur_tile[0] - 1, cur_tile[1] + 1))
        if (cur_tile[0] + 1 < len(col_x_coords) and cur_tile[1] + 1 < len(row_y_coords)) and ((cur_tile[0] + 1, cur_tile[1] + 1) not in queue and (cur_tile[0] + 1, cur_tile[1] + 1) not in visited):
            # note: row_y_coords.len() gives us the number of rows
            queue.append((cur_tile[0] + 1, cur_tile[1] + 1))
        # end = time.time()  # for testing
        # print(end - start)  # for testing

    # overall_end_time = time.time()  # for testing
    # print(overall_end_time - overall_start_time)  # for testing
    # print("Tiles visited:", end="")  # for testing
    # print(len(visited))
    return


# update gameboard depending on tile type
def update_tiles_dev_mode(gameboard, col_x_coords, row_y_coords, tile, zoom_size, screenshot, site) -> None:
    col_num = tile[0]
    row_num = tile[1]
    val = return_tile_type(zoom_size, col_x_coords, row_y_coords, screenshot, tile, site)
    if val == 0:
        # if current tile is an open space, we use bfs to update all tiles in the surrounding area
        bfs(gameboard, col_x_coords, row_y_coords, tile, zoom_size, screenshot, site)
    elif val != -2:
        # if current tile is not an open space, we update only one tile
        gameboard[row_num][col_num] = val
    return


# update gameboard depending on tile type + returns 1 if the tile is a mine (game ends), returns 0 otherwise
def update_tiles(gameboard, col_x_coords, row_y_coords, tile, zoom_size, screenshot, site) -> int:
    col_num = tile[0]
    row_num = tile[1]
    val = return_tile_type(zoom_size, col_x_coords, row_y_coords, screenshot, tile, site)
    if val == 0:
        # if current tile is an open space, we use bfs to scan all tiles in the surrounding area
        bfs(gameboard, col_x_coords, row_y_coords, tile, zoom_size, screenshot, site)
    elif val != -2:
        # if current tile is not an open space, we scan only one tile (and we return 1 if a mine is uncovered)
        if val == 9:
            return 1
        gameboard[row_num][col_num] = val
    return 0


# clicks specified tile and updates gameboard respectively, plus returns a 1 if a mine is clicked (0 otherwise)
def click_tile_and_update_board(gameboard, col_x_coords, row_y_coords, zoom_size, tile, screenshot, site) -> int:
    col_num = tile[0]
    row_num = tile[1]
    pyautogui.click(col_x_coords.get(col_num), row_y_coords.get(row_num))
    loss_status = update_tiles(gameboard, col_x_coords, row_y_coords, tile, zoom_size, screenshot, site)
    return loss_status


# restarts game and clear gameboard
def restart(gameboard, col_x_coords, row_y_coords, restart_coords) -> None:
    for i in range(len(row_y_coords)):
        for j in range(len(col_x_coords)):
            gameboard[i][j] = -1
    pyautogui.click(restart_coords[0], restart_coords[1])
    return



# FOR TESTING
# origin_x_coord = 319  # x-coordinate of top left corner tile
# origin_y_coord = -669  # y-coordinate of top left corner tile
# zoom_size = 30
#
# col_x_coords = {}
# for i in range(30):
#     col_x_coords[i] = origin_x_coord + (i * 30)
#
# row_y_coords = {}
# for i in range(16):
#     row_y_coords[i] = origin_y_coord + (i * 16)
#
# # testing new tile detection with screenshot of entire board
# image = screenshot_board(zoom_size, col_x_coords, row_y_coords)
# print(image.save(r"/Users/jakeduffy/Desktop/thingy.png"))
# start = time.time()
#
# print(return_tile_type(zoom_size, col_x_coords, row_y_coords, image, (1, 1)))
#
#
# # # checking if a specific color appears on the board at all
# # all_colors = image.getcolors(9000)
# # color_list = set()
# # for item in all_colors:
# #     if item not in color_list:
# #         color_list.add(item[1])
# # print(color_list)
# # print((0, 107, 20, 255) in color_list)
# # print()
# #
# #
# # # checking if a particular tile contains a particular color
# # tile = (5, 1)  # (col, row)
# # tile_colors = set()
# # margin = int(zoom_size / 5) + 1
# # offset = int(margin / 3)
# # x_start = int(zoom_size/2) + (tile[0] * zoom_size) - offset
# # x_end = x_start + margin
# # y_start = int(zoom_size/2) + (tile[1] * zoom_size) - offset
# # y_end = y_start + margin
# # for x in range(x_start, x_end + 1):
# #     for y in range(y_start, y_end + 1):
# #         cur_pixel_color = image.getpixel((x, y))
# #         tile_colors.add(cur_pixel_color)
# # print(tile_colors)
#
# print(time.time() - start)
