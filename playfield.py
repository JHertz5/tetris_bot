#!usr/bin/env python3
# Model tetris playfield as numpy array

import numpy as np
import random

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
                          + ' '.join(Tetromino.SHAPE_PRINT[x] for x in self.grid[row, :])
                          + ' │\n')
        print_str += '  └' + '─' * (self.WIDTH * 2 + 1) + '┘\n'
        print_str += '    ' + ' '.join([str(x) for x in range(self.WIDTH)])
        return print_str

    def _test_position_(self, tetromino, position):
        """ Check whether the tetromino is out of bounds or overlapping existing blocks when in the specified position. It is assumed that position specifies the position of the top left block of the tetromino grid (which may be an empty block). """
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
        """ Return the row of the top block of the tetromino if the tetromino is dropped with its left side aligned with the specified column """
        end_col = start_col + tetromino.width()
        if start_col < 0 or end_col > self.WIDTH:
            raise ValueError('drop puts tetromino out of bounds}')
        drop_row = self.HEIGHT # initialise to lowest possible row
        # for each column, get the drop row ignoring other columns. The highest of these is the final drop row
        for tetr_col, grid_col in enumerate(range(start_col, end_col)):
            # 8 appended to column represent floor of playing field
            col_data = np.append(self.grid[:, grid_col], 8)
            # Get row number of highest filled row
            stack_top = (col_data != 0 ).argmax()
            col_drop_row = ( stack_top
                             - tetromino.height()
                             + tetromino.elevation(tetr_col))
            # keep highest row, other drop rows will be overlapping in other columns
            drop_row = min(drop_row, col_drop_row)
        return drop_row

    def _lock_tetromino_(self, tetromino, position):
        """ Lock the tetromino in the field at specified position. It is assumed that position specifies the destination of the top left block of the tetromino grid (which may be an empty block). Note that if the tetromino is locked is a position that overlaps with existing filled blocks, the new tetromino will overwrite the exsting blocks. """
        for tetr_col in range(tetromino.width()):
            for tetr_row in range(tetromino.height()):
                grid_position = (position[0] + tetr_row,
                                 position[1] + tetr_col)
                tetr_position = (tetr_row, tetr_col)
                # Overwrite grid value with tetromino value
                if tetromino[tetr_position] != 0:
                    self.grid[grid_position] = tetromino[tetr_position]

    def _clear_filled_lines_(self):
        """ Check for and remove filled lines. Return number of lines cleared """
        num_cleared_lines = np.count_nonzero([row.all() for row in self.grid])
        # Get rows that are partially filled
        part_rows = np.array([row for row in self.grid if (not row.all()
                                                           and row.any())])
        self.grid.fill(0)
        if part_rows.any():
            self.grid[self.HEIGHT - part_rows.shape[0] :,:] = part_rows
        return num_cleared_lines

    def hold_tetromino(self, tetromino):
        """ Store tetromino (without rotations) and return previously held tetromino (if there is one) """
        assert isinstance(tetromino, Tetromino)
        swap = self.held_tetromino
        self.held_tetromino = tetromino.reset_rotations()
        return swap

    def drop_tetromino(self, tetromino, col):
        """ Drop tetromino with left side aligned with specified column. Return drop row """
        assert isinstance(tetromino, Tetromino)
        row = self._get_drop_row_(tetromino, col)
        self._lock_tetromino_(tetromino, (row, col))
        num_cleared_lines = self._clear_filled_lines_()
        return row, num_cleared_lines

    def get_gap_count(self):
        """ Return number of gaps in stack """
        # Append 8 to each column to represent floor
        field_with_floor = np.append(self.grid, [[8] * self.WIDTH], axis=0)
        # Get top stack row for each column so that leading 0s can be cut off
        col_tops = (field_with_floor != 0).argmax(axis=0)
        # Count number of zeros after top of stack for each columnss
        col_gaps = [np.count_nonzero(col[top:] == 0) for col, top in
                    zip(self.grid.T, col_tops)]
        return sum(col_gaps)

    def get_well_count(self):
        """ Return number of "wells" in stack that are > 2 deep, i.e. can only be cleared by I shape """
        field_with_floor = np.append(self.grid, [[8] * self.WIDTH], axis=0)
        # Get height of top filled block in each column
        col_heights = (field_with_floor != 0).argmax(axis=0)
        # Append walls on either side represented with height 0
        col_heights_walled = np.concatenate(([0], col_heights, [0]))
        # Get difference between column height and column height to the left/right for each column
        left_diffs = col_heights - col_heights_walled[0 : self.WIDTH]
        right_diffs = col_heights - col_heights_walled[2 : self.WIDTH+2]
        # If column on both sides is > 2 higher, column is a well
        return sum((left_diffs > 2) & (right_diffs > 2))

    def get_mean_height(self):
        """ Return the mean value of the stack height """
        # Append 8 to each column to represent floor
        field_with_floor = np.append(self.grid, [[8] * self.WIDTH], axis=0)
        # Get height of top filled block in each column and take mean
        return self.HEIGHT - np.mean((field_with_floor != 0).argmax(axis=0))

    def is_game_over(self, tetromino, col):
        """ Spawn and check drop of tetromino with left side aligned with specified column. Return whether game has ended.
            Game can end in two ways:
                - A piece is spawned overlapping with an existing
                  block (block out)
                - A piece locks completely above row 2 (lock out)
        """
        assert isinstance(tetromino, Tetromino)
        if not self._test_position_(tetromino.copy().reset_rotations(),
                                    tetromino.spawn_position()):
            return True # Game over (block out)
        row = self._get_drop_row_(tetromino, col)
        if row + tetromino.height() < 2:
            return True # Game over (lock out)
        return False

    def copy(self):
        return Playfield(self.grid, self.held_tetromino)

if __name__ == "__main__":
    playfield = Playfield()
    game_over = False

    while not game_over:
        shape = random.choice(Tetromino.SHAPES)
        tetromino = Tetromino(shape)
        game_over = playfield.is_game_over(tetromino, 0)
        playfield.drop_tetromino(tetromino, 0)
    print(playfield)
    print(playfield.get_well_count())
    print('   G A M E   O V E R')
