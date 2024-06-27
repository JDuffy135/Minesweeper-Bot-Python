import probabilityEngine as PE

# returns effective_utility value for the given tile within a 3x3 range
def return_effective_utility_3x3(gameboard, col_x_coords, row_y_coords, unfinished_numbers, tile) -> int:
    utility_list = []
    for c in range(tile[0] - 1, tile[0] + 2):
        for r in range(tile[1] - 1, tile[1] + 2):
            if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                if gameboard[r][c] >= 1 and gameboard[r][c] < 9 and ((c, r) in unfinished_numbers):
                    utility_list.append((c, r))

    effective_utility = 0
    for num_tile in utility_list:
        effective_value = gameboard[num_tile[1]][num_tile[0]]
        for c in range(num_tile[0] - 1, num_tile[0] + 2):
            for r in range(num_tile[1] - 1, num_tile[1] + 2):
                if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                    if gameboard[r][c] == 9:
                        effective_value = effective_value - 1
        effective_utility = effective_utility + effective_value

    return effective_utility

# used in return_all_border_tiles_effective_utility
def insert_into_min_pq(pq, tile, gameboard, col_x_coords, row_y_coords, unfinished_numbers) -> None:
    effective_utility = return_effective_utility_3x3(gameboard, col_x_coords, row_y_coords, unfinished_numbers, tile)
    new_item = (tile[0], tile[1], effective_utility)

    if len(pq) == 0:
        pq.append(new_item)
    else:
        index = 0
        while index < len(pq):
            if new_item[2] < pq[index][2]:
                pq.insert(index, new_item)
                return
            else:
                index = index + 1
        pq.append(new_item)
    return


# compiles all border tiles into a min priority queue based on effective_utility values in a 3x3 range for each tile
def return_all_border_tiles_effective_utility(gameboard, col_x_coords, row_y_coords, unfinished_numbers, aggregations) -> list[tuple]:
    all_border_tiles = []  # entry format: (col, row, effective_utility)
    visited_tiles = []
    for i in range(len(aggregations)):
        for tile in aggregations[i]:
            if tile not in visited_tiles:
                insert_into_min_pq(all_border_tiles, tile, gameboard, col_x_coords, row_y_coords, unfinished_numbers)
                visited_tiles.append(tile)
    return all_border_tiles


# returns effective utility value for a particular tile given it's utility_list (returned in return_utility function)
def return_effective_utility(gameboard, col_x_coords, row_y_coords, utility_list) -> int:
    effective_utility = 0
    for tile in utility_list:
        effective_value = gameboard[tile[1]][tile[0]]
        for c in range(tile[0] - 1, tile[0] + 2):
            for r in range(tile[1] - 1, tile[1] + 2):
                if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                    if gameboard[r][c] == 9:
                        effective_value = effective_value - 1
        effective_utility = effective_utility + effective_value
    return effective_utility


# returns utility value and list of unfinished number tiles in 5x5 range of given tile
def return_utility(gameboard, col_x_coords, row_y_coords, unfinished_numbers, tile) -> list[int, list[tuple]]:
    utility = 0
    utility_list = []
    for c in range(tile[0] - 2, tile[0] + 3):
        for r in range(tile[1] - 2, tile[1] + 3):
            if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                if gameboard[r][c] >= 1 and gameboard[r][c] < 9 and ((c, r) in unfinished_numbers):
                    utility = utility + 1
                    utility_list.append((c, r))
    return [utility, utility_list]


# used in the case where we must make a semi-educated guess far into the game (when we are making sub-aggregations)
def insert_into_max_pq(pq, tile, gameboard, col_x_coords, row_y_coords, unfinished_numbers) -> None:
    utility_result = return_utility(gameboard, col_x_coords, row_y_coords, unfinished_numbers, tile)
    utility = utility_result[0]
    utility_list = utility_result[1]
    effective_utility = return_effective_utility(gameboard, col_x_coords, row_y_coords, utility_list)
    new_item = (tile[0], tile[1], utility, effective_utility)

    if len(pq) == 0:
        pq.append(new_item)
    else:
        index = 0
        while index < len(pq):
            if new_item[2] >= pq[index][2]:
                if new_item[2] > pq[index][2]:
                    pq.insert(index, new_item)
                    return
                elif new_item[2] == pq[index][2] and new_item[3] <= pq[index][3]:
                    pq.insert(index, new_item)
                    return
                else:
                    index = index + 1
            else:
                index = index + 1
        pq.append(new_item)
    return


