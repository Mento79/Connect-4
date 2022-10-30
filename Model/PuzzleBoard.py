from typing import List


class PuzzleBoard:

    def __init__(self, state: List[int], parent=None, prev_step="", depth: int = 0,
                 length: int = 3, width: int = 3):
        self.__state = state
        self.__parent = parent
        self.__prev_step = prev_step
        self.__depth = depth
        self.__length = length
        self.__width = width
        # print(self.__prev_step)

    def get_parent(self):
        return self.__parent

    def get_prev_step(self):
        # print(self.__prev_step)
        return self.__prev_step

    def get_depth(self):
        return self.__depth

    def get_state(self) -> List[int]:
        return self.__state

    def __swap(self, i, j):
        new_state = self.__state.copy()
        new_state[i], new_state[j] = new_state[j], new_state[i]
        return new_state

    def __up(self):
        if self.__zero_index > self.__length:
            return PuzzleBoard(self.__swap(self.__zero_index, self.__zero_index - self.__length),
                               self, 'Up', self.__depth + 1, self.__length, self.__width)
        return None

    def __down(self):
        if self.__zero_index < self.__length * (self.__width - 1):
            return PuzzleBoard(self.__swap(self.__zero_index, self.__zero_index + self.__length),
                               self, 'Down', self.__depth + 1, self.__length, self.__width)
        return None

    def __left(self):
        if self.__zero_index % self.__length != 0:
            return PuzzleBoard(self.__swap(self.__zero_index, self.__zero_index - 1),
                               self, 'Left', self.__depth + 1, self.__length, self.__width)
        return None

    def __right(self):
        if (self.__zero_index + 1) % self.__length != 0:
            return PuzzleBoard(self.__swap(self.__zero_index, self.__zero_index + 1),
                               self, 'Right', self.__depth + 1, self.__length, self.__width)
        return None

    def get_children(self):
        # self.__current_puzzle = puzzle_board
        # self.__puzzle_state = [x for x in puzzle_board.get_state()]
        self.__zero_index = self.__state.index(0)
        # self.__puzzle_depth = puzzle_board.get_depth()
        children = [self.__up(), self.__down(), self.__left(), self.__right()]
        return list(filter(None, children))


