import math
from Connect4 import *
import random
def get_next_open_row(board,col):
	for r in range(6):
		if board[r][col] == 0:
			return r
def is_valid_location(board,col):
	return board[6-1][col] == 0
def get_valid_locations(Board):
    valid_locations = []
    for col in range (7):
        if is_valid_location(Board,col):
            valid_locations.append(col)
    return valid_locations
def drop_piece(board, row, col, piece):
	board[row][col] = piece

def randmoized():
    mo7sen = random.randrange(0,1)
    return mo7sen
def mini_max(Board,depth,maximizing_player):
    valid_location = get_valid_locations(Board)
    if depth == 0:
        return randmoized()
    if maximizing_player :
        value = -math.inf
        Column=random.randint(0,6)
        for col2 in valid_location:
            row = get_next_open_row(Board,col2)
            b_copy = Board.copy()
            drop_piece(b_copy,row,col2,2)
            new_score = max(value, mini_max(b_copy, depth - 1, False))
            if (new_score > value):
                value = new_score
                Column = col2
        return Column
    else:
        value= math.inf
        Column = random.randint(0,6)
        for col2 in valid_location:
            row = get_next_open_row(Board, col2)
            b_copy = Board.copy()
            drop_piece(b_copy,row,col2,1)
            new_score = min(value, mini_max(b_copy, depth - 1, True))
            if(new_score<value):
                value = new_score
                Column = col2
        return Column



