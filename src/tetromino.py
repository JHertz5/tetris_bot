#!usr/bin/env python3
# Model tetromino as numpy array

import numpy as np
import random


class Tetromino:

    # Each shape stored in a cuboid grid space in the default rotation. Zero-values represent empty space and non-zero
    # values represent space filled by the shape. The non-zero numbers each correspond to the shape.
    SHAPE_GRID = {
        "I": [[1, 1, 1, 1]],
        "O": [[2, 2], [2, 2]],
        "T": [[0, 3, 0], [3, 3, 3]],
        "S": [[0, 4, 4], [4, 4, 0]],
        "Z": [[5, 5, 0], [0, 5, 5]],
        "J": [[6, 0, 0], [6, 6, 6]],
        "L": [[0, 0, 7], [7, 7, 7]],
    }
    SHAPES = list(SHAPE_GRID.keys())
    SHAPE_MAX_HEIGHT = max([len(x) for x in SHAPE_GRID.values()])
    SHAPE_MAX_WIDTH = max([len(x[0]) for x in SHAPE_GRID.values()])

    def __init__(self, shape, rotations=0):
        if shape.upper() in self.SHAPES:
            self.grid = np.array(self.SHAPE_GRID[shape.upper()], dtype=np.uint8)
        else:
            raise ValueError("Type {} not recognised".format(shape))
        self.shape = shape
        self.rotations = 0
        self.rotate(rotations)

    def __str__(self):
        return self.shape

    def __getitem__(self, key):
        return self.grid[key]

    def height(self):
        return self.grid.shape[0]

    def width(self):
        return self.grid.shape[1]

    def rotate(self, rotations=1):
        """Perform 90 degrees clockwise rotations"""
        self.rotations = (self.rotations + rotations) % 4
        # np.rot90 does anti-clockwise rotations so negative rotations are
        # performed
        self.grid = np.rot90(self.grid, -rotations)
        return self

    def reset_rotations(self):
        """Rotate tetromino back to original position"""
        self.rotate(-self.rotations)
        return self

    def spawn_column(self):
        """
        Return column aligned with the spawn point of left side of the
        tetromino grid.
        """
        if self.shape == "O":
            return 4
        else:
            return 3

    def flat(self):
        return self.grid.flat

    def copy(self):
        """Return shallow copy of self"""
        return Tetromino(self.shape, self.rotations)

    def elevation(self, col):
        """
        Return number of empty spaces from bottom to lowest filled block
        in specified column .
        """
        if col < 0 or col >= self.width():
            raise ValueError("{} is not 0 <= col < width".format(col))
        # get row of lowest filled block in column
        return (np.flip(self.grid[:, col] != 0)).argmax()

    def get_zero_padded_grid(self):
        """
        Return a version of the grid padded to the maximum tetromino dimensions
        """
        padded_grid = np.zeros(
            (self.SHAPE_MAX_HEIGHT, self.SHAPE_MAX_WIDTH), dtype=np.uint8
        )
        height, width = self.grid.shape
        padded_grid[0:height, 0:width] = self.grid
        return padded_grid

    def get_zero_padded_grid_string_list(self):
        """
        Return a grid string list of the zero padded grid
        """
        print_str = []
        padded_grid = self.get_zero_padded_grid()
        for row in range(len(padded_grid)):
            print_str.append("".join(str(x) for x in padded_grid[row, :]))
        return print_str


def get_random_tetromino():
    """
    Return a randomly selected tetromino
    """
    return Tetromino(random.choice(Tetromino.SHAPES))


if __name__ == "__main__":
    tetromino = Tetromino("I")
    print(tetromino)
    tetromino = Tetromino("O")
    print(tetromino)
    tetromino = Tetromino("T", 1)
    print(tetromino)
    tetromino = Tetromino("S")
    print(tetromino)
    tetromino = Tetromino("Z")
    print(tetromino)
    tetromino = Tetromino("J")
    print(tetromino)
    tetromino = Tetromino("L", 3)
    print(tetromino)
