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


def aggregate_border_tiles(gameboard, col_x_coords, row_y_coords, border_tiles) -> list:
    return []


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
    aggregations = []

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
gameboard = [[5, 3, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, 7, -1, 5, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, 2, -1]]
col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420}
row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250, 4: 280}
unfinished_numbers = [(0,0), (1, 0), (1, 2), (3, 2), (3, 4)]

for i in range(len(row_y_coords)):
    print(gameboard[i])

print()
borders = return_border_tiles(gameboard, col_x_coords, row_y_coords, unfinished_numbers)
print(len(borders))
print(borders)
print()

for i in range(len(row_y_coords)):
    print(gameboard[i])
