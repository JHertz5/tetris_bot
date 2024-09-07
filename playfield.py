#!usr/bin/env python3
# Model tetris playfield as numpy array

import numpy as np

from tetromino import Tetromino


class Playfield:

    MAIN_BOX_HEIGHT = 22
    MAIN_BOX_WIDTH = 10

    HOLD_BOX_HEIGHT = 2
    HOLD_BOX_WIDTH = 5

    def __init__(self, grid=None, held_tetromino=None):
        # Set up grid
        if grid is not None:
            assert isinstance(grid, np.ndarray)
            assert grid.shape == (self.MAIN_BOX_HEIGHT, self.MAIN_BOX_WIDTH)
            self.grid = np.array(grid, dtype=np.uint8)
        else:
            self.grid = np.zeros(
                (self.MAIN_BOX_HEIGHT, self.MAIN_BOX_WIDTH), dtype=np.uint8
            )
        # Set up held tetromino
        if held_tetromino is not None:
            assert isinstance(held_tetromino, Tetromino)
        self.held_tetromino = held_tetromino
        self.num_rows_cleared = 0
        self.num_blocks_placed = 0

    def __str__(self):
        print_str = []
        # Print the top of the main box
        print_str.append("  ┌" + "─" * (self.MAIN_BOX_WIDTH * 2 + 1) + "┐")
        # Print the rows inside the main box
        for row in range(self.MAIN_BOX_HEIGHT):
            print_str.append(
                "{:2d}│ ".format(row)
                + " ".join(Tetromino.SHAPE_PRINT[x] for x in self.grid[row, :])
                + " │"
            )
        # Print the bottom of the main box
        print_str.append("  └" + "─" * (self.MAIN_BOX_WIDTH * 2 + 1) + "┘")
        print_str.append(
            "    " + " ".join([str(x) for x in range(self.MAIN_BOX_WIDTH)])
        )

        # TODO maybe make this as a separate list and append it on afterwards? Once you've figured out the basics.
        # Print the top of the hold box
        print_str[0] += " ┌" + "─" * (self.HOLD_BOX_WIDTH * 2 + 1) + "┐"
        print_str[1] += " │  H O L D  │"

        held_tetromino_grid = self.held_tetromino.grid.copy()
        held_tetromino_grid.resize((2, 4), refcheck=False)
        held_tetromino_grid = self.held_tetromino.get_zero_padded_grid()

        for row in range(self.HOLD_BOX_HEIGHT):
            print_str[row + 2] += (
                " │  "
                + " ".join(
                    Tetromino.SHAPE_PRINT[x] for x in held_tetromino_grid[row, :]
                )
                + "  │"
            )

        # Print the bottom of the hold box
        print_str[2 + self.HOLD_BOX_HEIGHT] += "".join(
            [" └" + "─" * (self.HOLD_BOX_WIDTH * 2 + 1) + "┘"]
        )

        return "\n".join(print_str)

    def _get_drop_row_(self, tetromino, start_col):
        """
        Return the row of the top block of the tetromino if the tetromino
        is dropped with its left side aligned with the specified column.
        """
        end_col = start_col + tetromino.width()
        if start_col < 0 or end_col > self.MAIN_BOX_WIDTH:
            raise ValueError("drop puts tetromino out of bounds}")
        # Initialise to lowest possible row
        drop_row = self.MAIN_BOX_HEIGHT
        # For each column, get the drop row ignoring other columns. The
        # highest of these is the final drop row
        for tetr_col, grid_col in enumerate(range(start_col, end_col)):
            # 8 appended to column represent floor of playing field
            col_data = np.append(self.grid[:, grid_col], 8)
            # Get row number of highest filled row
            stack_top = (col_data != 0).argmax()
            col_drop_row = (
                stack_top - tetromino.height() + tetromino.elevation(tetr_col)
            )
            # Keep highest row, other drop rows will be overlapping in other
            # columns
            drop_row = min(drop_row, col_drop_row)
        return drop_row

    def _lock_tetromino_(self, tetromino, position):
        """
        Lock the tetromino in the field at specified position. It is assumed
        that position specifies the destination of the top left block of the
        tetromino grid (which may be an empty block). Note that if the
        tetromino is locked is a position that overlaps with existing filled
        blocks, the new tetromino will overwrite the exsting blocks.
        """
        for tetr_col in range(tetromino.width()):
            for tetr_row in range(tetromino.height()):
                grid_position = (position[0] + tetr_row, position[1] + tetr_col)
                tetr_position = (tetr_row, tetr_col)
                # Overwrite grid value with tetromino value
                if tetromino[tetr_position] != 0:
                    self.grid[grid_position] = tetromino[tetr_position]

    def _clear_filled_rows_(self):
        """
        Check for and remove filled rows. Return a list of the rows cleared
        """
        # Get the number of the rows that are filled
        num_cleared_rows = np.count_nonzero([row.all() for row in self.grid])
        # Get rows that are partially filled
        part_rows = np.array(
            [row for row in self.grid if (not row.all() and row.any())]
        )
        # Reset grid with zeros
        self.grid.fill(0)
        # Refill the bottom of the grid with the partially filled rows, leaving out rows that were filled.
        if part_rows.any():
            self.grid[self.MAIN_BOX_HEIGHT - part_rows.shape[0] :, :] = part_rows
        return num_cleared_rows

    def hold_tetromino(self, tetromino):
        """
        Store tetromino (without rotations) and return previously held
        tetromino (if there is one)
        """
        assert isinstance(tetromino, Tetromino)
        swap = self.held_tetromino
        self.held_tetromino = tetromino.reset_rotations()
        return swap

    def drop_tetromino(self, tetromino, col):
        """
        Drop tetromino with left side aligned with specified column. This ends the turn, so update the score as
        required. Return drop row.
        """
        assert isinstance(tetromino, Tetromino)
        row = self._get_drop_row_(tetromino, col)
        self._lock_tetromino_(tetromino, (row, col))
        num_cleared_rows = self._clear_filled_rows_()
        self.num_rows_cleared += num_cleared_rows
        self.num_blocks_placed += 1
        return row

    def get_heights(self):
        """Return array containing heights of each column"""
        # Append 8 to each column to represent floor
        grid_with_floor = np.append(self.grid, [[8] * self.MAIN_BOX_WIDTH], axis=0)
        return self.MAIN_BOX_HEIGHT - (grid_with_floor != 0).argmax(axis=0)

    def get_gap_count(self):
        """Return number of gaps in stack"""
        # Count number of zeros after top of stack for each column
        return sum(
            [
                np.count_nonzero(col[top:] == 0)
                for col, top in zip(
                    self.grid.T, self.MAIN_BOX_HEIGHT - self.get_heights()
                )
            ]
        )

    def get_gap_depth(self):
        """Return sum of gap depth in stack"""
        # Get the row of the lowest gap for each column
        lowest_gaps = self.MAIN_BOX_HEIGHT - (np.flip(self.grid, axis=0) == 0).argmax(
            axis=0
        )
        return sum(lowest_gaps - (self.MAIN_BOX_HEIGHT - self.get_heights()) + 1)

    def get_well_count(self):
        """
        Return number of "wells" in stack that are > 2 deep, i.e. can only
        be cleared by I shape.
        """
        # Get height of top filled block in each column
        col_heights = self.MAIN_BOX_HEIGHT - self.get_heights()
        # Append walls on either side represented with height 0
        col_heights_walled = np.concatenate(([0], col_heights, [0]))
        # Get difference between column height and column height to the
        # left/right for each column
        left_diffs = col_heights - col_heights_walled[0 : self.MAIN_BOX_WIDTH]
        right_diffs = col_heights - col_heights_walled[2 : self.MAIN_BOX_WIDTH + 2]
        # If column on both sides is > 2 higher, column is a well
        return sum((left_diffs > 2) & (right_diffs > 2))

    def copy(self):
        return Playfield(self.grid, self.held_tetromino)

    def execute_outcome(self, outcome, tetromino):
        if outcome["hold_swap"]:
            tetromino = self.hold_tetromino(tetromino)
        # If hold swap returned an empty Tetromino, skip movement
        if tetromino is not None:
            tetromino.rotate(outcome["rotations"])
            self.drop_tetromino(tetromino, outcome["col"])

    def is_game_over(self):
        """
        Return true if the game is over.
        """
        return max(self.get_heights()) == self.MAIN_BOX_HEIGHT

    def print_display(self):
        """
        Print a graphical representation of the playfield.
        """
        # Clear the console using an ANSI escape code
        # See https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_(Control_Sequence_Introducer)_sequences for more
        # information
        print("\033c\033[3J", end="")
        # Print the progress metrics
        print(
            "num blocks placed = {}, num rows cleared = {}".format(
                self.num_blocks_placed, self.num_rows_cleared
            )
        )
        # Print the playfield
        print(self)
