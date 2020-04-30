"""
Graphical User Interface (GUI) for Pipe

When this script is run, it will attempt to open and play a game
of Pipe using the Pipe model in a2.py.

For the game to play successfully, everything must be correctly
implemented in a2.py.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

from a2 import *


class SelectionPanel(tk.Canvas):
    """
    Sidebar display of the selectable pipes.

    Shows all the types of pipes that can be placed within the game and how many are left to be placed.
    """
    def __init__(self, master, playable_pipes, panel_selection=None, selected=None, *args, **kwargs):
        """
        Construct a new selection panel canvas.

        Parameters:
            master (tk.Widget): Widget within which to place the selection panel.
            playable_pipes (dict<str, int>): Mapping of types of pipes to amount of pipes remaining.
            panel_selection (callable): Function or method to call when a pipe is selected.
            selected (str): Type of pipe that is currently selected.
        """
        super().__init__(master, *args, **kwargs)
        self._master = master

        self._selected = selected
        self._playable = playable_pipes
        self._panel_selection = panel_selection

        # map pipe types to their pipe display and remaining count
        self._pipes = {}

        self.draw_pipes()
        self.redraw()

    def draw_pipes(self):
        """Draw all the pipes in the selection panel"""
        for pipe_type in self._playable:
            image = get_image(f"images/{pipe_type}0")
            pipe_frame = tk.Frame(self, highlightthickness=2)
            selection = tk.Label(pipe_frame, image=image)
            selection.image = image

            selection.pack(side=tk.TOP)
            selection.bind("<Button-1>", lambda e, pipe=pipe_type: self._handle_click(pipe))

            number = tk.Label(pipe_frame, text=f"{self._playable[pipe_type]}")
            number.pack(side=tk.TOP)
            pipe_frame.pack(side=tk.TOP)
            pipe_frame.bind("<Button-1>", lambda e, pipe=pipe_type: self._handle_click(pipe))

            self._pipes[pipe_type] = (pipe_frame, number)

    def redraw(self, selected=None):
        """Update the pipes with current information

        - Sets the outline of selected pipes to red
        - Updates the amount of remaining pipes
        """
        for pipe, (frame, number) in self._pipes.items():
            if pipe == selected and self._playable[selected] > 0:
                border = "red"
            else:
                border = "white"
            frame.config(highlightbackground=border)
            number.config(text=f"{self._playable[pipe]}")

    def _handle_click(self, pipe):
        """Called when a pipe is clicked, handling calling the callback panel_selection method"""
        if self._panel_selection is not None:
            self._panel_selection(pipe)


class BoardView(tk.Canvas):
    """View of the Pipe game board"""

    def __init__(self, master, board_layout, place_pipe=None, remove_pipe=None, *args, **kwargs):
        """Construct a board view from a board_layout.

        Parameters:
            master (tk.Widget): Widget within which the board is placed.
            board_layout (list<list<Tile>>): 2D array of tiles in a board.
            place_pipe (callable): Callable to call when a pipe is being placed.
            remove_pipe (callable): Callable to call when a pipe is being removed.
        """
        super().__init__(master, *args, **kwargs)
        self._master = master

        self._board_layout = board_layout
        self.place_pipe = place_pipe
        self.remove_pipe = remove_pipe

        self._board = self.load_board()

    def load_board(self):
        """(list<list<Tile>>) Create a 2D array of labels representing the board to display."""
        labels = []

        for y, row in enumerate(self._board_layout):
            board_row = []
            for x, tile in enumerate(row):
                placement = tk.Label(self, text="T")
                placement.grid(column=x, row=y, ipady=4, ipadx=4)

                self.bind_clicks(placement, tile, (y, x))
                board_row.append(placement)

            labels.append(board_row)

        return labels

    def redraw(self):
        """Redraw the game board by updating the images displayed in each grid"""
        for y, row in enumerate(self._board_layout):
            for x, tile in enumerate(row):
                position = (y, x)
                image = self._load_tile_image(tile)

                placement = self._board[y][x]
                placement.config(image=image)
                placement.image = image
                self.bind_clicks(placement, tile, position)

    def bind_clicks(self, label, tile, position):
        """Bind clicks on a label to the left and right click handlers.

        Parameters:
            label (tk.Widget): Label which clicks should bound to.
            tile (Tile): Tile to pass as a parameter to the handlers.
            position (tuple<int, int>): Position to pass as a parameter to the handlers.
        """
        # bind left click
        label.bind("<Button-1>", lambda e, tile=tile, position=position: self._handle_left_click(tile, position))
        # bind right click
        # right click can be either Button-2 or Button-3 depending on operating system
        for i in range(2, 4):
            label.bind(f"<Button-{i}>",
                       lambda e, tile=tile, position=position: self._handle_right_click(tile, position))

    def _handle_left_click(self, pipe, position):
        """Handle left clicking on a tile to place a pipe.

        Calls the provided place_pipe method if available and pipe is selectable.
        """
        if self.place_pipe is not None and pipe.can_select():
            self.place_pipe(position)

    def _handle_right_click(self, pipe, position):
        """Handle right clicking on a tile"""
        if self.remove_pipe is not None and pipe.get_id() == "pipe" and pipe.can_select():
            if pipe.get_name() in PIPES.values():
                self.remove_pipe(position)

    def _load_tile_image(self, tile):
        """Load the PhotoImage to use for a given tile.

        If the tile class has not been fully implemented defaults to images/tile
        """
        try:
            if tile.get_id() != "tile":
                image = get_image(f"images/{tile.get_name()}{tile.get_orientation()}")
            else:
                image = get_image(f"images/{tile.get_name()}")
        except AttributeError:
            print("get_name(), get_orientation() and get_id() methods need to be implemented correctly.",
                  "\n",
                  "Make sure all class attributes are defined correctly.",
                  "\n")
            image = get_image("images/tile")

        return image


class GameApp:
    """Game application that manages communication between the selection panel, board view and game model."""

    def __init__(self, master):
        """Create a new game app within a master widget"""
        self._master = master
        self._level = ""
        self._game = PipeGame()

        self._selected = None

        # initialise GUI variables that are assigned in the draw method
        self._selection, self._board_view, self._button_frame = None, None, None
        self.draw()

    def select_pipe(self, pipe):
        """Select a pipe to be placed from the selection panel.

        Parameters:
            pipe (Pipe): The selected pipe.
        """
        # ignore selection if not enough pipes available
        if self._game.get_playable_pipes()[pipe] <= 0:
            return

        # unselect if pipe is clicked twice
        if self._selected == pipe:
            pipe = None

        self._selected = pipe
        self._selection.redraw(selected=self._selected)

    def place_pipe(self, position):
        """Place the selected pipe on the game board.

        Parameters:
            position (tuple<int, int>): The position to place the pipe within the board.
        """
        selected = self._selected
        # tile at the placing position
        tile = self._game.get_pipe(position)

        if tile.can_select() and selected is not None and tile.get_id() == "tile":
            self._game.set_pipe(Pipe(selected), position)

        # rotate already placed pipes
        if tile.get_id() == "pipe":
            tile.rotate(1)

        # unselect when placed
        self._selected = None
        self._selection.redraw()

        self._board_view.redraw()
        self.check_game_over()

    def remove_pipe(self, position):
        """Remove the pipe at the given position

        Parameters:
            position (tuple<int, int>): The position to remove the pipe from.
        """
        self._game.remove_pipe(position)
        self._board_view.redraw()
        self._selection.redraw()

    def check_game_over(self):
        """Check if the game is over and exit if so"""
        if self._game.check_win():
            messagebox.showinfo("Game Over", "You won! :D")
            self._master.destroy()

    def new_game(self):
        """Start a new level from the user inputted selection."""
        self._level = simpledialog.askstring("Input", "What level would you like to play?",
                                             parent=self._master)
        if self._level is not None:
            self.reset_game()

    def reset_game(self):
        """Restart the game on the current level."""
        if self._level == "":
            self._game = PipeGame()
        else:
            self._game = PipeGame(self._level)
        self.redraw()

    def redraw(self):
        """Redraw the whole game window."""
        self._selection.destroy()
        self._board_view.destroy()
        self._button_frame.destroy()

        self.draw()

    def draw(self):
        """Draw the game to the master widget."""
        try:
            self._selection = SelectionPanel(self._master, self._game.get_playable_pipes(), self.select_pipe)
            self._selection.pack(side=tk.LEFT)
        except AttributeError:
            print("get_playable_pipes() method needs to be implemented correctly.",
                  "\n")
        try:
            self._board_view = BoardView(self._master, self._game.get_board_layout(), self.place_pipe, self.remove_pipe)
            self._board_view.redraw()
            self._board_view.pack(side=tk.LEFT)
        except AttributeError:
            print("get_board_layout() method needs to be implemented correctly.",
                  "\n")

        self._button_frame = tk.Frame(self._master)

        restart_button = tk.Button(self._button_frame, text="Restart", command=self.reset_game)
        restart_button.pack(side=tk.TOP)

        new_button = tk.Button(self._button_frame, text="New Game", command=self.new_game)
        new_button.pack(side=tk.TOP)

        self._button_frame.pack(side=tk.LEFT)


def get_image(image_name):
    """(tk.PhotoImage) Get a image file based on capability.

    If a .png doesn't work, default to the .gif image.
    """
    try:
        image = tk.PhotoImage(file=image_name + ".png")
    except tk.TclError:
        image = tk.PhotoImage(file=image_name + ".gif")
    return image


def main():
    root = tk.Tk()
    root.title("Game")

    GameApp(root)

    root.update()
    root.mainloop()


if __name__ == "__main__":
    main()
