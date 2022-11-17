import math
import copy
import time
import State

# def get_next_open_row(board :State, col):
#     for r in range(5, -1, -1):
#         if board[r][col] == 0:
#             return r


# def is_valid_location(board, col):
#     return board[0][col] == 0

#
# def get_valid_locations(Board:State):
#     valid_locations = []
#
#     for col in range(Board.NoColomns):
#         if Board.check_column(col):
#             valid_locations.append(col)
#     return valid_locations

def get_valid_locations(Board:State):
    valid_locations = []
    for col in range(Board.NoColomns):
        if Board.check_column(col):
            valid_locations.append(col)
    return valid_locations


# def drop_piece(board, row, col, piece):
#     board[row][col] = piece


statesDict = {}

def start_minmax(Board,depth,alpha, beta ,maximing_player):
    state = State.State(Board)
    statesDict.clear()

    time_before= round(time.time() * 1000)
    value, Column = mini_max(state,depth,alpha, beta ,maximing_player)
    time_after= round(time.time() * 1000)
    print("Time Taken : ",time_after-time_before)
    return value, Column, state

def mini_max(Board:State, depth,alpha, beta, maximizing_player):
    valid_location = get_valid_locations(Board)
    if depth == 0 or len(valid_location) == 0:
        return Board.heuristic(), 0
    h = statesDict.get(Board.getLong(), None)
    if h is not None:
        Board.hvalue = h[0]
        return h

    if maximizing_player:
        value = -math.inf
        Column = valid_location[0]
        for col2 in valid_location:
            # row = Board.get_next_row(col2)
            b_copy = State.State(None,Board,col2,1)
            # drop_piece(b_copy, row, col2, 2)
            new_score, temp = mini_max(b_copy, depth - 1,alpha, beta, False)
            if (new_score > value):
                value = new_score
                Column = col2
            if alpha is not None:
                alpha = max(alpha, value)
                if (beta <= alpha):
                    break
        Board.hvalue = value
        statesDict[Board.getLong()] = (value, Column)
        return value, Column
    else:
        value = math.inf
        Column = valid_location[0]
        for col2 in valid_location:
            # row = Board.get_next_row(col2)
            b_copy = State.State(None,Board, col2, 0)
            # drop_piece(b_copy, row, col2, 1)
            new_score, temp = mini_max(b_copy, depth - 1, alpha, beta, True)
            if (new_score < value):
                value = new_score
                Column = col2
            if beta is not None:
                beta = min(beta, value)
                if (beta <= alpha):
                    break
        Board.hvalue = value
        statesDict[Board.getLong()] = (value, Column)
        return value, Column
