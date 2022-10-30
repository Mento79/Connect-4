import heapq
from queue import PriorityQueue
from collections import defaultdict
from abc import ABC, abstractmethod
import sys
from typing import List, Tuple
from queue import Queue

sys.path.append("..")

from Model.PuzzleBoard import PuzzleBoard
from Services.BoardServices import BoardServices


class Fringe(ABC):
    @abstractmethod
    def get_node(self) -> PuzzleBoard:
        pass

    @abstractmethod
    def add_node(self, val: PuzzleBoard, services: BoardServices) -> None:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def get_max_size(self) -> int:
        pass


class DFSFringe(Fringe):

    def __init__(self):
        self.__stack: List[PuzzleBoard] = []
        self.__max_size = 0

    def get_node(self) -> PuzzleBoard:
        return self.__stack.pop()

    def add_node(self, val: PuzzleBoard, services: BoardServices = None) -> None:
        self.__stack.append(val)
        self.__max_size = max(self.get_size(), self.__max_size)

    def get_size(self) -> int:
        return len(self.__stack)

    def is_empty(self) -> bool:
        return self.get_size() == 0

    def get_max_size(self):
        return self.__max_size


class BFSFringe(Fringe):

    def __init__(self):
        self.__q: Queue[PuzzleBoard] = Queue()
        self.__max_size = 0

    def get_node(self) -> PuzzleBoard:
        return self.__q.get()

    def add_node(self, val: PuzzleBoard, services: BoardServices = None) -> None:
        self.__q.put(val)
        self.__max_size = max(self.get_size(), self.__max_size)

    def get_size(self) -> int:
        return self.__q.qsize()

    def is_empty(self) -> bool:
        return self.__q.empty()

    def get_max_size(self):
        return self.__max_size


class ManhattanFringe(Fringe):

    def __init__(self):
        self.__pq: PriorityQueue[Tuple[int, int, PuzzleBoard]] = PriorityQueue()
        # self.__sdic = defaultdict(lambda: 999999)
        self.__max_size = 0
        self.__buff = 0

    def get_node(self) -> PuzzleBoard:
        # mmm = 999999
        # for x in self.__pq:
        #     print("\tff :", x[0])
        #     mmm = min(mmm, x[0])

        _, _, ans = self.__pq.get()
        # if cost != self.__sdic[tuple(ans.get_state())]:
        #     ans = self.get_node()
        # print("\t\t\t\t\tselected :", pp)
        # print("\t\t\t\t\tMin :", mmm)
        # print("\n\n\n\n\n******************************")
        return ans

    def add_node(self, val: PuzzleBoard, services: BoardServices = None) -> None:
        cost = services.manhattan_h(val.get_state()) + val.get_depth()
        # print(self.__sdic[tuple(val.get_state())])
        # if cost >= self.__sdic[tuple(val.get_state())]:
        #     print("pass")
        #     return
        self.__buff += 1
        # self.__sdic[tuple(val.get_state())] = cost
        self.__pq.put((services.manhattan_h(val.get_state()) + val.get_depth(), self.__buff, val))
        # heapq.heappush(self.__pq, (services.manhattan_h(val.get_state()) + val.get_depth(), self.__buff, val))
        # for xx in self.__pq:
        #     print(xx[0])
        # print("\n\n\n\n\n******************************")
        # print(f"Man: {services.manhattan_h(val.get_state()) + 1}")
        self.__max_size = max(self.get_size(), self.__max_size)

    def get_size(self) -> int:
        return self.__pq.qsize()

    def is_empty(self) -> bool:
        return self.get_size() == 0

    def get_max_size(self):
        return self.__max_size


class EuclideanFringe(Fringe):

    def __init__(self):
        self.__pq: PriorityQueue[Tuple[float, int, PuzzleBoard]] = PriorityQueue()
        self.__max_size = 0
        self.__buff = 0

    def get_node(self) -> PuzzleBoard:
        _, _, ans = self.__pq.get()
        return ans

    def add_node(self, val: PuzzleBoard, services: BoardServices = None) -> None:
        self.__buff += 1
        self.__pq.put((services.euclidean_h(val.get_state()) + float(val.get_depth()), self.__buff, val))
        # print(f"euc: {services.euclidean_h(val.get_state()) + 1}")
        self.__max_size = max(self.get_size(), self.__max_size)

    def get_size(self) -> int:
        return self.__pq.qsize()

    def is_empty(self) -> bool:
        return self.get_size() == 0

    def get_max_size(self):
        return self.__max_size
