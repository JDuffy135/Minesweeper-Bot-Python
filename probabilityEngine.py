import time

# inserts the given tile with the given safe_chance value into the given max priority queue (potential_clicks)
def insert_into_pq(pq, tile, safe_chance) -> None:
    new_item = (tile[0], tile[1], safe_chance, float(0))
    if len(pq) == 0:
        pq.append(new_item)
    else:
        index = 0
        while index < len(pq):
            if new_item[2] > pq[index][2]:
                pq.insert(index, new_item)
                return
            else:
                index = index + 1
        pq.append(new_item)
    return


# ...
def probabilityEngine(gameboard, col_x_coords, row_y_coords, aggregations, mine_combinations, bombs_remaining) -> list[tuple]:
    start = time.time()
    # max priority queue which holds tiles, their respective chance of being safe, and their chance of game resulting in a win if clicked
    # format of each entry: (col: int, row: int, safe_chance: float[0,1], win_chance: float[0,1])
    # NOTE: order by "safe_chance" values (highest to lowest since this is a max pq)
    # OTHER NOTE: "win_chance" values will all be 0 at this stage in the algorithm (handled in DEEP ANALYSIS step)
    potential_clicks = []

    for i in range(len(aggregations)):
        total_combinations = len(mine_combinations[i])
        if total_combinations >= 1:
            # CASE #1: if there is AT LEAST ONE valid mine combination for the current aggregation i, then
            # mine_combinations[i] will contain every valid combination of mines for aggregation i - in this case, for
            # each tile, we count how many of the total combinations the tile occurs in, and subtract this ratio from 1
            # EX: if an aggregation has 11 possible combinations, and a particular tile occurs in 5 of them, then the
            # probability that this tile is safe is 1 - 5/11 = 6/11 chance of being safe
            for border_tile in aggregations[i]:
                count = 0
                for combination in mine_combinations[i]:
                    if border_tile in combination:
                        count = count + 1
                safe_chance = float(1 - (count / total_combinations))
                insert_into_pq(potential_clicks, border_tile, safe_chance)
                # FOR TESTING
                # print(border_tile, end="")
                # print(" ", end="")
                # print(safe_chance, end="")
                # print(" ", end="")
                # print("count: ", end="")
                # print(count)

    # find probability of a random tile with no bordering number tiles being safe
    safe_chance_picking_random_tile = float(0)  # note: still need to implement this calcuation

    # if potential_clicks is empty or the most likely-to-be-safe tile has a safe_chance value that is lower than
    # safe_chance_picking_random_tile, then we make a semi-educated guess clicking a random tile on the board
    if len(potential_clicks) == 0:
        print("PLACEHOLDER")
        return []

    print(time.time() - start)
    return potential_clicks



# TESTING...

# TESTCASE #1a: 1 aggregation with all valid mine combinations
# expected output:
# [
#   (3, 4, 0.8181818181818181, 0.0),
#   (5, 4, 0.8181818181818181, 0.0),
#   (5, 3, 0.8181818181818181, 0.0),
#   (5, 2, 0.8181818181818181, 0.0),
#   (1, 4, 0.8181818181818181, 0.0),
#   ...
# ]
gameboard = [
    [-1, -1, 9, 9, 9, -1],
    [-1, -1, 4, 3, 3, -1],
    [-1, -1, 2, 0, 1, -1],
    [-1, -1, 2, 1, 1, -1],
    [-1, -1, -1, -1, -1, -1],
]
aggregations = [
    [(4, 4), (3, 4), (5, 4), (5, 3), (2, 4), (5, 2), (1, 4), (1, 3), (5, 1), (1, 2), (5, 0), (1, 1), (1, 0)]
]
mine_combinations = [
    [
        [(2, 4), (5, 2), (1, 2), (1, 1)],
        [(2, 4), (5, 2), (1, 3), (1, 1), (1, 0)],
        [(5, 3), (2, 4), (1, 2), (5, 0), (1, 1)],
        [(5, 3), (2, 4), (1, 3), (5, 0), (1, 1), (1, 0)],
        [(5, 4), (2, 4), (5, 1), (1, 2), (1, 1)],
        [(5, 4), (2, 4), (1, 3), (5, 1), (1, 1), (1, 0)],
        [(3, 4), (5, 1), (1, 2), (1, 1)],
        [(3, 4), (1, 3), (5, 1), (1, 1), (1, 0)],
        [(4, 4), (1, 3), (5, 1), (1, 2), (1, 0)],
        [(4, 4), (1, 4), (5, 1), (1, 2), (1, 1)],
        [(4, 4), (1, 4), (1, 3), (5, 1), (1, 1), (1, 0)]
    ]
]
bombs_remaining = 10
col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420, 5: 450}
row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250, 4: 280}


# TESTCASE #1b: 2 aggregations, both with all valid mine combinations
# ...


# TESTCASE #2: 1 aggregation with zero mine combinations
# ...


# TESTCASE #3: 2 aggregations, 1 with all valid mine combinations the other with zero mine combinations
# ...


# TESTCASE #4: 1 aggregation with a guaranteed 50-50 chance mine placement
# ...


for i in range(len(row_y_coords)):
    print(gameboard[i])
print()


potential_clicks = probabilityEngine(gameboard, col_x_coords, row_y_coords, aggregations, mine_combinations, bombs_remaining)
for item in potential_clicks:
    print(item)
print()


for i in range(len(row_y_coords)):
    print(gameboard[i])