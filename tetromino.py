#!usr/bin/env python3
# Model tetromino as numpy array

import numpy as np

# Tetromino stored as np array that can be superimposed onto playing field array. This class handles rotations of the tetromino

class Tetromino():

    SHAPES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
    SHAPE_PRINT = [
        ' ',
        '\033[38;5;14mI\033[m',  # I -> cyan
        '\033[38;5;11mO\033[m',  # O -> yellow
        '\033[38;5;13mT\033[m',  # T -> purple
        '\033[38;5;10mS\033[m',  # S -> green
        '\033[38;5;9mZ\033[m',   # Z -> red
        '\033[38;5;12mJ\033[m',  # J -> blue
        '\033[38;5;208mL\033[m'] # L -> orange
    SHAPE_GRID = {
        'I' : [
                [1, 1, 1, 1]
            ],
        'O' : [
                [2, 2],
                [2, 2]
            ],
        'T' : [
                [0, 3, 0],
                [3, 3, 3]
            ],
        'S' : [
                [0, 4, 4],
                [4, 4, 0]
            ],
        'Z' : [
                [5, 5, 0],
                [0, 5, 5]
            ],
        'J' : [
                [6, 0, 0],
                [6, 6, 6]
            ],
        'L' : [
                [0, 0, 7],
                [7, 7, 7]
            ]}

    def __init__(self, shape, rotations=0):
        if shape.upper() in self.SHAPES:
            self.grid = np.array(self.SHAPE_GRID[shape.upper()],
                                 dtype=np.uint8)
        else:
            raise ValueError('Type {} not recognised'.format(shape))
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
        """ Perform 90 degrees clockwise rotations """
        self.rotations = (self.rotations + rotations) % 4
        # np.rot90 does anti-clockwise rotations so negative rotations are
        # performed
        self.grid = np.rot90(self.grid, -rotations)
        return self

    def reset_rotations(self):
        """ Rotate tetromino back to original position """
        self.rotate(-self.rotations)
        return self
    
    def spawn_column(self):
        """ Return column aligned with the spawn point of left side of the tetromino grid. """
        if self.shape is 'O':
            return 4
        else:
            return 3

    def flat(self):
        return self.grid.flat
    
    def copy(self):
        """ Return shallow copy of self """
        return Tetromino(self.shape, self.rotations)

    def elevation(self, col):
        """ Return number of empty spaces from bottom to lowest filled block in specified column  """
        if col < 0 or col >= self.width():
            raise ValueError('{} is not 0 <= col < width'.format(col))
        # get row of lowest filled block in column
        return (np.flip(self.grid[:,col] != 0)).argmax()

    def rotation_column_offset(self):
        """ Performing rotations shifts the column alignment of the block. Return the difference in column alignment between the spawn state and the rotated state. """
        if self.shape is 'O':
            return 0
        elif self.shape is 'I':
            return [0, 2, 0, 1][self.rotations]
        else:
            return [0, 1, 0, 0][self.rotations]

if __name__ == "__main__":
    tetromino = Tetromino('I')
    print(tetromino)
    tetromino = Tetromino('O')
    print(tetromino)
    tetromino = Tetromino('T',1)
    print(tetromino)
    tetromino = Tetromino('S')
    print(tetromino)
    tetromino = Tetromino('Z')
    print(tetromino)
    tetromino = Tetromino('J')
    print(tetromino)
    tetromino = Tetromino('L', 3)
    print(tetromino)
    
