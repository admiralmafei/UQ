from a1_support import *


def main():
    """
    Main function aims to enter the game and verify some inputting instructions.
    The function also creates some important variables, which could represent the size of game map,
    the number of pokemon hidden in the map and the layout of this map.
    """
    grid_size = input("Please input the size of the grid: ")
    number_of_pokemons = input("Please input the number of pokemons: ")
    pokemons = generate_pokemons(int(grid_size), int(number_of_pokemons))
    game = UNEXPOSED * int(grid_size) ** 2
    grid_size = int(grid_size)
    number_of_pokemons = int(number_of_pokemons)
    while True:
        display_game(game, grid_size)
        action = input("\nPlease input action: ")
        if action == 'h':
            print(HELP_TEXT)
        elif action == ':)':
            print('It\'s rewind time.')
            pokemons = generate_pokemons(grid_size, number_of_pokemons)
            game = UNEXPOSED * int(grid_size) ** 2
        elif action == 'q':
            choice_out = input('You sure about that buddy? (y/n): ')
            if choice_out == 'y':
                print('Catch you on the flip side.')
                break
            elif choice_out == 'n':
                print('Let\'s keep going.')
            else:
                print('That ain\'t a valid action buddy.')
        else:
            if parse_position(action, grid_size) is None:
                print('That ain\'t a valid action buddy.')
            else:
                position = parse_position(action, grid_size)
                if position != None:
                    if action[0] == 'f':
                        if game[position_to_index(position, grid_size)] == FLAG:
                            game = replace_character_at_index(game, position_to_index(position, grid_size), UNEXPOSED)
                        else:
                            game = replace_character_at_index(game, position_to_index(position, grid_size), FLAG)
                    else:
                        if game[position_to_index(position, grid_size)] != FLAG:
                            if position_to_index(position, grid_size) in pokemons:
                                for pokemon in pokemons:
                                    game = replace_character_at_index(game, pokemon, POKEMON)
                                display_game(game, grid_size)
                                print('You have scared away all the pokemons.')
                                break
                            else:
                                # Following codes have the same function with big_fun_search()
                                # For these cells which located in neighbour directions of selected cell.
                                # If this cell's number_at_cell is zero, update this character as '0', then keep exploring.
                                # If this cell's number_at_cell is non-zero, update the character as 'num'.
                                neighbour = [position_to_index(position, grid_size)]
                                while neighbour:
                                    index = neighbour.pop()
                                    num = number_at_cell(game, pokemons, grid_size, index)
                                    if num != 0:
                                        if game[index] != FLAG:
                                            game = replace_character_at_index(game, index, '{0}'.format(num))
                                    else:
                                        if game[index] == UNEXPOSED:
                                            game = replace_character_at_index(game, index, '{0}'.format(num))
                                        for n in neighbour_directions(index, grid_size):
                                            if n not in neighbour and game[n] == UNEXPOSED:
                                                neighbour.append(n)

            if check_win(game, pokemons):
                display_game(game, grid_size)
                print("You win.")
                break


def display_game(game, grid_size):
    """
    Construct the map by inputting the size of a grid-shaped display.
    Parameters:
        game (str): Game string
        grid_size (int): Size of game
    """
    game_map = ""
    title = '  ' + WALL_VERTICAL
    line = WALL_HORIZONTAL * 4
    for i in range(grid_size):
        if i < 9:
            title += ' {0} {1}'.format(i + 1, WALL_VERTICAL)
        else:
            title += ' {0}{1}'.format(i + 1, WALL_VERTICAL)
        line += WALL_HORIZONTAL * 4

    game_map += title + "\n" + line + '\n'

    for y in range(grid_size):
        game_map += ALPHA[y] + " " + WALL_VERTICAL
        for x in range(grid_size):
            index = x + y * grid_size
            game_map += ' ' + game[index] + ' ' + WALL_VERTICAL
        game_map += '\n' + line + '\n'
    game_map = game_map.rstrip('\n')
    print(game_map)


def parse_position(action, grid_size):
    """
    This function checks the effectiveness of input action, and return None if the action is
    invalid input.
    Return:
        position (tuple<int>): Convert input action<str> to position<tuple>
    """
    while True:
        command_lst = action.split(' ')
        if len(command_lst) == 1:
            if command_lst[0] == '':
                return None
            command = command_lst[0][0]
            x = ALPHA.find(command[0])
            if x == -1:
                return None
            y_str = command_lst[0][1:]
            if not y_str.isdigit():
                return None
            y = int(y_str)
            if y > grid_size:
                return None
            position = (x, y - 1)
            return position
        elif len(command_lst) == 2:
            if command_lst[0] != 'f':
                return None
            else:
                command = command_lst[1]
                if command == '':
                    return None
                x = ALPHA.find(command[0])
                if x == -1:
                    return None
                y_str = command[1:]
                if not y_str.isdigit():
                    return None
                y = int(y_str)
                if y > grid_size:
                    return None
                position = (x, y - 1)
                return position


def position_to_index(position, grid_size) -> int:
    """
    This function should convert the row, column coordinate in the grid to the game strings index.
    The function returns an integer representing the index of the cell in the game string.
    Parameters:
        grid_size (int): Size of game.
        pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
    return:
        index (int): Convert position<tuple> to index<int>
    """
    index = position[0] * grid_size + position[1]
    return index


