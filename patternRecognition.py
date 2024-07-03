# if the given tile is a number tile, return True (return False otherwise)
def is_number(gameboard, tile) -> bool:
    if tile[1] >= len(gameboard) or tile[0] >= len(gameboard[0]) or tile[0] < 0 or tile[1] < 0:
        # out of bounds check
        return False
    if gameboard[tile[1]][tile[0]] > 0 and gameboard[tile[1]][tile[0]] < 9:
        # checking if number tile
        return True
    # return False if not number tile
    return False

# if a vertical pattern is found, check if closed tiles are to the right (1) or to the left (0) of the input tile
# (if neither side is clear: return -1, and if both are clear: return -2)
# NOTE: 'tiles' list should include every tile in the pattern
def check_is_clear_vertical(gameboard:list[list[int]], tiles:list[tuple[int,int,int]]) -> int:
    return_value = -1

    # checking to make sure all tiles TO THE RIGHT of the pattern are -1
    if tiles[0][0] < len(gameboard[0]) - 1:
        for i in range(len(tiles)):
            if i == len(tiles) - 1 and gameboard[tiles[i][1]][tiles[i][0] + 1] == -1:
                return_value = 1  # in this case, right is clear
            if gameboard[tiles[i][1]][tiles[i][0] + 1] != -1:
                break

    # checking to make sure all tiles TO THE LEFT of the pattern are -1
    if tiles[0][0] > 0:
        for i in range(len(tiles)):
            if i == len(tiles) - 1 and gameboard[tiles[i][1]][tiles[i][0] - 1] == -1:
                if return_value == 1:
                    return -2  # in this case, right is clear AND left is clear
                else:
                    return 0  # in this case, only left is clear
            if gameboard[tiles[i][1]][tiles[i][0] - 1] != -1:
                break

    # return_value will be -1 if neither of the if statement modified the return_value value
    return return_value


# if a horizontal pattern is found, check if closed tiles are above (1) or below (0) the input tile
# (if neither side is clear: return -1, and if both are clear: return -2)
# NOTE: 'tiles' list should include every tile in the pattern
def check_is_clear_horizontal(gameboard:list[list[int]], tiles:list[tuple[int,int,int]]) -> int:
    return_value = -1

    # checking to make sure all tiles ABOVE the pattern are -1
    if tiles[0][1] > 0:
        for i in range(len(tiles)):
            if i == len(tiles) - 1 and gameboard[tiles[i][1] - 1][tiles[i][0]] == -1:
                return_value = 1  # in this case, above is clear
            if gameboard[tiles[i][1] - 1][tiles[i][0]] != -1:
                break

    # checking to make sure all tiles BELOW the pattern are -1
    if tiles[0][1] < len(gameboard) - 1:
        for i in range(len(tiles)):
            if i == len(tiles) - 1 and gameboard[tiles[i][1] + 1][tiles[i][0]] == -1:
                if return_value == 1:
                    return -2  # in this case, above is clear AND below is clear
                else:
                    return 0  # in this case, only below is clear
            if gameboard[tiles[i][1] + 1][tiles[i][0]] != -1:
                break

    # return_value will be -1 if neither of the if statement modified the return_value value
    return return_value


# for a given number tile, computes its effective number (AKA how many mines there are left to be placed around it)
def compute_effective_tile_number(gameboard, col_x_coords, row_y_coords, tile) -> int:
    effective_number = gameboard[tile[1]][tile[0]]
    for c in range(tile[0] - 1, tile[0] + 2):
        for r in range(tile[1] - 1, tile[1] + 2):
            if (c >= 0 and c < len(col_x_coords)) and (r >= 0 and r < len(row_y_coords)):
                if gameboard[r][c] == 9:
                    effective_number = effective_number - 1
    return effective_number


