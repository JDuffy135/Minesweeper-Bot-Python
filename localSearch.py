import time
import copy
import patternRecognition as pR


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


# when there are only a few closed tiles left on the board, we check all remaining closed tiles in local search
def return_border_tiles_endgame(gameboard, col_x_coords, row_y_coords) -> list:
    border_tiles = []
    for c in range(len(col_x_coords)):
        for r in range(len(row_y_coords)):
            if gameboard[r][c] == -1:
                border_tiles.append((c, r))
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


# used in merge_aggregations - finds all bordering tiles in the unfinished_numbers list surrounding the given tile
def return_bordering_unfinished_numbers(gameboard, col_x_coords, row_y_coords, unfinished_numbers, tile) -> set[tuple]:
    bordering_number_tiles = set()
    for c in range(tile[0] - 1, tile[0] + 2):
        for r in range(tile[1] - 1, tile[1] + 2):
            if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                if (c, r) in unfinished_numbers:
                    bordering_number_tiles.add((c, r))
    return bordering_number_tiles


# merges any aggregations with at least one shared unfinishednumber tile (as they are dependent on one another)
def merge_aggregations(gameboard, col_x_coords, row_y_coords, unfinished_numbers, aggregations) -> None:
    # for each aggregation, create a set containing all bordering unfinished_number tiles
    number_sets = [set() for agg in aggregations]
    for i in range(len(aggregations)):
        for border_tile in aggregations[i]:
            cur_set = return_bordering_unfinished_numbers(gameboard, col_x_coords, row_y_coords, unfinished_numbers, border_tile)
            number_sets[i].update(cur_set)

    # compare all number sets to see if any aggregations need to be merged until all sets (including newly merged sets)
    # have been compared
    cur_item = 0
    cur_index = 1
    restart_flag = 0
    while cur_item < len(aggregations) - 1:
        while cur_index < len(aggregations):
            tmp_set = copy.deepcopy(number_sets[cur_item])
            tmp_set.update(number_sets[cur_index])
            if len(tmp_set) < len(number_sets[cur_item]) + len(number_sets[cur_index]):
                # in this case, there is a shared unfinished number tile between the 2 aggregations
                # merge sets
                number_sets[cur_item].update(number_sets[cur_index])
                number_sets.pop(cur_index)
                # merge aggregation lists
                for tile in aggregations[cur_index]:
                    aggregations[cur_item].append(tile)
                aggregations.pop(cur_index)
                # update restart flag and break
                restart_flag = 1
                break
            else:
                cur_index = cur_index + 1
        # after comparing aggregation[cur_item] to every following aggregation, we check if we should increment cur_item
        # or restart at index 0 (if any aggregations were just merged)
        if restart_flag != 1:
            cur_item = cur_item + 1
            cur_index = cur_item + 1
        else:
            cur_item = 0
            cur_index = 1
            restart_flag = 0

    return


