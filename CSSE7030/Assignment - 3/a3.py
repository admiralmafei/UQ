import time
import tkinter as tk
import random
from tkinter import messagebox

LENGTH = 60
TASK_ONE = 1
TASK_TWO = 2
POKEMON = "@"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (UP, DOWN, LEFT, RIGHT,
              f"{UP}-{LEFT}", f"{UP}-{RIGHT}",
              f"{DOWN}-{LEFT}", f"{DOWN}-{RIGHT}")
FLAG = "♥"
UNEXPOSED = "#"
EXPOSED = "0"


class BoardModel:
    """The model class of the game, responsible for executing the function and logic of the game"""

    def __init__(self, grid_size, num_pokemon):
        """
        Construct a new game board and some elements.

        Parameters:
            grid_size (int): The grid size of the game.
            num_pokemon (int): The number of pokemon of the game
        """
        self._game_board = UNEXPOSED * (grid_size ** 2)
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._pokemon_locations = self.generate_pokemon(grid_size)
        self._pokeball = self._num_pokemon

    def get_game(self):
        """Return game string information which can represent the state of the game."""
        return self._game_board

    def get_pokemon_locations(self):
        """Get pokemon location information"""
        return self._pokemon_locations

    def change_pokeball_number(self, number):
        """Change the number of pokeballs based on player actions on the status bar."""
        self._pokeball += number

    def get_pokeball_number(self):
        """Get the number of pokemon on the status bar."""
        return self._pokeball

    def generate_pokemon(self, grid_size):
        """Pokemons will be generated and given a random index within the game.

        Parameters:
            grid_size (int): The grid size of the game.

        Returns:
            (tuple<int>): A tuple containing  indexes where the pokemons are
            created for the game string.
        """
        cell_count = grid_size ** 2
        pokemon_locations = ()

        for _ in range(self._num_pokemon):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count - 1)

            while index in pokemon_locations:
                index = random.randint(0, cell_count - 1)

            pokemon_locations += (index,)

        return pokemon_locations

    def check_pokemon(self, index):
        """Check whether there is a pokemon hide in this index. """
        if index in self._pokemon_locations:
            self._num_pokemon -= 1
            return True
        return False

    def replace_character_at_index(self, index, character):
        """A specified index in the game string at the specified index is replaced by
        a new character.

        Parameters:
            index (int): The index in the game string where the character is replaced.
            character (str): The new character that will be replacing the old character.

        Returns:
            (str): The updated game string.
        """
        self._game_board = self._game_board[:index] + character + self._game_board[index + 1:]

    def get_num_pokemon(self):
        """Return the number of pokemon in the game."""
        return self._num_pokemon

    def big_fun_search(self, grid_size, pokemon_locations, index):
        """Searching adjacent cells to see if there are any Pokemon"s present.

        Parameters:
            grid_size (int): Size of game.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            index (int): Index of the currently selected cell

        Returns:
            (list<int>): List of cells to turn visible.
        """
        queue = [index]
        discovered = [index]
        visible = []

        if self._game_board[index] == FLAG:
            return queue

        number = self.number_at_cell(pokemon_locations, grid_size, index)
        if number != 0:
            return queue

        while queue:
            node = queue.pop()
            for neighbour in self.neighbour_directions(node, grid_size):
                if neighbour in discovered:
                    continue

                discovered.append(neighbour)
                if self._game_board[neighbour] != FLAG:
                    number = self.number_at_cell(pokemon_locations, grid_size, neighbour)
                    if number == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible

    def neighbour_directions(self, index, grid_size):
        """Seek out all direction that has a neighbouring cell.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.

        Returns:
            (list<int>): A list of index that has a neighbouring cell.
        """
        neighbours = []
        for direction in DIRECTIONS:
            neighbour = self.index_in_direction(index, grid_size, direction)
            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours

    def position_to_index(self, position, grid_size):
        """Convert the row, column coordinate in the grid to the game strings index.

        Parameters:
            position (tuple<int, int>): The row, column position of a cell.
            grid_size (int): The grid size of the game.

        Returns:
            (int): The index of the cell in the game string.
        """
        x, y = position
        return x * self._grid_size + y

    def index_in_direction(self, index, grid_size, direction):
        """The index in the game string is updated by determining the
        adjacent cell given the direction.
        The index of the adjacent cell in the game is then calculated and returned.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.
            direction (str): The direction of the adjacent cell.

        Returns:
            (int): The index in the game string corresponding to the new cell position
            in the game.

            None for invalid direction.
        """
        col = index % grid_size
        row = index // grid_size
        if RIGHT in direction:
            col += 1
        elif LEFT in direction:
            col -= 1
        # Notice the use of if, not elif here
        if UP in direction:
            row -= 1
        elif DOWN in direction:
            row += 1
        if not (0 <= col < grid_size and 0 <= row < grid_size):
            return None
        return col + row * int(grid_size)

    def flag_cell(self, index):
        """Toggle Flag on or off at selected index. If the selected index is already
        revealed, the game would return with no changes.

        Parameters:
            index (int): The index in the game string where a flag is placed.
        Returns
            (str): The updated game string.
        """
        if self._game_board[index] == FLAG:
            self.replace_character_at_index(index, UNEXPOSED)

        elif self._game_board[index] == UNEXPOSED:
            self.replace_character_at_index(index, FLAG)

        return self._game_board

    def number_at_cell(self, pokemon_locations, grid_size, index):
        """Calculates what number should be displayed at that specific index in the game.

        Parameters:
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (int): Number to be displayed at the given index in the game string.
        """
        count = 0
        neighbour_list = self.neighbour_directions(index, grid_size)
        if index not in pokemon_locations:
            for cell in neighbour_list:
                if cell in pokemon_locations:
                    count += 1
            return count

    def check_win(self):
        """Checking if the player has won the game.

        Returns:
            (bool): True if the player has won the game, false if not.

        """
        return UNEXPOSED not in self._game_board and self._game_board.count(FLAG) == len(self._pokemon_locations)

    def restart(self):
        """According to the player's instructions, restart this game."""
        self._game_board = UNEXPOSED * (self._grid_size ** 2)

    def newgame(self):
        """According to the player's instructions, create a new game,
        and reset the pokemon position."""
        self._game_board = UNEXPOSED * (self._grid_size ** 2)
        self._pokemon_locations = self.generate_pokemon(self._grid_size)


