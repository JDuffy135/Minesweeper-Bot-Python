import time
import copy


# returns adjacent tiles which are marked as closed for each tile in unfinished_numbers
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


# returns list of number tiles adjacent to the given tile
def return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords, tile) -> list:
    bordering_number_tiles = []
    for c in range(tile[0] - 1, tile[0] + 2):
        for r in range(tile[1] - 1, tile[1] + 2):
            if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                if gameboard[r][c] > 0 and gameboard[r][c] < 9:
                    bordering_number_tiles.append((c, r))
    return bordering_number_tiles


# separates border tiles into multiple aggregations of possible in order to reduce runtime of local search algorithm
def aggregate_border_tiles(gameboard, col_x_coords, row_y_coords, border_tiles) -> list[list[tuple]]:
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
            # NOTE: absolutely disgusting chunk of code right here but it works so stfu
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

    return aggregations


# used in is_valid_board_placement to figure out if a particular number tile is oversatisfied (returns True if so)
def is_oversatisfied(gameboard, col_x_coords, row_y_coords, tile) -> bool:
    mines_found = 0
    tile_number = gameboard[tile[1]][tile[0]]
    for c in range(tile[0] - 1, tile[0] + 2):
        for r in range(tile[1] - 1, tile[1] + 2):
            if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                if gameboard[r][c] == 9:
                    mines_found = mines_found + 1
    return (mines_found > tile_number)


# used in find_all_bomb_combinations backtracking algorithm to check if a particular mine combination is valid
# note: a combination is valid if none of the surrounding number tiles are oversatisfied (ex: 3 bombs around a 2 tile)
def is_valid_mine_placement(gameboard, aggregation, col_x_coords, row_y_coords, combination) -> bool:
    if len(combination) == 0:
        return True

    # create a deep copy of the gameboard and get dimensions of board
    tmp_gameboard = copy.deepcopy(gameboard)
    row_count = len(row_y_coords)
    col_count = len(col_x_coords)

    # place mines from combination list onto copy of gameboard
    for mine in combination:
        tmp_gameboard[mine[1]][mine[0]] = 9

    # return list of number tiles surrounding the aggregation
    bordering_number_tiles = set()
    for tile in aggregation:
        bordering_number_tiles.update(return_bordering_number_tiles(tmp_gameboard, col_x_coords, row_y_coords, tile))

    # if any of the number tiles are oversatisfied, return False
    for number_tile in bordering_number_tiles:
        if is_oversatisfied(tmp_gameboard, col_x_coords, row_y_coords, number_tile) == True:
            return False

    return True


# used in is_valid_combination to figure out if a particular number tile is satisfied (returns True if so)
def is_satisfied(gameboard, col_x_coords, row_y_coords, tile) -> bool:
    mines_found = 0
    tile_number = gameboard[tile[1]][tile[0]]
    for c in range(tile[0] - 1, tile[0] + 2):
        for r in range(tile[1] - 1, tile[1] + 2):
            if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                if gameboard[r][c] == 9:
                    mines_found = mines_found + 1
    return (mines_found == tile_number)


# used in base case of find_all_bomb_combinations backtracking algorithm to figure out if the combination is valid
# returns True if all surrounding number tiles are satisfied
def is_valid_combination(gameboard, aggregation, col_x_coords, row_y_coords, combination) -> bool:
    if len(combination) == 0:
        return False

    # create a deep copy of the gameboard and get dimensions of board
    tmp_gameboard = copy.deepcopy(gameboard)
    row_count = len(row_y_coords)
    col_count = len(col_x_coords)

    # place mines from combination list onto copy of gameboard
    for mine in combination:
        tmp_gameboard[mine[1]][mine[0]] = 9

    # return list of number tiles surrounding the aggregation
    bordering_number_tiles = set()
    for tile in aggregation:
        bordering_number_tiles.update(return_bordering_number_tiles(tmp_gameboard, col_x_coords, row_y_coords, tile))

    # if any of the number tiles arent satisfied, return False
    for number_tile in bordering_number_tiles:
        if is_satisfied(tmp_gameboard, col_x_coords, row_y_coords, number_tile) == False:
            return False

    # NOTE: FOR TESTING
    # print("tmp board: ", end="")
    # print()
    # for i in range(row_count):
    #     print(tmp_gameboard[i])

    return True


