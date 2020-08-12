#!usr/bin/env python3
# Attempts to play tetris using simple CV and keyboard inputs
# Intended for tetris link: https://tetris.com/play-tetris

from tetromino import Tetromino
from playfield import Playfield
from solver import Solver
from agent import Agent

agent = Agent()
sample = 'waiting'
solver = Solver()
playfield = Playfield()

current_tetromino = agent.start_game()

block_num = 0
game_over = False

while not game_over:
    block_num += 1

    # decide outcome
    chosen_outcome = solver.decide_outcome(playfield, current_tetromino)

    # execute outcome
    next_shape = agent.execute_outcome_and_sample(chosen_outcome,
                                                  interval=0.04,
                                                  sleep=0.4)
    playfield.execute_outcome(chosen_outcome, current_tetromino)

    # decode old sample and get new sample
    try:
        current_tetromino = Tetromino(next_shape)
    except:
        game_over = True

print('GAME OVER, {} blocks placed'.format(block_num))
