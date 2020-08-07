#!usr/bin/env python3
# Functions to print numpy grids representing tetris playfields and tetrominos

import numpy as np

def print_grid(grid):
    grid_string = ''
    if grid.ndim == 2:
        for col in grid:
            for value in col:
                if value == 0:
                    grid_string += ' '
                else:
                    grid_string += str(value)
            grid_string += '\n'
    elif grid.ndim == 1:
        for value in grid:
            if value == 0:
                grid_string += ' '
            else:
                grid_string += str(value)
    else:
        raise ValueError('Grid must be either 1 or 2 dimensions')

    return grid_string