class BoardView(tk.Canvas):
    """The view class of the game, responsible for the representation of the GUI of
    the game board."""

    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        """Construct a board view from a game string.

        Parameters:
            master (tk.Widget): Widget within which the board is placed.

        """
        super().__init__(master, *args, **kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self._statusbar = None
        self._board = None

        self.config(height=self._board_width, width=self._board_width)

    def draw_board(self, board: BoardModel):
        """Draw the layout of the game board by identifying the character string.
        """
        self._board = board
        self.delete(tk.ALL)

        for row in range(self._grid_size):
            for col in range(self._grid_size):
                char = self._board.get_game()[self.position_to_index((col, row), self._grid_size)]
                x1 = row * LENGTH
                y1 = col * LENGTH
                x2 = x1 + LENGTH
                y2 = y1 + LENGTH
                if char == UNEXPOSED:
                    self.create_rectangle(x1, y1, x2, y2, fill='dark green')
                elif char == POKEMON:
                    self.create_rectangle(x1, y1, x2, y2, fill="yellow")
                elif char.isdigit():
                    self.create_rectangle(x1, y1, x2, y2, fill="light green")
                    self.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=char)
                elif char == FLAG:
                    self.create_rectangle(x1, y1, x2, y2, fill="red")

        self.bind_clicks()

    def bind_clicks(self):
        """Bind clicks on a label to the left and right click handlers."""
        # call back function, e: event
        self.bind("<Button-1>", lambda e: self._handle_left_click((e.x, e.y)))
        self.bind("<Button-2>", lambda e: self._handle_right_click((e.x, e.y)))
        self.bind("<Button-3>", lambda e: self._handle_right_click((e.x, e.y)))

    def _handle_left_click(self, pixel):
        """Add the left click button with game function.

        Cover the grid according to the method written in the model class,
        including left click on tall grass square with hidden pokemon or not,
        it can check win or loss as well.
        """
        position = self.pixel_to_position(pixel)
        index = self.position_to_index(position, self._grid_size)

        if self._board.check_pokemon(index):
            for pokemon_index in self._board.get_pokemon_locations():
                self._board.replace_character_at_index(pokemon_index, POKEMON)
            self.draw_board(self._board)
            response = messagebox.askyesno("Game Over", "You lose! Would you like to play again?")
            if response:
                self._statusbar.restart_game()
            else:
                self._master.quit()

        else:
            number = self._board.number_at_cell(self._board.get_pokemon_locations(), self._grid_size, index)
            self._board.replace_character_at_index(index, str(number))
            clear = self._board.big_fun_search(self._grid_size, self._board.get_pokemon_locations(),
                                               index)
            for i in clear:
                if self._board.get_game()[i] != FLAG:
                    number = self._board.number_at_cell(self._board.get_pokemon_locations(), self._grid_size, i)
                    self._board.replace_character_at_index(i, str(number))

            self.draw_board(self._board)
            if self._board.check_win():
                pass

    def _handle_right_click(self, pixel):
        """Add the right click button with game function.
        Put the pokemon ball in the right click position.
        """
        position = self.pixel_to_position(pixel)
        index = self.position_to_index(position, self._grid_size)

        if self._board.get_game()[index] == UNEXPOSED:
            self._board.replace_character_at_index(index, FLAG)
            self._board.change_pokeball_number(-1)
            self._statusbar.update_label(self._board.get_pokeball_number())

        elif self._board.get_game()[index] == FLAG:
            self._board.replace_character_at_index(index, UNEXPOSED)
            self._board.change_pokeball_number(1)
            self._statusbar.update_label(self._board.get_pokeball_number())

        self.draw_board(self._board)

        if self._board.check_win():
            messagebox.showinfo("Game over", "You won! :D")
            self._master.destroy()

    def get_bbox(self, pixel):
        """Returns the bounding box for a cell centered at the provided pixel coordinates."""
        pass

    def position_to_index(self, position, grid_size):
        """Convert the row, column coordinate in the grid to the game strings index.

        Parameters:
            position (tuple<int, int>): The row, column position of a cell.
            grid_size (int): The grid size of the game.

        Returns:
            (int): The index of the cell in the game string.
        """
        x, y = position
        return x * self._grid_size + y

    def pixel_to_position(self, pixel):
        """Converts the supplied pixel to the position of the cell it is contained
        within."""
        x, y = pixel
        return y // LENGTH, x // LENGTH

    def get_status(self, status):
        """Call the Statusbar class"""
        self._statusbar = status