# for a given aggregation of border tiles, we return a list of closed tiles bordering said aggregation, with two
# additional attributes: 1.) utility (number of unfinished number tiles in a 5x5 area surrounding the given tile), and
# 2.) effective_utility (sum of effective number values for each unfinished number in 5x5 range)
# NOTE: sub_aggregation is a max priority queue, ordering first by highest utility, second by lowest effective_utility
def return_sub_aggregation(gameboard, col_x_coords, row_y_coords, aggregations, unfinished_numbers) -> list[tuple]:
    sub_aggregation = []
    visited_tiles = []
    for aggregation in aggregations:
        for tile in aggregation:
            for c in range(tile[0] - 1, tile[0] + 2):
                for r in range(tile[1] - 1, tile[1] + 2):
                    if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                        if gameboard[r][c] == -1 and ((c, r) not in visited_tiles) and ((c, r) not in aggregation):
                            # flag system is setup so that the given tile (c, r) must have closed tiles in every
                            # position within a 3x3 range to be considered in the subaggregation
                            flag = 0
                            for x in range(c - 1, c + 2):
                                for y in range(r - 1, r + 2):
                                    if (x >= 0 and x < len(col_x_coords)) and (y >= 0 and y < len(row_y_coords)):
                                        if gameboard[y][x] != -1:
                                            flag = 1
                            if flag == 0:
                                visited_tiles.append((c, r))
                                insert_into_max_pq(sub_aggregation, (c, r), gameboard, col_x_coords, row_y_coords, unfinished_numbers)
    return sub_aggregation


# returns the second safest tile in potential_clicks if one exists (returns None otherwise)
def return_second_safest_tile(potential_clicks) -> tuple:
    highest_safe_chance = potential_clicks[0][2]
    for tile in potential_clicks:
        cur_safety_chance = tile[2]
        if cur_safety_chance < highest_safe_chance:
            return tile
    return None


# after probability engine runs, the best_guess function returns the tile with the highest chance of progressing the
# game forward with the current information
def best_guess(gameboard, col_x_coords, row_y_coords, potential_clicks, aggregations, unfinished_numbers, bombs_remaining) -> tuple:
    final_guess = (0, 0)

    # find rough probability of a random tile being safe
    closed_tiles_left = len(col_x_coords) * len(row_y_coords)
    for r in range(len(row_y_coords)):
        for c in range(len(col_x_coords)):
            if gameboard[r][c] != -1:
                closed_tiles_left = closed_tiles_left - 1

    safe_chance_picking_random_tile = 1.0 - float((bombs_remaining / closed_tiles_left)) - 0.01

    print()
    print("SAFE CHANCE PICKING RANDOM TILE: ", end="")
    print(safe_chance_picking_random_tile)
    print(bombs_remaining, end="")
    print(" bombs left")
    print()


    # WORST CASE: SEMI-EDUCATED GUESS (a tile not found in potential_clicks will be returned)

    # if potential_clicks is 1.) empty, or 2.) the most-likely-to-be-safe tile (potential_clicks[0]) has a safe_chance
    # value that is less than the safe_chance_picking_random_tile value, then we make a semi-educated guess
    if len(potential_clicks) == 0 or potential_clicks[0][2] < safe_chance_picking_random_tile:
        # CASE #1: if less than 20% of the board has been opened and/or if there is only one aggregation and it's too
        # large to be probed with local search, we resort to clicking a corner tile (if any corners remain unopened)

        if closed_tiles_left > int(len(col_x_coords) * len(row_y_coords) * 0.8) or (len(potential_clicks) == 0 and len(aggregations) == 1 and closed_tiles_left > int(len(col_x_coords) * len(row_y_coords) * 0.5)):
            corners = [(len(col_x_coords) - 1, 0), (0, len(row_y_coords) - 1), (len(col_x_coords) - 1, len(row_y_coords) - 1)]
            for corner in corners:
                if gameboard[corner[1]][corner[0]] == -1:
                    final_guess = corner
                    print("SEMI-EDUCATED GUESS: corner guess")  # for testing
                    return final_guess


        # # CASE #2: find a tile 2 tiles away from an unfinished number tile in a large aggregation
        #
        # # create sub-aggregation (closed tiles that are touching the arregation tiles)
        # sub_aggregation = return_sub_aggregation(gameboard, col_x_coords, row_y_coords, aggregations, unfinished_numbers)
        # # if sub_aggregation isn't empty, we choose the first item as our final_guess value and return
        #  # (other wise we repeat this process for another aggregation)
        # if len(sub_aggregation) != 0:
        #     final_guess = (sub_aggregation[0][0], sub_aggregation[0][1])
        #     print("SEMI-EDUCATED GUESS: 2 tiles from smallest valid aggregation")  # for testing
        #     return final_guess


        # SAFETY CASE: if nothing is returned by this point in the code, we look at all the aggregations and find the
        # border tile with the lowest effective utility value in a 3x3 range
        print("SEMI-EDUCATED GUESS: lowest effective utility within all aggregations")  # for testing
        all_border_tiles = return_all_border_tiles_effective_utility(gameboard, col_x_coords, row_y_coords, unfinished_numbers, aggregations)
        final_guess = (all_border_tiles[0][0], all_border_tiles[0][1])
        return final_guess


    # BEST CASE: EDUCATED GUESS (a border tile from potential_clicks will be returned)

    choice_1 = potential_clicks[0]  # safest tile with highest utility
    choice_2 = return_second_safest_tile(potential_clicks)  # second safest tile with highest utility
    if (choice_2 != None) and (choice_2[3] > choice_1[3] + 2) and (choice_1[2] - choice_2[2] < 0.05) and (choice_2[2] >= 0.75):
        # basically, if the second safest tile's utility value is at least 3 higher than the safest tile's utility,
        # there is less than an 5% difference in safe_chance, and the safe_chance value of the second safest tile is
        # at least 75%, then the second safest tile is returned
        print("BEST GUESS: second safest tile with 3+ higher utility")  # for testing
        final_guess = (choice_2[0], choice_2[1])
    elif (choice_2 != None) and (choice_2[3] > choice_1[3] + 1) and (choice_1[2] - choice_2[2] < 0.03) and (choice_2[2] >= 0.79):
        # basically, if the second safest tile's utility value is at least 2 higher than the safest tile's utility,
        # there is less than an 3% difference in safe_chance, and the safe_chance value of the second safest tile is
        # at least 79%, then the second safest tile is returned
        print("BEST GUESS: second safest tile with 2+ higher utility")  # for testing
        final_guess = (choice_2[0], choice_2[1])
    else:
        # in this case (most cases), the safest tile with the highest utility is returned
        print("BEST GUESS: safest tile")  # for testing
        final_guess = (choice_1[0], choice_1[1])


    return final_guess



