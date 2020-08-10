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
sample = 'waiting'
solver = Solver()
playfield = Playfield()

current_tetromino = agent.start_game()

turn_num = 0
game_over = False

while not game_over:
    t = time.time()

    # decide and execute
    chosen_outcome = solver.decide_outcome(playfield, current_tetromino)
    next_shape = agent.execute_outcome_and_sample(chosen_outcome,interval=0.04)
    # pyautogui.screenshot('./screen_captures/{}.png'.format(turn_num))
    playfield.execute_outcome(chosen_outcome, current_tetromino)
    print(playfield)
    time.sleep(0.4)

    # decode old sample and get new sample
    try:
        current_tetromino = Tetromino(next_shape)
    except:
        game_over = True        
    turn_num += 1
    print('{}s'.format (time.time() - t))

print('GAME OVER')
