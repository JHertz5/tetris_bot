#!usr/bin/env python3
# Model Tetromino as numpy array

import numpy as np
import grid_printer

# Tetromino stored as np array that can be superimposed onto playing field array. This class handles rotations of the tetromino

class Tetromino(object):

    TYPES = [' ', 'I', 'O', 'T', 'S', 'Z', 'J', 'L']
    TYPE_COLOUR = {} # TODO
    TYPE_GRID = {
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

    def __init__(self, letter):
        if letter.upper() in self.TYPES [1:]:
            self.grid = np.array( self.TYPE_GRID[ letter.upper() ], dtype=np.uint8 )
        else:
            raise ValueError('Type {} not recognised'.format(letter))

    def __str__(self):
        return grid_printer.print_grid(self.grid)

    def rotate(self):
        self.grid = np.rot90(self.grid, 3)
        return self

if __name__ == "__main__":
    tetromino = Tetromino('I')
    tetromino.rotate()
    print('{}'.format(tetromino))
    tetromino = Tetromino('O')
    print('{}'.format(tetromino))
    tetromino = Tetromino('T')
    tetromino.rotate()
    print('{}'.format(tetromino))
    tetromino = Tetromino('S')
    print('{}'.format(tetromino))
    tetromino = Tetromino('Z')
    print('{}'.format(tetromino))
    tetromino = Tetromino('J')
    print('{}'.format(tetromino))
    tetromino = Tetromino('L')
    print('{}'.format(tetromino))
