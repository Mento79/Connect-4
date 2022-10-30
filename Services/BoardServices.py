import copy
import math
import sys
sys.path.append("..")

from Model.PuzzleBoard import PuzzleBoard
from typing import List


class BoardServices(object):
    __current_puzzle: PuzzleBoard = None
    __zero_index: int = 0
    __puzzle_state = []
    __puzzle_depth: int = 0

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BoardServices, cls).__new__(cls)
        return cls.instance

    def set_board_dim(self, length: int, width: int):
        self.__length = length
        self.__width = width
        self.__goal_state = [i for i in range(self.__length * self.__width)]

    def is_goal(self, state: List[int]):
        if self.__length * self.__width == len(state):
            for i, x in enumerate(state):
                if x != self.__goal_state[i]:
                    return False
            return True
        return False

    def manhattan_h(self, state: List[int]):
        if self.__length * self.__width == len(state):
            total = 0
            for i, x in enumerate(state):
                total += abs(i % self.__length - x % self.__length) + abs(i // self.__width - x // self.__width)
            return total
        return -1

    def euclidean_h(self, state: List[int]):
        if self.__length * self.__width == len(state):
            total: float = 0.0
            for i, x in enumerate(state):
                total += math.sqrt((i % self.__length - x % self.__length) ** 2 + abs(i // self.__width - x // self.__width) ** 2)
            return total
        return -1

