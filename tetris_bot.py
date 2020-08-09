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
decode = 'waiting'
solver = Solver()
playfield = Playfield()

while decode == 'waiting':
    decode = agent.get_sample()
time.sleep(3)

# Decode and hold first piece so that there's always a held piece to compare against
tetromino = Tetromino(decode)
pyautogui.screenshot('./screen_captures/0.png')
decode = agent.get_sample() # get next decode in advance
playfield.hold_tetromino(tetromino)
pyautogui.press(agent.KEY_MAPPING['hold_swap'])
pyautogui.screenshot('./screen_captures/1.png')

ban_hold = True
block = 1
while decode not in ['paused', 'game_over']:
    block += 1
    t = time.time()
    print('decoded: {}'.format(decode))
    tetromino = Tetromino(decode)
    decode = agent.get_sample() # get next sample after current tetromino has been decoded
    chosen_outcome = solver.decide_outcome(playfield, tetromino, ban_hold)
    playfield.execute_outcome(chosen_outcome, tetromino)
    agent.execute_outcome(chosen_outcome)
    print('placed: {}'.format(chosen_outcome['tetromino'].shape))
    print(playfield)
    time.sleep(0.2)
    pyautogui.screenshot('./screen_captures/{}.png'.format(block))
    ban_hold = False

print('GAME OVER')
