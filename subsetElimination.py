import patternRecognition as PR
import copy

# returns a list of disjoint subsets of bordering unopened tiles surrounding the given tile
def return_subsets(gameboard, col_x_coords, row_y_coords, tile) -> list[set]:
    # creating subsets of size 1 for each bordering unopened tile
    subset_list = []
    for c in range(tile[0] - 1, tile[0] + 2):
        for r in range(tile[1] - 1, tile[1] + 2):
            if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                if gameboard[r][c] == -1:
                    cur_subset = set()
                    cur_subset.add((c, r))
                    subset_list.append(cur_subset)

    # merging subsets with adjacent tiles (if multiple subsets exist)
    index = 0
    current_comparison_index = 1
    while index < len(subset_list) - 1:
        break_flag = 0
        while current_comparison_index < len(subset_list):
            for t in subset_list[index]:
                if break_flag == 1:
                    break
                for cmp_t in subset_list[current_comparison_index]:
                    if cmp_t == (t[0] + 1, t[1]) or cmp_t == (t[0] - 1, t[1]) or cmp_t == (t[0], t[1] + 1) or cmp_t == (t[0], t[1] - 1):
                        # if an adjacent tile is found between 2 subsets, we update the set at subset_list[index] to include all the
                        # items from the comparison subset, and consequently delete the comparison subset
                        break_flag = 1
                        break
            # INNER LOOP: check if break from inner while loop or to continue to next comparison subset
            if break_flag == 1:
                subset_list[index].update(subset_list[current_comparison_index])
                subset_list.pop(current_comparison_index)
                break
            else:
                current_comparison_index = current_comparison_index + 1
        # OUTTER LOOP: check if subsets were merged
        if break_flag == 1:
            # restart from beginning if subsets were merged
            index = 0
            current_comparison_index = 1
        else:
            # start process from the next index if no subsets were merged
            index = index + 1
            current_comparison_index = index + 1

    return subset_list


# given two subsets, return True if they overlap entirely (AKA one subset is completely contained within the other)
# and are different sizes - return False otherwise
def is_overlapping_and_different_size(subset_a, subset_b) -> bool:
    if len(subset_a) == len(subset_b):
        return False

    # checking if every element in subset_a is in subset_b
    successes = 0
    for a in subset_a:
        if a not in subset_b:
            break
        else:
            successes = successes + 1
    if successes == len(subset_a):
        return True

    # checking if every element in subset_b is in subset_a
    successes = 0
    for b in subset_b:
        if b not in subset_a:
            break
        else:
            successes = successes + 1
    if successes == len(subset_b):
        return True

    return False


# orders overlapping subset entries in order of decreasing subset length
def return_ordered_overlapping_subsets(overlapping_subsets) -> list[int , set]:
    overlapping_subsets_ordered = []

    for item in overlapping_subsets:
        if len(overlapping_subsets_ordered) == 0:
            overlapping_subsets_ordered.append(item)
            continue

        index = 0
        while index < len(overlapping_subsets_ordered):
            if len(item[1]) > len(overlapping_subsets_ordered[index][1]):
                overlapping_subsets_ordered.insert(index, item)
                break
            else:
                index = index + 1

        overlapping_subsets_ordered.append(item)

    return overlapping_subsets_ordered


# performs subset elimination on the given set of overlapping subsets (with each subset's respective effective number
# value at index 0 of each tuple) - returns a list where index 0 is the number of mines to (potentially) be placed, and
# index 1 is a set of border tiles in which to place said mines if result is valid
def perform_subset_elimination(overlapping_subsets) -> list[int, set]:
    result = [0, set()]
    if len(overlapping_subsets) < 2:
        # note: this case shouldn't occur but adding it as a safety measure
        print("WHYYYYYYYYYYYYYYYYY (overlapping subset list of size less than 2 is present)")
        return result
    else:
        overlapping_subsets_copy = copy.deepcopy(overlapping_subsets)
        # print("OVERLAPPING SUBSETS COPY")  # for testing
        # print(overlapping_subsets_copy)  # for testing
        while len(overlapping_subsets_copy) > 1:
            # STEP 1: order items in order of decreasing subset length
            overlapping_subsets_ordered = return_ordered_overlapping_subsets(overlapping_subsets_copy)
            # print("OVERLAPPING SUBSET ORDERED")  # for testing
            # print(overlapping_subsets_ordered)  # for testing

            # STEP 2: subset elimination on first 2 elements in overlapping_subsets_ordered
            bigger_subset = overlapping_subsets_ordered[0]
            smaller_subset = overlapping_subsets_ordered[1]
            new_effective_number = bigger_subset[0] - smaller_subset[0]
            new_set = bigger_subset[1] - smaller_subset[1]
            resulting_item = [new_effective_number, new_set]

            # STEP 3: update overlapping_subsets_copy
            overlapping_subsets_copy.remove(bigger_subset)
            overlapping_subsets_copy.remove(smaller_subset)
            overlapping_subsets_copy.insert(0, resulting_item)

        result = overlapping_subsets_copy[0]

    return result


