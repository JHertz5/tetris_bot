#!usr/bin/env python3
# Model tetromino as numpy array

import numpy as np

# Tetromino stored as np array that can be superimposed onto playing field array. This class handles rotations of the tetromino

class Tetromino(object):

    SHAPES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
    SHAPE_PRINT = [
        ' ',
        '\033[36mI\033[m',       # I -> cyan
        '\033[33mO\033[m',       # O -> yellow
        '\033[35mT\033[m',       # T -> purple
        '\033[32mS\033[m',       # S -> green
        '\033[31mZ\033[m',       # Z -> red
        '\033[34mJ\033[m',       # J -> blue
        '\033[38;5;214mL\033[m'  # L -> orange
    ]
    SHAPE_SPAWN_POSITION = {
        'I' : (3, 3),
        'O' : (2, 4),
        'T' : (2, 3),
        'S' : (2, 3),
        'Z' : (2, 3),
        'J' : (2, 3),
        'L' : (2, 3)
    }
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
            ]
    }

    def __init__(self, shape, rotations=0):
        if shape.upper() in self.SHAPES:
            self.grid = np.array(self.SHAPE_GRID[shape.upper()],
                                 dtype=np.uint8)
        else:
            raise ValueError('Type {} not recognised'.format(shape))
        self.shape = shape
        assert(rotations < 4)
        self.rotations = 0
        self.rotate(rotations)

    def __str__(self):
        grid_string = ''
        if self.grid.ndim == 2:
            col_strings = []
            for col in self.grid:
                col_strings.append( ''.join([self.SHAPE_PRINT[x] for x in col]) )
            grid_string = '\n'.join(col_strings)
        elif self.grid.ndim == 1:
            grid_string += ''.join(self.grid)
        else:
            raise ValueError('Grid must be either 1 or 2 dimensions')
        return grid_string

    def __getitem__(self, key):
        return self.grid[key]

    def height(self):
        return self.grid.shape[0]

    def width(self):
        return self.grid.shape[1]

    def rotate(self, rotations=1):
        """ Perform 90 degrees clockwise rotations """
        self.rotations += rotations % 4
        # np.rot90 does anti-clockwise rotations so negative rotations are
        # performed
        self.grid = np.rot90(self.grid, -rotations)
        return self

    def reset_rotations(self):
        """ Rotate tetromino back to original position """
        self.rotate(-self.rotations)
        return self
    
    def spawn_position(self):
        """ Return spawn position of top left block of tetromino grid. Note that this may be an empty square """
        return self.SHAPE_SPAWN_POSITION[self.shape]

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
    
