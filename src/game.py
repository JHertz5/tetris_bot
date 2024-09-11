#!/usr/bin/env python3
# Top-level wrapper for the game elements, i.e. playfield, holder, etc.

from src import tetromino
from src.holder import Holder
from src.tetromino_queue import TetrominoQueue
from src.playfield import Playfield


class Game:

    def __init__(self):
        # Initialise game objects
        self.playfield = Playfield()
        self.tetromino_queue = TetrominoQueue()
        self.holder = Holder()
        # Get first tetronimo and hold it, since it is always optimal to have a piece held
        self.holder.swap(self.tetromino_queue.get_next())
        # Get the next tetromino ready for the first turn
        self.current_tetromino = self.tetromino_queue.get_next()

    def is_over(self):
        """
        Return true if the game is over
        """
        return self.playfield.is_game_over()

    def next_turn(self, chosen_outcome):
        """
        Progress the gamestate to the next turn, using the chosen outcome to determine the placement of the current
        teromino.
        """
        # Execute the outcome chosen by the solver
        self.playfield.execute_outcome(
            chosen_outcome, self.current_tetromino, self.holder
        )
        # Get the next tetromino ready
        self.current_tetromino = self.tetromino_queue.get_next()