# returns a list of lists of lists defined as follows...
# mine_combinations[i] = i-th aggregation's list of possbile mine combinations (list of lists)
# mine_combinations[i][j] = i-th aggregation's j-th mine combination (list of tuples, each representing a mine tile)
# mine_combinations[i][j][k] = the k-th mine tile in the i-th aggregation's j-th mine combination (tuple)
def find_all_mine_combinations(gameboard, col_x_coords, row_y_coords, aggregations, bombs_remaining) -> list[list[list[tuple]]]:
    # final returned list, which contains a list of mine combination lists for each aggregation
    mine_combinations = [[] for aggregation in aggregations]

    # backtracking algorithm which returns a list of lists (each inner list is a list of bomb tiles which are tuples)
    def backtrack(gameboard, col_x_coords, row_y_coords, aggregation_index, aggregation, start_index, combination, max_mines) -> None:
        # base case
        if ((start_index == len(aggregation))):
            # print("BASE CASE")
            # print(combination)
            if is_valid_combination(gameboard, aggregation, col_x_coords, row_y_coords, combination):
                mine_combinations[aggregation_index].append(combination.copy())
                # print("appended")
            return

        # if the board placement is valid, try backtracking algorithm first without adding the next mine, and then
        # try again with adding the next mine
        if is_valid_mine_placement(gameboard, aggregation, col_x_coords, row_y_coords, combination) == True:
            backtrack(gameboard, col_x_coords, row_y_coords, aggregation_index, aggregation, start_index + 1, combination, max_mines)
            combination.append(aggregation[start_index])
            backtrack(gameboard, col_x_coords, row_y_coords, aggregation_index, aggregation, start_index + 1, combination, max_mines)
            combination.pop()
        else:
            return

    # for each aggregation, we find all possible vald combinations of mine placements
    for i in range(len(mine_combinations)):
        backtrack(gameboard, col_x_coords, row_y_coords, i, aggregations[i], 0, [], bombs_remaining)

    return mine_combinations


# runs local search algorithm and returns a list with 2 indices...
# index 0: number of tiles that were marked as mines
# index 1: list of tiles (tuples of format (cols, rows)) to be clicked
def local_search(gameboard, col_x_coords, row_y_coords, unfinished_numbers, bombs_remaining) -> list:
    start = time.time()
    mine_tiles = []
    click_tiles = []

    # NOTE TO SELF FOR LATER ON: make sure to take "bombs_remaining" value into account to make the algorithm more
    # accurate at the end of the game (when there are only a few bombs left)


    # STEP 1: make list of border tiles
    border_tiles = return_border_tiles(gameboard, col_x_coords, row_y_coords, unfinished_numbers)

    # STEP 2: aggregate border tiles into distinct groups with shared number tiles
    aggregations = aggregate_border_tiles(gameboard, col_x_coords, row_y_coords, border_tiles)
    for i in range(len(aggregations)):
        if len(aggregations[i]) > 21:
            print("local search not practical for this aggregation")
            aggregations[i] = []

    # STEP 3: for each aggregation, find all possible combinations of bomb placements
    mine_combinations = find_all_mine_combinations(gameboard, col_x_coords, row_y_coords, aggregations, bombs_remaining)

    # FOR TESTING
    # print("mine combinations for each aggregate...")
    # for agg in mine_combinations:
    #     print(agg)

    # STEP 4a: for each tile in each aggregation, check if it is...
    # a.) in every bomb combination for it's respective aggregation (if so, mark it as a mine and append to mine_tiles)
    for a in range(len(aggregations)):
        for border_tile in aggregations[a]:
            flag = 0
            for combination in mine_combinations[a]:
                if border_tile not in combination:
                    flag = 1
                    break
            if flag == 0 and len(mine_combinations[a]) > 0:
                gameboard[border_tile[1]][border_tile[0]] = 9
                mine_tiles.append(border_tile)

    # STEP 4b: for each tile in each aggregation, check if it...
    # b.) in NONE of the bomb combinations for it's respective aggregation (if so, append to click_tiles)
    for a in range(len(aggregations)):
        for border_tile in aggregations[a]:
            flag = 0
            for combination in mine_combinations[a]:
                if border_tile in combination:
                    flag = 1
                    break
            if flag == 0:
                click_tiles.append(border_tile)

    print(time.time() - start)
    return [len(mine_tiles), click_tiles]



