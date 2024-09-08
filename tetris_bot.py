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
    playfield.hold_tetromino(tetromino_queue.get_next())

    while not playfield.is_game_over():
        current_tetromino = tetromino_queue.get_next()
        chosen_outcome = solver.decide_outcome(playfield, current_tetromino)
        playfield.execute_outcome(chosen_outcome, current_tetromino)
        playfield.print_display()
        print(tetromino_queue)
    print("GAME OVER")


if __name__ == "__main__":
    main()
