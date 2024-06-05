import pyautogui
import time  # for testing


# returns the type of tile the mouse is currently hovering over
# -1 is a closed space, 0 is an open space, 1 - 8 are the number tiles, and 9 is a bomb
# if the function returns -2, then none of the known tiles were detected
def return_tile_type(zoom_size: int) -> int:
    # for testing
    # start_time = time.time()

    # obtaining pixel colors near current mouse position
    margin = int(zoom_size / 5)
    offset = int(margin / 3)
    x, y = pyautogui.position()
    pixels = pyautogui.screenshot(region=(x - offset, y - offset, margin, margin))
    colors = pixels.getcolors()

    # iterating through pixel colors to find if tile is a number from 1-8 or a bomb
    tile_type = -2
    for color in colors:
        tup = color[1]
        if (tup[0] > 0 and tup[1] > 0 and tup[2] > 0) and (tup[0] < 26 and tup[1] < 26 and tup[2] < 26):
            return 9
        match tup:
            case (0, 13, 248, 255):
                # end_time = time.time()
                # print(end_time - start_time)
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

    # if not a number or bomb, we must distinguish between an open or closed space
    if (margin * margin, (191, 191, 191, 255)) in colors:
        pixels = pyautogui.screenshot(region=(x, y - int(zoom_size / 1.5), 1, margin * 2))
        # NOTE: if I come back to optimize this, the above line of code ^^ takes about 0.06 seconds to execute,
        # which accounts for roughly half of the execution time of this function when it runs from start to end
        new_colors = pixels.getcolors()
        for color in new_colors:
            if color[1] == (255, 255, 255, 255):
                return -1
        return 0

    return tile_type


# performs bfs algorithm to update board surrounding an open tile
# NOTE: the function titled 'update_tiles_bfs2' is used instead - this is the original, unoptimized code
# def update_tiles_bfs(gameboard, col_x_coords, row_y_coords, col_num, row_num, zoom_size) -> None:
#     # for testing
#     overall_start_time = time.time()
#
#     queue = [(col_num, row_num)]
#     visited = []
#     while len(queue) > 0:
#         # for testing
#         start = time.time()
#
#         # returns and deletes first element (tuple) in queue
#         cur_tile = queue.pop(0)
#         visited.append(cur_tile)
#
#         # checks current tile type and updates gameboard (or skips to next item in queue if closed tile)
#         pyautogui.moveTo(col_x_coords.get(cur_tile[0]), row_y_coords.get(cur_tile[1]))
#         cur_tile_type = return_tile_type(zoom_size)
#         if cur_tile_type >= 0:
#             gameboard[cur_tile[1]][cur_tile[0]] = cur_tile_type
#         else:
#             end = time.time()
#             print(end - start)
#             continue
#
#         # adds 4 adjacent neighbors to queue if they are 1.) within the range of the board size, 2.) not already in
#         # the queue, and 3.) and already visited
#         if (cur_tile[0] - 1 >= 0) and ((cur_tile[0] - 1, cur_tile[1]) not in queue and (cur_tile[0] - 1, cur_tile[1]) not in visited):
#             queue.append((cur_tile[0] - 1, cur_tile[1]))
#         if (cur_tile[0] + 1 < len(col_x_coords)) and ((cur_tile[0] + 1, cur_tile[1]) not in queue and (cur_tile[0] + 1, cur_tile[1]) not in visited):
#             # note: col_x_coords.len() gives us the number of columns
#             queue.append((cur_tile[0] + 1, cur_tile[1]))
#         if (cur_tile[1] - 1 >= 0) and ((cur_tile[0], cur_tile[1] - 1) not in queue and (cur_tile[0], cur_tile[1] - 1) not in visited):
#             queue.append((cur_tile[0], cur_tile[1] - 1))
#         if (cur_tile[1] + 1 < len(row_y_coords)) and ((cur_tile[0], cur_tile[1] + 1) not in queue and (cur_tile[0], cur_tile[1] + 1) not in visited):
#             # note: row_y_coords.len() gives us the number of rows
#             queue.append((cur_tile[0], cur_tile[1] + 1))
#         end = time.time()
#         print(end - start)
#
#     overall_end_time = time.time()
#     print(overall_end_time - overall_start_time)
#     print("Tiles visited:", end="")
#     print(len(visited))
#     return


# optimized version of my original BFS algorithm (uses less pyautogui function calls - roughly 25% faster on average)
def update_tiles_bfs2(gameboard, col_x_coords, row_y_coords, col_num, row_num, zoom_size) -> None:
    # for testing
    overall_start_time = time.time()

    queue = [(col_num, row_num)]
    visited = []
    while len(queue) > 0:
        # for testing
        start = time.time()

        # returns and deletes first element (tuple) in queue
        cur_tile = queue.pop(0)
        visited.append(cur_tile)

        # checks current tile type and updates gameboard (or skips to next item in queue if tile is a number)
        pyautogui.moveTo(col_x_coords.get(cur_tile[0]), row_y_coords.get(cur_tile[1]))
        cur_tile_type = return_tile_type(zoom_size)
        if cur_tile_type <= 0:
            gameboard[cur_tile[1]][cur_tile[0]] = cur_tile_type
        else:
            end = time.time()
            print(end - start)
            gameboard[cur_tile[1]][cur_tile[0]] = cur_tile_type
            continue

        # adds 8 adjacent neighbors to queue if they are 1.) within the range of the board size, 2.) not already in
        # the queue, and 3.) and already visited
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
        end = time.time()
        print(end - start)

    overall_end_time = time.time()
    print(overall_end_time - overall_start_time)
    print("Tiles visited:", end="")
    print(len(visited))
    return


# update gameboard depending on what type of tile the mouse is currently hovering over
def update_tiles(gameboard, col_x_coords, row_y_coords, col_num, row_num, zoom_size) -> None:
    val = return_tile_type(zoom_size)
    if val == 0:
        # if current tile is an open space, we use bfs to scan all tiles in the surrounding area
        update_tiles_bfs2(gameboard, col_x_coords, row_y_coords, col_num, row_num, zoom_size)
    elif val != -2:
        # if current tile is not an open space, we scan only one tile
        gameboard[row_num][col_num] = val
    return
