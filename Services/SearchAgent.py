import datetime
import sys

sys.path.append("..")

from Model.PuzzleBoard import PuzzleBoard
from Model.Answer import Answer
from Services.BoardServices import BoardServices
from Services.SearchStrategy import SearchStrategy

from typing import List


class SearchAgent(object):

    __search_strategy: SearchStrategy
    __answer: Answer

    def set_initial_puzzle(self, initial_state, length=3, width=3):
        self.__initial_puzzle = PuzzleBoard(initial_state, None, "", 0, length, width)

    def set_board_services(self, length, width):
        self.__board_services = BoardServices()
        self.__board_services.set_board_dim(length, width)

    def set_search_strategy(self, search_strategy: SearchStrategy):
        self.__search_strategy = search_strategy

    def __add_path_ans(self):
        if self.__answer.found:
            cur_board = self.__answer.puzzle_sol
            steps = [cur_board.get_prev_step()]
            states = [cur_board.get_state()]
            while cur_board.get_parent() is not None:
                steps.append(cur_board.get_parent().get_prev_step())
                states.append(cur_board.get_parent().get_state())
                cur_board = cur_board.get_parent()
            steps.reverse()
            states.reverse()
            self.__answer.add_path_step(steps[1:])
            self.__answer.add_path_states(states[1:])


    def solvePuzzle(self):
        prev = datetime.datetime.now().timestamp()
        self.__answer = self.__search_strategy.search(self.__initial_puzzle, self.__board_services)
        time = (datetime.datetime.now().timestamp() - prev)*1000.0
        self.__answer.setTime(time)

        self.__add_path_ans()
        return self.__answer