def replace_character_at_index(game, index, character) -> str:
    """
    The function modifies the specified characters in the game according to the index of cell.
    Parameters:
        game (str): Game string.
        index (int): Index of the currently selected cell
        character (str): A flag or other characters could be placed on each call
    Return:
        game (str): Updated game string.
    """
    game = game[:index] + character + game[index + 1:]
    return game


def flag_cell(game, index) -> str:
    """
    The function judges whether the cell is a flag, then converts to '~' if it's a flag,
    converts to flag if it's '~'.
    """
    if game[index] == FLAG:
        return replace_character_at_index(game, index, UNEXPOSED)
    else:
        return replace_character_at_index(game, index, FLAG)


def index_in_direction(index, grid_size, direction):
    """
    The function return the index of the direction position.
    Parameters:
        direction: Neighbouring directions, provided by support.py, namely up, down, left, right，etc.
    Return:
        new_index (int): Index of effective directions of neighbouring pokemon.
    """
    up = DIRECTIONS[0]
    down = DIRECTIONS[1]
    left = DIRECTIONS[2]
    right = DIRECTIONS[3]
    up_left = DIRECTIONS[4]
    up_right = DIRECTIONS[5]
    down_left = DIRECTIONS[6]
    down_right = DIRECTIONS[7]

    if direction == up:
        if index < grid_size:
            return None
        else:
            new_index = index - grid_size
            return new_index
    elif direction == down:
        if index >= grid_size * grid_size - grid_size:
            return None
        else:
            new_index = index + grid_size
            return new_index

    elif direction == left:
        if index < (index // grid_size) * grid_size + 1:
            return None
        else:
            new_index = index - 1
            return new_index

    elif direction == right:
        if index >= (index // grid_size + 1) * grid_size - 1:
            return None
        else:
            new_index = index + 1
            return new_index

    elif direction == up_left:
        if index - grid_size - 1 >= (index // grid_size - 1) * grid_size and index - grid_size - 1 >= 0:
            new_index = index - grid_size - 1
            return new_index
        else:
            return None

    elif direction == up_right:
        if index // grid_size * grid_size > index - grid_size + 1 >= 0:
            new_index = index - grid_size + 1
            return new_index
        else:
            return None

    elif direction == down_left:
        if (index // grid_size + 1) * grid_size <= index + grid_size - 1 < (
                index // grid_size + 2) * grid_size and index + grid_size - 1 < grid_size * grid_size:
            new_index = index + grid_size - 1
            return new_index
        else:
            return None

    elif direction == down_right:
        if (index // grid_size + 1) * grid_size <= index + grid_size + 1 < (
                index // grid_size + 2) * grid_size and index + grid_size + 1 < grid_size * grid_size:
            new_index = index + grid_size + 1
            return new_index
        else:
            return None


def neighbour_directions(index, grid_size):
    """
    Creat a list to store index of neighbouring directions.
    Return:
        (list<int>): Index of neighbouring direction.
    """
    neighbours = []
    for i in DIRECTIONS:
        if index_in_direction(index, grid_size, i) is not None:
            neighbours.append(index_in_direction(index, grid_size, i))
    return neighbours


def number_at_cell(game, pokemon_locations, grid_size, index) -> int:
    """
    Count the number of pokemon(s) in neighbouring directions.
    Return:
        count (int): The number of pokemon in neighbouring direction
    """
    count = 0
    if index not in pokemon_locations:
        for n in neighbour_directions(index, grid_size):
            if n in pokemon_locations:
                count += 1
    return count


def check_win(game, pokemon_locations) -> bool:
    """
    Check win or not by methods of judging whether these flags are in the positions
    of all pokemon，and other judgment methods.
    Return:
        (bool): Boolean output related to current game.
    """
    count_flag = 0
    count_exopsed = 0
    for i in game:
        if i == FLAG:
            count_flag += 1
        if i == UNEXPOSED:
            count_exopsed += 1
    if count_exopsed != 0 or count_flag != len(pokemon_locations):
        return False
    for k in pokemon_locations:
        if game[k] != FLAG:
            return False
    return True


# #########################UNCOMMENT THIS FUNCTION WHEN READY#######################
def big_fun_search(game, grid_size, pokemon_locations, index):
    """Searching adjacent cells to see if there are any Pokemon"s present.
	Using some sick algorithms.
	Find all cells which should be revealed when a cell is selected.
	For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
	neighbours are revealed. If one of the neighbouring cells is also zero then
	all of that cell"s neighbours are also revealed. This repeats until no
	zero value neighbours exist.
	For cells which have a non-zero value (i.e. cells with neighbour pokemons), only
	the cell itself is revealed.
	Parameters:
		game (str): Game string.
		grid_size (int): Size of game.
		pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
		index (int): Index of the currently selected cell
	Returns:
		(list<int>): List of cells to turn visible.
	"""
    queue = [index]
    discovered = [index]
    visible = []

    if game[index] == FLAG:
        return queue

    number = number_at_cell(game, pokemon_locations, grid_size, index)
    if number != 0:
        return queue

    while queue:
        node = queue.pop()
        for neighbour in neighbour_directions(node, grid_size):
            if neighbour in discovered or neighbour is None:
                continue

            discovered.append(neighbour)
            if game[neighbour] != FLAG:
                number = number_at_cell(game, pokemon_locations, grid_size, neighbour)
                if number == 0:
                    queue.append(neighbour)
            visible.append(neighbour)
    return visible


# #########################UNCOMMENT THIS FUNCTION WHEN READY#######################

if __name__ == "__main__":
    main()
