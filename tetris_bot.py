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
turn_num = 0
game_over = False
ban_hold = False

while not game_over:
    t = time.time()

    # decide and execute
    if current_tetromino is not None:
        chosen_outcome = solver.decide_outcome(playfield, current_tetromino, ban_hold)
        agent.execute_outcome(chosen_outcome)
        # pyautogui.screenshot('./screen_captures/{}.png'.format(turn_num))
        playfield.execute_outcome(chosen_outcome, current_tetromino)
        ban_hold = chosen_outcome['tetromino'] is None # Ban hold on next turn if first hold was performed
        print('placed: {}'.format(chosen_outcome['tetromino']))
        print(chosen_outcome['cost'])
        print(playfield)
    time.sleep(0.4)

    # decode old sample and get new sample
    print('decoded: {}'.format(next_tetromino))
    current_tetromino = next_tetromino
    try:
        next_tetromino = Tetromino(agent.get_sample()) # get next sample after current tetromino has been decoded
    except:
        game_over = True        
    turn_num += 1
    print('{}s'.format (time.time() - t))

print('GAME OVER')
