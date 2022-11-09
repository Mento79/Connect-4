from bitarray import bitarray
import math
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


    def __init__(self, prevState:Model.State.State, where: int, what:bool):
        self.NoRows = prevState.NoRows
        self.NoColomns = prevState.NoColomns
        self.NoBitsOfNoC = prevState.NoBitsOfNoC

        self.A = prevState.A.copy()

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
        index = self.NoColomns*(self.NoBitsOfNoC + row) + colomn
        return self.A[index]

    def set(self, row, colomn, value):
        index = self.NoColomns*(self.NoBitsOfNoC + row) + colomn
        self.A[index] = value