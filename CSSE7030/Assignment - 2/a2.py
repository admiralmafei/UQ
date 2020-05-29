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


class Tile(object):
    """Representation of an available space in board game"""

    def __init__(self, name, selectable: bool = True):
        """Construct a tile object, add attributes for name and whether this tile
        is selectable.

        Parameters:
            name (str): the name of the tile
            selectable (bool): whether this tile could be selectable
        """
        self._name = name
        self._selectable = selectable

    def get_name(self):
        """Gets the name of the tile"""
        return self._name

    def get_id(self):
        """Return the id of the tile class

        Return:
            str: Gets a unique id for this class
        """
        return 'tile'

    def set_select(self, select: bool):
        """Sets the status of the tile

        Parameters:
            select (bool): The state of the tile
        """
        self._selectable = select

    def can_select(self):
        """Checks whether the tile is selectable.

        Return：
            bool: True when the tile is selectable, or False if the tile is not selectable
        """
        return self._selectable

    def __str__(self):
        return f"{self.__class__.__name__}('{self._name}', {self._selectable})"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._name}', {self._selectable})"


class Pipe(Tile):
    """Representation of a pipe in board game, these pipes have different shapes.

    In the game, player can adjust the orientation of the pipes by rotating these pipes to
    make the player form an effective pass and finally reach the end.
    """

    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    ST = PIPES["ST"]
    CO = PIPES["CO"]
    CR = PIPES["CR"]
    JT = PIPES["JT"]
    DI = PIPES["DI"]
    OU = PIPES["OU"]

    def __init__(self, name, orientation=0, selectable=True):
        """Construct a pipe object, add name, orientation and selectable attributes.

        Parameters:
            orientation (int): From zero to four represents the four directions, and
                the four directions can be rotated clockwise。
        """
        super().__init__(name, selectable)
        self._orientation = orientation

    def get_id(self):
        """Gets the id of the pipe class"""
        return 'pipe'

    def get_connected(self, side: str):
        """(list<str>) A list of all sides that are connected to the given side."""
        if self._name == self.ST:
            return self._get_straight_connection(side)
        elif self._name == self.CO:
            return self._get_corner_connection(side)
        elif self._name == self.CR:
            return self._get_cross_connection(side)
        elif self._name == self.JT:
            return self._get_junction_t_connection(side)
        elif self._name == self.DI:
            return self._get_diagonals_connection(side)
        elif self._name == self.OU:
            return self._get_over_under_connection(side)

    def _get_straight_connection(self, side: str):
        """Checks the direction that can be connected in the straight pipe from
        given side.

        Parameters:
            side (str): Four directions, namely east, south, west and north.

        Return:
            list<str>: Returns a list of possible connected sides.
        """
        vertical_ori = {self.NORTH: [self.SOUTH], self.SOUTH: [self.NORTH]}
        horizontal_ori = {self.EAST: [self.WEST], self.WEST: [self.EAST]}

        if self._orientation == 0 or self._orientation == 2:
            return vertical_ori.get(side, [])
        return horizontal_ori.get(side, [])

    def _get_corner_connection(self, side: str):
        """Returns a list of possible connected sides in corner pipe."""
        corner_ori_ne = {self.NORTH: [self.EAST], self.EAST: [self.NORTH]}
        corner_ori_se = {self.EAST: [self.SOUTH], self.SOUTH: [self.EAST]}
        corner_ori_sw = {self.SOUTH: [self.WEST], self.WEST: [self.SOUTH]}
        corner_ori_nw = {self.WEST: [self.NORTH], self.NORTH: [self.WEST]}
        if self._orientation == 0:
            return corner_ori_ne.get(side, [])
        elif self._orientation == 1:
            return corner_ori_se.get(side, [])
        elif self._orientation == 2:
            return corner_ori_sw.get(side, [])
        return corner_ori_nw.get(side, [])

    def _get_cross_connection(self, side: str):
        """Returns a list of possible connected sides in cross pipe."""
        cross_ori = {self.NORTH: [self.EAST, self.SOUTH, self.WEST],
                     self.EAST: [self.NORTH, self.SOUTH, self.WEST],
                     self.SOUTH: [self.NORTH, self.EAST, self.WEST],
                     self.WEST: [self.NORTH, self.EAST, self.SOUTH]}
        return cross_ori.get(side)

    def _get_junction_t_connection(self, side: str):
        """Returns a list of possible connected sides in junction-t pipe."""
        jt_ori_0 = {self.NORTH: [], self.EAST: [self.SOUTH, self.WEST], self.SOUTH: [self.EAST, self.WEST],
                    self.WEST: [self.EAST, self.SOUTH]}
        jt_ori_1 = {self.EAST: [], self.NORTH: [self.SOUTH, self.WEST], self.SOUTH: [self.WEST, self.NORTH],
                    self.WEST: [self.SOUTH, self.NORTH]}
        jt_ori_2 = {self.SOUTH: [], self.NORTH: [self.EAST, self.WEST], self.EAST: [self.NORTH, self.WEST],
                    self.WEST: [self.NORTH, self.EAST]}
        jt_ori_3 = {self.WEST: [], self.NORTH: [self.EAST, self.SOUTH], self.EAST: [self.NORTH, self.SOUTH],
                    self.SOUTH: [self.NORTH, self.EAST]}
        jt = [jt_ori_0, jt_ori_1, jt_ori_2, jt_ori_3]
        return jt[self._orientation][side]

    def _get_diagonals_connection(self, side: str):
        """Returns a list of possible connected sides in diagonals pipe."""
        diag_ori_0 = {self.NORTH: [self.EAST], self.EAST: [self.NORTH], self.SOUTH: [self.WEST],
                      self.WEST: [self.SOUTH]}
        diag_ori_1 = {self.NORTH: [self.WEST], self.EAST: [self.SOUTH], self.SOUTH: [self.EAST],
                      self.WEST: [self.NORTH]}
        return diag_ori_0.get(side) if self._orientation == 0 or \
                                       self._orientation == 2 else diag_ori_1.get(side)

    def _get_over_under_connection(self, side: str):
        """Returns a list of possible connected sides in over-under pipe."""
        ou_ori = {self.NORTH: [self.SOUTH], self.EAST: [self.WEST],
                  self.SOUTH: [self.NORTH], self.WEST: [self.EAST]}
        return ou_ori.get(side)

    def rotate(self, direction: int):
        """Rotates the selected pipe。

        The direction determines the rotation of the pipe.

        Parameters:
            direction (int): The plus or minus of an integer determines the direction of rotation.
        """
        self._orientation = (self._orientation + direction) % 4

    def get_orientation(self):
        """The orientation of the pipe determines what status the pipe is in.

        Return:
            int: An integer from 0 to 3
        """
        if self._orientation:
            if int(self._orientation) > 3:
                self._orientation = 0
            elif int(self._orientation) < 0:
                self._orientation = 3
        return self._orientation

    def __str__(self):
        return f"{self.__class__.__name__}('{self._name}', {self._orientation})"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._name}', {self._orientation})"