# returns a list containing 2 more lists: 1.) mines placed on gameboard, and 2.) tiles to be clicked
# NOTE: not particularly comprehensive; only checks for a few common patterns in certain orientations - in most cases,
# if an aggregation is too large to be probed with local search, we won't be able to make any decisive moves around
# said aggregation(s)
def pattern_recognition(gameboard:list[list[int]], col_x_coords:dict, row_y_coords:dict, bordering_unfinished_numbers:list, bombs_remaining:int) -> list[list[tuple], list[tuple]]:
    mine_tiles = []
    click_tiles = []

    stop_flag = 0
    while stop_flag == 0:
        # this value gets set back to 0 if a pattern is found
        stop_flag = 1
        print("   SEARCHING FOR PATTERNS...")  # FOR TESTING

        # STEP #1: for each bordering unfinished number tile, compute it's effective number (AKA how many mines remain
        # to be placed) and remove tiles from the input list if their effective number value is 0 (note: this should
        # never occur on the first iteration of the outer while loop)
        eff_nums = []
        index = 0
        while index < len(bordering_unfinished_numbers):
            tile = bordering_unfinished_numbers[index]
            effective_num = compute_effective_tile_number(gameboard, col_x_coords, row_y_coords, tile)
            if effective_num == 0:
                bordering_unfinished_numbers.remove(tile)
            else:
                tile_tup = (tile[0], tile[1], effective_num)
                eff_nums.append(tile_tup)
                index = index + 1

        # FOR TESTING
        print("   CURRENT EFFECTIVE NUMBERS: ", end="")
        print(eff_nums)


        # STEP #2: for each '1' tile in eff_numbers, we check for the precence of each pattern in all directions
        # (order of directional checks: up, right, down, left)
        for t in eff_nums:
            if t[2] != 1:
                continue  # note: since all patterns start with 1, we don't care about other numbers
            cur_tiles = []
            clear_check = -1
            cur_tiles_ver = []
            cur_tiles_hor = []
            clear_check_ver = []
            clear_check_hor = []

            # 2a.) check for 1-2-1 patterns...
            if ((t[0], t[1] - 1, 2) in eff_nums) and ((t[0], t[1] - 2, 1) in eff_nums):
                # vertical
                cur_tiles = [t, (t[0], t[1] - 1, 2), (t[0], t[1] - 2, 1)]
                clear_check = check_is_clear_vertical(gameboard, cur_tiles)
                if clear_check == 1:
                    # place mines to the right
                    gameboard[t[1]][t[0] + 1] = 9
                    gameboard[t[1] - 2][t[0] + 1] = 9
                    mine_tiles.append((t[0] + 1, t[1]))
                    mine_tiles.append((t[0] + 1, t[1] - 2))
                    click_tiles.append((t[0] + 1, t[1] - 1))
                elif clear_check == 0:
                    # place mines to the left
                    gameboard[t[1]][t[0] - 1] = 9
                    gameboard[t[1] - 2][t[0] - 1] = 9
                    mine_tiles.append((t[0] - 1, t[1]))
                    mine_tiles.append((t[0] - 1, t[1] - 2))
                    click_tiles.append((t[0] - 1, t[1] - 1))
                if clear_check >= 0:
                    stop_flag = 0
                    break
            elif ((t[0] + 1, t[1], 2) in eff_nums) and ((t[0] + 2, t[1], 1) in eff_nums):
                # horizontal
                cur_tiles = [t, (t[0] + 1, t[1], 2), (t[0] + 2, t[1], 1)]
                clear_check = check_is_clear_horizontal(gameboard, cur_tiles)
                if clear_check == 1:
                    # place mines above
                    gameboard[t[1] - 1][t[0]] = 9
                    gameboard[t[1] - 1][t[0] + 2] = 9
                    mine_tiles.append((t[0], t[1] - 1))
                    mine_tiles.append((t[0] + 2, t[1] - 1))
                    click_tiles.append((t[0] + 1, t[1] - 1))
                elif clear_check == 0:
                    # place mines below
                    gameboard[t[1] + 1][t[0]] = 9
                    gameboard[t[1] + 1][t[0] + 2] = 9
                    mine_tiles.append((t[0], t[1] + 1))
                    mine_tiles.append((t[0] + 2, t[1] + 1))
                    click_tiles.append((t[0] + 1, t[1] + 1))
                if clear_check >= 0:
                    stop_flag = 0
                    break


            # 2b.) check for 1-2-2-1 patterns...
            if ((t[0], t[1] - 1, 2) in eff_nums) and ((t[0], t[1] - 2, 2) in eff_nums) and ((t[0], t[1] - 3, 1) in eff_nums):
                # vertical
                cur_tiles = [t, (t[0], t[1] - 1, 2), (t[0], t[1] - 2, 2), (t[0], t[1] - 3, 1)]
                clear_check = check_is_clear_vertical(gameboard, cur_tiles)
                if clear_check == 1:
                    # place mines to the right
                    gameboard[t[1] - 1][t[0] + 1] = 9
                    gameboard[t[1] - 2][t[0] + 1] = 9
                    mine_tiles.append((t[0] + 1, t[1] - 1))
                    mine_tiles.append((t[0] + 1, t[1] - 2))
                    click_tiles.append((t[0] + 1, t[1]))
                    click_tiles.append((t[0] + 1, t[1] - 3))
                elif clear_check == 0:
                    # place mines to the left
                    gameboard[t[1] - 1][t[0] - 1] = 9
                    gameboard[t[1] - 2][t[0] - 1] = 9
                    mine_tiles.append((t[0] - 1, t[1] - 1))
                    mine_tiles.append((t[0] - 1, t[1] - 2))
                    click_tiles.append((t[0] - 1, t[1]))
                    click_tiles.append((t[0] - 1, t[1] - 3))
                if clear_check >= 0:
                    stop_flag = 0
                    break
            elif ((t[0] + 1, t[1], 2) in eff_nums) and ((t[0] + 2, t[1], 2) in eff_nums) and ((t[0] + 3, t[1], 1) in eff_nums):
                # horizontal
                cur_tiles = [t, (t[0] + 1, t[1], 2), (t[0] + 2, t[1], 2), (t[0] + 3, t[1], 1)]
                clear_check = check_is_clear_horizontal(gameboard, cur_tiles)
                if clear_check == 1:
                    # place mines above
                    gameboard[t[1] - 1][t[0] + 1] = 9
                    gameboard[t[1] - 1][t[0] + 2] = 9
                    mine_tiles.append((t[0] + 1, t[1] - 1))
                    mine_tiles.append((t[0] + 2, t[1] - 1))
                    click_tiles.append((t[0], t[1] - 1))
                    click_tiles.append((t[0] + 3, t[1] - 1))
                elif clear_check == 0:
                    # place mines below
                    gameboard[t[1] + 1][t[0] + 1] = 9
                    gameboard[t[1] + 1][t[0] + 2] = 9
                    mine_tiles.append((t[0] + 1, t[1] + 1))
                    mine_tiles.append((t[0] + 2, t[1] + 1))
                    click_tiles.append((t[0], t[1] + 1))
                    click_tiles.append((t[0] + 3, t[1] + 1))
                if clear_check >= 0:
                    stop_flag = 0
                    break


            # 2c.) check for consecutive patterns on a corner stemming from vertical 1-2-1 pattern...
            if ((t[0], t[1] - 1, 2) in eff_nums) and ((t[0], t[1] - 2, 2) in eff_nums):
                # ONE: (closed tiles on outter top and left)
                # 2 2 1
                # 2
                # 1
                if ((t[0] + 1, t[1] - 2, 2) in eff_nums) and ((t[0] + 2, t[1] - 2, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] - 1, 2), (t[0], t[1] - 2, 2)]
                    cur_tiles_hor = [(t[0], t[1] - 2, 2), (t[0] + 1, t[1] - 2, 2), (t[0] + 2, t[1] - 2, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 0 and clear_check_hor == 1:
                        gameboard[t[1]][t[0] - 1] = 9
                        gameboard[t[1] - 2][t[0] - 1] = 9
                        gameboard[t[1] - 3][t[0]] = 9
                        gameboard[t[1] - 3][t[0] + 2] = 9
                        mine_tiles.append((t[0] - 1, t[1]))
                        mine_tiles.append((t[0] - 1, t[1] - 2))
                        mine_tiles.append((t[0], t[1] - 3))
                        mine_tiles.append((t[0] + 2, t[1] - 3))
                        click_tiles.append((t[0] - 1, t[1] - 1))
                        click_tiles.append((t[0] + 1, t[1] - 3))
                        stop_flag = 0
                        break

                # TWO: (closed tiles on outter top and right)
                # 1 2 2
                #     2
                #     1
                if ((t[0] - 1, t[1] - 2, 2) in eff_nums) and ((t[0] - 2, t[1] - 2, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] - 1, 2), (t[0], t[1] - 2, 2)]
                    cur_tiles_hor = [(t[0], t[1] - 2, 2), (t[0] - 1, t[1] - 2, 2), (t[0] - 2, t[1] - 2, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 1 and clear_check_hor == 1:
                        gameboard[t[1]][t[0] + 1] = 9
                        gameboard[t[1] - 2][t[0] + 1] = 9
                        gameboard[t[1] - 3][t[0]] = 9
                        gameboard[t[1] - 3][t[0] - 2] = 9
                        mine_tiles.append((t[0] + 1, t[1]))
                        mine_tiles.append((t[0] + 1, t[1] - 2))
                        mine_tiles.append((t[0], t[1] - 3))
                        mine_tiles.append((t[0] - 2, t[1] - 3))
                        click_tiles.append((t[0] + 1, t[1] - 1))
                        click_tiles.append((t[0] - 1, t[1] - 3))
                        stop_flag = 0
                        break

                # THREE: (closed tiles on outter top and left)
                # 2 2 2 1
                # 2
                # 1
                if ((t[0] + 1, t[1] - 2, 2) in eff_nums) and ((t[0] + 2, t[1] - 2, 2) in eff_nums) and ((t[0] + 3, t[1] - 2, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] - 1, 2), (t[0], t[1] - 2, 2)]
                    cur_tiles_hor = [(t[0], t[1] - 2, 2), (t[0] + 1, t[1] - 2, 2), (t[0] + 2, t[1] - 2, 2), (t[0] + 3, t[1] - 2, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 0 and clear_check_hor == 1:
                        gameboard[t[1]][t[0] - 1] = 9
                        gameboard[t[1] - 2][t[0] - 1] = 9
                        gameboard[t[1] - 3][t[0] + 1] = 9
                        gameboard[t[1] - 3][t[0] + 2] = 9
                        mine_tiles.append((t[0] - 1, t[1]))
                        mine_tiles.append((t[0] - 1, t[1] - 2))
                        mine_tiles.append((t[0] + 1, t[1] - 3))
                        mine_tiles.append((t[0] + 2, t[1] - 3))
                        click_tiles.append((t[0] - 1, t[1] - 1))
                        click_tiles.append((t[0], t[1] - 3))
                        click_tiles.append((t[0] + 3, t[1] - 3))
                        stop_flag = 0
                        break

                # FOUR: (closed tiles on outter top and right)
                # 1 2 2 2
                #       2
                #       1
                if ((t[0] - 1, t[1] - 2, 2) in eff_nums) and ((t[0] - 2, t[1] - 2, 2) in eff_nums) and ((t[0] - 3, t[1] - 2, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] - 1, 2), (t[0], t[1] - 2, 2)]
                    cur_tiles_hor = [(t[0], t[1] - 2, 2), (t[0] - 1, t[1] - 2, 2), (t[0] - 2, t[1] - 2, 2), (t[0] - 3, t[1] - 2, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 1 and clear_check_hor == 1:
                        gameboard[t[1]][t[0] + 1] = 9
                        gameboard[t[1] - 2][t[0] + 1] = 9
                        gameboard[t[1] - 3][t[0] - 1] = 9
                        gameboard[t[1] - 3][t[0] - 2] = 9
                        mine_tiles.append((t[0] + 1, t[1]))
                        mine_tiles.append((t[0] + 1, t[1] - 2))
                        mine_tiles.append((t[0] - 1, t[1] - 3))
                        mine_tiles.append((t[0] - 2, t[1] - 3))
                        click_tiles.append((t[0] + 1, t[1] - 1))
                        click_tiles.append((t[0], t[1] - 3))
                        click_tiles.append((t[0] - 3, t[1] - 3))
                        stop_flag = 0
                        break

            if ((t[0], t[1] + 1, 2) in eff_nums) and ((t[0], t[1] + 2, 2) in eff_nums):
                # FIVE: (closed tiles on outter bottom and left)
                # 1
                # 2
                # 2 2 1
                if ((t[0] + 1, t[1] + 2, 2) in eff_nums) and ((t[0] + 2, t[1] + 2, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] + 1, 2), (t[0], t[1] + 2, 2)]
                    cur_tiles_hor = [(t[0], t[1] + 2, 2), (t[0] + 1, t[1] + 2, 2), (t[0] + 2, t[1] + 2, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 0 and clear_check_hor == 0:
                        gameboard[t[1]][t[0] - 1] = 9
                        gameboard[t[1] + 2][t[0] - 1] = 9
                        gameboard[t[1] + 3][t[0]] = 9
                        gameboard[t[1] + 3][t[0] + 2] = 9
                        mine_tiles.append((t[0] - 1, t[1]))
                        mine_tiles.append((t[0] - 1, t[1] + 2))
                        mine_tiles.append((t[0], t[1] + 3))
                        mine_tiles.append((t[0] + 2, t[1] + 3))
                        click_tiles.append((t[0] - 1, t[1] + 1))
                        click_tiles.append((t[0] + 1, t[1] + 3))
                        stop_flag = 0
                        break

                # SIX: (closed tiles on outter bottom and right)
                #     1
                #     2
                # 1 2 2
                if ((t[0] - 1, t[1] + 2, 2) in eff_nums) and ((t[0] - 2, t[1] + 2, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] + 1, 2), (t[0], t[1] + 2, 2)]
                    cur_tiles_hor = [(t[0], t[1] + 2, 2), (t[0] - 1, t[1] + 2, 2), (t[0] - 2, t[1] + 2, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 1 and clear_check_hor == 0:
                        gameboard[t[1]][t[0] + 1] = 9
                        gameboard[t[1] + 2][t[0] + 1] = 9
                        gameboard[t[1] + 3][t[0]] = 9
                        gameboard[t[1] + 3][t[0] - 2] = 9
                        mine_tiles.append((t[0] + 1, t[1]))
                        mine_tiles.append((t[0] + 1, t[1] + 2))
                        mine_tiles.append((t[0], t[1] + 3))
                        mine_tiles.append((t[0] - 2, t[1] + 3))
                        click_tiles.append((t[0] + 1, t[1] + 1))
                        click_tiles.append((t[0] - 1, t[1] + 3))
                        stop_flag = 0
                        break

                # SEVEN: (closed tiles on outter bottom and left)
                # 1
                # 2
                # 2 2 2 1
                if ((t[0] + 1, t[1] + 2, 2) in eff_nums) and ((t[0] + 2, t[1] + 2, 2) in eff_nums) and ((t[0] + 3, t[1] + 2, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] + 1, 2), (t[0], t[1] + 2, 2)]
                    cur_tiles_hor = [(t[0], t[1] + 2, 2), (t[0] + 1, t[1] + 2, 2), (t[0] + 2, t[1] + 2, 2), (t[0] + 3, t[1] + 2, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 0 and clear_check_hor == 0:
                        gameboard[t[1]][t[0] - 1] = 9
                        gameboard[t[1] + 2][t[0] - 1] = 9
                        gameboard[t[1] + 3][t[0] + 1] = 9
                        gameboard[t[1] + 3][t[0] + 2] = 9
                        mine_tiles.append((t[0] - 1, t[1]))
                        mine_tiles.append((t[0] - 1, t[1] + 2))
                        mine_tiles.append((t[0] + 1, t[1] + 3))
                        mine_tiles.append((t[0] + 2, t[1] + 3))
                        click_tiles.append((t[0] - 1, t[1] + 1))
                        click_tiles.append((t[0], t[1] + 3))
                        click_tiles.append((t[0] + 3, t[1] + 3))
                        stop_flag = 0
                        break

                # EIGHT: (closed tiles on outter bottom and right)
                #       1
                #       2
                # 1 2 2 2
                if ((t[0] - 1, t[1] + 2, 2) in eff_nums) and ((t[0] - 2, t[1] + 2, 2) in eff_nums) and ((t[0] - 3, t[1] + 2, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] + 1, 2), (t[0], t[1] + 2, 2)]
                    cur_tiles_hor = [(t[0], t[1] + 2, 2), (t[0] - 1, t[1] + 2, 2), (t[0] - 2, t[1] + 2, 2), (t[0] - 3, t[1] + 2, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 1 and clear_check_hor == 0:
                        gameboard[t[1]][t[0] + 1] = 9
                        gameboard[t[1] + 2][t[0] + 1] = 9
                        gameboard[t[1] + 3][t[0] - 1] = 9
                        gameboard[t[1] + 3][t[0] - 2] = 9
                        mine_tiles.append((t[0] + 1, t[1]))
                        mine_tiles.append((t[0] + 1, t[1] + 2))
                        mine_tiles.append((t[0] - 1, t[1] + 3))
                        mine_tiles.append((t[0] - 2, t[1] + 3))
                        click_tiles.append((t[0] + 1, t[1] + 1))
                        click_tiles.append((t[0], t[1] + 3))
                        click_tiles.append((t[0] - 3, t[1] + 3))
                        stop_flag = 0
                        break


            # 2d.) check for consecutive patterns on a corner stemming from vertical 1-2-2-1 pattern...
            if ((t[0], t[1] - 1, 2) in eff_nums) and ((t[0], t[1] - 2, 2) in eff_nums) and ((t[0], t[1] - 3, 2) in eff_nums):
                # ONE: (closed tiles on outter top and left)
                # 2 2 2 1
                # 2
                # 2
                # 1
                if ((t[0] + 1, t[1] - 3, 2) in eff_nums) and ((t[0] + 2, t[1] - 3, 2) in eff_nums)  and ((t[0] + 3, t[1] - 3, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] - 1, 2), (t[0], t[1] - 2, 2), (t[0], t[1] - 3, 2)]
                    cur_tiles_hor = [(t[0], t[1] - 3, 2), (t[0] + 1, t[1] - 3, 2), (t[0] + 2, t[1] - 3, 2), (t[0] + 3, t[1] - 3, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 0 and clear_check_hor == 1:
                        gameboard[t[1] - 1][t[0] - 1] = 9
                        gameboard[t[1] - 2][t[0] - 1] = 9
                        gameboard[t[1] - 4][t[0] + 1] = 9
                        gameboard[t[1] - 4][t[0] + 2] = 9
                        mine_tiles.append((t[0] - 1, t[1] - 1))
                        mine_tiles.append((t[0] - 1, t[1] - 2))
                        mine_tiles.append((t[0] + 1, t[1] - 4))
                        mine_tiles.append((t[0] + 2, t[1] - 4))
                        click_tiles.append((t[0] - 1, t[1]))
                        click_tiles.append((t[0] - 1, t[1] - 3))
                        click_tiles.append((t[0], t[1] - 4))
                        click_tiles.append((t[0] + 3, t[1] - 4))
                        stop_flag = 0
                        break

                # TWO: (closed tiles on outter top and right)
                # 1 2 2 2
                #       2
                #       2
                #       1
                if ((t[0] - 1, t[1] - 3, 2) in eff_nums) and ((t[0] - 2, t[1] - 3, 2) in eff_nums) and ((t[0] - 3, t[1] - 3, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] - 1, 2), (t[0], t[1] - 2, 2), (t[0], t[1] - 3, 2)]
                    cur_tiles_hor = [(t[0], t[1] - 3, 2), (t[0] - 1, t[1] - 3, 2), (t[0] - 2, t[1] - 3, 2), (t[0] - 3, t[1] - 3, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 1 and clear_check_hor == 1:
                        gameboard[t[1] - 1][t[0] + 1] = 9
                        gameboard[t[1] - 2][t[0] + 1] = 9
                        gameboard[t[1] - 4][t[0] - 1] = 9
                        gameboard[t[1] - 4][t[0] - 2] = 9
                        mine_tiles.append((t[0] + 1, t[1] - 1))
                        mine_tiles.append((t[0] + 1, t[1] - 2))
                        mine_tiles.append((t[0] - 1, t[1] - 4))
                        mine_tiles.append((t[0] - 2, t[1] - 4))
                        click_tiles.append((t[0] + 1, t[1]))
                        click_tiles.append((t[0] + 1, t[1] - 3))
                        click_tiles.append((t[0], t[1] - 4))
                        click_tiles.append((t[0] - 3, t[1] - 4))
                        stop_flag = 0
                        break

                # THREE: (closed tiles on outter top and left)
                # 2 2 1
                # 2
                # 2
                # 1
                if ((t[0] + 1, t[1] - 3, 2) in eff_nums) and ((t[0] + 2, t[1] - 3, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] - 1, 2), (t[0], t[1] - 2, 2), (t[0], t[1] - 3, 2)]
                    cur_tiles_hor = [(t[0], t[1] - 3, 2), (t[0] + 1, t[1] - 3, 2), (t[0] + 2, t[1] - 3, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 0 and clear_check_hor == 1:
                        gameboard[t[1] - 1][t[0] - 1] = 9
                        gameboard[t[1] - 2][t[0] - 1] = 9
                        gameboard[t[1] - 4][t[0]] = 9
                        gameboard[t[1] - 4][t[0] + 2] = 9
                        mine_tiles.append((t[0] - 1, t[1] - 1))
                        mine_tiles.append((t[0] - 1, t[1] - 2))
                        mine_tiles.append((t[0], t[1] - 4))
                        mine_tiles.append((t[0] + 2, t[1] - 4))
                        click_tiles.append((t[0] - 1, t[1]))
                        click_tiles.append((t[0] - 1, t[1] - 3))
                        click_tiles.append((t[0] + 1, t[1] - 4))
                        stop_flag = 0
                        break

                # FOUR: (closed tiles on outter top and right)
                # 1 2 2
                #     2
                #     2
                #     1
                if ((t[0] - 1, t[1] - 3, 2) in eff_nums) and ((t[0] - 2, t[1] - 3, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] - 1, 2), (t[0], t[1] - 2, 2), (t[0], t[1] - 3, 2)]
                    cur_tiles_hor = [(t[0], t[1] - 3, 2), (t[0] - 1, t[1] - 3, 2), (t[0] - 2, t[1] - 3, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 1 and clear_check_hor == 1:
                        gameboard[t[1] - 1][t[0] + 1] = 9
                        gameboard[t[1] - 2][t[0] + 1] = 9
                        gameboard[t[1] - 4][t[0]] = 9
                        gameboard[t[1] - 4][t[0] - 2] = 9
                        mine_tiles.append((t[0] + 1, t[1] - 1))
                        mine_tiles.append((t[0] + 1, t[1] - 2))
                        mine_tiles.append((t[0], t[1] - 4))
                        mine_tiles.append((t[0] - 2, t[1] - 4))
                        click_tiles.append((t[0] + 1, t[1]))
                        click_tiles.append((t[0] + 1, t[1] - 3))
                        click_tiles.append((t[0] - 1, t[1] - 4))
                        stop_flag = 0
                        break

            if ((t[0], t[1] + 1, 2) in eff_nums) and ((t[0], t[1] + 2, 2) in eff_nums) and ((t[0], t[1] + 3, 2) in eff_nums):
                # FIVE: (closed tiles on outter bottom and left)
                # 1
                # 2
                # 2
                # 2 2 2 1
                if ((t[0] + 1, t[1] + 3, 2) in eff_nums) and ((t[0] + 2, t[1] + 3, 2) in eff_nums) and ((t[0] + 3, t[1] + 3, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] + 1, 2), (t[0], t[1] + 2, 2), (t[0], t[1] + 3, 2)]
                    cur_tiles_hor = [(t[0], t[1] + 3, 2), (t[0] + 1, t[1] + 3, 2), (t[0] + 2, t[1] + 3, 2), (t[0] + 3, t[1] + 3, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 0 and clear_check_hor == 0:
                        gameboard[t[1] + 1][t[0] - 1] = 9
                        gameboard[t[1] + 2][t[0] - 1] = 9
                        gameboard[t[1] + 4][t[0] + 1] = 9
                        gameboard[t[1] + 4][t[0] + 2] = 9
                        mine_tiles.append((t[0] - 1, t[1] + 1))
                        mine_tiles.append((t[0] - 1, t[1] + 2))
                        mine_tiles.append((t[0] + 1, t[1] + 4))
                        mine_tiles.append((t[0] + 2, t[1] + 4))
                        click_tiles.append((t[0] - 1, t[1]))
                        click_tiles.append((t[0] - 1, t[1] + 3))
                        click_tiles.append((t[0], t[1] + 4))
                        click_tiles.append((t[0] + 3, t[1] + 4))
                        stop_flag = 0
                        break

                # SIX: (closed tiles on outter bottom and right)
                #       1
                #       2
                #       2
                # 1 2 2 2
                if ((t[0] - 1, t[1] + 3, 2) in eff_nums) and ((t[0] - 2, t[1] + 3, 2) in eff_nums) and ((t[0] - 3, t[1] + 3, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] + 1, 2), (t[0], t[1] + 2, 2), (t[0], t[1] + 3, 2)]
                    cur_tiles_hor = [(t[0], t[1] + 3, 2), (t[0] - 1, t[1] + 3, 2), (t[0] - 2, t[1] + 3, 2), (t[0] - 3, t[1] + 3, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 1 and clear_check_hor == 0:
                        gameboard[t[1] + 1][t[0] + 1] = 9
                        gameboard[t[1] + 2][t[0] + 1] = 9
                        gameboard[t[1] + 4][t[0] - 1] = 9
                        gameboard[t[1] + 4][t[0] - 2] = 9
                        mine_tiles.append((t[0] + 1, t[1] + 1))
                        mine_tiles.append((t[0] + 1, t[1] + 2))
                        mine_tiles.append((t[0] - 1, t[1] + 4))
                        mine_tiles.append((t[0] - 2, t[1] + 4))
                        click_tiles.append((t[0] + 1, t[1]))
                        click_tiles.append((t[0] + 1, t[1] + 3))
                        click_tiles.append((t[0], t[1] + 4))
                        click_tiles.append((t[0] - 3, t[1] + 4))
                        stop_flag = 0
                        break

                # SEVEN: (closed tiles on outter bottom and left)
                # 1
                # 2
                # 2
                # 2 2 1
                if ((t[0] + 1, t[1] + 3, 2) in eff_nums) and ((t[0] + 2, t[1] + 3, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] + 1, 2), (t[0], t[1] + 2, 2), (t[0], t[1] + 3, 2)]
                    cur_tiles_hor = [(t[0], t[1] + 3, 2), (t[0] + 1, t[1] + 3, 2), (t[0] + 2, t[1] + 3, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 0 and clear_check_hor == 0:
                        gameboard[t[1] + 1][t[0] - 1] = 9
                        gameboard[t[1] + 2][t[0] - 1] = 9
                        gameboard[t[1] + 4][t[0]] = 9
                        gameboard[t[1] + 4][t[0] + 2] = 9
                        mine_tiles.append((t[0] - 1, t[1] + 1))
                        mine_tiles.append((t[0] - 1, t[1] + 2))
                        mine_tiles.append((t[0], t[1] + 4))
                        mine_tiles.append((t[0] + 2, t[1] + 4))
                        click_tiles.append((t[0] - 1, t[1]))
                        click_tiles.append((t[0] - 1, t[1] + 3))
                        click_tiles.append((t[0] + 1, t[1] + 4))
                        stop_flag = 0
                        break

                # EIGHT: (closed tiles on outter bottom and right)
                #     1
                #     2
                #     2
                # 1 2 2
                if ((t[0] - 1, t[1] + 3, 2) in eff_nums) and ((t[0] - 2, t[1] + 3, 1) in eff_nums):
                    cur_tiles_ver = [t, (t[0], t[1] + 1, 2), (t[0], t[1] + 2, 2), (t[0], t[1] + 3, 2)]
                    cur_tiles_hor = [(t[0], t[1] + 3, 2), (t[0] - 1, t[1] + 3, 2), (t[0] - 2, t[1] + 3, 1)]
                    clear_check_ver = check_is_clear_vertical(gameboard, cur_tiles_ver)  # checks right(1)/left(0)
                    clear_check_hor = check_is_clear_horizontal(gameboard, cur_tiles_hor)  # checks above(1)/below(0)
                    if clear_check_ver == 1 and clear_check_hor == 0:
                        gameboard[t[1] + 1][t[0] + 1] = 9
                        gameboard[t[1] + 2][t[0] + 1] = 9
                        gameboard[t[1] + 4][t[0]] = 9
                        gameboard[t[1] + 4][t[0] - 2] = 9
                        mine_tiles.append((t[0] + 1, t[1] + 1))
                        mine_tiles.append((t[0] + 1, t[1] + 2))
                        mine_tiles.append((t[0], t[1] + 4))
                        mine_tiles.append((t[0] - 2, t[1] + 4))
                        click_tiles.append((t[0] + 1, t[1]))
                        click_tiles.append((t[0] + 1, t[1] + 3))
                        click_tiles.append((t[0] - 1, t[1] + 4))
                        stop_flag = 0
                        break

            # 2e.) check for 1-1-X and X-1-1 patterns...
            if ((t[0] + 1, t[1], 1) in eff_nums):
                # ONE
                # ?  1  1  X
                # W -1 -1  C
                if is_number(gameboard, (t[0] + 2, t[1])) and (t[0] == 0 or is_number(gameboard, (t[0] - 1, t[1] + 1))):
                    if t[1] < len(row_y_coords) - 1 and gameboard[t[1] + 1][t[0]] == -1 and gameboard[t[1] + 1][t[0] + 1] == -1 and gameboard[t[1] + 1][t[0] + 2] == -1:
                        if (t[0] + 2, t[1] + 1) not in click_tiles:
                            click_tiles.append((t[0] + 2, t[1] + 1))
                            stop_flag = 0
                            break

                # TWO
                # W -1 -1  C
                # ?  1  1  X
                if is_number(gameboard, (t[0] + 2, t[1])) and (t[0] == 0 or is_number(gameboard, (t[0] - 1, t[1] - 1))):
                    if t[1] > 0 and gameboard[t[1] - 1][t[0]] == -1 and gameboard[t[1] - 1][t[0] + 1] == -1 and gameboard[t[1] - 1][t[0] + 2] == -1:
                        if (t[0] + 2, t[1] - 1) not in click_tiles:
                            click_tiles.append((t[0] + 2, t[1] - 1))
                            stop_flag = 0
                            break

                # THREE
                # X  1  1  ?
                # C -1 -1  W
                if is_number(gameboard, (t[0] - 1, t[1])) and (t[0] + 1 == len(col_x_coords) - 1 or is_number(gameboard, (t[0] + 2, t[1] + 1))):
                    if t[1] < len(row_y_coords) - 1 and gameboard[t[1] + 1][t[0] - 1] == -1 and gameboard[t[1] + 1][t[0]] == -1 and gameboard[t[1] + 1][t[0] + 1] == -1:
                        if (t[0] - 1, t[1] + 1) not in click_tiles:
                            click_tiles.append((t[0] - 1, t[1] + 1))
                            stop_flag = 0
                            break

                # FOUR
                # C -1 -1  W
                # X  1  1  ?
                if is_number(gameboard, (t[0] - 1, t[1])) and (t[0] + 1 == len(col_x_coords) - 1 or is_number(gameboard, (t[0] + 2, t[1] - 1))):
                    if t[1] > 0 and gameboard[t[1] - 1][t[0] - 1] == -1 and gameboard[t[1] - 1][t[0]] == -1 and gameboard[t[1] - 1][t[0] + 1] == -1:
                        if (t[0] - 1, t[1] - 1) not in click_tiles:
                            click_tiles.append((t[0] - 1, t[1] - 1))
                            stop_flag = 0
                            break

            if ((t[0], t[1] - 1, 1) in eff_nums):
                # FIVE
                #  W ?
                # -1 1
                # -1 1
                #  C X
                if is_number(gameboard, (t[0], t[1] + 1)) and (t[1] - 1 == 0 or is_number(gameboard, (t[0] - 1, t[1] - 2))):
                    if t[0] > 0 and gameboard[t[1] - 1][t[0] - 1] == -1 and gameboard[t[1]][t[0] - 1] == -1 and gameboard[t[1] + 1][t[0] - 1] == -1:
                        if (t[0] - 1, t[1] + 1) not in click_tiles:
                            click_tiles.append((t[0] - 1, t[1] + 1))
                            stop_flag = 0
                            break

                # SIX
                # ?  W
                # 1 -1
                # 1 -1
                # X  C
                if is_number(gameboard, (t[0], t[1] + 1)) and (t[1] - 1 == 0 or is_number(gameboard, (t[0] + 1, t[1] - 2))):
                    if t[0] < len(col_x_coords) - 1 and gameboard[t[1] - 1][t[0] + 1] == -1 and gameboard[t[1]][t[0] + 1] == -1 and gameboard[t[1] + 1][t[0] + 1] == -1:
                        if (t[0] + 1, t[1] + 1) not in click_tiles:
                            click_tiles.append((t[0] + 1, t[1] + 1))
                            stop_flag = 0
                            break

                # SEVEN
                #  C X
                # -1 1
                # -1 1
                #  W ?
                if is_number(gameboard, (t[0], t[1] - 2)) and (t[1] == len(row_y_coords) - 1 or is_number(gameboard, (t[0] - 1, t[1] + 1))):
                    if t[0] > 0 and gameboard[t[1]][t[0] - 1] == -1 and gameboard[t[1] - 1][t[0] - 1] == -1 and gameboard[t[1] - 2][t[0] - 1] == -1:
                        if (t[0] - 1, t[1] - 2) not in click_tiles:
                            click_tiles.append((t[0] - 1, t[1] - 2))
                            stop_flag = 0
                            break

                # EIGHT
                # X  C
                # 1 -1
                # 1 -1
                # ?  W
                if is_number(gameboard, (t[0], t[1] - 2)) and (t[1] == len(row_y_coords) - 1 or is_number(gameboard, (t[0] + 1, t[1] + 1))):
                    if t[0] < len(col_x_coords) - 1 and gameboard[t[1]][t[0] + 1] == -1 and gameboard[t[1] - 1][t[0] + 1] == -1 and gameboard[t[1] - 2][t[0] + 1] == -1:
                        if (t[0] + 1, t[1] - 2) not in click_tiles:
                            click_tiles.append((t[0] + 1, t[1] - 2))
                            stop_flag = 0
                            break

    # print("OUT OF WHILE LOOP")  # for testing

    # NOTE: if no moves will be made, this returned list will contain 2 empty lists
    return [mine_tiles, click_tiles]



# FOR TESTING

# GAME BOARD #1
# gameboard = [
#     [-1, -1, -1, 2, 0],
#     [1, -1, -1, 3, 9],
#     [2, -1, -1, 4, 9],
#     [1, -1, -1, 2, 1],
#     [-1, -1, -1, 1, 0],
# ]
# bordering_unfinished_numbers = [
#     (0, 1),
#     (0, 2),
#     (0, 3),
#     (3, 0),
#     (3, 1),
#     (3, 2),
#     (3, 3),
#     (3, 4),
#     (4, 1),
#     (4, 3)
# ]
# col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420}
# row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250, 4: 280}
# bombs_remaining = 15


# GAME BOARD #2
# gameboard = [
#     [-1, -1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1, -1],
#     [ 2, -1, -1, -1, -1, -1,  1],
#     [ 1, -1, -1, -1, -1, -1,  1],
#     [ 1, -1, -1, -1, -1, -1,  1],
#     [ 0, 2, -1, -1, -1,  2,  0],
# ]
# bordering_unfinished_numbers = [
#     (6, 2),
#     (6, 3),
#     (6, 4),
#     (5, 5),
#     (0, 2),
#     (0, 3),
#     (0, 4),
#     (1, 5)
# ]
# col_x_coords = {0: 300, 1: 330, 2: 360, 3: 390, 4: 420, 5: 450, 6: 480}
# row_y_coords = {0: 160, 1: 190, 2: 220, 3: 250, 4: 280, 5: 310}
# bombs_remaining = 15


# for i in range(len(row_y_coords)):
#     print(gameboard[i])
# print()
#
# results = pattern_recognition(gameboard, col_x_coords, row_y_coords, bordering_unfinished_numbers, bombs_remaining)
# print()
# print("RESULTS: ", end="")
# print(results)
# print()
#
# for i in range(len(row_y_coords)):
#     print(gameboard[i])