# attempts to place mines around an aggregation using subset elimination
def subset_elimination(gameboard, col_x_coords, row_y_coords, bordering_unfinished_numbers) -> list[tuple]:
    # create temporary copy of gameboard and initialize mine tiles list (these mines will be placed on the actual
    # (gameboard at the end if the final mine combination is valid)
    tmp_gameboard = copy.deepcopy(gameboard)
    final_mine_tiles = []

    loop_flag = 1
    while loop_flag == 1:
        # print("NEW ITERATION")  # for testing

        # STEP 1: initialize groups dictionary
        # 'groups' dictionary format - KEY: num_tile (col, row), VALUE: [effective_number_value, list of subsets]
        # NOTE: the list of subsets contain border tiles from the aggregation (within 3x3 range of the given number tile),
        # and we maintain a list of subsets since a single tile can have multiple disjoint subsets (if a mine or another
        # number tile is placed in between border tiles)
        groups = {}
        for num_tile in bordering_unfinished_numbers:
            effective_value = PR.compute_effective_tile_number(tmp_gameboard, col_x_coords, row_y_coords, num_tile)
            subset_list = return_subsets(tmp_gameboard, col_x_coords, row_y_coords, num_tile)
            groups[num_tile] = [effective_value, subset_list]

        # FOR TESTING
        # print("GROUPS")
        # for group in groups:
        #     print(groups.get(group))
        # print()


        # STEP 2: subset elimination on all overlapping subsets of different sizes
        # finding all overlapping subsets
        overlapping_subsets = []  # list[tuple[num_tile, set(border_tiles)]]
        for i in range(len(bordering_unfinished_numbers)):
            num_tile = bordering_unfinished_numbers[i]
            num_tile_subset_list = groups.get(num_tile)[1]
            for subset in num_tile_subset_list:
                cur_overlapping_subsets = [(groups.get(num_tile)[0], subset)]
                for j in range(len(bordering_unfinished_numbers)):
                    cmp_num_tile = bordering_unfinished_numbers[j]
                    cmp_num_tile_subset_list = groups.get(cmp_num_tile)[1]
                    for cmp_subset in cmp_num_tile_subset_list:
                        if is_overlapping_and_different_size(subset, cmp_subset) == True:
                            unique_flag = 1
                            for item in cur_overlapping_subsets:
                                # this is here so that we only add unique subsets to cur_overlapping_subsets
                                if item[1] == cmp_subset:
                                    unique_flag = 0
                                    break
                            if unique_flag == 1:
                                cur_overlapping_subsets.append((groups.get(cmp_num_tile)[0], cmp_subset))
                if len(cur_overlapping_subsets) > 1:
                    overlapping_subsets.append(cur_overlapping_subsets)

        # FOR TESTING
        # print("OVERLAPPING SUBSETS")
        # for item in overlapping_subsets:
        #     print(item)
        # print()

        # subset elimination on all overlapping subsets
        subset_elimination_valid_results = []
        for overlapping_subset_list in overlapping_subsets:
            cur_result = perform_subset_elimination(overlapping_subset_list)
            # only add cur_result to the list of subset elimination results if the result is a 'valid' result
            if cur_result[0] > 0 and cur_result[0] == len(cur_result[1]) and cur_result not in subset_elimination_valid_results:
                subset_elimination_valid_results.append(cur_result)

        # FOR TESTING
        # print("VALID SUBSET ELIMINATION RESULTS")
        # for item in subset_elimination_valid_results:
        #     print(item)
        # print()

        # break from loop if no valid results
        if len(subset_elimination_valid_results) == 0:
            loop_flag = 0
            break


        # STEP 3: iterate through subset_elimination_valid_results and add mines to valid positions
        for result in subset_elimination_valid_results:
            for position in result[1]:
                tmp_gameboard[position[1]][position[0]] = 9
                final_mine_tiles.append((position[0], position[1]))

        # FOR TESTING
        # print("CURRENT GAME BOARD:")
        # for row in tmp_gameboard:
        #     print(row)
        # print()


    # FINAL STEP: checking if final mine combination is valid
    # return early if no mines were found
    if len(final_mine_tiles) == 0:
        print("   NO MINES FOUND IN SUBSET ELIMINATION")
        return []

    # return early with empty list if any of the number tiles are oversatisfied (AKA final combination is not valid)
    for num_tile in bordering_unfinished_numbers:
        effective_value = PR.compute_effective_tile_number(tmp_gameboard, col_x_coords, row_y_coords, num_tile)
        if effective_value < 0:
            print("   SUBSET ELIMINATION FOUND INVALID COMBINATION")
            return []

    # if final combination is valid, we place the mines onto the actual gameboard
    for mine in final_mine_tiles:
        gameboard[mine[1]][mine[0]] = 9

    print("VALID MINE PLACEMENTS FROM SUBSET ELIMINATION...")  # for testing
    for item in final_mine_tiles:  # for testing
        print(item)  # for testing
    print()  # for testing

    return final_mine_tiles



# FOR TESTING

# GAME BOARD #1
# gameboard = [
#     [-1,  1,  0,  0,  0],
#     [-1,  2,  0,  0,  0],
#     [-1,  2,  1,  2,  1],
#     [-1, -1, -1, -1, -1],
# ]
# bordering_unfinished_numbers = [
#     (1, 0),
#     (1, 1),
#     (1, 2),
#     (2, 2),
#     (3, 2),
#     (4, 2)
# ]
# col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420}
# row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250}


# GAME BOARD #2
# gameboard = [
#     [-1,  1,  0,  0],
#     [-1,  2,  2,  1],
#     [-1, -1, -1, -1]
# ]
# bordering_unfinished_numbers = [
#     (1, 0),
#     (1, 1),
#     (2, 1),
#     (3, 1)
# ]
# col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390}
# row_y_coords = {0: 160, 1: 190, 2: 220}
#
#
#
# result = subset_elimination(gameboard, col_x_coords, row_y_coords, bordering_unfinished_numbers)
# print("result of subset elimination: ", end="")
# print(result)
#
# print()
# print("gameboard after running subset elimination...")
# for row in gameboard:
#     print(row)

# for tile in bordering_unfinished_numbers:
#     print("TILE: ", end="")
#     print(tile, end="")
#     print("  (tile number: ", end="")
#     print(gameboard[tile[1]][tile[0]], end="")
#     print(")")
#     print(return_subsets(gameboard, col_x_coords, row_y_coords, tile))
#     print()