class ImageBoardView(BoardView):
    """The subclass of BoardView, complete the requirements of the graphical interface of the game board"""

    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        super().__init__(master, grid_size, board_width, *args, **kwargs)
        self._images = []

    def draw_board(self, board: BoardModel):
        """Draw the game board by using the specified picture to form a graphical interface at a specific
        string position"""

        self._board = board
        self.delete(tk.ALL)

        for row in range(self._grid_size):
            for col in range(self._grid_size):
                char = self._board.get_game()[self.position_to_index((col, row), self._grid_size)]
                x1 = row * LENGTH
                y1 = col * LENGTH
                x2 = x1 + LENGTH
                y2 = y1 + LENGTH

                if char == UNEXPOSED:
                    image = tk.PhotoImage(file="./images/unrevealed.png")
                elif char == POKEMON:
                    image = tk.PhotoImage(file=f"./images/pokemon_sprites/{self.get_pokemon_pic()}")
                elif char == FLAG:
                    image = tk.PhotoImage(file="./images/pokeball.png")
                elif char.isdigit():
                    image = tk.PhotoImage(file=f"./images/{self.get_num_pic(char)}")
                else:
                    image = None
                self._images.append(image)
                self.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=image)

        self.bind_clicks()

    def get_pokemon_pic(self):
        """Create a list to store randomly selected pictures."""
        pictures = ['pikachu.png', 'togepi.png', 'charizard.gif', 'cyndaquil.png', 'psyduck.png', 'umbreon.png']

        index = random.randint(0, (len(pictures) - 1))
        return pictures[index]

    def get_num_pic(self, char):
        """Create a dictionary to store pictures with the number and then place them according to the
        index of specific numbers"""
        pictures = {'0': 'zero_adjacent.png', '1': 'one_adjacent.png', '2': 'two_adjacent.png',
                    '3': 'three_adjacent.png', '4': 'four_adjacent.png', '5': 'five_adjacent.png',
                    '6': 'six_adjacent.png', '7': 'seven_adjacent.png', '8': 'eight_adjacent.png'}
        return pictures.get(char)


