EMPTY_TILE = "tile"
START_PIPE = "start"
END_PIPE = "end"
LOCKED_TILE = "locked"

SPECIAL_TILES = {
    "S": START_PIPE,
    "E": END_PIPE,
    "L": LOCKED_TILE
}

PIPES = {
    "ST": "straight",
    "CO": "corner",
    "CR": "cross",
    "JT": "junction-t",
    "DI": "diagonals",
    "OU": "over-under"
}

PIPE_STRUCTURE = {
    # name of pipe: (N, E, S, W)
    "straight": (1, 0, 1, 0),
    "corner": (1, 1, 0, 0),
    "cross": (1, 1, 1, 1),
    "junction-t": (0, 1, 1, 1),
    "diagonals": (1, 1, 2, 2),
    "over-under": (1, 2, 1, 2),
    START_PIPE: (0, 0, 0, 0),
    END_PIPE: (0, 0, 0, 0),
}

OP_SIDE = {
    "N": "S",
    "E": "W",
    "W": "E",
    "S": "N",
}

DIRECTIONS = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}


class Tile:
    """
    Representation of a tile.
    """
    _id = "tile"

    def __init__(self, name, selectable=True):
        """
        Construct a tile with a given name.
        Parameters:
            name (str): The name of the tile
            selectable (bool): If the tile can be interacted with.
        """
        self._name = name
        self._select = selectable

    def get_name(self):
        """(str): Returns the name of the tile."""
        return self._name

    def get_id(self):
        """(str): Returns the id of the tile."""
        return self._id

    def set_select(self, selectable):
        """
        Sets rather or not the tile can be interacted with.
        Parameters:
            selectable (bool): True if the tile can be interacted with, False otherwise.
        """
        self._select = selectable

    def can_select(self):
        """(bool): Returns whether or not the tile can be interacted with."""
        return self._select

    def __str__(self):
        return f"{self.__class__.__name__}('{self._name}', {self._select})"

    def __repr__(self):
        return str(self)


class Pipe(Tile):
    """
    Representation of a pipe.
    """
    _id = "pipe"

    def __init__(self, name, orientation=0, selectable=True):
        """
            Construct a pipe with a given name and orientation.
            Parameters:
                name (str): name of the pipe
                orientation (int): orientation of the pipe.
                    orientation is represented by a single number.
                    - 0 means default
                    - 1 means rotated clockwise once
                    - 2 means rotated clockwise twice
                    - 3 means rotated clockwise three times
        """
        super().__init__(name, selectable)
        self._parts = PIPE_STRUCTURE[name]
        self._orientation = orientation
        self.rotate(0)

    def get_connected(self, side):
        """ (list<str>): Returns a list of all sides that are connected to the given side.
        Parameters:
            side (str): one of N, E, S, W
        """
        connected = []
        parts = self._parts[-self._orientation:] + self._parts[:-self._orientation]
        sides = list(DIRECTIONS)
        index = sides.index(side)

        if parts[index] == 0:
            return connected

        for i, part in enumerate(parts):
            if part == parts[index] and i != index:
                connected.append(sides[i])

        return connected

    def rotate(self, direction):
        """
        Rotates the pipe.
        Parameters:
            direction (int): positive number for Clockwise rotation and negative for Counter-Clockwise rotation.
        """
        self._orientation = (self._orientation + direction) % 4

    def get_orientation(self):
        """(int): Returns the orientation of the pipe."""
        return self._orientation

    def __str__(self):
        return f"{self.__class__.__name__}('{self._name}', {self._orientation})"


class SpecialPipe(Pipe):
    """
    Abstract representation of a special pipe.
    """
    _id = "special_pipe"

    def rotate(self, direction):
        """
        Special pipes should not rotate.

        Paramenters:
            direction (int): positive number for Clockwise rotation and negative for Counter-Clockwise rotation.
        """
        pass

    def __str__(self):
        return f"{self.__class__.__name__}({self._orientation})"


class StartPipe(SpecialPipe):
    """
    Representation of a start pipe.
    """
    def __init__(self, orientation=0):
        """
            Construct a start pipe.
        """
        super().__init__(START_PIPE, orientation, False)

    def get_connected(self, side=None):
        """(list<str>): Returns the direction that the start pipe is facing."""
        return [list(DIRECTIONS)[self.get_orientation()]]


