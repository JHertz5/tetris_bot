#!usr/bin/env python3
# Manage the tetromino hold storeage and swapping.

from .tetromino import Tetromino


class Holder:

    def __init__(self, held_tetromino=None):
        # Set up held tetromino
        if held_tetromino is not None:
            assert isinstance(held_tetromino, Tetromino)
        self.held_tetromino = held_tetromino

    def __str__(self):
        print_str = []
        # Add a title
        print_str.append("HOLD")
        # Append empty line
        print_str.append(" " * Tetromino.SHAPE_MAX_WIDTH)
        # Append the tetromino's zero padded grid string
        print_str += self.held_tetromino.get_zero_padded_grid_string_list()

        return "\n".join(print_str)

    def swap(self, tetromino):
        """
        Store tetromino (without rotations) and return previously held
        tetromino
        """
        assert isinstance(tetromino, Tetromino)
        swap = self.held_tetromino
        self.held_tetromino = tetromino.reset_rotations()
        return swap


if __name__ == "__main__":
    tetromino_holder = Holder()
    print(tetromino_holder)
