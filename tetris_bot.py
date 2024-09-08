#!usr/bin/env python3
# Attempts to play tetris using simple CV and keyboard inputs
# Intended for tetris link: https://tetris.com/play-tetris

from src import tetromino
from src.holder import Holder
from src.tetromino_queue import TetrominoQueue
from src.playfield import Playfield
from src.solver import Solver
from src.display import update_display


def main():

    # Initialise game objects
    solver = Solver()
    playfield = Playfield()
    tetromino_queue = TetrominoQueue()
    holder = Holder()

    # Get first tetronimo and hold it, since it is always optimal to have a piece held.
    holder.swap(tetromino.get_random_tetromino())

    while not playfield.is_game_over():
        current_tetromino = tetromino_queue.get_next()
        chosen_outcome = solver.decide_outcome(
            playfield, current_tetromino, holder.held_tetromino
        )
        playfield.execute_outcome(chosen_outcome, current_tetromino, holder)
        update_display(playfield, holder, tetromino_queue)
    print("GAME OVER")


if __name__ == "__main__":
    main()
