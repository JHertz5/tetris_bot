#!usr/bin/env python3
# Attempts to play tetris using simple CV and keyboard inputs
# Intended for tetris link: https://tetris.com/play-tetris

import pyautogui
import time

from tetromino import Tetromino
from playfield import Playfield
from solver import Solver
from agent import Agent

agent = Agent()
agent.start_game()
sample = 'waiting'
solver = Solver()
playfield = Playfield()

while sample not in Tetromino.SHAPES:
    sample = agent.get_sample()

time.sleep(3)
current_tetromino = None
next_tetromino    = Tetromino(sample)
# turn_num = 0
game_over = False
ban_hold = False

while not game_over:
    # t = time.time()

    # pyautogui.screenshot('./screen_captures/{}.png'.format(turn_num))

    # decide and execute
    if current_tetromino is not None:
        chosen_outcome = solver.decide_outcome(playfield, current_tetromino, ban_hold)
        print('placed: {}'.format(chosen_outcome['tetromino']))
        playfield.execute_outcome(chosen_outcome, current_tetromino)
        agent.execute_outcome(chosen_outcome)
        ban_hold = chosen_outcome['tetromino'] is None # Ban hold on next turn if first hold was performed
        print(playfield)
    time.sleep(0.3)

    # decode old sample and get new sample
    print('decoded: {}'.format(next_tetromino))
    current_tetromino = next_tetromino
    next_tetromino = Tetromino(agent.get_sample()) # get next sample after current tetromino has been decoded

    # turn_num += 1
    game_over == agent.get_sample() not in Tetromino.SHAPES # TODO improve end of game detection

print('GAME OVER')