class SpecialPipe(Pipe):
    """Representation of two special pipes in the game.

    Special pipe inherits some methods of superclass pipe.
    """

    def get_id(self):
        """Gets a unique id for specific subclass"""
        return 'special_pipe'

    def __str__(self):
        return f"{self.__class__.__name__}({self._orientation})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self._orientation})"


class StartPipe(SpecialPipe):
    """Representation of the start pipe in the game."""

    def __init__(self, orientation=0):
        """Construct a start pipe object"""
        super().__init__("StartPipe", orientation, False)
        self._sides = [self.NORTH, self.EAST, self.SOUTH, self.WEST]

    def get_name(self):
        """Gets the name of start pipe"""
        return 'start'

    def get_connected(self, side=None):
        """Returns a list contains of the direction that start pipe is facing."""
        return [f"{self._sides[self._orientation]}"]


class EndPipe(SpecialPipe):
    """Representation of the end pipe in the game."""

    def __init__(self, orientation=0):
        """Construct an end pipe object"""
        super().__init__("EndPipe", orientation, False)
        self._sides = [self.NORTH, self.EAST, self.SOUTH, self.WEST]

    def get_name(self):
        """Gets the name of end pipe"""
        return 'end'

    def get_connected(self, side=None):
        """Returns a list contains the direction end pipe is facing."""
        if int(self._orientation) == 0 or int(self._orientation) == 1:
            return [f"{self._sides[self._orientation + 2]}"]
        elif int(self._orientation) == 2:
            return [f"{self._sides[0]}"]
        elif int(self._orientation) == 3:
            return [f"{self._sides[1]}"]


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
        self._board_layout, self._playable_pipes = self.load_file(game_file)
        self._start, self._end = self.end_pipe_positions()

    def load_file(self, game_file):
        """Load the board game elements and pipes information through IO"""

        # Reads csv file
        with open(game_file, "r") as f:
            lines = f.readlines()

            board_layout = []
            playable_pipes = {}
            pipes = ['straight', 'corner', 'cross', 'junction-t', 'diagonals', 'over-under']

            # Creates a list of lists to store board game elements
            for index, line in enumerate(lines[:-1]):
                board_row = []
                grids = line.split(",")
                for grid in grids:
                    char = "".join([i for i in grid if i.isalpha()])

                    if char in SPECIAL_TILES:
                        grid_name = SPECIAL_TILES[char]
                        if grid_name == START_PIPE:
                            cell = StartPipe(0 if grid.isalpha() else int(grid[-1]))
                        elif grid_name == END_PIPE:
                            cell = EndPipe(int(grid[-1]) if grid[-1].isdigit() else 0)
                        elif grid_name == LOCKED_TILE:
                            cell = Tile(LOCKED_TILE, False)

                    elif char in PIPES:
                        cell = Pipe(PIPES[char], 0 if grid.isalpha() else int(grid[-1]), False)

                    else:
                        cell = Tile(EMPTY_TILE, True)

                    board_row.append(cell)

                board_layout.append(board_row)

            # Creates a dictionary to store pipes and its quantity
            for i, value in enumerate(lines[-1].split(",")):
                playable_pipes[pipes[i]] = int(value)

            self._playable_pipes = playable_pipes
            self._board_layout = board_layout

        return self._board_layout, self._playable_pipes

    def get_board_layout(self):
        """Gets board game layout.

        Return:
            list<list<Tile, ...>>: Each elements represents tile or pipe in board.
        """
        return self._board_layout

    def get_board_pipes(self):
        """Gets a dictionary of pipe information.

        Return:
            dict<str:int>: Dictionary contains pipe and quantity information.
        """
        return self._playable_pipes

    def change_playable_amount(self, pipe_name: str, number: int):
        """Modifies the quantity of specific pipes according to their names

        Parameters:
            pipe_name (str): Name of specific pipes.
            number (int): Quantity of specific pipes.
        """
        if pipe_name in self._playable_pipes.keys():
            self._playable_pipes[pipe_name] += number

    def get_playable_pipes(self):
        """Gets the quantity of pipes that can be played and its number

        Return:
             dict<str:int>: Dictionary contains the information of playable pipes
        """
        return self._playable_pipes

    def get_pipe(self, position):
        """Gets Pipe or Tile elements at given position.

        Parameters:
            position (tuple<int, int>): The position of grid
        """
        cow, col = position
        if self._board_layout[cow][col].get_id() == 'pipe':
            return self._board_layout[cow][col]
        return Tile(EMPTY_TILE, True)

    def set_pipe(self, pipe: Pipe, position):
        """Places the specified pipe at the given position in the board game.

        The quantity of available pipes should also be modified.
        """
        cow, col = position
        self._board_layout[cow][col] = pipe
        self.change_playable_amount(pipe.get_name(), -1)

    def pipe_in_position(self, position):
        """Checks whether the given position is a pipe.

        Return:
            Pipe: Return pipe when the given position is pipe, otherwise return None
        """
        if position is not None:
            row, col = position
            pipe = self._board_layout[row][col]
            if row < len(self._board_layout) and col < len(self._board_layout[0]):
                if isinstance(pipe, Pipe) or isinstance(pipe, SpecialPipe):
                    return pipe
        return None

    def remove_pipe(self, position):
        """Removes the pipe in given position."""
        cow, col = position
        pipe = self._board_layout[cow][col]
        self._board_layout[cow][col] = (Tile('tile', True))
        self.change_playable_amount(pipe.get_name(), 1)

    def position_in_direction(self, direction, position):
        """According to the given direction and position information,
        if the resulting position is valid and not outbound, return its information.

        Return:
            tuple<str, tuple<int, int>>: The direction and position of the pipe could be connected.
        """
        rows = len(self._board_layout)
        cols = len(self._board_layout[0])
        row, col = position
        directions = ["N", "E", "S", "W"]
        if direction == directions[0] and row - 1 >= 0:
            return directions[2], (row - 1, col)
        elif direction == directions[1] and col + 1 < cols:
            return directions[3], (row, col + 1)
        elif direction == directions[2] and row + 1 < rows:
            return directions[0], (row + 1, col)
        elif direction == directions[3] and col - 1 >= 0:
            return directions[1], (row, col - 1)
        else:
            return None

    def end_pipe_positions(self):
        """Find and save the start and end pipe locations from the constructor"""
        return self.get_starting_position(), self.get_ending_position()

    def get_starting_position(self):
        """Gets the position of start pipe.

        Return:
            tuple<int, int>: The position of start pipe
        """
        for y, row in enumerate(self._board_layout):
            for x, cell in enumerate(row):
                if self._board_layout[y][x].get_name() == START_PIPE:
                    return y, x

    def get_ending_position(self):
        """Gets the position of end pipe."""
        for y, row in enumerate(self._board_layout):
            for x, cell in enumerate(row):
                if self._board_layout[y][x].get_name() == END_PIPE:
                    return y, x

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


def main():
    print("Please run gui.py instead")


if __name__ == "__main__":
    main()
