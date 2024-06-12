import time

def return_border_tiles(gameboard, col_x_coords, row_y_coords, unfinished_numbers) -> list:
    border_tiles = []
    for tile in unfinished_numbers:
        open_tiles = []
        for c in range(tile[0] - 1, tile[0] + 2):
            for r in range(tile[1] - 1, tile[1] + 2):
                if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                    if gameboard[r][c] == -1:
                        open_tiles.append((c, r))
        border_tiles = list(set(border_tiles + open_tiles))  # don't want any duplciates
    return border_tiles


def return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords, tile) -> list:
    bordering_number_tiles = []
    for c in range(tile[0] - 1, tile[0] + 2):
        for r in range(tile[1] - 1, tile[1] + 2):
            if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                if gameboard[r][c] > 0 and gameboard[r][c] < 9:
                    bordering_number_tiles.append((c, r))
    return bordering_number_tiles


def aggregate_border_tiles(gameboard, col_x_coords, row_y_coords, border_tiles) -> list:
    aggregations = []

    # create copy of border_tiles because we don't want to modify the border_tiles list itself
    remaining_border_tiles = border_tiles.copy()

    # repeatedly runs a modified bfs algorithm until all aggregations are found
    while len(remaining_border_tiles) > 0:
        queue = []
        queue.append(remaining_border_tiles[0])
        visited = []
        # bfs algorithm
        while len(queue) > 0:
            # returns and deletes first element (tuple) in queue, and removes this element from remaining_border_tiles
            cur_tile = queue.pop(0)
            visited.append(cur_tile)
            remaining_border_tiles.remove(cur_tile)

            # finds the location of the number tiles that border cur_tile
            bordering_number_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords, cur_tile)

            # adds 8 adjacent neighbors to queue if they 1.) are within the range of the board size, 2.) aren't already
            # in the queue, 3.) aren't already in visited, 4.) are present in remaining_border_tiles, and 5.) have at
            # least one number tile in it's range that is also in range of the current tile (i.e. the current border
            # tile and the neighboring border tile both have at least one bordering number tile in common)
            # NOTE: absolutely disgusting chunk of code right here but it fucking works so stfu
            if (cur_tile[0] - 1 >= 0) and ((cur_tile[0] - 1, cur_tile[1]) not in queue and (cur_tile[0] - 1, cur_tile[1]) not in visited):
                if ((cur_tile[0] - 1, cur_tile[1]) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords, (cur_tile[0] - 1, cur_tile[1]))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)):
                        queue.append((cur_tile[0] - 1, cur_tile[1]))
            if (cur_tile[0] + 1 < len(col_x_coords)) and ((cur_tile[0] + 1, cur_tile[1]) not in queue and (cur_tile[0] + 1, cur_tile[1]) not in visited):
                # note: col_x_coords.len() gives us the number of columns
                if ((cur_tile[0] + 1, cur_tile[1]) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords, (cur_tile[0] + 1, cur_tile[1]))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)):
                        queue.append((cur_tile[0] + 1, cur_tile[1]))
            if (cur_tile[1] - 1 >= 0) and ((cur_tile[0], cur_tile[1] - 1) not in queue and (cur_tile[0], cur_tile[1] - 1) not in visited):
                if ((cur_tile[0], cur_tile[1] - 1) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords,(cur_tile[0], cur_tile[1] - 1))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)):
                        queue.append((cur_tile[0], cur_tile[1] - 1))
            if (cur_tile[1] + 1 < len(row_y_coords)) and ((cur_tile[0], cur_tile[1] + 1) not in queue and (cur_tile[0], cur_tile[1] + 1) not in visited):
                # note: row_y_coords.len() gives us the number of rows
                if ((cur_tile[0], cur_tile[1] + 1) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords,(cur_tile[0], cur_tile[1] + 1))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)):
                        queue.append((cur_tile[0], cur_tile[1] + 1))

            if (cur_tile[0] - 1 >= 0 and cur_tile[1] - 1 >= 0) and ((cur_tile[0] - 1, cur_tile[1] - 1) not in queue and (cur_tile[0] - 1, cur_tile[1] - 1) not in visited):
                if ((cur_tile[0] - 1, cur_tile[1] - 1) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords,(cur_tile[0] - 1, cur_tile[1] - 1))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)):
                        queue.append((cur_tile[0] - 1, cur_tile[1] - 1))
            if (cur_tile[0] + 1 < len(col_x_coords) and cur_tile[1] - 1 >= 0) and ((cur_tile[0] + 1, cur_tile[1] - 1) not in queue and (cur_tile[0] + 1, cur_tile[1] - 1) not in visited):
                # note: col_x_coords.len() gives us the number of columns
                if ((cur_tile[0] + 1, cur_tile[1] - 1) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords,(cur_tile[0] + 1, cur_tile[1] - 1))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)):
                        queue.append((cur_tile[0] + 1, cur_tile[1] - 1))
            if (cur_tile[0] - 1 >= 0 and cur_tile[1] + 1 < len(row_y_coords)) and ((cur_tile[0] - 1, cur_tile[1] + 1) not in queue and (cur_tile[0] - 1, cur_tile[1] + 1) not in visited):
                if ((cur_tile[0] - 1, cur_tile[1] + 1) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords,(cur_tile[0] - 1, cur_tile[1] + 1))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)):
                        queue.append((cur_tile[0] - 1, cur_tile[1] + 1))
            if (cur_tile[0] + 1 < len(col_x_coords) and cur_tile[1] + 1 < len(row_y_coords)) and ((cur_tile[0] + 1, cur_tile[1] + 1) not in queue and (cur_tile[0] + 1, cur_tile[1] + 1) not in visited):
                # note: row_y_coords.len() gives us the number of rows
                if ((cur_tile[0] + 1, cur_tile[1] + 1) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords,(cur_tile[0] + 1, cur_tile[1] + 1))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)):
                        queue.append((cur_tile[0] + 1, cur_tile[1] + 1))
        # add visited list to aggregations as a new list within the aggregations list
        aggregations.append(visited)

    print("aggregations found: ", end="")
    print(len(aggregations))
    print("aggregations: ", end="")
    print(aggregations)
    return aggregations


