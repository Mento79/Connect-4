import math
import copy
import random


def get_next_open_row(board, col):
    for r in range(5, -1, -1):
        if board[r][col] == 0:
            return r


def is_valid_location(board, col):
    return board[0][col] == 0


def get_valid_locations(Board):
    valid_locations = []
    for col in range(len(Board[0])):
        if is_valid_location(Board, col):
            valid_locations.append(col)
    return valid_locations


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def heuristic():
    return random.random()


def mini_max(Board, depth, alpha, beta,maximizing_player):
    valid_location = get_valid_locations(Board)
    if depth == 0 or len(valid_location) == 0:
        return heuristic(), 0
    if maximizing_player:
        value = -math.inf
        for col2 in valid_location:
            b_copy = copy.deepcopy(Board)
            drop_piece(b_copy, get_next_open_row(Board, col2), col2, 2)
            new_value, temp = mini_max(b_copy, depth - 1, alpha, beta, False)
            if (new_value > value):
                value = new_value
                Column = col2
            if(value>=beta):
                break
        return value, Column
    else:
        value = math.inf
        for col2 in valid_location:
            b_copy = copy.deepcopy(Board)
            drop_piece(b_copy, get_next_open_row(Board, col2), col2, 1)
            new_value, temp = mini_max(b_copy, depth - 1,alpha, beta, True)
            if (new_value < value):
                value = new_value
                Column = col2
            if(value<=alpha):
                break
            beta=max(beta,value)
        return value, Column