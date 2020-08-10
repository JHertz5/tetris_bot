#!usr/bin/env python3
# Given playfield and tetromino, decide best action and determine moves needed to take action.

import numpy as np
import random

from tetromino import Tetromino
from playfield import Playfield

class Solver():

    # These weights are almost definitely not optimal, but they have been manually tuned to be "good enough"
    WEIGHTS = [
        20,  # wells
        10,  # gaps
        -10   # row
    ]
    WEIGHTS_VECTOR = np.array(WEIGHTS, dtype=np.int8)

    def __init__(self):
        pass
    
    def get_all_outcomes(self, playfield, tetromino, ban_hold=False):
        """ Get all potential outcomes so that they can be scored and filtered """
        assert(isinstance(playfield, Playfield))
        assert(isinstance(tetromino, Tetromino))

        outcomes = []
        hold_swap_options = [False]
        if not ban_hold:
            hold_swap_options += [True]

        for hold_swap in hold_swap_options:
            if hold_swap and playfield.held_tetromino is None:
                outcomes.append({
                    'playfield' : playfield,
                    'tetromino': None,
                    'rotations' : 0,
                    'row' : outcome_playfield.HEIGHT,
                    'col' : 0,
                    'hold_swap' : hold_swap,
                    'gaps' : outcome_playfield.get_gap_count(),
                    'wells' : outcome_playfield.get_well_count(),
                })
                continue
            else:
                if hold_swap:
                    active_tetromino = playfield.held_tetromino
                else:
                    active_tetromino = tetromino
            # Get all outcomes for each hold/rotate permutation of tetromino
            for tetr in [active_tetromino.copy().rotate(n) for n in range(4)]:
                for col in range(playfield.WIDTH - tetr.width() + 1):
                    outcome_playfield = playfield.copy()
                    row = outcome_playfield.drop_tetromino(tetr, col)
                    outcomes.append({
                        'playfield' : outcome_playfield,
                        'tetromino': tetr,
                        'rotations' : tetr.rotations,
                        'row' : row,
                        'col' : col,
                        'hold_swap' : hold_swap,
                        'gaps' : outcome_playfield.get_gap_count(),
                        'wells' : outcome_playfield.get_well_count(),
                    })
        return outcomes

    def get_outcome_cost(self, outcome):
        """ Get scoring vector for outcome by performing dot product with
            weights vector. Each outcome is scored on the following paramters:
                How many gaps it contains (fewer is better)
                How many wells it contains (fewer is better)
                Drop row (lower is better)
        """
        score_vector  = np.array([
            outcome['wells'],
            outcome['gaps'],
            outcome['row']
        ], dtype=np.uint8)
        return np.dot(score_vector, Solver.WEIGHTS_VECTOR)

    def decide_outcome(self, playfield, tetromino, ban_hold=False):
        """ Score and filter all potential outcomes to determine the best action to take. Return outcome that has lowest cost """
        outcomes = self.get_all_outcomes(playfield, tetromino, ban_hold)
        for index, outcome in enumerate(outcomes):
            outcomes[index]['cost'] = self.get_outcome_cost(outcome)
        # Filter out any outcome that doesn't have the lowest cost
        lowest_cost = min([outcome['cost'] for outcome in outcomes])
        outcomes = list(filter(lambda outcome: outcome['cost'] == lowest_cost, outcomes))
        # With multiple lowest cost outcomes, selection is only affected by number of keystrokes outcome requires.
        # The lowest outcome in the list is more likely to not require swap and not require any rotations
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
        playfield.execute_outcome(chosen_outcome, tetromino)
        print('score = {}, cost = {}'.format(score, chosen_outcome['cost']))
        print(playfield)
        score += 1
    print('GAME OVER, score = {}'.format(score))
    print(chosen_outcome)