# runs local search algorithm and returns a list with 2 indices...
# index 0: number of tiles that were marked as mines
# index 1: list of tiles (tuples of format (cols, rows)) to be clicked
def local_search(gameboard, col_x_coords, row_y_coords, unfinished_numbers, bombs_remaining) -> list:
    mine_tiles = []
    click_tiles = []

    # NOTE TO SELF FOR LATER ON: make sure to take "bombs_remaining" value into account to make the algorithm more
    # accurate at the end of the game (when there are only a few bombs left)


    # STEP 1: make list of border tiles
    border_tiles = return_border_tiles(gameboard, col_x_coords, row_y_coords, unfinished_numbers)

    # STEP 2: aggregate border tiles into groups of connected tiles (use a modified bfs algorithm)
    aggregations = aggregate_border_tiles(gameboard, col_x_coords, row_y_coords, border_tiles)

    # STEP 3: for each aggregation, find all possible combinations of possible bomb placements
    # note: bomb combinations is a list of lists containing lists defined as follows...
    # bomb_combinations[i] = i-th aggregation's list of possbile bomb combinations
    # bomb_combinations[i][j] = i-th aggregation's j-th bomb combination (list of tuples, each representing a bomb tile)
    # bomb_combinations[i][j][k] = the k-th bomb tile in the i-th aggregation's j-th bomb combination
    bomb_combinations = []
    # ...

    # STEP 4: for each aggregation's possible bomb combinations, check for the following...
    # a.) if a tile is in every combination, mark it as a bomb on gameboard and append tile to mine_tiles
    # b.) if a tile is NOT in ANY combination, append tile to click_tiles (as it is guaranteed to be safe)
    # ...

    return [len(mine_tiles), click_tiles]


# TESTING
gameboard = [[-1, 2, -1, -1, 2], [-1, -1, -1, -1, 2], [-1, -1, -1, -1,-1], [-1, -1, -1, -1, 2], [-1, -1, -1, -1, -1]]
col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420}
row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250, 4: 280}
unfinished_numbers = [(1,0), (4,0), (4,1), (4,3)]

for i in range(len(row_y_coords)):
    print(gameboard[i])

print()
borders = return_border_tiles(gameboard, col_x_coords, row_y_coords, unfinished_numbers)
print("number of border tiles found: ", end="")
print(len(borders))
print("border tiles: ", end="")
print(borders)
aggregate_border_tiles(gameboard, col_x_coords, row_y_coords, borders)
print()

for i in range(len(row_y_coords)):
    print(gameboard[i])