# separates border tiles into multiple aggregations (if possible) in order to reduce runtime of local search algorithm
def aggregate_border_tiles(gameboard, col_x_coords, row_y_coords, unfinished_numbers, border_tiles, endgame:bool) -> list[list[tuple]]:
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
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)) or endgame == True:
                        queue.append((cur_tile[0] - 1, cur_tile[1]))
            if (cur_tile[0] + 1 < len(col_x_coords)) and ((cur_tile[0] + 1, cur_tile[1]) not in queue and (cur_tile[0] + 1, cur_tile[1]) not in visited):
                # note: col_x_coords.len() gives us the number of columns
                if ((cur_tile[0] + 1, cur_tile[1]) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords, (cur_tile[0] + 1, cur_tile[1]))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)) or endgame == True:
                        queue.append((cur_tile[0] + 1, cur_tile[1]))
            if (cur_tile[1] - 1 >= 0) and ((cur_tile[0], cur_tile[1] - 1) not in queue and (cur_tile[0], cur_tile[1] - 1) not in visited):
                if ((cur_tile[0], cur_tile[1] - 1) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords,(cur_tile[0], cur_tile[1] - 1))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)) or endgame == True:
                        queue.append((cur_tile[0], cur_tile[1] - 1))
            if (cur_tile[1] + 1 < len(row_y_coords)) and ((cur_tile[0], cur_tile[1] + 1) not in queue and (cur_tile[0], cur_tile[1] + 1) not in visited):
                # note: row_y_coords.len() gives us the number of rows
                if ((cur_tile[0], cur_tile[1] + 1) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords,(cur_tile[0], cur_tile[1] + 1))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)) or endgame == True:
                        queue.append((cur_tile[0], cur_tile[1] + 1))

            if (cur_tile[0] - 1 >= 0 and cur_tile[1] - 1 >= 0) and ((cur_tile[0] - 1, cur_tile[1] - 1) not in queue and (cur_tile[0] - 1, cur_tile[1] - 1) not in visited):
                if ((cur_tile[0] - 1, cur_tile[1] - 1) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords,(cur_tile[0] - 1, cur_tile[1] - 1))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)) or endgame == True:
                        queue.append((cur_tile[0] - 1, cur_tile[1] - 1))
            if (cur_tile[0] + 1 < len(col_x_coords) and cur_tile[1] - 1 >= 0) and ((cur_tile[0] + 1, cur_tile[1] - 1) not in queue and (cur_tile[0] + 1, cur_tile[1] - 1) not in visited):
                # note: col_x_coords.len() gives us the number of columns
                if ((cur_tile[0] + 1, cur_tile[1] - 1) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords,(cur_tile[0] + 1, cur_tile[1] - 1))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)) or endgame == True:
                        queue.append((cur_tile[0] + 1, cur_tile[1] - 1))
            if (cur_tile[0] - 1 >= 0 and cur_tile[1] + 1 < len(row_y_coords)) and ((cur_tile[0] - 1, cur_tile[1] + 1) not in queue and (cur_tile[0] - 1, cur_tile[1] + 1) not in visited):
                if ((cur_tile[0] - 1, cur_tile[1] + 1) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords,(cur_tile[0] - 1, cur_tile[1] + 1))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)) or endgame == True:
                        queue.append((cur_tile[0] - 1, cur_tile[1] + 1))
            if (cur_tile[0] + 1 < len(col_x_coords) and cur_tile[1] + 1 < len(row_y_coords)) and ((cur_tile[0] + 1, cur_tile[1] + 1) not in queue and (cur_tile[0] + 1, cur_tile[1] + 1) not in visited):
                # note: row_y_coords.len() gives us the number of rows
                if ((cur_tile[0] + 1, cur_tile[1] + 1) in remaining_border_tiles):
                    neighbor_num_tiles = return_bordering_number_tiles(gameboard, col_x_coords, row_y_coords,(cur_tile[0] + 1, cur_tile[1] + 1))
                    if len(set(neighbor_num_tiles + bordering_number_tiles)) < (len(neighbor_num_tiles) + len(bordering_number_tiles)) or endgame == True:
                        queue.append((cur_tile[0] + 1, cur_tile[1] + 1))
        # add visited list to aggregations as a new list within the aggregations list
        aggregations.append(visited)


    # if any two aggregations have at least one shared unfinished number tile between them, merge them together
    if len(aggregations) > 1:
        merge_aggregations(gameboard, col_x_coords, row_y_coords, unfinished_numbers, aggregations)

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
    def backtrack(gameboard, col_x_coords, row_y_coords, aggregation_index, aggregation, start_index, combination) -> None:
        # base case
        if ((start_index == len(aggregation))):
            if is_valid_combination(gameboard, aggregation, col_x_coords, row_y_coords, combination):
                mine_combinations[aggregation_index].append(combination.copy())
                # print(combination)
            return

        # if the board placement is valid, try backtracking algorithm first without adding the next mine, and then
        # try again with adding the next mine
        if is_valid_mine_placement(gameboard, aggregation, col_x_coords, row_y_coords, combination) == True:
            backtrack(gameboard, col_x_coords, row_y_coords, aggregation_index, aggregation, start_index + 1, combination)
            combination.append(aggregation[start_index])
            backtrack(gameboard, col_x_coords, row_y_coords, aggregation_index, aggregation, start_index + 1, combination)
            combination.pop()
        else:
            return

    # for each aggregation with less than 22 tiles, we find all possible valid combinations of mines
    for i in range(len(mine_combinations)):
        if len(aggregations[i]) < 22:
            backtrack(gameboard, col_x_coords, row_y_coords, i, aggregations[i], 0, [])
        else:
            # NOTE: mine_combinations[i] will be an empty list in this case
            print("   local search not practical for this aggregation (size: ", end="")
            print(len(aggregations[i]), end="")
            print(")")

    return mine_combinations


