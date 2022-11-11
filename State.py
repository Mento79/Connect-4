from bitarray import bitarray
import math
import copy


class State:
    """
    A = array of the number of element at each colomn =>  NoColomns*(floor(lgNoRows)+1 )
        + 2d array of bits => NoColomns* NoRows
    """

    def __init__(self, board: [[int]] = None, prevState=None, where: int = None, what=None):
        if prevState is None:
            self.build(board)
        else:
            self.parent = prevState
            self.children: list[State] = []
            self.parent.children.append(self)
            self.hvalue = None

            self.NoRows = prevState.NoRows
            self.NoColomns = prevState.NoColomns
            self.NoBitsOfNoC = prevState.NoBitsOfNoC

            self.A = copy.deepcopy(prevState.A)
            self.addToColomn(where, what)


    def build(self, board: [[int]]):
        self.NoRows = len(board)
        self.NoColomns = len(board[0])
        self.NoBitsOfNoC = math.floor(math.log2(self.NoRows)) + 1

        self.A: bitarray = (self.NoColomns * (self.NoBitsOfNoC + self.NoRows)) * bitarray('0')
        self.parent: State = None
        self.children: list[State] = []
        self.hvalue = None

        for i in range(self.NoColomns):
            for j in range(self.NoRows-1, -1 , -1):
                if board[j][i] == 0:
                    break
                else:
                    self.addToColomn(i, board[j][i]-1)

    def addToColomn(self, where: int, what):
        start = self.NoBitsOfNoC * where
        inwhere = self.bitsToInt(self.A[start:start + self.NoBitsOfNoC])
        draft = self.intToBits(inwhere + 1)
        for i in range(start, start + self.NoBitsOfNoC):
            self.A[i] = draft[i - start]

        self.set(inwhere, where, what)

    # def get_next_row(self, where: int):
    #     start = self.NoBitsOfNoC*where
    #     inwhere = self.bitsToInt(self.A[start:start+self.NoBitsOfNoC])
    #     return inwhere

    def bitsToInt(self, bitArray):
        res = int("".join(str(x) for x in bitArray), 2)
        #(res, bitArray)
        return res

    def intToBits(self, number):
        n2 = number
        res = self.NoBitsOfNoC * bitarray('0')
        for i in range(self.NoBitsOfNoC - 1, -1, -1):
            res[i] = int(number) % 2
            number /= 2
        return res

    def get(self, row, colomn):
        if self.checkCell(row, colomn):
            index = self.NoColomns * (self.NoBitsOfNoC + row) + colomn
            return self.A[index]
        else:
            return None

    def set(self, row, colomn, value):
        index = self.NoColomns * (self.NoBitsOfNoC + row) + colomn
        self.A[index] = value


    def checkCell(self, row, colomn):
        if row >= self.NoRows or colomn >= self.NoColomns:
            return False

        start = self.NoBitsOfNoC * colomn
        inwhere = self.bitsToInt(self.A[start:start + self.NoBitsOfNoC])
        if row >= inwhere:
            return False
        else:
            return True

    def check_column(self, colomn):
        if colomn >= self.NoColomns:
            return False

        start = self.NoBitsOfNoC * colomn
        inwhere = self.bitsToInt(self.A[start:start+self.NoBitsOfNoC])
        if self.NoRows == inwhere:
            return False
        else:
            return True

    def heuristic(self):
        to = []
        for i in range(0, self.NoColomns):
            start = i * self.NoBitsOfNoC
            to.append(self.bitsToInt(self.A[start: start+self.NoBitsOfNoC]))

        enmy = [8,4,1]
        ai = [8,4,1]


        h = 0
        #down
        for j in range(self.NoColomns):
            for i in range(self.NoRows-3):
                # complete
                if(i<to[j]-3 and self.get(i,j)==0 and self.get(i+1,j)==0 and self.get(i+2,j)==0  and self.get(i+3,j)==0 ):
                    h-=enmy[0]
                if(i<to[j]-3 and self.get(i, j) == 1 and self.get(i + 1, j) == 1 and self.get(i + 2, j) == 1 and self.get(i + 3,j) == 1):
                    h += ai[0]

                # if 3
                if(i==to[j]-3 and self.get(i,j)==0 and self.get(i+1,j)==0 and self.get(i+2,j)==0  and self.get(i+3,j)==0 ):
                    h-=enmy[1]
                if(i==to[j]-3 and self.get(i, j) == 1 and self.get(i + 1, j) == 1 and self.get(i + 2, j) == 1 and self.get(i + 3,j) == 0):
                    h += ai[1]

                # if 2
                if(i==to[j]-2 and self.get(i,j)==0 and self.get(i+1,j)==0):
                    h-=enmy[2]
                if(i==to[j]-2 and self.get(i, j) == 1 and self.get(i + 1, j) == 1):
                    h += ai[2]

        #right and left
        for j in range(self.NoColomns-3):
            for i in range(self.NoRows):
                if (to[j]>i and self.get(i,j)==0 and to[j+1]>i and self.get(i,j+1)==0 and to[j+2]>i and self.get(i,j+2)==0 and to[j+3]>i and self.get(i,j+3)==0):
                    h-=enmy[0]
                if (to[j]>i and self.get(i,j)==1 and to[j+1]>i and self.get(i,j+1)==1 and to[j+2]>i and self.get(i,j+2)==1 and to[j+3]>i and self.get(i,j+3)==1):
                    h+=ai[0]

                #if 3
                if ((to[j]<=i or (to[j]>i and self.get(i,j)==0)) and (to[j+1]<=i or (to[j+1]>i and self.get(i,j+1)==0)) and (to[j+2]<=i or (to[j+2]>i and self.get(i,j+2)==0)) and (to[j+3]<=i or (to[j+3]>i and self.get(i,j+3)==0))):
                    sum1 = 0
                    for k in range(4):
                        if to[j+k]>i and self.get(i,j+k)==0:
                            sum1+=1
                    if sum1 ==3:
                        h-=enmy[1]
                    elif sum1 ==2:
                        h-=enmy[2]

                if ((to[j]<=i or to[j]>i and self.get(i,j)==1) and (to[j+1]<=i or to[j+1]>i and self.get(i,j+1)==1) and (to[j+2]<=i or to[j+2]>i and self.get(i,j+2)==1) and (to[j+3]<=i or to[j+3]>i and self.get(i,j+3)==1)):
                    sum1 = 0
                    for k in range(4):
                        if to[j+k]>i and self.get(i,j+k)==1:
                            sum1+=1
                    if sum1 ==3:
                        h+=ai[1]
                    elif sum1 ==2:
                        h+=ai[2]

        #digonally
        for j in range(self.NoColomns-3):
            for i in range( self.NoRows-3):
                if (to[j]>i and self.get(i,j)==0 and to[j+1]>i+1 and self.get(i+1,j+1)==0 and to[j+2]>i+2 and self.get(i+2,j+2)==0 and to[j+3]>i+3 and self.get(i+3,j+3)==0):
                    h-=enmy[0]
                if (to[j]>i and self.get(i,j)==1 and to[j+1]>i+1 and self.get(i+1,j+1)==1 and to[j+2]>i+2 and self.get(i+2,j+2)==1 and to[j+3]>i+3 and self.get(i+3,j+3)==1):
                    h+=ai[0]

                #if 3
                if ((to[j]<=i or to[j]>i and self.get(i,j)==0) and (to[j+1]<=i+1 or to[j+1]>i+1 and self.get(i+1,j+1)==0) and (to[j+2]<=i+2 or to[j+2]>i+2 and self.get(i+2,j+2)==0) and (to[j+3]<=i+3 or to[j+3]>i+3 and self.get(i+3,j+3)==0)):
                    sum1 = 0
                    for k in range(4):
                        if to[j+k]>i+k and self.get(i+k,j+k)==0:
                            sum1+=1
                    if sum1 ==3:
                        h-=enmy[1]
                    elif sum1 ==2:
                        h-=enmy[2]

                if ((to[j]<=i or to[j]>i and self.get(i,j)==1) and (to[j+1]<=i+1 or to[j+1]>i+1 and self.get(i+1,j+1)==1) and (to[j+2]<=i+2 or to[j+2]>i+2 and self.get(i+2,j+2)==1) and (to[j+3]<=i+3 or to[j+3]>i+3 and self.get(i+3,j+3)==1)):
                    sum1 = 0
                    for k in range(4):
                        if to[j+k]>i+k and self.get(i+k,j+k)==1:
                            sum1+=1
                    if sum1 ==3:
                        h+=ai[1]
                    elif sum1 ==2:
                        h+=ai[2]


        #reverse diagonal
        for j in range(self.NoColomns-3):
            for i in range(3, self.NoRows, 1):
                if (to[j]>i and self.get(i,j)==0 and to[j+1]>i-1 and self.get(i-1,j+1)==0 and to[j+2]>i-2 and self.get(i-2,j+2)==0 and to[j+3]>i-3 and self.get(i-3,j+3)==0):
                    h-=enmy[0]
                if (to[j]>i and self.get(i,j)==1 and to[j+1]>i-1 and self.get(i-1,j+1)==1 and to[j+2]>i-2 and self.get(i-2,j+2)==1 and to[j+3]>i-3 and self.get(i-3,j+3)==1):
                    h+=ai[0]

                #if 3
                if ((to[j]<=i or to[j]>i and self.get(i,j)==0) and (to[j+1]<=i-1 or to[j+1]>i-1 and self.get(i-1,j+1)==0) and (to[j+2]<=i-2 or to[j+2]>i-2 and self.get(i-2,j+2)==0) and (to[j+3]<=i-3 or to[j+3]>i-3 and self.get(i-3,j+3)==0)):
                    sum1 = 0
                    for k in range(4):
                        if to[j+k]>i-k and self.get(i-k,j+k)==0:
                            sum1+=1
                    if sum1 ==3:
                        h-=enmy[1]
                    elif sum1 ==2:
                        h-=enmy[2]

                if ((to[j]<=i or to[j]>i and self.get(i,j)==1) and (to[j+1]<=i-1 or to[j+1]>i-1 and self.get(i-1,j+1)==1) and (to[j+2]<=i-2 or to[j+2]>i-2 and self.get(i-2,j+2)==1) and (to[j+3]<=i-3 or to[j+3]>i-3 and self.get(i-3,j+3)==1)):
                    sum1 = 0
                    for k in range(4):
                        if to[j+k]>i-k and self.get(i-k,j+k)==1:
                            sum1+=1
                    if sum1 ==3:
                        h+=ai[1]
                    elif sum1 ==2:
                        h+=ai[2]



        self.hvalue = h
        print("hahahaha", h)
        return h

