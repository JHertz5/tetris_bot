#!usr/bin/env python3
# Attempts to play tetris using simple CV and keyboard inputs
# Intended for tetris link: https://tetris.com/play-tetris

from tetromino import Tetromino
from playfield import Playfield
from solver import Solver

import random


def main():

    solver = Solver()
    playfield = Playfield()
    game_over = False

    shape = random.choice(Tetromino.SHAPES)
    tetromino = Tetromino(shape)
    tetromino = playfield.hold_tetromino(tetromino)

    while not playfield.is_game_over():
        shape = random.choice(Tetromino.SHAPES)
        tetromino = Tetromino(shape)
        chosen_outcome = solver.decide_outcome(playfield, tetromino)
        playfield.execute_outcome(chosen_outcome, tetromino)
        playfield.print_display()
    print("GAME OVER")


if __name__ == "__main__":
    main()
