import pyautogui


def run_intro_prompts() -> list:
    return_values = []

    # initial opening statements
    print("Welcome to Minesweeper Bot, developed by Jake Duffy!")
    print("To begin, open minesweeper and respond to the following prompts in your terminal...")
    print()

    # prompt 0: ask which website the user is using -> int
    print("Which Minesweeper website are you using?")
    print("   Enter '1' for minesweeper.one (DEFAULT - recommended)")
    print("   Enter '2' for minesweeper.online (not recommended since your IP can get blocked)")
    website = input()
    if website == '2':
        website = 2
    else:
        website = 1

    # prompt 1: get x-y coordinates of start/restart button -> Point(tuple)
    print("1.) Hover your mouse over the start/restart button and type enter")
    input()
    return_values.append(pyautogui.position())

    # prompt 2: get x-y coordinates of center of first tile -> Point(tuple)
    print("2.) Hover your mouse over the center of the tile in the top left corner of the game board and type enter")
    print("note: if you don't click close enough to the center, the bot may not function properly")
    input()
    return_values.append(pyautogui.position())

    # prompt 3: get the user's zoom size -> string (integer)
    print("3.) Enter the zoom size you're using")
    print("(for minesweeper.online, this will be the number next to the drop-down with the magnifying glass)")
    print("(for minesweeper.one, the zoom size will be 32 by default, but this changes if you zoom in or out")
    zoom_value = input()
    return_values.append(zoom_value)

    # prompt 4: get the user's board size -> string
    print("4.) Enter the board size")
    print("note: enter 'beginner', 'intermediate', 'expert' or '<columns>x<rows>' ('columns' and 'rows' are integers)")
    print("IMPORTANT NOTE: 'expert' and 'beginner' modes need to be typed in manually on 'custom' mode if using minesweeper.one")
    board_size = input()
    return_values.append(board_size)

    # prompt 5: get the bomb count -> string (integer)
    print("5.) Enter the number of bombs")
    print("note: if you entered beginner, intermediate, or expert, this value will be auto-filled")
    if board_size.lower() == "beginner":
        bomb_count = '10'
        print(10)
    elif board_size.lower() == "intermediate":
        bomb_count = '40'
        print(40)
    elif board_size.lower() == "expert":
        bomb_count = '99'
        print(99)
    else:
        bomb_count = input()
    return_values.append(bomb_count)

    # prompt 6: developer mode or no -> string
    print("6.) Enter developer mode? (type y if yes, otherwise press enter)")
    developer_mode = 'n'
    tmp = input()
    if tmp.lower() == 'y':
        developer_mode = 'y'
    return_values.append(developer_mode)

    # prompt 7: number of games -> string
    print("7.) How many games do you want the bot to play? (default is 100)")
    game_count = input()
    if len(game_count) < 1:
        game_count = '100'
    return_values.append(game_count)

    # appending the website value (1 or 2) to end of return_values list
    return_values.append(website)

    # final message
    print()
    print("Reminders before beginning:")
    print()
    print("   * press the escape key at any point to terminate the program")
    print("   1. if you're using minesweeper.online, use the light theme (this is necessary for tile detection)")
    print("   2. make sure game board is fully in view and completely unobstructed while the bot runs")
    print("   3. don't move your browser window or change it's size while the bot runs")
    print("   4. don't move your mouse while the bot runs")
    print()
    print("Press enter whenever you are ready to begin...")
    input()

    return return_values
