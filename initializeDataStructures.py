# converts the user input string into a tuple containing 2 ints of format (columns, rows)
def return_board_size(board_size) -> tuple:
    if board_size == 'beginner':
        return (9, 9)
    elif board_size == 'intermediate':
        return (16, 16)
    elif board_size == 'expert':
        return (30, 16)
    else:
        tmp = board_size.split('x')
        return (int(tmp[0]), int(tmp[1]))


# returns a 2D list filled with -1 in each space
def return_gameboard(board_size) -> list:
    size = return_board_size(board_size)
    board = [[-1 for i in range(size[0])] for j in range(size[1])]
    return board


# returns a dictionary mapping the y coordinate value to each row index
def return_coord_map_rows(zoom_size, first_tile_coords, board_size) -> dict:
    size = return_board_size(board_size)
    row_map = {}
    for i in range(size[1]):
        row_map[i] = first_tile_coords[1] + (i * zoom_size)
    return row_map


# returns a dictionary mapping the x coordinate value to each column index
def return_coord_map_cols(zoom_size, first_tile_coords, board_size) -> dict:
    size = return_board_size(board_size)
    col_map = {}
    for i in range(size[0]):
        col_map[i] = first_tile_coords[0] + (i * zoom_size)
    return col_map
