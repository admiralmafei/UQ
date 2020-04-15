from a1_support import *


def main():
    pass


# #########################UNCOMMENT THIS FUNCTION WHEN READY#######################
# def big_fun_search(game, grid_size, pokemon_locations, index):
# 	"""Searching adjacent cells to see if there are any Pokemon"s present.

# 	Using some sick algorithms.

# 	Find all cells which should be revealed when a cell is selected.

# 	For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
# 	neighbours are revealed. If one of the neighbouring cells is also zero then
# 	all of that cell"s neighbours are also revealed. This repeats until no
# 	zero value neighbours exist.

# 	For cells which have a non-zero value (i.e. cells with neightbour pokemons), only
# 	the cell itself is revealed.

# 	Parameters:
# 		game (str): Game string.
# 		grid_size (int): Size of game.
# 		pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
# 		index (int): Index of the currently selected cell

# 	Returns:
# 		(list<int>): List of cells to turn visible.
# 	"""
# 	queue = [index]
# 	discovered = [index]
# 	visible = []

# 	if game[index] == FLAG:
# 		return queue

# 	number = number_at_cell(game, pokemon_locations, grid_size, index)
# 	if number != 0:
# 		return queue

# 	while queue:
# 		node = queue.pop()
# 		for neighbour in neighbour_directions(node, grid_size):
# 			if neighbour in discovered or neighbour is None:
# 				continue

# 			discovered.append(neighbour)
# 			if game[neighbour] != FLAG:
# 				number = number_at_cell(game, pokemon_locations, grid_size, neighbour)
# 				if number == 0:
# 					queue.append(neighbour)
# 			visible.append(neighbour)
# 	return visible
# #########################UNCOMMENT THIS FUNCTION WHEN READY#######################

if __name__ == "__main__":
    main()
