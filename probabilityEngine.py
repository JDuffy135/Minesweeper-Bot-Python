import time

# naive approach to calculating utility for a given potential click tile
def return_utility(gameboard, col_x_coords, row_y_coords, unfinished_numbers, tile) -> int:
    utility = 0
    for c in range(tile[0] - 1, tile[0] + 2):
        for r in range(tile[1] - 1, tile[1] + 2):
            if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                if gameboard[r][c] >= 1 and gameboard[r][c] < 9 and ((c, r) in unfinished_numbers):
                    utility = utility + 1
    return utility


# inserts the given tile with the given safe_chance value into the given max priority queue (potential_clicks)
# NOTE: pq orders items first by safe_chance value, then by utility value
def insert_into_pq(pq, tile, safe_chance, gameboard, col_x_coords, row_y_coords, unfinished_numbers) -> None:
    utility = return_utility(gameboard, col_x_coords, row_y_coords, unfinished_numbers, tile)
    new_item = (tile[0], tile[1], safe_chance, utility)
    if len(pq) == 0:
        pq.append(new_item)
    else:
        index = 0
        while index < len(pq):
            if new_item[2] >= pq[index][2]:
                if new_item[2] > pq[index][2]:
                    pq.insert(index, new_item)
                    return
                elif new_item[2] == pq[index][2] and new_item[3] >= pq[index][3]:
                    pq.insert(index, new_item)
                    return
                else:
                    index = index + 1
            else:
                index = index + 1
        pq.append(new_item)
    return


# find probability and utility values for all border tiles in aggregations that were probed with local search
def probabilityEngine(gameboard, col_x_coords, row_y_coords, aggregations, mine_combinations, unfinished_numbers) -> list[tuple]:
    # max priority queue which holds tiles, their respective chance of being safe, and their "utility" (which measures
    # how useful the tile is to the continuation of the game if it turns out to be safe)
    # ENTRY FORMAT: (col: int, row: int, safe_chance: float[0,1], utility: int[0,#_of_tiles_on_board - 1])
    # NOTE: order by "safe_chance" values (highest to lowest since this is a max pq)
    potential_clicks = []

    # for all aggregations with at least 1 valid mine combination, find the probability of each border tile being safe
    for i in range(len(aggregations)):
        total_combinations = len(mine_combinations[i])
        if total_combinations >= 1:
            # for each tile, we count how many of the total combinations the tile occurs in, and subtract this ratio from 1
            # EX: if an aggregation has 11 valid combinations, and a particular tile occurs in 4 of them, then the
            # probability that this tile is safe is 1 - 4/11 = 7/11 chance of being safe
            for border_tile in aggregations[i]:
                count = 0
                for combination in mine_combinations[i]:
                    if border_tile in combination:
                        count = count + 1
                safe_chance = float(1 - (count / total_combinations))
                insert_into_pq(potential_clicks, border_tile, safe_chance, gameboard, col_x_coords, row_y_coords, unfinished_numbers)
                # FOR TESTING
                # print(border_tile, end="")
                # print(" ", end="")
                # print(safe_chance, end="")
                # print(" ", end="")
                # print("count: ", end="")
                # print(count)

    return potential_clicks



# TESTING...

# TESTCASE #1a: 1 aggregation with all valid mine combinations
# expected output:
# [
#   (3, 4, 0.8181818181818181, 3),
#   (5, 4, 0.8181818181818181, 3),
#   (5, 3, 0.8181818181818181, 2),
#   (5, 2, 0.8181818181818181, 1),
#   (1, 4, 0.8181818181818181, 1),
#   ...
# ]
# gameboard = [
#     [-1, -1,  9,  9,  9, -1],
#     [-1, -1,  4,  3,  3, -1],
#     [-1, -1,  2,  0,  1, -1],
#     [-1, -1,  2,  1,  1, -1],
#     [-1, -1, -1, -1, -1, -1],
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
# bombs_remaining = 10
# col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420, 5: 450}
# row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250, 4: 280}


# TESTCASE #1b: 2 aggregations, both with all valid mine combinations
# ...


# TESTCASE #2: 1 aggregation with zero mine combinations
# ...


# TESTCASE #3: 2 aggregations, 1 with all valid mine combinations the other with zero mine combinations
# ...


# TESTCASE #4: 1 aggregation with a guaranteed 50-50 chance mine placement
# ...


# for i in range(len(row_y_coords)):
#     print(gameboard[i])
# print()
#
#
# potential_clicks = probabilityEngine(gameboard, col_x_coords, row_y_coords, aggregations, mine_combinations, unfinished_numbers)
# for item in potential_clicks:
#     print(item)
# print()
#
#
# for i in range(len(row_y_coords)):
#     print(gameboard[i])