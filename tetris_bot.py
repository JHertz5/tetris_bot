#!usr/bin/env python3
# Plays tetris using by modelling, solving and displaying the game

from src.game import Game
from src.solver import Solver
from src.display import update_display


def main():

    # Initialise game objects
    solver = Solver()
    game = Game()

    while not game.is_over():
        chosen_outcome = solver.decide_outcome(game)
        game.next_turn(chosen_outcome)
        update_display(game)
    print("GAME OVER")


if __name__ == "__main__":
    main()
