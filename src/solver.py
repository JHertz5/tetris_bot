#!usr/bin/env python3
# Given playfield and tetromino, decide best action and determine moves needed
# to take action.

import numpy as np

from .playfield import Playfield


class Solver:

    # These weights define how costly each move is. A higher cost is worse. See get_outcome_cost for details.
    # These weights are not optimal, but they have been manually tuned to be
    # "good enough"
    WEIGHTS = {"wells": 40, "gaps": 20, "gap depth": 5, "row": -20}

    WEIGHTS_VECTOR = np.array(list(WEIGHTS.values()), dtype=np.int8)

    def __init__(self):
        self.ban_hold = False
        pass

    def get_all_outcomes(self, playfield, current_tetromino, held_tetromino):
        """
        Get all potential outcomes so that they can be scored and filtered.
        """
        assert isinstance(playfield, Playfield)

        if current_tetromino is None:
            return [
                {
                    "playfield": playfield,
                    "tetromino": None,
                    "rotations": 0,
                    "row": playfield.MAIN_BOX_HEIGHT,
                    "col": 0,
                    "hold_swap": False,
                    "gaps": 0,
                    "gap_depth": 0,
                    "wells": 0,
                }
            ]

        outcomes = []
        hold_swap_options = [False]
        if not self.ban_hold:
            hold_swap_options += [True]

        for hold_swap in hold_swap_options:
            if hold_swap and held_tetromino is None:
                outcomes.append(
                    {
                        "playfield": playfield,
                        "tetromino": None,
                        "rotations": 0,
                        "row": outcome_playfield.MAIN_BOX_HEIGHT,
                        "col": 0,
                        "hold_swap": hold_swap,
                        "gaps": 0,
                        "gap_depth": 0,
                        "wells": 0,
                    }
                )
                continue
            else:
                if hold_swap:
                    active_tetromino = held_tetromino
                else:
                    active_tetromino = current_tetromino
            # Get all outcomes for each hold/rotate permutation of tetromino
            for tetr in [active_tetromino.copy().rotate(n) for n in range(4)]:
                for col in range(playfield.MAIN_BOX_WIDTH - tetr.width() + 1):
                    outcome_playfield = playfield.copy()
                    row = outcome_playfield.drop_tetromino(tetr, col)
                    outcomes.append(
                        {
                            "playfield": outcome_playfield,
                            "tetromino": tetr,
                            "rotations": tetr.rotations,
                            "row": row,
                            "col": col,
                            "hold_swap": hold_swap,
                            "gaps": outcome_playfield.get_gap_count(),
                            "gap_depth": outcome_playfield.get_gap_depth(),
                            "wells": outcome_playfield.get_well_count(),
                        }
                    )
        return outcomes

    def get_outcome_cost(self, outcome):
        """Get scoring vector for outcome by performing dot product with
        weights vector. Each outcome is scored on the following paramters:
            How many wells it contains (fewer is better)
            How many gaps it contains (fewer is better)
            How many blocks are above gaps (fewer is better)
            Drop row (lower is better)
        """
        score_vector = np.array(
            [outcome["wells"], outcome["gaps"], outcome["gap_depth"], outcome["row"]],
            dtype=np.uint8,
        )
        return np.dot(score_vector, Solver.WEIGHTS_VECTOR)

    def decide_outcome(self, game):
        """
        Score and filter all potential outcomes to determine the best action
        to take. Return outcome that has lowest cost.
        """
        outcomes = self.get_all_outcomes(
            game.playfield, game.current_tetromino, game.holder.held_tetromino
        )
        for index, outcome in enumerate(outcomes):
            outcomes[index]["cost"] = self.get_outcome_cost(outcome)
        # Filter out any outcome that doesn't have the lowest cost
        lowest_cost = min([outcome["cost"] for outcome in outcomes])
        outcomes = list(
            filter(lambda outcome: outcome["cost"] == lowest_cost, outcomes)
        )
        # if None was swapped out, ban hold for next turn
        self.ban_hold = outcomes[0]["tetromino"] is None
        # With multiple lowest cost outcomes, selection is only affected by
        # number of keystrokes outcome requires. The lowest outcome in the
        # list is more likely to not require swap and not require any
        # rotations
        return outcomes[0]
