from bitarray import bitarray
import math
import copy


class State:
    """
    A = array of the number of element at each colomn =>  NoColomns*(floor(lgNoRows)+1 )
        + 2d array of bits => NoColomns* NoRows
    """

    def __init__(self, board: [[int]]):
        self.NoRows = len(board)
        self.NoColomns = len(board[0])
        self.NoBitsOfNoC = math.floor(math.log2(self.NoRows)) + 1

        self.A: bitarray = (self.NoColomns*(self.NoBitsOfNoC+self.NoRows)) * bitarray('0')
        self.parent : State = None
        self.children : list[State] = []
        self.hvalue = None

        for i in range(self.NoColomns):
            for j in range(self.NoRows):
                if board[j][i] == 0:
                    break
                else:
                    self.addToColomn(j, board[j][i])





    def __init__(self, prevState, where: int, what):
        self.parent = prevState
        self.children : list[State] = []
        self.parent.children.append(self)
        self.hvalue = None


        self.NoRows = prevState.NoRows
        self.NoColomns = prevState.NoColomns
        self.NoBitsOfNoC = prevState.NoBitsOfNoC

        self.A = copy.deepcopy(prevState.A)
        self.addToColomn(where,what)



    def addToColomn(self, where: int, what):
        start = self.NoBitsOfNoC*where
        inwhere = self.bitsToInt(self.A[start:start+self.NoBitsOfNoC])
        draft = self.intToBits(inwhere+1)
        for i in range(start, start+self.NoBitsOfNoC):
            self.A[i] = draft[i-start]

        self.set(inwhere, where, what)


    # def get_next_row(self, where: int):
    #     start = self.NoBitsOfNoC*where
    #     inwhere = self.bitsToInt(self.A[start:start+self.NoBitsOfNoC])
    #     return inwhere



    def bitsToInt(self, bitArray):
        res = int("".join(str(x) for x in bitArray), 2)
        return res

    def intToBits(self, number):
        res = self.NoBitsOfNoC*bitarray(0)
        for i in range(self.NoBitsOfNoC-1,-1,-1):
            res[i] = number%2
            number /= 2
        return res


    def get(self, row, colomn):
        if self.checkCell(row,colomn):
            index = self.NoColomns*(self.NoBitsOfNoC + row) + colomn
            return self.A[index]
        else:
            return None

    def set(self, row, colomn, value):
        if self.checkCell(row,colomn):
            index = self.NoColomns * (self.NoBitsOfNoC + row) + colomn
            self.A[index] = value
            return True
        else:
            return False



    def checkCell(self,row, colomn):
        if row>=self.NoRows or colomn>=self.NoColomns:
            return False

        start = self.NoBitsOfNoC * colomn
        inwhere = self.bitsToInt(self.A[start:start + self.NoBitsOfNoC])
        if row >= inwhere:
            return False
        else:
            return True

    def check_column(self, colomn):
        if  colomn >= self.NoColomns:
            return False

        start = self.NoBitsOfNoC * colomn
        inwhere = self.bitsToInt(self.A[start:start + self.NoBitsOfNoC])
        if self.NoRows == inwhere:
            return False
        else:
            return True
