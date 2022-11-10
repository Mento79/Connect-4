from bitarray import bitarray
import math
import copy
import Model.State


class State:
    """
    A = array of the number of element at each colomn =>  NoColomns*(floor(lgNoRows)+1 )
        + 2d array of bits => NoColomns* NoRows
    """

    def __init__(self, NoColomns, NoRows):
        self.NoRows = NoRows
        self.NoColomns = NoColomns
        self.NoBitsOfNoC = math.floor(math.log2(NoRows)) + 1

        self.A: bitarray = (NoColomns*(self.NoBitsOfNoC+NoRows)) * bitarray('0')
        self.parent : Model.State.State = None
        self.children : list[Model.State.State] = []
        self.hvalue = None


    def __init__(self, prevState:Model.State.State, where: int, what:bool):
        self.parent = prevState
        self.children : list[Model.State.State] = []
        self.parent.children.append(self)
        self.hvalue = None


        self.NoRows = prevState.NoRows
        self.NoColomns = prevState.NoColomns
        self.NoBitsOfNoC = prevState.NoBitsOfNoC

        self.A = copy.deepcopy(prevState.A)

        start = self.NoBitsOfNoC*where
        inwhere = self.bitsToInt(self.A[start:start+self.NoBitsOfNoC])
        self.set(inwhere, where, what)

        draft = self.intToBits(inwhere+1)
        for i in range(start, start+self.NoBitsOfNoC):
            self.A[i] = draft[i-start]




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
