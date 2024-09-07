#!usr/bin/env python3
# Model tetris playfield as numpy array

import numpy as np

from tetromino import Tetromino

class Playfield():

    HEIGHT = 22
    WIDTH  = 10

    def __init__(self, grid=None, held_tetromino=None):
        # set up grid
        if grid is not None:
            assert(isinstance(grid, np.ndarray))
            assert(grid.shape == (self.HEIGHT, self.WIDTH))
            self.grid = np.array( grid, dtype=np.uint8)
        else:
            self.grid = np.zeros((self.HEIGHT, self.WIDTH), dtype=np.uint8)
        # set up held tetromino
        if held_tetromino is not None:
            assert(isinstance(held_tetromino, Tetromino))
        self.held_tetromino = held_tetromino

    def __str__(self):
        print_str  = '  ┌' + '─' * (self.WIDTH * 2 + 1) + '┐\n'
        for row in range(self.HEIGHT):
            print_str += ('{:2d}│ '.format(row)
                          + ' '.join(Tetromino.SHAPE_PRINT[x] for x
                            in self.grid[row, :])
                          + ' │\n')
        print_str += '  └' + '─' * (self.WIDTH * 2 + 1) + '┘\n'
        print_str += '    ' + ' '.join([str(x) for x in range(self.WIDTH)])
        return print_str

    def _test_position_(self, tetromino, position):
        """
        Check whether the tetromino is out of bounds or overlapping existing
        blocks when in the specified position. It is assumed that position
        specifies the position of the top left block of the tetromino grid
        (which may be an empty block).
        """
        # Test whether placement puts tetromino out of bounds
        if ( position[1] <  0
             or position[0] < 0
             or position[1] + tetromino.width() > self.WIDTH
             or position[0] + tetromino.height() > self.HEIGHT ):
            return False
        # Test for overlap
        # Get grid area where tetromino would be locked
        test_grid = self.grid[
                position[0] : position[0] + tetromino.height(),
                position[1] : position[1] + tetromino.width()]
        for test_block, tetr_block in zip(test_grid.flat, tetromino.flat()):
            if test_block != 0 and tetr_block != 0:
                return False
        return True

    def _get_drop_row_(self, tetromino, start_col):
        """
        Return the row of the top block of the tetromino if the tetromino
        is dropped with its left side aligned with the specified column.
        """
        end_col = start_col + tetromino.width()
        if start_col < 0 or end_col > self.WIDTH:
            raise ValueError('drop puts tetromino out of bounds}')
        drop_row = self.HEIGHT # Initialise to lowest possible row
        # For each column, get the drop row ignoring other columns. The
        # highest of these is the final drop row
        for tetr_col, grid_col in enumerate(range(start_col, end_col)):
            # 8 appended to column represent floor of playing field
            col_data = np.append(self.grid[:, grid_col], 8)
            # Get row number of highest filled row
            stack_top = (col_data != 0 ).argmax()
            col_drop_row = ( stack_top
                             - tetromino.height()
                             + tetromino.elevation(tetr_col))
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
                grid_position = (position[0] + tetr_row,
                                 position[1] + tetr_col)
                tetr_position = (tetr_row, tetr_col)
                # Overwrite grid value with tetromino value
                if tetromino[tetr_position] != 0:
                    self.grid[grid_position] = tetromino[tetr_position]

    def _clear_filled_lines_(self):
        """
        Check for and remove filled lines. Return number of lines cleared
        """
        num_cleared_lines = np.count_nonzero([row.all() for row in self.grid])
        # Get rows that are partially filled
        part_rows = np.array([row for row in self.grid if (not row.all()
                                                           and row.any())])
        self.grid.fill(0)
        if part_rows.any():
            self.grid[self.HEIGHT - part_rows.shape[0] :,:] = part_rows
        return num_cleared_lines

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
        Drop tetromino with left side aligned with specified column. Return
        drop row.
        """
        assert isinstance(tetromino, Tetromino)
        row = self._get_drop_row_(tetromino, col)
        self._lock_tetromino_(tetromino, (row, col))
        self._clear_filled_lines_()
        return row

    def get_heights(self):
        """ Return array containing heights of each column """
        # Append 8 to each column to represent floor
        grid_with_floor = np.append(self.grid, [[8] * self.WIDTH], axis=0)
        return self.HEIGHT - (grid_with_floor != 0).argmax(axis=0)

    def get_gap_count(self):
        """ Return number of gaps in stack """
        # Count number of zeros after top of stack for each column
        return sum([np.count_nonzero(col[top:] == 0) for col, top in
                    zip(self.grid.T, self.HEIGHT - self.get_heights())])

    def get_gap_depth(self):
        """ Return sum of gap depth in stack """
        # Get the row of the lowest gap for each column
        lowest_gaps = (self.HEIGHT
                       - (np.flip(self.grid, axis=0) == 0).argmax(axis=0))
        return sum(lowest_gaps - (self.HEIGHT - self.get_heights())  + 1)

    def get_well_count(self):
        """
        Return number of "wells" in stack that are > 2 deep, i.e. can only
        be cleared by I shape.
        """
        # Get height of top filled block in each column
        col_heights = self.HEIGHT - self.get_heights()
        # Append walls on either side represented with height 0
        col_heights_walled = np.concatenate(([0], col_heights, [0]))
        # Get difference between column height and column height to the
        # left/right for each column
        left_diffs = col_heights - col_heights_walled[0 : self.WIDTH]
        right_diffs = col_heights - col_heights_walled[2 : self.WIDTH+2]
        # If column on both sides is > 2 higher, column is a well
        return sum((left_diffs > 2) & (right_diffs > 2))

    def copy(self):
        return Playfield(self.grid, self.held_tetromino)

    def execute_outcome(self, outcome, tetromino):
        if outcome['hold_swap']:
            tetromino = self.hold_tetromino(tetromino)
        # If hold swap returned an empty Tetromino, skip movement
        if tetromino is not None:
            tetromino.rotate(outcome['rotations'])
            self.drop_tetromino(tetromino, outcome['col'])
        print(self)

    def is_game_over(self):
        """
        Return true if the game is over.
        """
        return max(self.get_heights()) == self.HEIGHT
