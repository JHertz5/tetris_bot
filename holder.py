#!usr/bin/env python3
# Manage the tetromino hold storeage and swapping.

from tetromino import Tetromino


class Holder:

    HOLD_BOX_HEIGHT = 2

    def __init__(self, held_tetromino=None):
        # Set up held tetromino
        if held_tetromino is not None:
            assert isinstance(held_tetromino, Tetromino)
        self.held_tetromino = held_tetromino

    def __str__(self):
        print_str = []
        print_str.append("HOLD")
        # Get the zero-padded shape and print it into the hold box
        held_tetromino_grid = self.held_tetromino.get_zero_padded_grid()
        for row in range(self.HOLD_BOX_HEIGHT):
            print_str.append("".join(str(x) for x in held_tetromino_grid[row, :]))

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