class EndPipe(SpecialPipe):
    """
    Representation of a end pipe.
    """
    def __init__(self, orientation=0):
        """
            Construct a start pipe.
        """
        super().__init__(END_PIPE, orientation, False)

    def get_connected(self, side=None):
        """
        (list<str>): Returns the opposite of the direction that the end 
            pipe is facing.
        """
        return [OP_SIDE[list(DIRECTIONS)[self.get_orientation()]]]


class PipeGame:
    """
    A game of Pipes.
    """
    def __init__(self, game_file='game_1.csv'):
        """
        Construct a game of Pipes from a file name.
        Parameters:
            game_file (str): name of the game file.
        """
        
        board_layout = [
            [
                Tile('tile', True), Tile('tile', True), Tile('tile', True),
                Tile('tile', True), Tile('tile', True), Tile('tile', True)
            ],
            [
                StartPipe(1), Tile('tile', True), Tile('tile', True),
                Tile('tile', True), Tile('tile', True), Tile('tile', True)
            ],
            [
                Tile('tile', True), Tile('tile', True), Tile('tile', True),
                Pipe('junction-t', 0, False), Tile('tile', True), Tile('tile', True)
            ],
            [
                Tile('tile', True), Tile('tile', True), Tile('tile', True),
                Tile('tile', True), Tile('locked', False), Tile('tile', True)
            ],
            [
                Tile('tile', True), Tile('tile', True), Tile('tile', True),
                Tile('tile', True), EndPipe(3), Tile('tile', True)
            ],
            [
                Tile('tile', True), Tile('tile', True), Tile('tile', True),
                Tile('tile', True), Tile('tile', True), Tile('tile', True)
            ]
        ]

        playable_pipes = {
            'straight': 1, 
            'corner': 1, 
            'cross': 1, 
            'junction-t': 1, 
            'diagonals': 1, 
            'over-under': 1
        }

        # #########################UNCOMMENT THIS FOR load_file#######################
        playable_pipes, board_layout = self.load_file(game_file)
        # #########################UNCOMMENT THIS FOR load_file#######################

        self._board = board_layout
        self._inventory = playable_pipes

        self._starting_point = None
        self._ending_point = None

        self.end_pipe_positions()


    def get_board_layout(self):
        """(list<list<Tile>>): Returns a 2D array representation of the board."""
        return self._board

    def get_playable_pipes(self):
        """(dict<str, int>): Returns a dictionary of all the playable pipes and number of times each pipe can be played."""
        return self._inventory

    def change_playable_amount(self, pipe_name, number):
        """
        Set how many times the pipe can be played.
        Parameters:
            pipe_name (str): The name of the pipe.
            number (int): Change in how many times the pipe can be played.
        """
        self._inventory[pipe_name] += number

    def get_pipe(self, position):
        """
        Get the pipe at the given position within the board. If there is not pipe at that position, return a tile.
        Parameters:
            position (tuple<int, int>): The position to look for a pipe.
        Returns:
            (Pipe|Tile): The pipe at the position or the tile if there is no pipe at that position.
        """
        y, x = position
        return self.get_board_layout()[y][x]

    def set_pipe(self, pipe, position):
        """
        Place a pipe at a position on the board. The playable number of the given pipe should also be updated.
        If the player does not have enough of the give pipe in their inventory, it should not be placed.
        Parameters:
            position (tuple<int, int>): The position in the game board where the pipe is placed.
            pipe (Pipe): The pipe to be placed in the board.
        """
        pipe_name = pipe.get_name()
        if self._inventory[pipe_name] <= 0:
            return

        y, x = position
        self._board[y][x] = pipe
        self.change_playable_amount(pipe_name, -1)

    def remove_pipe(self, position):
        """
        Removing a pipe in the board. i.e. Creating an empty tile at the given position and 
            adding increasing the playable number of the given pipe.
        Parameters:
            position (tuple<int, int>): The position in the game board where the pipe is removed.
        """
        pipe = self.get_pipe(position)

        y, x = position
        self.get_board_layout()[y][x] = Tile(EMPTY_TILE)
        self.change_playable_amount(pipe.get_name(), 1)

    def position_in_direction(self, direction, position):
        """
        Returns the position in a given direction.
        Returns None if the position in a given direction is not in the board.
        Parameters:
            direction (str): A directory string, e.g. N, S, E or W
            position (tuple<int, int>): The position in the board to calculate from.
        Returns:
            (tuple<str, tuple<int, int>>):
        """
        diff_position = DIRECTIONS[direction]
        new_position = tuple(
            position[i] + diff_position[i] for i in range(len(position))
        )

        size = len(self.get_board_layout())
        if 0 <= new_position[0] < size and 0 <= new_position[1] < size:
            return OP_SIDE[direction], new_position

    def pipe_in_position(self, position):
        """
        Return the pipe in a given position in the game board if there is a Pipe in the given position.
        None if the position given is None or if the object in the given position is not a Pipe.
        Returns:
            (Pipe): Pipe in the given position. Returns None for invalid cases.
        """
        if position is None:
            return None

        tile = self.get_pipe(position)
        if tile is not None and "pipe" in tile.get_id():
            return tile

    def end_pipe_positions(self):
        """
        Find the end pipe (start and end pipe) positions in the game board.
        """
        for y, row in enumerate(self.get_board_layout()):
            for x, tile in enumerate(row):
                position = (y, x)
                if tile.get_name() == START_PIPE:
                    self._starting_point = position
                elif tile.get_name() == END_PIPE:
                    self._ending_point = position

    def get_starting_position(self):
        """(tuple<int, int>): The position of the start pipe."""
        return self._starting_point

    def get_ending_position(self):
        """(tuple<int, int>): The position of the end pipe."""
        return self._ending_point

    def load_file(self, filename):
        """
        Loads the csv file as list of lists.

        Parameters:
            filename (str): the name of the game file

        Returns:
            (tuple<dict<str, int>, list<list<Tile>>): The playable pipes, and 
                the board_layout.

        """
        board_layout = []
        with open(filename, 'r') as file:
            file_contents = file.readlines()
            playable_pipes = file_contents.pop().split(",")
            file_contents = "".join(file_contents).strip()
        for line in file_contents.split('\n'):
            line = line.split(",")
            row = []
            for item in line:
                try:
                    if item[:-1] in PIPES or item in PIPES:
                        if len(item) == 3:
                            tile = Pipe(PIPES[item[:-1]], int(item[-1]))
                        else:
                            tile = Pipe(PIPES[item])
                        tile.set_select(False)
                    elif item[0] in SPECIAL_TILES:
                        name, orientation = self.parse_name(item)
                        if "S" in item:
                            tile = StartPipe(orientation)
                        elif "E" in item:
                            tile = EndPipe(orientation)
                        elif item == "L":
                            tile = Tile(LOCKED_TILE, False)
                    else:
                        tile = Tile(EMPTY_TILE)
                except NameError:
                    tile = None
                row.append(tile)
            board_layout.append(row)

        playable = {}
        for number, pipe in enumerate(PIPES):
            playable[PIPES[pipe]] = int(playable_pipes[number])

        return playable, board_layout

    def parse_name(self, name):
        """
        Parse the given string into the name and the orientation of the pipe.

        Parameters:
            (str): the name of the game.
        """
        if len(name) == 2:
            return name[:-1], int(name[-1])
        return name, 0

    #########################################################################################################
    #########################################################################################################
    ######################                        check win                             #####################
    #########################################################################################################
    #########################################################################################################

    def check_win(self):
        """
        (bool) Returns True  if the player has won the game False otherwise.
        """
        position = self.get_starting_position()
        pipe = self.pipe_in_position(position)
        queue = [(pipe, None, position)]
        discovered = [(pipe, None)]
        while queue:
            pipe, direction, position = queue.pop()
            for direction in pipe.get_connected(direction):
                
                if self.position_in_direction(direction, position) is None:
                    new_direction = None 
                    new_position = None
                else:
                    new_direction, new_position = self.position_in_direction(direction, position)
                if new_position == self.get_ending_position() and direction == self.pipe_in_position(
                        new_position).get_connected()[0]:
                    return True

                pipe = self.pipe_in_position(new_position)
                if pipe is None or (pipe, new_direction) in discovered:
                    continue
                discovered.append((pipe, new_direction))
                queue.append((pipe, new_direction, new_position))
        return False
