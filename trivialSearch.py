# runs trivial search algorithm and returns a list with 2 indices...
# index 0: number of tiles that were marked as mines
# index 1: list of tiles (tuples of format (cols, rows)) to be clicked
def trivial_search(gameboard, col_x_coords, row_y_coords, unfinished_numbers) -> list:
    mine_tiles = []
    click_tiles = []

    # CASE 1: tile needs 'n' bombs to be satisfied and has only 'n' closed tiles remaining
    # NOTE TO SELF: find the number of bombs the tile needs to be satisfied (may or may not be equal to the tile number
    # itself), and then check if the number of remaining closed tiles matches this number
    for tile in unfinished_numbers:
        current_number = gameboard[tile[1]][tile[0]]
        open_tiles_count = 0
        open_tiles_list = []
        bombs_remaining = current_number
        for c in range(tile[0] - 1, tile[0] + 2):
            for r in range(tile[1] - 1, tile[1] + 2):
                if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                    if gameboard[r][c] == -1:
                        open_tiles_count = open_tiles_count + 1
                        open_tiles_list.append((c, r))
                    elif gameboard[r][c] == 9:
                        bombs_remaining = bombs_remaining - 1
        if open_tiles_count == bombs_remaining:
            mine_tiles = list(set(mine_tiles + open_tiles_list))  # don't want any duplciates

    # flagging mines on gameboard if mine_tiles is not empty
    for mine_tile in mine_tiles:
        gameboard[mine_tile[1]][mine_tile[0]] = 9

    # CASE 2: tile already has max number of bombs in it's area, but has closed tiles to be clicked
    for tile in unfinished_numbers:
        current_number = gameboard[tile[1]][tile[0]]
        open_tiles_count = 0
        open_tiles_list = []
        bombs_remaining = current_number
        for c in range(tile[0] - 1, tile[0] + 2):
            for r in range(tile[1] - 1, tile[1] + 2):
                if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                    if gameboard[r][c] == -1:
                        open_tiles_count = open_tiles_count + 1
                        open_tiles_list.append((c, r))
                    elif gameboard[r][c] == 9:
                        bombs_remaining = bombs_remaining - 1
        if bombs_remaining <= 0:
            click_tiles = list(set(click_tiles + open_tiles_list))  # don't want any duplicates

    return [len(mine_tiles), click_tiles]


# TESTING
# gameboard = [[1, 2, 2, 1, -1], [2, 9, 9, -1, -1], [3, 9, -1, -1,-1], [9, -1, -1, -1, -1], [1, -1, -1, -1, -1]]
# col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420}
# row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250, 4: 280}
# unfinished_numbers = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (0, 2), (0, 4)]
#
# for i in range(len(row_y_coords)):
#     print(gameboard[i])
#
# print()
# print(trivial_search(gameboard, col_x_coords, row_y_coords, unfinished_numbers))
# print()
#
# for i in range(len(row_y_coords)):
#     print(gameboard[i])