# TESTING

# gameboard #1
# gameboard = [
#     [-1, -1, 9, 9, 9, -1, -1],
#     [-1, -1, 4, 3, 3, -1, -1],
#     [-1, -1, 2, 0, 1, -1, -1],
#     [-1, -1, 2, 1, 1, -1, -1],
#     [-1, -1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1, -1],
# ]
# unfinished_numbers = [
#     (2, 1),
#     (2, 2),
#     (2, 3),
#     (3, 3),
#     (4, 1),
#     (4, 2),
#     (4, 3)
# ]
# aggregations = [
#     [(4, 4), (3, 4), (5, 4), (5, 3), (2, 4), (5, 2), (1, 4), (1, 3), (5, 1), (1, 2), (5, 0), (1, 1), (1, 0)]
# ]
# mine_combinations = [
#     [
#         [(2, 4), (5, 2), (1, 2), (1, 1)],
#         [(2, 4), (5, 2), (1, 3), (1, 1), (1, 0)],
#         [(5, 3), (2, 4), (1, 2), (5, 0), (1, 1)],
#         [(5, 3), (2, 4), (1, 3), (5, 0), (1, 1), (1, 0)],
#         [(5, 4), (2, 4), (5, 1), (1, 2), (1, 1)],
#         [(5, 4), (2, 4), (1, 3), (5, 1), (1, 1), (1, 0)],
#         [(3, 4), (5, 1), (1, 2), (1, 1)],
#         [(3, 4), (1, 3), (5, 1), (1, 1), (1, 0)],
#         [(4, 4), (1, 3), (5, 1), (1, 2), (1, 0)],
#         [(4, 4), (1, 4), (5, 1), (1, 2), (1, 1)],
#         [(4, 4), (1, 4), (1, 3), (5, 1), (1, 1), (1, 0)]
#     ]
# ]
# bombs_remaining = 8
# col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420, 5: 450, 6: 480}
# row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250, 4: 280, 5: 310}
#
#
# for i in range(len(row_y_coords)):
#     print(gameboard[i])
# print()
#
#
# potential_clicks = PE.probabilityEngine(gameboard, col_x_coords, row_y_coords, aggregations, mine_combinations, unfinished_numbers)
# print("results of probability engine...")
# for obj in potential_clicks:
#     print(obj)
# print()
#
# print("best guess: ", end="")
# print(best_guess(gameboard, col_x_coords, row_y_coords, potential_clicks, aggregations, unfinished_numbers, bombs_remaining))
# print()
#
# print("sub-aggregations... ")
# sub_aggregation = return_sub_aggregation(gameboard, col_x_coords, row_y_coords, aggregations, unfinished_numbers)
# for item in sub_aggregation:
#     print(item)
# print()
#
# print("all border tiles effective utility values...")
# all_border_tiles_with_effective_utility = return_all_border_tiles_effective_utility(gameboard, col_x_coords, row_y_coords, unfinished_numbers, aggregations)
# for thing in all_border_tiles_with_effective_utility:
#     print(thing)
# print()
#
#
# for i in range(len(row_y_coords)):
#     print(gameboard[i])