# TESTING
gameboard = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 2, 1, 2, 9, -1, -1, -1, -1],
    [-1, 2, 0, 1, 1, 2, 1, 2, -1],
    [-1, 2, 0, 0, 0, 0, 0, 1, -1],
    [-1, 4, 2, 1, 1, 0, 0, 1, -1],
    [-1, -1, -1, 9, 2, 2, 2, 2, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
]
unfinished_numbers = [
    (1,3),
    (1,4),
    (1,5),
    (1,6),
    (2,3),
    (2,6),
    (3,3),
    (3,4),
    (3,6),
    (4,4),
    (4,6),
    (4,7),
    (5,4),
    (5,7),
    (6,4),
    (6,7),
    (7,4),
    (7,5),
    (7,6),
    (7,7)
]
col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420, 5: 450, 6: 480, 7: 510, 8: 540}
row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250, 4: 280, 5: 310, 6: 340, 7: 370, 8: 400}

# gameboard = [
#     [2, 2, 1, 0, 0, 0, 1, 1, 1],
#     [9, 9, 1, 0, 0, 0, 1, 9, 1],
#     [2, 3, 2, 1, 1, 1, 2, 1, 1],
#     [0, 2, 9, 3, 2, 9, 1, 0, 0],
#     [0, 3, 9, -1, -1, 2, 1, 0, 0],
#     [1, 3, 9, -1, -1, 2, 1, 0, 0],
#     [9, 2, 2, -1, 2, 9, 1, 0, 0],
#     [1, 1, 1, -1, 2, 1, 1, 0, 0],
# ]
# unfinished_numbers = [
#     (3,3),
#     (4,3),
#     (5,4),
#     (5,5),
#     (4,6),
#     (4,7),
#     (2,6),
#     (2,7)
# ]
# col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420, 5: 450, 6: 480, 7: 510, 8: 540}
# row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250, 4: 280, 5: 310, 6: 340, 7: 370}

for i in range(len(row_y_coords)):
    print(gameboard[i])
print()

# borders = return_border_tiles(gameboard, col_x_coords, row_y_coords, unfinished_numbers)
# print("number of border tiles found: ", end="")
# print(len(borders))
# print("border tiles: ", end="")
# print(borders)
# aggregations = aggregate_border_tiles(gameboard, col_x_coords, row_y_coords, borders)
# print("size of each aggregation:")
# for a in aggregations:
#     print(len(a))
# print()
# print("bomb combinations for each aggregation respectively...")
# all_combinations = find_all_mine_combinations(gameboard, col_x_coords, row_y_coords, aggregations, 99)
# print(all_combinations)
# for i in range(len(all_combinations)):
#     print(len(all_combinations[i]))
# print()

print("LOCAL SEARCH FUNCTION RESULTS: [mines marked, click tiles]")
print(local_search(gameboard, col_x_coords, row_y_coords, unfinished_numbers, 99))
print()


for i in range(len(row_y_coords)):
    print(gameboard[i])
