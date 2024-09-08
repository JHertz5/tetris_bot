#!usr/bin/env python3
# Manage the queue of tetrominoes

import tetromino


class TetrominoQueue:

    LENGTH = 3

    def __init__(self):
        self.queue = []
        for _ in range(self.LENGTH):
            self.queue.append(tetromino.get_random_tetromino())

    def __str__(self):
        return " ".join([str(tetronimo) for tetronimo in self.queue])

    def get_next(self):
        """
        Pop the next tetromino out of the queue and fill that back of the queue with a new tetromino. Return the popped
        Tetromino
        """
        # Append a new tetromino to the back of the queue.
        self.queue.append(tetromino.get_random_tetromino())
        # Pop and return the tetromino at the front of the queue.
        return self.queue.pop(0)


if __name__ == "__main__":
    tetromino_queue = TetrominoQueue()
    print(tetromino_queue)
    tetromino = tetromino_queue.get_next()
    print(str(tetromino) + ", " + str(tetromino_queue))