# runs local search algorithm and returns a list with 4 indices...
# index 0: number of tiles that were marked as mines
# index 1: list of tiles (tuples of format (cols, rows)) to be clicked
# index 2: aggregations of border tiles
# index 3: all possible mine combinations for each aggregation
# NOTE: data from indices 2 and 3 are used in the probability calculations if no guaranteed moves exist
def local_search(gameboard, col_x_coords, row_y_coords, unfinished_numbers, bombs_remaining) -> list[int, list[tuple], list[list[tuple]], list[list[list[tuple]]]]:
    start = time.time()
    mine_tiles = []
    click_tiles = []

    # STEP 0: initializing bool value for end-game optimizations
    endgame = False
    num_of_closed_tiles = 0
    for c in range(len(col_x_coords)):
        for r in range(len(row_y_coords)):
            if gameboard[r][c] == -1:
                num_of_closed_tiles = num_of_closed_tiles + 1

    if num_of_closed_tiles < 22:
        print("END GAME MODE ACTIVATED")  # for testing
        endgame = True


    # STEP 1: make list of border tiles + END-GAME OPTIMIZATION #1
    if endgame == False:
        border_tiles = return_border_tiles(gameboard, col_x_coords, row_y_coords, unfinished_numbers)
    else:
        border_tiles = return_border_tiles_endgame(gameboard, col_x_coords, row_y_coords)


    # STEP 2: aggregate border tiles into distinct groups with shared number tiles (if not endgame)
    # note: we only have one aggregation in the endgame case since we want to try and brute force the entire board
    if endgame == False:
        aggregations = aggregate_border_tiles(gameboard, col_x_coords, row_y_coords, unfinished_numbers, border_tiles, endgame)
    else:
        # aggregation_count = len(aggregate_border_tiles(gameboard, col_x_coords, row_y_coords, border_tiles, endgame))
        aggregations = []
        aggregations.append(border_tiles)


    # STEP 3: for each aggregation, find all possible combinations of bomb placements
    mine_combinations = find_all_mine_combinations(gameboard, col_x_coords, row_y_coords, aggregations, bombs_remaining)


    # FOR TESTING
    # print()
    # print("mine combinations for each aggregate BEFORE end-game optimization #2...")
    # for agg in mine_combinations:
    #     print(agg)
    # print()


    # END-GAME OPTIMIZATION #2: remove all mine combinations whose length is larger than bombs_remaining
    # (as, for instance, it's not possible to have a combination with 3 mines if there are only 2 remaining mines)
    if endgame == True:
        for agg in mine_combinations:
            index = 0
            while index < len(agg):
                if len(agg[index]) > bombs_remaining:
                    # print("REMOVED AGGREGATION OF SIZE ", end="")  # for testing
                    # print(len(agg[index]))  # for testing
                    agg.remove(agg[index])
                else:
                    index = index + 1
        print("total valid endgame mine combinations: ", end="")  # for testing
        print(len(mine_combinations[0]))  # for testing


    # FOR TESTING
    # print("mine combinations for each aggregate AFTER end-game optimization #2...")
    # for agg in mine_combinations:
    #     print(agg)
    # print()


    # STEP 4a: for each tile in each aggregation, check if it is...
    # a.) in every bomb combination for it's respective aggregation (if so, mark it as a mine and append to mine_tiles)
    for a in range(len(aggregations)):
        if len(aggregations[a]) >= 22:
            # aggregations of size 22+ are ignored by local search
            continue
        for border_tile in aggregations[a]:
            flag = 0
            for combination in mine_combinations[a]:
                if border_tile not in combination:
                    flag = 1
                    break
            if flag == 0 and len(mine_combinations[a]) > 0:
                gameboard[border_tile[1]][border_tile[0]] = 9
                mine_tiles.append(border_tile)


    # STEP 4b: for each tile in each aggregation, check if it is...
    # b.) in NONE of the bomb combinations for it's respective aggregation (if so, append to click_tiles)
    for a in range(len(aggregations)):
        if len(aggregations[a]) >= 22:
            # aggregations of size 22+ are ignored by local search
            continue
        for border_tile in aggregations[a]:
            flag = 0
            for combination in mine_combinations[a]:
                if border_tile in combination:
                    flag = 1
                    break
            if flag == 0 and len(mine_combinations[a]) > 0:
                click_tiles.append(border_tile)


    # STEP 5: for each aggregation that is too large to be probed with local search (AKA aggregations of size 22+), we
    # pass them into the pattern recognition function to see if there are any guaranteed moves we can make without
    # computing all the possible mine combinations
    for i in range(len(aggregations)):
        if len(aggregations[i]) >= 22:
            bordering_unfinished_numbers = set()
            for border_tile in aggregations[i]:
                cur_set = return_bordering_unfinished_numbers(gameboard, col_x_coords, row_y_coords, unfinished_numbers, border_tile)
                bordering_unfinished_numbers.update(cur_set)
            result = pR.pattern_recognition(gameboard, col_x_coords, row_y_coords, list(bordering_unfinished_numbers), bombs_remaining - len(mine_tiles))
            mine_tiles.extend(result[0])
            click_tiles.extend(result[1])


    # print(time.time() - start)
    return [len(mine_tiles), click_tiles, aggregations, mine_combinations]



