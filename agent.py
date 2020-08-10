#!usr/bin/env python3
# Responsible for interacting with the screen and keyboard in order to control external game

import gi
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk
import pyautogui
import time
from tetromino import Tetromino

class Agent():

    PLAY_BUTTON_IMAGE_PATH = './data/play_button.png'
    PLAY_BUTTON_TO_SAMPLE_OFFSET = (260, -100)
    SAMPLE_COLOUR_DECODER = {
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
        self.next_sample = 'waiting'
        pass


    # TODO make  code more readable
    def get_sample(self):
        """ Get colour of sample pixel and return decode value """
        window = Gdk.get_default_root_window()
        pixbuf = Gdk.pixbuf_get_from_window(window, *self.pixel_sample_location, 1, 1)
        pixel = tuple(pixbuf.get_pixels())
        if pixel not in self.SAMPLE_COLOUR_DECODER.keys():
            self.next_sample = 'game_over'
        else:
            self.next_sample = self.SAMPLE_COLOUR_DECODER[pixel]

    def get_next_tetromino(self):
        """ Decode next_sample and return the shape of the next Tetromino """
        return Tetromino(self.next_sample)

    def start_game(self):
        """ Find and click start button twice (first time to focus on window), set up sample location. Return first tetromino """ # TODO finish docstring
        self.play_button_location = pyautogui.locateCenterOnScreen(
                                    self.PLAY_BUTTON_IMAGE_PATH)
        if self.play_button_location is None:
            raise Exception('Could not find play button')
        pyautogui.click(self.play_button_location, clicks=2, interval=0.1)
        pyautogui.move(self.PLAY_BUTTON_TO_SAMPLE_OFFSET)
        self.pixel_sample_location = pyautogui.position()
        # wait for game to start
        while self.next_sample not in Tetromino.SHAPES:
            self.get_sample()
        time.sleep(3)
        # Return first tetromino
        print('decoded: {}'.format(self.next_sample))
        return self.get_next_tetromino()

    # TODO figure out position changes due to rotation to decrease number of keystrokes
    def execute_position(self, outcome, interval=0.1):
        """ Generate a list of actions required to execute outcome. Map these to keystrokes and perform them """
        # Start off by performing rotations and moving to the left wall. This is done because the tetris rotation scheme is complex and it is easier to got to the left wall and start from a known position than to model the rotation scheme for no real benefit
        if outcome['hold_swap']:
            if outcome['tetromino'] is None:
                # if None is swapped out, take sample
                self.get_sample()
            pyautogui.press(self.KEY_MAPPING['hold_swap'], interval=0.25)

        if outcome['tetromino'] is None:
            # If there is no tetromino to place, end actions here
            return

        actions = []
        # Do rotations
        if outcome['rotations'] == 3:
            actions += ['rotate_ccw']
        else:
            actions += ['rotate_cw'] * outcome['rotations']

        # determine number of left/right moves
        displacement = outcome['tetromino'].spawn_column() - outcome['col'] + outcome['tetromino'].rotation_column_offset()
        if displacement > 0:
            direction = ['left']
        else:
            direction = ['right']
        actions += direction * abs(displacement)

        print([self.KEY_MAPPING[x] for x in actions])
        pyautogui.typewrite([self.KEY_MAPPING[x] for x in actions], interval=interval)

    def execute_outcome_and_sample(self, outcome, interval=0.1):
        """ Position tetromino, capture sample of next tetromino and drop tetromino """
        self.execute_position(outcome, interval)
        if outcome['tetromino'] is not None:
            self.get_sample()
            pyautogui.press(self.KEY_MAPPING['drop'])
        else:
            time.sleep(1)
        print('placed: {}'.format(outcome['tetromino']))
        return self.next_sample