class StatusBar(tk.Frame):
    """A widget contains several game details and two functional buttons"""

    def __init__(self, master, num_pokemon, grid_size):
        super().__init__(master)
        self._master = master
        self._num_pokemon = num_pokemon
        self._grid_size = grid_size
        self._time = time.time()
        self._model = BoardModel(grid_size, num_pokemon)
        self._board = None

        self._pokeball = tk.PhotoImage(file=f"./images/{self.pokemonball()}")
        self._timer_pic = tk.PhotoImage(file="./images/clock.png")

        status_left = tk.Frame(self._master, padx=50, width=200)

        pokemon_ball = tk.Label(status_left, image=self._pokeball)
        pokemon_ball.pack(side=tk.LEFT)
        self._attempted_catches = tk.Label(status_left, text=f"0 attempted catches")
        self._attempted_catches.pack(side=tk.TOP, anchor=tk.W)
        self._pokemon_left = tk.Label(status_left, text=f"{num_pokemon} pokeball left")
        self._pokemon_left.pack(side=tk.TOP, anchor=tk.W)

        status_left.pack(side=tk.LEFT)

        status_mid = tk.Frame(self._master, width=200)

        time_elapse = tk.Label(status_mid, image=self._timer_pic)
        time_elapse.pack(side=tk.LEFT)
        self._timer_text = tk.Label(status_mid, text="Time elapse")
        self._timer_text.pack(side=tk.TOP, anchor=tk.W)
        self._timer_second = tk.Label(status_mid, text="0m 00s", font=('Times', 20))
        self._timer_second.pack(side=tk.TOP, anchor=tk.W)
        self.update_clock()

        status_mid.pack(side=tk.LEFT)

        status_right = tk.Frame(self._master, padx=30)

        self._new_game = tk.Button(status_right, text="New game", command=self.new_game)
        self._new_game.pack(side=tk.TOP, anchor=tk.W, padx=10)
        self._restart_game = tk.Button(status_right, text="Restart game", command=self.restart_game)
        self._restart_game.pack(side=tk.TOP, anchor=tk.W)

        status_right.pack(side=tk.LEFT)

    def pokemonball(self):
        """Change pokeball picture turns gray when there is no pokemon ball."""
        pokemonball = ['full_pokeball.png', 'empty_pokeball.png']
        if self._num_pokemon == 0:
            return pokemonball[1]

        return pokemonball[0]

    def update_label(self, pokeball):
        """Update the information about the number of pokeball left and attempted catches"""
        self._pokemon_left.config(text=f"{pokeball} attempted catches")
        self._attempted_catches.config(text=f"{self._num_pokemon - pokeball} pokeball left")

    def update_clock(self):
        """Update timer"""
        seconds = int(time.time() - self._time)
        self._timer_second.config(text=f"{seconds // 60}m {seconds % 60}s")
        self._master.after(1000, self.update_clock)

    def reset_time(self):
        """Reset timer when the game is restart."""
        self._time = time.time()

    def get_board_view(self, board):
        """Call the BoardView class"""
        self._board = board

    def new_game(self):
        """Create a new game, and pokemon locations are changing."""
        self.reset_time()
        self._model.newgame()
        self.update_label(self._model.get_pokeball_number())
        self._board.draw_board(self._model)

    def restart_game(self):
        """Restart the game without changing the pokemon locations"""
        self.reset_time()
        self._model.restart()
        self.update_label(self._model.get_pokeball_number())
        self._board.draw_board(self._model)


