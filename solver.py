#!usr/bin/env python3
# Given playfield and tetromino, decide best action and determine moves needed to take action.

import numpy as np
import random

from tetromino import Tetromino
from playfield import Playfield

class Solver():

    WEIGHTS = [
        100, # game_over
        20,  # wells
        10,  # gaps
        2,   # mean_height   TODO check whether this actually makes difference
        -5,  # cleared_lines TODO check whether this actually makes difference
        -7.5 # row
    ]
    WEIGHTS_VECTOR = np.array(WEIGHTS, dtype=np.int8)

    def __init__(self):
        pass
    
    def get_all_outcomes(self, playfield, tetromino):
        """ Get all potential outcomes so that they can be scored and filtered """
        assert(isinstance(playfield, Playfield))
        assert(isinstance(tetromino, Tetromino))

        outcomes = []
        hold_swap_options = [False]
        if playfield.held_tetromino is not None:
            hold_swap_options += [True]

        for hold_swap in hold_swap_options:
            if hold_swap:
                active_tetromino = playfield.held_tetromino
            else:
                active_tetromino = tetromino
            # Get all outcomes for each hold/rotate permutation of tetromino
            for tetr in [active_tetromino.copy().rotate(n) for n in range(4)]:
                for col in range(playfield.WIDTH - tetr.width() + 1):
                    outcome_playfield = playfield.copy()
                    row, cleared_lines = outcome_playfield.drop_tetromino(tetr, col)
                    outcomes.append({
                        'playfield' : outcome_playfield,
                        'tetromino': tetr,
                        'row' : row,
                        'col' : col,
                        'hold_swap' : hold_swap,
                        'gaps' : outcome_playfield.get_gap_count(),
                        'wells' : outcome_playfield.get_well_count(),
                        'mean_height' : outcome_playfield.get_mean_height(),
                        'cleared_lines' : cleared_lines,
                        'game_over' : playfield.is_game_over(tetr, col)
                    })
        return outcomes

    def get_outcome_cost(self, outcome):
        """ Get scoring vector for outcome by performing dot product with
            weights vector. Each outcome is scored on the following paramters:
                Whether it causes game over
                How many gaps it contains (fewer is better)
                Mean height of stack (lower is better)
                How many wells it contains (fewer is better)
                Cleared lines (more is better)
                Drop row (lower is better)
        """
        score_vector  = np.array([
            outcome['game_over'],
            outcome['wells'],
            outcome['gaps'],
            outcome['mean_height'],
            outcome['cleared_lines'],
            outcome['row']
        ], dtype=np.uint8)
        return np.dot(score_vector, Solver.WEIGHTS_VECTOR)

    def decide_outcome(self, playfield, tetromino):
        """ Score and filter all potential outcomes to determine the best action to take. Return outcome that has lowest cost """
        outcomes = self.get_all_outcomes(playfield, tetromino)
        for index, outcome in enumerate(outcomes):
            outcomes[index]['cost'] = self.get_outcome_cost(outcome)
        # Filter out any outcome that results in game_over. If there is no surviving outcome, just return the first outcome
        lowest_cost = min([outcome['cost'] for outcome in outcomes])
        outcomes = list(filter(lambda outcome: outcome['cost'] == lowest_cost, outcomes))
        # With multiple top scoring outcomes, selection is arbitrary. Return the first one
        return outcomes[0]

if __name__ == "__main__":
    solver = Solver()
    playfield = Playfield()
    game_over = False

    shape = random.choice(Tetromino.SHAPES)
    tetromino = Tetromino(shape)
    tetromino = playfield.hold_tetromino(tetromino)

    score = 0
    while not game_over:
        shape = random.choice(Tetromino.SHAPES)
        tetromino = Tetromino(shape)
        chosen_outcome = solver.decide_outcome(playfield, tetromino)
        col = chosen_outcome['col']
        if chosen_outcome['hold_swap']:
            playfield.hold_tetromino(tetromino)
        tetromino = chosen_outcome['tetromino']
        game_over = playfield.is_game_over(tetromino, col)
        playfield.drop_tetromino(tetromino, col)
        print('score = {}, cost = {}'.format(score, chosen_outcome['cost']))
        print(playfield)
        score += 1
    print('GAME OVER, score = {}'.format(score))
    print(chosen_outcome)
