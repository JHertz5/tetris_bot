#!usr/bin/env python3
# Responsible for interacting with the screen and keyboard in order to control external game

import pyautogui
import time

class Agent():

    PLAY_BUTTON_IMAGE_PATH = './data/play_button.png'
    PLAY_BUTTON_TO_SAMPLE_OFFSET = (260, -100)
    COLOUR_DECODER = {
        ( 36,  36,  36) : 'waiting',
        ( 30,  32,  33) : 'paused',
        (  0, 114, 127) : 'I',
        (127, 117,   0) : 'O',
        (140,  63, 155) : 'T',
        ( 63, 155,  91) : 'S',
        (155,  63,  63) : 'Z',
        ( 63, 115, 155) : 'J',
        (155, 126,  63) : 'L'
    }
    KEY_MAPPING = {
        'left' : 'left',
        'right' : 'right',
        'rotate_cw' : 'up',
        'rotate_ccw' : 'z',
        'drop' : ' ',
        'hold_swap' : 'c'
    }

    def __init__(self):
        pass

    def start_game(self):
        """ Find and click start button twice (first time to focus on window), set up sample location """
        self.play_button_location = pyautogui.locateCenterOnScreen(
                                    self.PLAY_BUTTON_IMAGE_PATH)
        if self.play_button_location is None:
            raise Exception('Could not find play button')
        pyautogui.click(self.play_button_location, clicks=2, interval=0.1)
        pyautogui.move(self.PLAY_BUTTON_TO_SAMPLE_OFFSET)
        self.pixel_sample_location = pyautogui.position()

    def get_sample(self):
        """ Get colour of sample pixel and return decode value """
        pixel = pyautogui.pixel(*self.pixel_sample_location)
        if pixel not in self.COLOUR_DECODER.keys():
            return('game_over')
        return self.COLOUR_DECODER[pixel]

    def execute_outcome(self, outcome):
        """ Generate a list of actions required to execute outcome. Map these to keystrokes and perform them """
        # Start off by performing rotations and moving to the left wall. This is done because the tetris rotation scheme is complex and it is easier to got to the left wall and start from a known position than to model the rotation scheme for no real benefit
        actions = ['hold_swap'] * outcome['hold_swap']
        actions += ['rotate_cw'] * outcome['rotations'] # TODO reduce number of keypresses by rotating anti-clockwise if rotations = 3
        actions += ['left'] * 5 # TODO reduce number of keypresses here by moving to the right instead of left if end position is closer
        actions += ['right'] * outcome['col']
        actions += ['drop']
        pyautogui.typewrite([self.KEY_MAPPING[x] for x in actions], interval=0.04)

if __name__ == "__main__":
    agent = Agent()
    agent.start_game()
    decode = ''
    while decode not in ['paused', 'game_over']:
        t = time.time()
        decode = agent.get_sample()
        print('{}, {}s'.format(decode, time.time() - t))
