#!usr/bin/env python3
# Attempts to play tetris using simple CV and keyboard inputs
# Intended for tetris link: https://tetris.com/play-tetris

from tetromino import Tetromino
from tetromino_queue import TetrominoQueue
from playfield import Playfield
from solver import Solver

import random


def main():

    # Initialise game objects
    solver = Solver()
    playfield = Playfield()
    tetromino_queue = TetrominoQueue()

    # Get first tetronimo and hold it, since it is always optimal to have a piece held.
    tetromino = tetromino_queue.get_next()
    playfield.hold_tetromino(tetromino)

    while not playfield.is_game_over():
        tetromino = tetromino_queue.get_next()
        chosen_outcome = solver.decide_outcome(playfield, tetromino)
        playfield.execute_outcome(chosen_outcome, tetromino)
        playfield.print_display()
        print(tetromino_queue)
    print("GAME OVER")


if __name__ == "__main__":
    main()