# TESTING

# GAMEBOARD #1
# expected output: [7, [(0, 4), (2, 7), (7, 3), (5, 3), (3, 8)]]
# gameboard = [
#     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
#     [-1, 2, 1, 2, 9, -1, -1, -1, -1],
#     [-1, 2, 0, 1, 1, 2, 1, 2, -1],
#     [-1, 2, 0, 0, 0, 0, 0, 1, -1],
#     [-1, 4, 2, 1, 1, 0, 0, 1, -1],
#     [-1, -1, -1, 9, 2, 2, 2, 2, -1],
#     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
# ]
# unfinished_numbers = [
#     (1,3),
#     (1,4),
#     (1,5),
#     (1,6),
#     (2,3),
#     (2,6),
#     (3,3),
#     (3,4),
#     (3,6),
#     (4,4),
#     (4,6),
#     (4,7),
#     (5,4),
#     (5,7),
#     (6,4),
#     (6,7),
#     (7,4),
#     (7,5),
#     (7,6),
#     (7,7)
# ]
# col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420, 5: 450, 6: 480, 7: 510, 8: 540}
# row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250, 4: 280, 5: 310, 6: 340, 7: 370, 8: 400}


# GAMEBOARD #2
# expected output: [1, [(3, 4), (4, 5), (3, 5)]]
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


# GAMEBOARD #3 (end-game scenario)
# expected output with bombs_remaining set to 1: [1, [(2, 1), (1, 2), (2, 2)]]
# expected output with bombs_remaining == 2 or 3: [0, []]
# note: if bombs_remaining > 3, this is not a valid gameboard
# gameboard = [
#     [9, 3, 1],
#     [9, -1, -1],
#     [2, -1, -1]
# ]
# unfinished_numbers = [
#     (1,0),
#     (2,0),
#     (0,2)
# ]
# col_x_coords = {0: 300, 1: 330, 2: 360}
# row_y_coords = {0: 160, 1: 190, 2: 220}


# GAME BOARD #4 (end-game scenario)
# expected output with bombs_remaining set to 2: [0, [(3, 2)]]
# note: if bombs_remaining != 2, this is not a valid gameboard
# gameboard = [
#     [1, 2, 3, 9, 9, 9],
#     [9, 4, 9, 9, -1, 4],
#     [9, -1, -1, -1, -1, 9]
# ]
# unfinished_numbers = [
#     (1,1),
#     (5,1)
# ]
# col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420, 5: 450}
# row_y_coords = {0: 160, 1: 190, 2: 220}


# GAME BOARD #5
# expected output with bombs_remaining set to 10+: [0, [], ...]
# gameboard = [
#     [0, 1, 2, -1, -1],
#     [0, 1, 9, -1, -1],
#     [1, 3, 3, -1, -1],
#     [-1, -1, 9, -1, -1],
#     [-1, -1, -1, -1, -1]
# ]
# unfinished_numbers = [
#     (2, 0),
#     (0, 2),
#     (1, 2),
#     (2, 2)
# ]
# col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420, 5: 450}
# row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250, 4: 280}
#
#
# # GAME BOARD #6
# # expected output with bombs_remaining set to 3: [0, [...], ...]
# gameboard = [
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1,  9, -1, -1,  9],
#     [ 2,  3,  0,  2,  3,  9],
#     [ 0,  9,  0,  0,  0,  0],
# ]
# unfinished_numbers = [
# ]
# col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420, 5: 450}
# row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250}
#
#
#
#
# for i in range(len(row_y_coords)):
#     print(gameboard[i])
# print()
#
#
# results = local_search(gameboard, col_x_coords, row_y_coords, unfinished_numbers, 3)
# print()
# print(results)
# print("^^ LOCAL SEARCH FUNCTION RESULTS: [mines marked, click tiles, aggregations, mine combinations]")
# print()
# print("number of aggregations: ",end="")
# print(len(results[2]))
# print("aggregations...")
# for i in range(len(results[2])):
#     print("length is ", end="")
#     print(len(results[2][i]), end="")
#     print(": ", end="")
#     print(results[2][i])
# print()
# print("number of valid mine combinations for each aggregation...")
# for i in range(len(results[2])):
#     print(len(results[3][i]))
# print()
#
#
# for i in range(len(row_y_coords)):
#     print(gameboard[i])
