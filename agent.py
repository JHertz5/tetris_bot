#!usr/bin/env python3
# Responsible for interacting with the screen and keyboard in order to control external game

import gi
gi.require_version("Gdk", "3.0")    
from gi.repository import Gdk
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
        'hold_swap' : 'c',
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

    # TODO make  code more readable
    def get_sample(self):
        """ Get colour of sample pixel and return decode value """
        w = Gdk.get_default_root_window()
        pb = Gdk.pixbuf_get_from_window(w, *self.pixel_sample_location, 1, 1)
        pixel = tuple(pb.get_pixels())
        if pixel not in self.COLOUR_DECODER.keys():
            return('game_over')
        return self.COLOUR_DECODER[pixel]

    # TODO figure out position changes due to rotation to decrease number of keystrokes
    def execute_outcome(self, outcome):
        """ Generate a list of actions required to execute outcome. Map these to keystrokes and perform them """
        # Start off by performing rotations and moving to the left wall. This is done because the tetris rotation scheme is complex and it is easier to got to the left wall and start from a known position than to model the rotation scheme for no real benefit
        if outcome['hold_swap']:
            pyautogui.press(self.KEY_MAPPING['hold_swap'], interval=0.25)
            # pyautogui.typewrite(self.KEY_MAPPING['hold_swap'], interval=0.25)

        if outcome['tetromino'] is not None:
            # determine number of left/right moves
            if outcome['rotations'] == 0:
                # no need to move to wall as no rotations means no ambiguity on position
                displacement = outcome['tetromino'].spawn_position()[1] - outcome['col']
                if displacement > 0:
                    direction =  'left'
                    # direction = ['left']
                else:
                    direction = 'right'
                    # direction = ['right']
                pyautogui.press(self.KEY_MAPPING[direction], presses=abs(displacement), interval=0.05)
                # actions += direction * abs(displacement)
            else:
                # Do rotations
                if outcome['rotations'] == 3:
                    pyautogui.press(self.KEY_MAPPING['rotate_ccw'], interval=0.05)
                    # actions += ['rotate_ccw']
                else:
                    pyautogui.press(self.KEY_MAPPING['rotate_cw'], presses=outcome['rotations'], interval=0.05)
                    # actions += ['rotate_cw'] * outcome['rotations']
                # Move left/right
                if outcome['col'] < 5:
                    pyautogui.press(self.KEY_MAPPING['left'], presses=5, interval=0.05)
                    pyautogui.press(self.KEY_MAPPING['right'], presses=outcome['col'], interval=0.05)
                    # actions += ['left'] * 5
                    # actions += ['right'] * outcome['col']
                else: 
                    pyautogui.press(self.KEY_MAPPING['right'], presses=5, interval=0.05)
                    pyautogui.press(self.KEY_MAPPING['left'], presses=(outcome['playfield'].WIDTH - outcome['tetromino'].width() - outcome['col']), interval=0.05)
                    # actions += ['right'] * 5
                    # actions += ['left'] * (outcome['playfield'].WIDTH - outcome['tetromino'].width() - outcome['col'])
            # actions += ['pause']
            pyautogui.press(self.KEY_MAPPING['drop'], interval=0.05)
        #     actions += ['drop']
        #     print([self.KEY_MAPPING[x] for x in actions])
        # pyautogui.typewrite([self.KEY_MAPPING[x] for x in actions], interval=0.075)

if __name__ == "__main__":
    agent = Agent()
    agent.start_game()
    decode = ''
    while decode not in ['paused', 'game_over']:
        t = time.time()
        decode = agent.get_sample()
        print('{}, {}s'.format(decode, time.time() - t))