class PokemonGame:
    """The controller class of the game, responsible for managing the cooperation
    between model class and view class."""

    def __init__(self, master, grid_size=10, num_pokemon=10, task=TASK_TWO):
        """Create a new game app within a master widget"""
        self._master = master
        self._length = LENGTH
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._task = task
        self._model = BoardModel(self._grid_size, num_pokemon)
        self._board = None
        self._text = tk.Text(master)
        self._statusbar = None
        self.menu()
        self.draw()

    def menu(self):
        """Create the filemenu."""
        menubar = tk.Menu(self._master)
        self._master.config(menu=menubar)

        filename = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=filename)
        filename.add_command(label='Save game', command=self.save)
        filename.add_command(label='Load game', command=self.load)
        filename.add_command(label='Restart game', command=self.restart)
        filename.add_command(label='Quit', command=self.quit)

    def save(self):
        """Save current game in order to play later."""
        record_page = tk.Tk()
        record_page.title('Save your game!')
        label = tk.Label(record_page, text='Enter your name:').pack(side=tk.LEFT)
        entry = tk.Entry(record_page).pack(side=tk.LEFT)

        def record():
            name = entry.get()
            with open("save_game.txt", 'w') as f:
                f.write(f"{name} {self._model.get_game()}\n")

        enter = tk.Button(record_page, text='enter', command=record).pack(side=tk.LEFT)

    def load(self):
        """Load the game."""
        with open('save_time.txt', 'r') as f:
            game_string = []
            for line in f:
                game = line.split()
                game_string.append(game[1])

        self._model._game_board = game_string
        self._board.draw_board(self._model)

    def restart(self):
        """Restart the game."""
        self._board.get_status(self._statusbar)
        self._statusbar.restart_game()

    def quit(self):
        """Quit the game."""
        response = messagebox.askyesno("Quit game!", "Whether you are sure to quit?")
        if response:
            self._master.destroy()

    def draw(self):
        """Draw the master widget of the game board."""
        label = tk.Label(self._master, bg="IndianRed2", fg="white", text="Pokemon: Got 2 Find them All!",
                         font=("Courier", 20, "bold"), padx=10)
        label.pack(side=tk.TOP, fill=tk.BOTH)

        if self._task == TASK_ONE:
            self._board = BoardView(self._master, self._grid_size, self._grid_size * LENGTH)
        elif self._task == TASK_TWO:
            self._board = ImageBoardView(self._master, self._grid_size, self._grid_size * LENGTH)

        self._board.pack()
        self._board.draw_board(self._model)

        self._statusbar = StatusBar(self._master, self._grid_size, self._num_pokemon)
        self._board.get_status(self._statusbar)
        self._statusbar.pack(side=tk.BOTTOM)
        self._statusbar.get_board_view(self._board)


def main():
    root = tk.Tk()
    root.title("Pokemon: Got 2 Find them All!")
    root.resizable(False, False)

    PokemonGame(root)

    root.update()
    root.mainloop()


if __name__ == "__main__":
    main()
