import sys

sys.path.append("..")
from Model.PuzzleBoard import PuzzleBoard

class Answer(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Answer, cls).__new__(cls)
        return cls.instance

    def add_answer_attr(self, puzzle_sol: PuzzleBoard, found: bool, max_depth: int, no_nodes_exp: int, fringe_size: int, max_fsize:int):
        self.puzzle_sol = puzzle_sol
        self.max_depth = max_depth
        self.no_nodes_exp = no_nodes_exp - 1
        self.fringe_size = fringe_size
        self.max_fsize = max_fsize
        self.found = found
        if(found):
            self.sol_cost = puzzle_sol.get_depth()

    def setTime(self,time):
        self.time = time

    def add_path_step(self, steps):
        self.steps = steps

    def add_path_states(self, states):
        self.states = states
