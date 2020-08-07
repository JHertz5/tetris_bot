#!usr/bin/env python3
# Model tetris playfield as numpy array

import numpy as np

from tetromino import Tetromino
import grid_printer

class Playfield():
    HEIGHT = 22
    WIDTH  = 10

    def __init__(self, grid=None):
        if grid is not None:
            assert(type(grid) is np.ndarray)
            assert(grid.shape == (self.HEIGHT, self.WIDTH))
            self.grid = np.array( grid, dtype=np.uint8)
        else:
            self.grid = np.zeros((self.HEIGHT, self.WIDTH), dtype=np.uint8)

    def __str__(self):
        return grid_printer.print_grid(self.grid)

if __name__ == "__main__":
    playfield = Playfield()
    playfield2 = Playfield(playfield.grid)
    print(playfield)
